package demo.verification;

import java.lang.reflect.InvocationTargetException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.time.Month;
import java.util.LinkedHashMap;
import org.springframework.boot.SpringBootConfiguration;
import org.springframework.boot.WebApplicationType;
import org.springframework.boot.autoconfigure.EnableAutoConfiguration;
import org.springframework.boot.builder.SpringApplicationBuilder;

/** Runs the real auto-configured mapper. Reflection keeps the probe identical across Jackson generations. */
@SpringBootConfiguration
@EnableAutoConfiguration
public class WireProbe {
    public record Quantity(int quantity) {}
    public record MonthValue(Month period) {}

    public static void main(String[] args) throws Exception {
        int generation = Integer.parseInt(args[0]);
        try (var context = new SpringApplicationBuilder(WireProbe.class)
                .web(WebApplicationType.NONE)
                .properties("spring.main.banner-mode=off", "logging.level.root=ERROR")
                .run()) {
            Class<?> mapperType = Class.forName(generation == 3
                    ? "com.fasterxml.jackson.databind.ObjectMapper" : "tools.jackson.databind.ObjectMapper");
            Object mapper = context.getBean(mapperType);
            var write = mapperType.getMethod("writeValueAsString", Object.class);
            var read = mapperType.getMethod("readValue", String.class, Class.class);
            var result = new LinkedHashMap<String, Object>();
            String invoice = (String) write.invoke(mapper, new demo.billing.InvoiceController().invoice("42"));
            String legacy = "{\"id\":\"42\",\"status\":\"PAID\",\"period\":\"JANUARY\",\"quantity\":null}";
            result.put("bootGeneration", generation);
            result.put("bootVersion", org.springframework.boot.SpringBootVersion.getVersion());
            result.put("mapper", mapper.getClass().getName());
            result.put("invoiceJson", invoice);
            result.put("enumJson", write.invoke(mapper, demo.billing.InvoiceStatus.PAID));
            result.put("monthJson", write.invoke(mapper, Month.JANUARY));
            result.put("monthNumberOne", ((MonthValue) read.invoke(mapper, "{\"period\":1}", MonthValue.class)).period().name());
            result.put("nullPrimitive", accepts(read, mapper, "{\"quantity\":null}", Quantity.class));
            result.put("absentPrimitive", accepts(read, mapper, "{}", Quantity.class));
            result.put("readsOwnInvoice", accepts(read, mapper, invoice, demo.orders.InvoiceView.class));
            result.put("readsLegacyInvoice", accepts(read, mapper, legacy, demo.orders.InvoiceView.class));
            Path output = Path.of(args[1]);
            Files.createDirectories(output.getParent());
            Files.writeString(output, (String) write.invoke(mapper, result));
            System.out.println("WIRE_OBSERVATION " + output);
        }
    }

    private static boolean accepts(java.lang.reflect.Method read, Object mapper, String json, Class<?> target)
            throws IllegalAccessException {
        try {
            read.invoke(mapper, json, target);
            return true;
        } catch (InvocationTargetException error) {
            if (error.getCause().getClass().getName().contains("MismatchedInputException")
                    || error.getCause().getClass().getName().contains("InvalidFormatException")) return false;
            throw new IllegalStateException("Unexpected mapper failure", error.getCause());
        }
    }
}
