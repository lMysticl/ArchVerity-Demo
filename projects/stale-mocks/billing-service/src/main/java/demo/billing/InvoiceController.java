package demo.billing;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class InvoiceController {
    @GetMapping("/invoices/{id}")
    public InvoiceView invoice(@PathVariable("id") String id) {
        return new InvoiceView(id, 1200);
    }
}
