package demo.orders;

public record InvoiceView(String id, InvoiceStatus status, java.time.Month period, int quantity, int discount) {
}
