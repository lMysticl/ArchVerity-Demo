package demo.billing

data class InvoiceView(
    val id: String,
    val total: Long,
    val note: String? = null
)
