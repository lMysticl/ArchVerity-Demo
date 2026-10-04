"""Exercise self-contained fixture inputs before opening the project in IDEA."""

import hashlib
import json
import os
import shutil
import ssl
import subprocess
import threading
import urllib.error
import urllib.request
import zipfile
from pathlib import Path

from apply_impact import SCENARIOS
from local_api import make_server
from verify_coverage import verify

PROJECT = Path(__file__).resolve().parents[1]


def request(url, payload=None):
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    headers = {} if data is None else {"Content-Type": "application/json"}
    with urllib.request.urlopen(urllib.request.Request(url, data=data, headers=headers), timeout=3) as response:
        return response.status, json.load(response)


def main():
    checks = {}
    checks["registered_capabilities"] = verify()
    provider = (PROJECT / "payment-app/src/main/java/sample/payment/PaymentController.java").read_text(encoding="utf-8")
    consumer = (PROJECT / "order-app/src/main/java/sample/order/PaymentClient.java").read_text(encoding="utf-8")
    assert "@PostMapping" in provider and "@PostMapping" in consumer
    assert "mandatoryRiskToken" not in provider
    assert "@jakarta.validation.constraints.NotNull String providerReference" in provider
    checks["architecture_baseline"] = "matching HTTP method plus required response field"
    for name, replacements in SCENARIOS.items():
        staged = {}
        for relative, before, after in replacements:
            if relative not in staged:
                staged[relative] = (PROJECT / relative).read_text(encoding="utf-8")
            assert staged[relative].count(before) == 1, (name, relative, before)
            staged[relative] = staged[relative].replace(before, after, 1)
    checks["impact_scenarios"] = sorted(SCENARIOS)

    required = [
        "payment-app/src/main/resources/application.yml",
        "payment-app/src/main/resources/application-dev.yml",
        "payment-app/src/main/resources/mappers/PaymentMapper.xml",
        "ansible/professional/playbooks/site.yml",
        "ansible/professional/inventories/prod/hosts.yml",
        "shell-professional/bin/deploy",
        "shell-professional/test/deploy.bats",
        "mybatis-console-fixture/src/main/java/sample/mybatis/MyBatisConsoleFixture.java",
        "ansible/qa.ansi",
        "ansible/vault-plain.yml",
        "payment-app/src/main/resources/application-qa.properties",
        "qa-curl.txt",
        "qa-slow.http",
        "qa-cert.der",
        "qa-public-artifacts.pem",
        "qa-request.csr",
        "qa-public-key.pem",
        "qa-asyncapi.json",
        "qa-backstage.json",
        "contracts/qa-loopback.archflow.json",
        "contracts/qa-event-bus.archflow.json",
        "contracts/qa-backstage.archflow.json",
    ]
    assert all((PROJECT / file).is_file() for file in required)
    checks["developer_inputs"] = len(required)
    for path, field in (("contracts/qa-loopback.archflow.json", "httpEndpoints"),
                        ("contracts/qa-event-bus.archflow.json", "kafkaProducers")):
        document = json.loads((PROJECT / path).read_text(encoding="utf-8"))
        assert document["schemaVersion"] == 1 and document["services"][0][field]
    catalog = json.loads((PROJECT / "contracts/qa-backstage.archflow.json").read_text(encoding="utf-8"))
    assert catalog["schemaVersion"] == 1 and catalog["services"][0]["id"] == "qa-catalog-service"
    checks["external_manifests"] = "OpenAPI HTTP, AsyncAPI Kafka and Backstage service declarations present"

    openapi = json.loads((PROJECT / "qa-openapi.json").read_text(encoding="utf-8"))
    postman = json.loads((PROJECT / "qa-postman.json").read_text(encoding="utf-8"))
    http = (PROJECT / "qa-api.http").read_text(encoding="utf-8")
    assert "/qa-openapi" in openapi["paths"]
    assert postman["item"][0]["request"]["url"]["raw"].endswith("/qa-postman")
    assert "POST http://127.0.0.1:18427/qa-roundtrip" in http
    with make_server(0) as server:
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        base = f"http://127.0.0.1:{server.server_port}"
        try:
            assert request(base + "/health") == (200, {"fixture": "archverity-validation", "status": "ok"})
            assert request(base + "/qa-openapi")[1]["source"] == "openapi"
            assert request(base + "/qa-roundtrip", {"amount": 42})[1]["received"] == {"amount": 42}
            assert request(base + "/qa-postman", {"qa": True})[1]["source"] == "qa-postman"
            assert request(base + "/qa-slow?delay_ms=0") == (200, {"source": "slow", "delay_ms": 0})
            for invalid in ("/qa-slow", "/qa-slow?delay_ms=5001", "/qa-slow?delay_ms=abc",
                            "/qa-slow?delay_ms=0&bad", "/qa-slow?delay_ms=0&delay_ms=1",
                            "/qa-slow?delay_ms=999999999999999999999"):
                try:
                    request(base + invalid)
                    raise AssertionError(f"Invalid delay unexpectedly succeeded: {invalid}")
                except urllib.error.HTTPError as error:
                    assert error.code == 400
            try:
                request(base + "/does-not-exist")
                raise AssertionError("Unknown route unexpectedly succeeded")
            except urllib.error.HTTPError as error:
                assert error.code == 404
            bad = urllib.request.Request(base + "/qa-roundtrip", data=b"not-json", method="POST")
            try:
                urllib.request.urlopen(bad, timeout=3)
                raise AssertionError("Invalid JSON unexpectedly succeeded")
            except urllib.error.HTTPError as error:
                assert error.code == 400
            too_large = urllib.request.Request(base + "/qa-roundtrip", data=b"x" * 32769, method="POST")
            try:
                urllib.request.urlopen(too_large, timeout=3)
                raise AssertionError("Oversized JSON unexpectedly succeeded")
            except urllib.error.HTTPError as error:
                assert error.code == 413
            checks["api_loopback"] = "GET, POST, bounded slow route, 400, 404 and 413 observed"
        finally:
            server.shutdown()
            thread.join(timeout=3)

    pem = (PROJECT / "qa-cert.pem").read_text(encoding="ascii")
    der = ssl.PEM_cert_to_DER_cert(pem)
    assert len(der) > 500
    assert (PROJECT / "qa-cert.der").read_bytes() == der
    checks["public_x509_sha256"] = hashlib.sha256(der).hexdigest()
    public_bundle = (PROJECT / "qa-public-artifacts.pem").read_bytes()
    csr = (PROJECT / "qa-request.csr").read_bytes()
    public_key = (PROJECT / "qa-public-key.pem").read_bytes()
    assert public_bundle.count(b"-----BEGIN CERTIFICATE-----") == 1
    assert public_bundle.count(b"-----BEGIN X509 CRL-----") == 1
    assert csr.startswith(b"-----BEGIN CERTIFICATE REQUEST-----")
    assert public_key.startswith(b"-----BEGIN PUBLIC KEY-----")
    try:
        from cryptography import x509
        from cryptography.hazmat.primitives import serialization
        from cryptography.hazmat.primitives.asymmetric import padding
    except ImportError:
        checks["public_x509_variants"] = "PEM block labels present; signature validation NOT RUN: optional cryptography package absent"
    else:
        bundle_cert = x509.load_pem_x509_certificate(public_bundle)
        crl = x509.load_pem_x509_crl(public_bundle)
        csr_request = x509.load_pem_x509_csr(csr)
        decoded_key = serialization.load_pem_public_key(public_key)
        expected_key = bundle_cert.public_key().public_bytes(
            serialization.Encoding.DER, serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        assert decoded_key.public_bytes(serialization.Encoding.DER, serialization.PublicFormat.SubjectPublicKeyInfo) == expected_key
        assert csr_request.is_signature_valid and csr_request.subject == bundle_cert.subject
        assert crl.issuer == bundle_cert.subject and len(crl) == 1
        bundle_cert.public_key().verify(crl.signature, crl.tbs_certlist_bytes, padding.PKCS1v15(), crl.signature_hash_algorithm)
        checks["public_x509_variants"] = "DER matches PEM; CSR, public key and one-entry CRL signatures verified"

    truststore = PROJECT / "qa-truststore.p12"
    assert truststore.is_file() and truststore.stat().st_size > 500
    java_home = os.environ.get("JAVA_HOME")
    keytool = Path(java_home, "bin", "keytool.exe") if java_home else None
    executable = str(keytool) if keytool and keytool.is_file() else shutil.which("keytool")
    if executable:
        result = subprocess.run(
            [executable, "-list", "-v", "-keystore", str(truststore),
             "-storetype", "PKCS12", "-storepass", "archverity-qa-only"],
            capture_output=True, timeout=10, check=True,
        )
        assert b"archverity-qa" in result.stdout and b"trustedCertEntry" in result.stdout
        checks["public_truststore"] = "trustedCertEntry, no private key"
    else:
        checks["public_truststore"] = "present; keytool validation NOT RUN"

    with zipfile.ZipFile(PROJECT / "archflow-studio.aficons") as archive:
        names = archive.namelist()
        assert "manifest.tsv" in names and "rules.tsv" in names
        assert all(not Path(name).is_absolute() and ".." not in Path(name).parts for name in names)
        icons = [name for name in names if name.endswith(".svg")]
        assert len(icons) >= 60
        checks["dev_icons"] = len(icons)
    with zipfile.ZipFile(PROJECT / "archverity-qa.aficons") as archive:
        assert archive.testzip() is None
        assert archive.read("manifest.tsv").startswith(b"archverity-qa\t")
        assert len([name for name in archive.namelist() if name.endswith(".svg")]) == len(icons)
        checks["custom_dev_icons"] = len(icons)

    package = json.loads((PROJECT / "rn-qa/package.json").read_text(encoding="utf-8"))
    assert "react-native" in package["dependencies"] and "qa:verify" in package["scripts"]
    node = shutil.which("node")
    if node:
        result = subprocess.run(
            [node, "scripts/qa-verify.js"], cwd=PROJECT / "rn-qa",
            text=True, capture_output=True, timeout=10, check=True,
        )
        assert "RN_SCRIPT_OK" in result.stdout
        assert (PROJECT / "rn-qa/work/qa-script-result.txt").read_text(encoding="utf-8") == "RN_SCRIPT_OK\n"
        checks["rn_script"] = "executed and produced RN_SCRIPT_OK"
    else:
        checks["rn_script"] = "NOT RUN: Node.js unavailable"

    print(json.dumps({"status": "PASS", "project": str(PROJECT), "checks": checks}, ensure_ascii=False))


if __name__ == "__main__":
    main()
