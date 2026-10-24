package demo.verification;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.LinkedHashMap;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.web.context.WebServerApplicationContext;
import org.springframework.web.client.RestClient;

/**
 * Starts the real billing service on a free loopback port and calls it the way orders does: a default RestClient
 * reading orders' own InvoiceView. Records billing's raw answer and what orders reads from it.
 */
public class RealCall {
    public static void main(String[] args) throws Exception {
        try (var billing = SpringApplication.run(demo.billing.BillingApplication.class,
                "--server.port=0", "--server.address=127.0.0.1", "--spring.main.banner-mode=off", "--logging.level.root=ERROR")) {
            int port = ((WebServerApplicationContext) billing).getWebServer().getPort();
            RestClient client = RestClient.create("http://127.0.0.1:" + port);
            String raw = client.get().uri("/invoices/{id}", "42").retrieve().body(String.class);
            demo.orders.InvoiceView read = client.get().uri("/invoices/{id}", "42").retrieve().body(demo.orders.InvoiceView.class);
            var result = new LinkedHashMap<String, Object>();
            result.put("billingJson", raw);
            result.put("ordersId", read.id());
            result.put("ordersTotal", read.total());
            Path output = Path.of(args[0]);
            Files.createDirectories(output.getParent());
            Files.writeString(output, new com.fasterxml.jackson.databind.ObjectMapper().writeValueAsString(result));
            System.out.println("REAL_CALL " + output);
        }
    }
}
