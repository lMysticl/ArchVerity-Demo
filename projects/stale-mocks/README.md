# See a consumer's test stay green after the provider changes

Two Spring Boot **3.5.15** services. `billing` renamed a response field: it now
sends `invoiceId` where it used to send `id`. `orders` still reads `id`, and its
test fakes billing with the JSON billing used to send. That test stays green,
while the real call leaves the id empty. ArchVerity **5.5.0** reports the stale
fake from source as `AFG-MOCK-001`, before anyone runs the services together.

[All-lab launch guide](../../docs/DEMO_RUNBOOK_RU.md) · [English tour](../../docs/PRODUCT_TOUR_EN.md)

## Prepare a separate project

Run from the **ArchVerity-Demo repository root**:

```powershell
python -B -X utf8 suite-support/prepare_project.py --project stale-mocks --output ../archverity-stale-mocks
```

Open the resulting `archverity-stale-mocks` directory as a Gradle project.
Use JDK 21, allow the first dependency download, finish import/indexing and
activate a legitimate Trial/Pro in the separately installed plugin. No server,
database, Docker or broker is required for the analysis. All service names are
synthetic. The reproduction pin is intentional; it is not a deployment recommendation.

| Side | Source | What it does |
| --- | --- | --- |
| billing | [InvoiceController](billing-service/src/main/java/demo/billing/InvoiceController.java), [InvoiceView](billing-service/src/main/java/demo/billing/InvoiceView.java) | `GET /invoices/{id}` answers `{"invoiceId": "42", "total": 1200}` |
| orders | [BillingClient](orders-service/src/main/java/demo/orders/BillingClient.java), [InvoiceView](orders-service/src/main/java/demo/orders/InvoiceView.java) | Calls billing and reads `id` and `total` |
| orders test | [BillingInvoiceTest](orders-service/src/test/java/demo/orders/BillingInvoiceTest.java) | A `MockRestServiceServer` expectation answers `{"id": "42", "total": 1200}` |

## See the problem without the plugin

From the **prepared project directory**:

```powershell
.\gradlew.bat :orders-service:test realCall --console=plain
python -B -X utf8 verification/verify_stale_mock.py
```

On Linux/macOS use `./gradlew`. The first task runs orders' test against its fake.
The second starts the real billing service on a free loopback port and calls it
with a default `RestClient` and orders' own `InvoiceView`
([RealCall](verification/src/demo/verification/RealCall.java)).
Expected: `STALE_MOCK_CONFIRMED`. Orders' test passes, billing sends
`invoiceId` and `total`, and orders reads `id` as `null`. Nothing fails, so the data is wrong without an error.

## Find it in ArchVerity

1. In ArchVerity **Overview**, use **Map this project** / refresh the analysis.
2. Open the HTTP link from `orders` to `billing`. Both sides must resolve to the
   sources above; if they do not, inspect import, scope and diagnostics first.
3. Expected finding: **`AFG-MOCK-001` Test stub answers with fields the provider no longer sends**
   (warning). It names `orders-service/src/test/java/demo/orders/BillingInvoiceTest.java:20`,
   `GET /invoices/42`, the property `'id'` and billing's `InvoiceView`. The same stub is listed
   in the link's Contract X-ray.

The finding is an observation, not a verdict. A stale fake does not prove the
real call breaks, and a fresh fake does not prove it works. ArchVerity reads the
stub from source and does not run tests. It judges a fake only when the
consumer's client is linked to exactly one provider endpoint with a known
response DTO, and it never changes a change review or a commit check.

## Let the consumer move first, then check again

On a fresh prepared copy:

```powershell
python -B -X utf8 qa-support/apply_scenario.py --scenario fix
.\gradlew.bat :orders-service:test realCall --console=plain
python -B -X utf8 verification/verify_stale_mock.py --fixed
```

The [fix](qa-support/apply_scenario.py) makes orders read both names
(`@JsonAlias("invoiceId")` on `id`), and its fake answers with what billing sends now.
Expected: `STALE_MOCK_FIXED`. The test is still green, and the real call now reads id `42`.
After **Analyze**, `AFG-MOCK-001` is gone. Because ArchVerity 5.5 reads `@JsonAlias`, a later removal of the
alias shows up in review as a contract change.

The helper refuses an original repository, an edited copy and a second
scenario in the same copy; prepare a new copy instead.

## Boundaries

- `verify_stale_mock.py` proves library behavior: the real test result and the real
  loopback call. It does not claim an ArchVerity scan, licence, GUI action or exported finding.
  Record those separately in the [run record](../../docs/RUN_RECORD.md).
- Java and Kotlin WireMock stubs and WireMock JSON mappings (with `__files` bodies)
  are read the same way; this lab shows the `MockRestServiceServer` form.
