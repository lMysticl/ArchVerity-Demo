package demo.billing;

/** Human-readable label; the wire representation changes with Jackson defaults. */
public enum InvoiceStatus {
    PAID, REFUNDED;

    @Override
    public String toString() {
        return name().charAt(0) + name().substring(1).toLowerCase(java.util.Locale.ROOT);
    }
}
