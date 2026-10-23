package demo.billing;

public record InvoiceView(String id, InvoiceStatus status, java.time.Month period, Integer quantity) {
}
