package demo.orders;

import org.springframework.web.client.RestClient;

/** Explicit synthetic URL binds this caller to billing; no server is needed. The path includes billing's context path. */
public class BillingClient {
    private final RestClient billing = RestClient.create("http://billing.example.test");

    public InvoiceView invoice(String id) {
        return billing.get().uri("/billing/invoices/{id}", id).retrieve().body(InvoiceView.class);
    }
}
