package demo.evidence;

import java.util.Map;
import org.springframework.web.bind.annotation.*;

@RestController
public class PaymentController {
    @GetMapping("/payments/{id}")
    public Payment payment(@PathVariable("id") String id) { return new Payment(id, "PAID", "demo-1"); }

    @GetMapping("/demo-identity")
    public Map<String, String> identity() {
        return Map.of("repositoryRevision", System.getenv().getOrDefault("DEMO_SOURCE_REVISION", "unbound"),
                      "configurationSha256", System.getenv().getOrDefault("DEMO_CONFIG_SHA256", "unbound"),
                      "environment", "demo", "providerVersion", "demo-1");
    }

    @GetMapping("/intentional-error")
    public Payment failure() { throw new IllegalStateException("intentional demo failure"); }
}
record Payment(String id, String status, String version) {}
