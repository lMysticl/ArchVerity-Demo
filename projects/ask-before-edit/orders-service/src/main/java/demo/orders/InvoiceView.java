package demo.orders;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

/** Orders reads only what it needs; other properties billing sends are ignored. */
@JsonIgnoreProperties(ignoreUnknown = true)
public record InvoiceView(String id, long total) {
}
