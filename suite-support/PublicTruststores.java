import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardCopyOption;
import java.nio.file.StandardOpenOption;
import java.security.KeyStore;
import java.security.MessageDigest;
import java.security.Provider;
import java.security.cert.CertificateFactory;
import java.util.Arrays;
import java.util.HexFormat;
import java.util.Map;

/** Generate or verify public-certificate-only inputs, using the plugin's BC 1.85 version. */
class PublicTruststores {
    private static final char[] PASSWORD = "archverity-qa-only".toCharArray();
    private static final String ALIAS = "archverity-qa";
    private static final Map<String, String> TYPES = Map.of(
            "jks", "JKS", "jceks", "JCEKS", "p12", "PKCS12", "pfx", "PKCS12",
            "bks", "BKS", "bcfks", "BCFKS", "uber", "UBER");

    private static Provider bcProvider() throws Exception {
        try {
            Provider provider = (Provider) Class.forName("org.bouncycastle.jce.provider.BouncyCastleProvider")
                    .getDeclaredConstructor().newInstance();
            if (!"1.85".equals(provider.getVersionStr())) {
                throw new IllegalArgumentException("Expected the plugin's bcprov 1.85; got " + provider.getVersionStr());
            }
            return provider;
        } catch (ClassNotFoundException absent) {
            return null;
        }
    }

    private static KeyStore open(String type, Provider bc) throws Exception {
        return switch (type) {
            case "BKS", "BCFKS", "UBER" -> KeyStore.getInstance(type, bc);
            default -> KeyStore.getInstance(type);
        };
    }

    private static void verify(byte[] bytes, String type, Provider bc, byte[] certificate) throws Exception {
        KeyStore store = open(type, bc);
        store.load(new ByteArrayInputStream(bytes), PASSWORD);
        if (store.size() != 1 || !store.isCertificateEntry(ALIAS) || store.isKeyEntry(ALIAS)
                || !Arrays.equals(certificate, store.getCertificate(ALIAS).getEncoded())) {
            throw new IllegalStateException("Expected exactly one matching trusted certificate: " + type);
        }
        try {
            open(type, bc).load(new ByteArrayInputStream(bytes), "incorrect-demo-password".toCharArray());
            throw new IllegalStateException("Wrong password was accepted: " + type);
        } catch (java.io.IOException expected) {
            // A wrong integrity password must be rejected.
        }
    }

    public static void main(String[] args) throws Exception {
        if (args.length < 2 || !(args[0].equals("generate") || args[0].equals("verify"))) {
            throw new IllegalArgumentException("Usage: PublicTruststores.java generate|verify <workspace> [--require-bc]");
        }
        boolean generate = args[0].equals("generate");
        boolean requireBc = generate || Arrays.asList(args).contains("--require-bc");
        Path root = Path.of(args[1]).toAbsolutePath().normalize();
        byte[] certificate = Files.readAllBytes(root.resolve("qa-cert.der"));
        var parsed = CertificateFactory.getInstance("X.509")
                .generateCertificate(new ByteArrayInputStream(certificate));
        Provider bc = bcProvider();
        if (requireBc && bc == null) throw new IllegalStateException("bcprov-jdk18on 1.85 classpath is required");
        int checked = 0;
        for (var entry : TYPES.entrySet().stream().sorted(Map.Entry.comparingByKey()).toList()) {
            String type = entry.getValue();
            boolean needsBc = type.equals("BKS") || type.equals("BCFKS") || type.equals("UBER");
            if (needsBc && bc == null) {
                System.out.println("NOT_RUN " + type + ": BC 1.85 not on standalone verifier classpath");
                continue;
            }
            Path path = root.resolve("qa-truststore." + entry.getKey());
            if (generate && !entry.getKey().equals("p12")) {
                if (Files.exists(path)) throw new IllegalArgumentException("Refusing to overwrite: " + path);
                KeyStore store = open(type, bc);
                store.load(null, PASSWORD);
                store.setCertificateEntry(ALIAS, parsed);
                var output = new ByteArrayOutputStream();
                store.store(output, PASSWORD);
                byte[] bytes = output.toByteArray();
                verify(bytes, type, bc, certificate);
                Path temporary = path.resolveSibling(path.getFileName() + ".tmp");
                Files.write(temporary, bytes, StandardOpenOption.CREATE_NEW);
                Files.move(temporary, path, StandardCopyOption.ATOMIC_MOVE);
            }
            verify(Files.readAllBytes(path), type, bc, certificate);
            checked++;
            System.out.println("PASS " + type + " " + path.getFileName() + " trustedCertEntry; wrong password rejected");
        }
        System.out.println("PUBLIC_TRUSTSTORES_PASS files=" + checked + " sha256="
                + HexFormat.of().formatHex(MessageDigest.getInstance("SHA-256").digest(certificate)));
    }
}
