package demo.orders;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.springframework.test.web.client.match.MockRestRequestMatchers.method;
import static org.springframework.test.web.client.match.MockRestRequestMatchers.requestTo;
import static org.springframework.test.web.client.response.MockRestResponseCreators.withSuccess;

import org.junit.jupiter.api.Test;
import org.springframework.http.HttpMethod;
import org.springframework.http.MediaType;
import org.springframework.test.web.client.MockRestServiceServer;
import org.springframework.web.client.RestClient;

/** Orders' test fakes billing with the JSON billing used to send. It stays green after billing renames the field. */
class BillingInvoiceTest {
    @Test
    void readsTheInvoiceBillingSends() {
        RestClient.Builder builder = RestClient.builder();
        MockRestServiceServer billing = MockRestServiceServer.bindTo(builder).build();
        billing.expect(requestTo("/invoices/42"))
                .andExpect(method(HttpMethod.GET))
                .andRespond(withSuccess("{\"id\": \"42\", \"total\": 1200}", MediaType.APPLICATION_JSON));

        InvoiceView invoice = builder.build().get().uri("/invoices/{id}", "42").retrieve().body(InvoiceView.class);

        assertEquals("42", invoice.id());
        billing.verify();
    }
}
