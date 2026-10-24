package demo.billing;

/** What billing sends now. It used to call the first field {@code id}. */
public record InvoiceView(String invoiceId, long total) {
}
