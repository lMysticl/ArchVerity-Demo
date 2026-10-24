package demo.billing

import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.PathVariable
import org.springframework.web.bind.annotation.RestController

/** Served under the context path from application.yml: the full route is GET /billing/invoices/{id}. */
@RestController
class InvoiceController {
    @GetMapping("/invoices/{id}")
    fun invoice(@PathVariable("id") id: String): InvoiceView = InvoiceView(id, 4200)
}
