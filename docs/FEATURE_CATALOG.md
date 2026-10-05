# Function and input catalog

Detailed steps, counterexamples and recovery: [all 62 functions](ALL_FUNCTIONS_RU.md).
Separate registered control recipes: [all 87 entry points](ENTRY_POINTS_RU.md).

Generated from `suite-support/features.json` and the workspace's registered-entry contract.
Each row is an acceptance recipe. It is not a PASS receipt for an unobserved IDEA/device action.

## Capabilities

| ID / function | Input | Action | Observable result | Prerequisite / guide |
| --- | --- | --- | --- | --- |
| ARCH-MVC — Spring MVC, inherited and composed mappings | [DemoContractsController.java](../projects/workspace/payment-app/src/main/java/sample/payment/DemoContractsController.java), [DemoGet.java](../projects/workspace/payment-app/src/main/java/sample/payment/DemoGet.java), [InheritedController.java](../projects/workspace/payment-app/src/main/java/sample/payment/InheritedController.java) | Analyze; Inventory → HTTP; open each mapped endpoint | /demo, /inherited and composed paths have source locations; both inherited and composed declarations remain inspectable | [Guide](../docs/ARCHITECTURE_WALKTHROUGH_RU.md) — IDEA import/index and entitled analysis |
| ARCH-FEIGN — OpenFeign mismatch and correction | [PaymentClient.java](../projects/first-result/order-app/src/main/java/demo/orders/PaymentClient.java), [PaymentController.java](../projects/first-result/payment-app/src/main/java/demo/payments/PaymentController.java) | Analyze POST caller vs PUT provider, then change caller to PUT | Method-mismatch has two-sided evidence; that finding disappears after correction | [Guide](../projects/first-result/README.md) — IDEA, JDK 21, Trial/Pro |
| ARCH-EXCHANGE — Spring HttpExchange clients | [PaymentHttpExchange.java](../projects/workspace/order-app/src/main/java/sample/order/PaymentHttpExchange.java) | Analyze and navigate from GET/POST clients to provider/source | Declared paths/methods and source evidence appear; unresolved headers/target facts stay UNKNOWN | [Guide](../docs/ARCHITECTURE_WALKTHROUGH_RU.md) — IDEA import/index |
| ARCH-FLUENT — RestTemplate, RestClient, WebClient inference | [FluentPaymentClients.java](../projects/workspace/order-app/src/main/java/sample/order/FluentPaymentClients.java) | Analyze fixed targets and inspect confidence/evidence | Conservative inferred calls are distinguished from resolved annotation contracts | [Guide](../docs/ARCHITECTURE_WALKTHROUGH_RU.md) — IDEA import/index |
| ARCH-HTTP-CONDITIONS — Media types, query and header constraints | [DemoContractsController.java](../projects/workspace/payment-app/src/main/java/sample/payment/DemoContractsController.java), [extended_scenarios.py](../projects/workspace/qa-support/extended_scenarios.py) | Fresh copies: http-media-type and http-header-condition | Condition/media changes retain directed compatibility and unresolved client facts; no fabricated matching header value | [Guide](../docs/ARCHITECTURE_WALKTHROUGH_RU.md) — Complete clean HEAD scan |
| ARCH-NESTED-DTO — Java/Kotlin nested, collection, map, enum and nullability shapes | [DemoContractsController.java](../projects/workspace/payment-app/src/main/java/sample/payment/DemoContractsController.java), [AmqpListener.kt](../projects/workspace/notification-app/src/main/kotlin/sample/notification/AmqpListener.kt), [extended_scenarios.py](../projects/workspace/qa-support/extended_scenarios.py) | Inspect DTO details; fresh copies: nested-request-required, enum-response-added | Field paths and before/after types are visible; required request and possible response enum changes need consumer-aware verdicts | [Guide](../docs/ARCHITECTURE_WALKTHROUGH_RU.md) — Complete clean HEAD scan |
| ARCH-JACKSON — Jackson names, access directions, inheritance and polymorphism | [BasicWireDto.java](../projects/workspace/payment-app/src/main/java/sample/payment/BasicWireDto.java), [WireController.java](../projects/workspace/payment-app/src/main/java/sample/payment/WireController.java) | Inspect request/response DTO projections for /wire/dto | wire_id, inherited fields, READ_ONLY/WRITE_ONLY, ignore hints and explicit kind subtypes have source evidence | [Guide](../docs/ARCHITECTURE_WALKTHROUGH_RU.md) — IDEA import/index |
| ARCH-UNKNOWN — Boundaries for generic, recursive and dynamic contracts | [UnknownContractsController.java](../projects/workspace/payment-app/src/main/java/sample/payment/UnknownContractsController.java), [AmqpPublisher.java](../projects/workspace/order-app/src/main/java/sample/order/AmqpPublisher.java) | Inspect generic/recursive HTTP and dynamic AMQP routing | Unsupported shape/routing stays UNKNOWN with explanation, never a fabricated SAFE or proven wire break | [Guide](../docs/ARCHITECTURE_WALKTHROUGH_RU.md) — IDEA import/index |
| ARCH-KAFKA — Kafka sends/listeners, retry/DLT, partitions, patterns, replies and groups | [OrderPublisher.java](../projects/workspace/order-app/src/main/java/sample/order/OrderPublisher.java), [OrderListener.java](../projects/workspace/payment-app/src/main/java/sample/payment/OrderListener.java), [KafkaAdvanced.java](../projects/workspace/payment-app/src/main/java/sample/payment/KafkaAdvanced.java) | Analyze; Kafka protocol filter; fresh copy: kafka-topic | Topic/group/source edges and retry/reply declarations are inspectable; orphan and unresolved pattern are explicit | [Guide](../docs/ARCHITECTURE_WALKTHROUGH_RU.md) — IDEA; no Kafka broker needed for static analysis |
| ARCH-AMQP — RabbitMQ Java/Kotlin producer/exchange/binding/queue/consumer | [AmqpPublisher.java](../projects/workspace/order-app/src/main/java/sample/order/AmqpPublisher.java), [AmqpTopology.java](../projects/workspace/payment-app/src/main/java/sample/payment/AmqpTopology.java), [AmqpListener.kt](../projects/workspace/notification-app/src/main/kotlin/sample/notification/AmqpListener.kt) | Analyze AMQP paths; fresh copy: amqp-binding | Direct/topic/fanout/default declarations share explicit cluster/vhost; dynamic routing remains UNKNOWN; no delivery claim | [Guide](../docs/ARCHITECTURE_WALKTHROUGH_RU.md) — IDEA; no broker needed for declaration analysis |
| ARCH-SCOPE — Profiles, module/path scope and comparable baseline | [.archflow.yml](../projects/workspace/.archflow.yml), [extended_scenarios.py](../projects/workspace/qa-support/extended_scenarios.py) | Fresh copy: scope-change; compare to clean saved baseline | Scope fingerprint changes; lost findings are unobserved rather than silently resolved | [Guide](../docs/ARCHITECTURE_WALKTHROUGH_RU.md) — Complete clean HEAD scan |
| ARCH-PROPERTIES — Spring YAML/properties, profile groups and local imports | [application.yml](../projects/workspace/payment-app/src/main/resources/application.yml), [application-demo.properties](../projects/workspace/payment-app/src/main/resources/application-demo.properties), [application-dev.yml](../projects/workspace/payment-app/src/main/resources/application-dev.yml) | Inspect profile dev/demo/local and imported demo keys | Effective profile/module keys and imported source navigation; unsupported dynamic configuration stays UNKNOWN | [Guide](../projects/workspace/QA_MATRIX_RU.md) — IDEA Spring configuration surface |
| ARCH-MANIFESTS — OpenAPI, AsyncAPI and Backstage declarations | [qa-openapi.json](../projects/workspace/qa-openapi.json), [qa-asyncapi.json](../projects/workspace/qa-asyncapi.json), [qa-backstage.json](../projects/workspace/qa-backstage.json), [qa-loopback.archflow.json](../projects/workspace/contracts/qa-loopback.archflow.json), [qa-event-bus.archflow.json](../projects/workspace/contracts/qa-event-bus.archflow.json), [qa-backstage.archflow.json](../projects/workspace/contracts/qa-backstage.archflow.json) | Fresh copies: manifest-import and manifest-missing; optional tools importer commands | External declarations and provenance visible; missing manifest yields explicit diagnostic/partial boundary | [Guide](../docs/ARCHITECTURE_WALKTHROUGH_RU.md) — IDEA; ArchVerity Tools distribution for raw-format conversion |
| ARCH-POLICIES — Dependency allow/deny and bounded cycle inspection | [.archflow.yml](../projects/workspace/.archflow.yml), [extended_scenarios.py](../projects/workspace/qa-support/extended_scenarios.py) | Fresh copy: dependency-deny; inspect policy finding and path evidence | Observed dependency violation is distinct from a wire break; cycle settings do not invent absent paths | [Guide](../docs/ARCHITECTURE_WALKTHROUGH_RU.md) — Complete clean HEAD scan |
| ARCH-VERIFICATION — Pact/Drift local verification, PASS/FAIL and context rejection | [capture.py](../projects/runtime-evidence/capture.py), [.archflow.yml](../projects/runtime-evidence/.archflow.yml), [payment-openapi.json](../projects/runtime-evidence/contracts/payment-openapi.json) | Capture pact/drift positive and negative controls in separate clean copies; rescan; then invalidate exact report hash/revision | Actual local-check PASS/FAIL with LOCAL_FILE provenance; mismatched context/hash is UNKNOWN; no vendor-run attestation | [Guide](../projects/runtime-evidence/README.md) — Running local Boot app, current IDEA snapshot |
| ARCH-RUNTIME — Real local Actuator bean observations | [KafkaBindings.java](../projects/runtime-evidence/src/main/java/demo/evidence/KafkaBindings.java), [run_local.py](../projects/runtime-evidence/run_local.py), [capture.py](../projects/runtime-evidence/capture.py) | Capture /actuator/beans and current identity; inspect template/factory dependencies | Actual bean names/types/dependencies refine runtime binding; expiry/dirty source/wrong identity is UNKNOWN | [Guide](../projects/runtime-evidence/README.md) — Clean isolated project, running app, current IDEA snapshot |
| IDE-IMPACT — HEAD/base → worktree, Breaking/Safe/Unknown, two-sided evidence | [apply_impact.py](../projects/workspace/qa-support/apply_impact.py), [prepare_impact.py](../projects/workspace/qa-support/prepare_impact.py) | Scan clean HEAD; apply one scenario per new copy; analyze Impact | Exact base/head identities, field before/after, consumer/source navigation and bounded verdicts | [Guide](../docs/ARCHITECTURE_WALKTHROUGH_RU.md) — Git root of prepared project and complete HEAD snapshot |
| IDE-UNSAVED — Unsaved editor changes and gutter → Impact | [PaymentController.java](../projects/workspace/payment-app/src/main/java/sample/payment/PaymentController.java) | Edit the mapping without saving; use Java gutter/Impact; compare saved and unsaved states | Working comparison includes current editor text; source navigation targets this file/version | [Guide](../docs/ARCHITECTURE_WALKTHROUGH_RU.md) — Running IDEA on prepared project |
| IDE-BASELINE — Save/clear baseline and Git comparison controls | [.archflow.yml](../projects/workspace/.archflow.yml) | Save clean baseline, apply change, compare, Clear baseline; test explicit existing base revision | Comparable snapshot diff appears; Clear removes comparison; changed scope is not reported resolved | [Guide](../projects/workspace/QA_MATRIX_RU.md) — Trial/Pro and complete snapshots |
| IDE-REVIEW — Markdown PR review and downstream REVIEW paths | [.archflow.yml](../projects/workspace/.archflow.yml), [PaymentClient.java](../projects/workspace/notification-app/src/main/java/sample/notification/PaymentClient.java) | Impact → Review; copy/save Markdown; inspect downstream source hops and owners | Comparison, direct consumers, unknowns and review limits are readable; reachability is not claimed as field transmission or wire break | [Guide](../docs/ARCHITECTURE_WALKTHROUGH_RU.md) — Current licensed Impact result |
| IDE-NAVIGATION — Workspace, Editor Companion, Graphite Focus, Paper Review and history | [PaymentController.java](../projects/workspace/payment-app/src/main/java/sample/payment/PaymentController.java) | Select one change; switch three layouts; use breadcrumbs and Alt+Left/Alt+Right | Selection/base comparison remain consistent; keyboard/history return to correct surfaces | [Guide](../projects/workspace/QA_MATRIX_RU.md) — IDEA with a build containing these workspace layouts |
| IDE-TOPOLOGY — Inventory, Topology, Relations and filters/focus | [.archflow.yml](../projects/workspace/.archflow.yml) | Filter protocol/search/service; select node; one-hop focus; clear focus | Graph/list selection agrees and source links open the exact declaration | [Guide](../projects/workspace/QA_MATRIX_RU.md) — Complete analyzed project |
| IDE-FINDINGS — Findings, diagnostics, confidence and reasoned suppressions | [PaymentClient.java](../projects/first-result/order-app/src/main/java/demo/orders/PaymentClient.java), [extended_scenarios.py](../projects/workspace/qa-support/extended_scenarios.py) | Open both finding sides; use deterministic alias/manifest guidance; suppress with reason and expiry; fresh copy: rule-severity | PROVEN_MISMATCH/UNKNOWN/OBSERVATION and source proof remain distinct; suppression is persisted and expiry enforced | [Guide](../projects/workspace/QA_MATRIX_RU.md) — Real finding and authorized disposable config edit |
| IDE-EXPORTS — JSON, Impact JSON, Mermaid, SVG, PNG, SARIF and Review Markdown | [inspect_export.py](../suite-support/inspect_export.py), [QA_MATRIX_RU.md](../projects/workspace/QA_MATRIX_RU.md) | Export from current analysis/Impact; inspect saved files; copy/save JSON and Review text | Readable nonempty formats with current run/scope/base/head, redaction and explicit incomplete status | [Guide](../docs/ENVIRONMENT_CHECKS_RU.md) — Trial/Pro, user-selected output directory |
| DEV-SPRING — Spring inspect, conversions, completion, documentation and navigation | [application.yml](../projects/workspace/payment-app/src/main/resources/application.yml), [application-qa.properties](../projects/workspace/payment-app/src/main/resources/application-qa.properties) | Profile filter, Ctrl+B/completion/docs; YAML↔properties; copy key/env/placeholder | Consumers reflect the selected profile and the original key; conversions preserve meaning | [Guide](../projects/workspace/QA_MATRIX_RU.md) — Running IDEA |
| DEV-MYBATIS — Restore/format SQL, live capture and Java/Kotlin mapper↔XML | [MyBatisConsoleFixture.java](../projects/workspace/mybatis-console-fixture/src/main/java/sample/mybatis/MyBatisConsoleFixture.java), [PaymentMapper.xml](../projects/workspace/payment-app/src/main/resources/mappers/PaymentMapper.xml), [PaymentNotificationMapper.kt](../projects/workspace/notification-app/src/main/kotlin/sample/notification/PaymentNotificationMapper.kt) | Select Preparing/Parameters, Restore SQL; run fixture; navigate mapper↔XML | id=42 and escaped O'Reilly; real run console capture; both mapper directions target findById | [Guide](../projects/workspace/QA_MATRIX_RU.md) — IDEA and JDK 21 |
| DEV-ANSIBLE — Ansible roles, inventory, variables, collections and Vault | [site.yml](../projects/workspace/ansible/professional/playbooks/site.yml), [vault-plain.yml](../projects/workspace/ansible/vault-plain.yml) | Scan/complete/navigate; syntax check; separate operator-supplied disposable Vault encrypt/edit/decrypt | Actual definition locations; encrypted file persists and wrong password cannot mutate it | [Guide](../projects/workspace/QA_MATRIX_RU.md) — Ansible for syntax/Vault execution; operator-supplied disposable password |
| DEV-SHELL — Shell/Bats completion, navigation, rename, formatter and local/remote debugger | [common.sh](../projects/workspace/shell-professional/lib/common.sh), [deploy.bats](../projects/workspace/shell-professional/test/deploy.bats), [qa-debug.sh](../projects/workspace/shell-professional/qa-debug.sh) | ShellCheck/shfmt/Bats; break/step/next/continue/stack/print/clear/stop; prepared SSH remote debugger | Two Bats pass; expected formatter diff; debugger stops on actual selected line and variable | [Guide](../docs/ENVIRONMENT_CHECKS_RU.md) — Bash/ShellCheck/shfmt/Bats; existing authorized SSH target for remote |
| DEV-ANSI — ANSI raw/rendered editor, search/wrap and source links | [qa.ansi](../projects/workspace/ansible/qa.ansi), [archflow-live.ansi](../projects/workspace/archflow-live.ansi) | Open raw/rendered, search and follow a log source link | Colors differ from escape text, matched line/source is correct, large log remains bounded | [Guide](../projects/workspace/QA_MATRIX_RU.md) — Running IDEA |
| DEV-ICONS — Three builtin styles, preview/apply/import/export/replace and project rules | [archverity-qa.aficons](../projects/workspace/archverity-qa.aficons), [archflow-studio.aficons](../projects/workspace/archflow-studio.aficons), [generate_icon_pack.py](../projects/workspace/qa-support/generate_icon_pack.py) | Preview Studio/Outline/Contrast; import/apply/export; generate v2 and Replace | Project View changes; replacement changes real version and SVG color; export is parseable | [Guide](../projects/workspace/QA_MATRIX_RU.md) — Actual entitled icon feature state in IDEA |
| DEV-CRYPTO — X.509, PEM/DER, CSR/CRL/public key, truststore and private-key metadata boundary | [qa-cert.pem](../projects/workspace/qa-cert.pem), [qa-cert.der](../projects/workspace/qa-cert.der), [qa-public-artifacts.pem](../projects/workspace/qa-public-artifacts.pem), [qa-request.csr](../projects/workspace/qa-request.csr), [qa-public-key.pem](../projects/workspace/qa-public-key.pem), [qa-truststore.p12](../projects/workspace/qa-truststore.p12) | Inspect/fingerprint/compare; public truststore password archverity-qa-only; wrong password; separate disposable private-key input | PEM/DER fingerprints equal; CSR/CRL verify; trustedCertEntry; no private key is exposed/exported | [Guide](../projects/workspace/QA_MATRIX_RU.md) — IDEA; separate operator-provisioned synthetic key for private-key metadata check |
| API-HTTP — HTTP client, four imports, environments/PasswordSafe, response and request exports | [requests.http](../projects/api-lab/requests.http), [qa-openapi.json](../projects/workspace/qa-openapi.json), [qa-postman.json](../projects/workspace/qa-postman.json), [qa-curl.txt](../projects/workspace/qa-curl.txt) | Import/send/export/reimport; configure nonsecret env; operator-provided PasswordSafe secret; cancel/error/limit | Actual loopback response; environment resolution, transient cookies and bounded errors; secret excluded from saved output | [Guide](../projects/api-lab/README.md) — Local HTTP server; licensed backend |
| API-WEBSOCKET — WebSocket connect/send/receive/text/binary/close/errors | [websocket_server.py](../projects/api-lab/websocket_server.py) | Connect ws://127.0.0.1:18428; send text; close/error; deadline/cancel; repeat session | Ordered real messages and proper terminal session state; UI/backend cleanup is visible | [Guide](../projects/api-lab/README.md) — Pinned Python dependencies, running echo server, entitled backend |
| API-GRPC — gRPC unary/server-stream, descriptor imports, deadlines/cancel/budgets/unsupported streams | [echo.proto](../projects/api-lab/schema/echo.proto), [echo.pb](../projects/api-lab/schema/echo.pb), [grpc_server.py](../projects/api-lab/grpc_server.py) | Say/Watch/Health/Fail; schema import; cancel/deadline; Upload/Chat and unknown JSON field negative inputs | Real HTTP/2 result and statuses; unsupported transports/unknown fields explicitly rejected | [Guide](../projects/api-lab/README.md) — Pinned Python dependencies, server, licensed backend |
| API-SCENARIOS — Sequential HTTP, declarative DSL, structural JSON assertions and captures | [happy.json](../projects/api-lab/scenarios/happy.json), [assertion-fails.json](../projects/api-lab/scenarios/assertion-fails.json), [missing-variable.json](../projects/api-lab/scenarios/missing-variable.json) | Run each JSON array in Scenarios; rerun with fresh transient variables | ID captured and used; first error stops later steps; absent variable fails before request; no arbitrary JS | [Guide](../projects/api-lab/README.md) — Local HTTP server and entitled backend |
| DEV-MOBILE — All 16 React Native/Expo/Gradle/iOS/ADB commands | [package.json](../projects/mobile-lab/package.json), [package-lock.json](../projects/mobile-lab/package-lock.json), [index.js](../projects/mobile-lab/index.js), [App.js](../projects/mobile-lab/App.js), [app.json](../projects/mobile-lab/app.json) | Follow all 16 command rows in mobile-lab README | Real process, bundle, app screen and selected serial; native setup and iOS are observed separately | [Guide](../projects/mobile-lab/README.md) — Node; prebuild+SDK/JDK/device for native; macOS for iOS; explicit install/uninstall/clear authority |
| IDE-SETTINGS — Five application/project settings pages | [coverage.json](../projects/workspace/qa-support/coverage.json) | Change a nonsecret option; reopen and observe consumer; return to original value | Setting persists in correct scope and changes actual editor/API/icon/MyBatis behavior | [Guide](../projects/workspace/QA_MATRIX_RU.md) — Running IDEA on disposable project |
| MCP-TOOLS — Four read-only bounded MCP tools | [.archflow.yml](../projects/workspace/.archflow.yml), [coverage.json](../projects/workspace/qa-support/coverage.json) | Use exact JSON examples in environment guide; filter/limits/directions and negative inputs | Current matching project data, bounded result, relative paths; no source snippets or license bypass | [Guide](../docs/ENVIRONMENT_CHECKS_RU.md) — JetBrains MCP Server and real Trial/Pro |
| IDE-LICENSE — Free/Trial/Pro/expired/offline gates | [QA_MATRIX_RU.md](../projects/workspace/QA_MATRIX_RU.md) | Repeat paid reads/exports/MCP with independently provisioned genuine entitlement states | UI/backend agree; cached paid data remains gated; no synthetic entitlement is accepted as proof | [Guide](../docs/ENVIRONMENT_CHECKS_RU.md) — Real external license states; each NOT RUN until observed |
| IDE-RUNTIME — Local/Split Mode, JCEF/native, light/dark, scale/accessibility/persistence | [QA_MATRIX_RU.md](../projects/workspace/QA_MATRIX_RU.md) | Repeat selected project actions in bound frontend/backend; theme/scale/keyboard; reopen project | Same source/selection/result; bounded cleanup; actual selected graph renderer and accessible controls | [Guide](../docs/ENVIRONMENT_CHECKS_RU.md) — Prepared IDEA runtimes and genuine entitlement |
| TOOLS-CI — Exported JSON gates, converters/diff/policy and fresh headless PSI | [qa-loopback.archflow.json](../projects/workspace/contracts/qa-loopback.archflow.json), [qa-openapi.json](../projects/workspace/qa-openapi.json), [inspect_export.py](../suite-support/inspect_export.py) | Run documented ArchVerity Tools commands on real exports and committed prepared demo revisions | Incomplete/UNKNOWN inputs fail closed; fresh producer has commit/toolchain identity; JSON gate is distinct from a source scan | [Guide](../docs/ENVIRONMENT_CHECKS_RU.md) — Separately supplied Tools distribution; compatible IDE/plugin and provisioned licensed CI config for producer |

## Registered IDEA entry points

All entries below bind to the executable/manual case in [QA matrix](../projects/workspace/QA_MATRIX_RU.md).
Process commands also use the complete [mobile table](../projects/mobile-lab/README.md) and [environment guide](ENVIRONMENT_CHECKS_RU.md).
The workspace-only coverage preserves its truthful six local inputs and sixteen external environments; the mobile app supplies additional real inputs after setup.

### surfaces (15)

| Entry | Case | Workspace fixture |
| --- | --- | --- |
| WORKSPACE | QA-WORKSPACE | [README_RU.md](../projects/workspace/README_RU.md) |
| IMPACT | QA-IMPACT | [PaymentController.java](../projects/workspace/payment-app/src/main/java/sample/payment/PaymentController.java), [apply_impact.py](../projects/workspace/qa-support/apply_impact.py), [qa-loopback.archflow.json](../projects/workspace/contracts/qa-loopback.archflow.json), [qa-event-bus.archflow.json](../projects/workspace/contracts/qa-event-bus.archflow.json), [qa-backstage.archflow.json](../projects/workspace/contracts/qa-backstage.archflow.json) |
| INVENTORY | QA-INVENTORY | [PaymentClient.java](../projects/workspace/order-app/src/main/java/sample/order/PaymentClient.java) |
| TOPOLOGY | QA-TOPOLOGY | [OrderPublisher.java](../projects/workspace/order-app/src/main/java/sample/order/OrderPublisher.java), [OrderListener.java](../projects/workspace/payment-app/src/main/java/sample/payment/OrderListener.java) |
| RELATIONS | QA-RELATIONS | [PaymentListener.kt](../projects/workspace/notification-app/src/main/kotlin/sample/notification/PaymentListener.kt) |
| DIAGNOSTICS | QA-DIAGNOSTICS | [.archflow.yml](../projects/workspace/.archflow.yml), [apply_impact.py](../projects/workspace/qa-support/apply_impact.py) |
| SPRING | QA-SPRING | [application.yml](../projects/workspace/payment-app/src/main/resources/application.yml), [application-dev.yml](../projects/workspace/payment-app/src/main/resources/application-dev.yml), [application-qa.properties](../projects/workspace/payment-app/src/main/resources/application-qa.properties) |
| MYBATIS | QA-MYBATIS | [PaymentMapper.java](../projects/workspace/payment-app/src/main/java/sample/payment/PaymentMapper.java), [PaymentMapper.xml](../projects/workspace/payment-app/src/main/resources/mappers/PaymentMapper.xml), [MyBatisConsoleFixture.java](../projects/workspace/mybatis-console-fixture/src/main/java/sample/mybatis/MyBatisConsoleFixture.java) |
| ANSIBLE | QA-ANSIBLE | [site.yml](../projects/workspace/ansible/professional/playbooks/site.yml), [release.yml](../projects/workspace/ansible/professional/vars/release.yml), [vault-plain.yml](../projects/workspace/ansible/vault-plain.yml) |
| SHELL | QA-SHELL | [deploy](../projects/workspace/shell-professional/bin/deploy), [deploy.bats](../projects/workspace/shell-professional/test/deploy.bats), [common.sh](../projects/workspace/shell-professional/lib/common.sh) |
| API | QA-API | [qa-api.http](../projects/workspace/qa-api.http), [qa-slow.http](../projects/workspace/qa-slow.http), [qa-openapi.json](../projects/workspace/qa-openapi.json), [qa-postman.json](../projects/workspace/qa-postman.json), [qa-curl.txt](../projects/workspace/qa-curl.txt), [local_api.py](../projects/workspace/qa-support/local_api.py) |
| REACT_NATIVE | QA-RN | [package.json](../projects/workspace/rn-qa/package.json), [qa-verify.js](../projects/workspace/rn-qa/scripts/qa-verify.js) |
| ANSI | QA-ANSI | [archflow-live.ansi](../projects/workspace/archflow-live.ansi), [qa.ansi](../projects/workspace/ansible/qa.ansi) |
| DEV_ICONS | QA-ICONS | [archverity-qa.aficons](../projects/workspace/archverity-qa.aficons), [archflow-studio.aficons](../projects/workspace/archflow-studio.aficons) |
| KEYSTORE | QA-CRYPTO | [qa-cert.pem](../projects/workspace/qa-cert.pem), [qa-cert.der](../projects/workspace/qa-cert.der), [qa-public-artifacts.pem](../projects/workspace/qa-public-artifacts.pem), [qa-request.csr](../projects/workspace/qa-request.csr), [qa-public-key.pem](../projects/workspace/qa-public-key.pem), [qa-truststore.p12](../projects/workspace/qa-truststore.p12) |

### actions (6)

| Entry | Case | Workspace fixture |
| --- | --- | --- |
| ArchFlow.RestoreMyBatisSql | QA-MYBATIS | [MyBatisConsoleFixture.java](../projects/workspace/mybatis-console-fixture/src/main/java/sample/mybatis/MyBatisConsoleFixture.java) |
| ArchFlow.SpringConfigTools | QA-SPRING | [application-qa.properties](../projects/workspace/payment-app/src/main/resources/application-qa.properties) |
| ArchFlow.InspectKeystore | QA-CRYPTO | [qa-truststore.p12](../projects/workspace/qa-truststore.p12) |
| ArchFlow.InspectX509Artifact | QA-CRYPTO | [qa-cert.pem](../projects/workspace/qa-cert.pem), [qa-cert.der](../projects/workspace/qa-cert.der), [qa-public-artifacts.pem](../projects/workspace/qa-public-artifacts.pem), [qa-request.csr](../projects/workspace/qa-request.csr), [qa-public-key.pem](../projects/workspace/qa-public-key.pem) |
| ArchFlow.DecryptEditAnsibleVault | QA-ANSIBLE | [vault-plain.yml](../projects/workspace/ansible/vault-plain.yml) |
| ArchFlow.EncryptAnsibleVault | QA-ANSIBLE | [vault-plain.yml](../projects/workspace/ansible/vault-plain.yml) |

### mcp (4)

| Entry | Case | Workspace fixture |
| --- | --- | --- |
| archverity_change_impact | QA-MCP | [apply_impact.py](../projects/workspace/qa-support/apply_impact.py) |
| archverity_findings | QA-MCP | [.archflow.yml](../projects/workspace/.archflow.yml) |
| archverity_contract_evidence | QA-MCP | [PaymentController.java](../projects/workspace/payment-app/src/main/java/sample/payment/PaymentController.java) |
| archverity_trace_flow | QA-MCP | [PaymentClient.java](../projects/workspace/order-app/src/main/java/sample/order/PaymentClient.java) |

### processCommands (22)

| Entry | Case | Workspace fixture |
| --- | --- | --- |
| RN_SCRIPT | QA-RN | [package.json](../projects/workspace/rn-qa/package.json) |
| RN_METRO | QA-RN | See mobile/environment setup |
| RN_EXPO | QA-RN | See mobile/environment setup |
| RN_ANDROID_RUN | QA-RN | See mobile/environment setup |
| RN_IOS_RUN | QA-RN | See mobile/environment setup |
| RN_BUNDLE | QA-RN | See mobile/environment setup |
| GRADLE_TASK | QA-RN | See mobile/environment setup |
| COCOAPODS_INSTALL | QA-RN | See mobile/environment setup |
| IOS_DEVICES | QA-RN | See mobile/environment setup |
| ADB_DEVICES | QA-RN | See mobile/environment setup |
| ADB_LOGCAT | QA-RN | See mobile/environment setup |
| ADB_REVERSE | QA-RN | See mobile/environment setup |
| ADB_RELOAD | QA-RN | See mobile/environment setup |
| ADB_INSTALL_APK | QA-RN | See mobile/environment setup |
| ADB_UNINSTALL | QA-RN | See mobile/environment setup |
| ADB_CLEAR_DATA | QA-RN | See mobile/environment setup |
| ANSIBLE_SYNTAX_CHECK | QA-ANSIBLE | [site.yml](../projects/workspace/ansible/professional/playbooks/site.yml) |
| SHELLCHECK | QA-SHELL | [common.sh](../projects/workspace/shell-professional/lib/common.sh) |
| SHFMT_DIFF | QA-SHELL | [common.sh](../projects/workspace/shell-professional/lib/common.sh) |
| BATS_TEST | QA-SHELL | [deploy.bats](../projects/workspace/shell-professional/test/deploy.bats) |
| BASH_DEBUG | QA-SHELL | [qa-debug.sh](../projects/workspace/shell-professional/qa-debug.sh) |
| BASH_REMOTE_DEBUG | QA-SHELL | See mobile/environment setup |

### debugCommands (7)

| Entry | Case | Workspace fixture |
| --- | --- | --- |
| STEP | QA-SHELL | [qa-debug.sh](../projects/workspace/shell-professional/qa-debug.sh) |
| NEXT | QA-SHELL | [qa-debug.sh](../projects/workspace/shell-professional/qa-debug.sh) |
| CONTINUE | QA-SHELL | [qa-debug.sh](../projects/workspace/shell-professional/qa-debug.sh) |
| BREAKPOINT | QA-SHELL | [qa-debug.sh](../projects/workspace/shell-professional/qa-debug.sh) |
| CLEAR_BREAKPOINTS | QA-SHELL | [qa-debug.sh](../projects/workspace/shell-professional/qa-debug.sh) |
| PRINT_VARIABLE | QA-SHELL | [qa-debug.sh](../projects/workspace/shell-professional/qa-debug.sh) |
| STACK | QA-SHELL | [qa-debug.sh](../projects/workspace/shell-professional/qa-debug.sh) |

### exports (6)

| Entry | Case | Workspace fixture |
| --- | --- | --- |
| JSON | QA-EXPORT | [.archflow.yml](../projects/workspace/.archflow.yml) |
| MERMAID | QA-EXPORT | [.archflow.yml](../projects/workspace/.archflow.yml) |
| SVG | QA-EXPORT | [.archflow.yml](../projects/workspace/.archflow.yml) |
| PNG | QA-EXPORT | [.archflow.yml](../projects/workspace/.archflow.yml) |
| SARIF | QA-EXPORT | [.archflow.yml](../projects/workspace/.archflow.yml) |
| IMPACT | QA-EXPORT | [apply_impact.py](../projects/workspace/qa-support/apply_impact.py) |

### settings (5)

| Entry | Case | Workspace fixture |
| --- | --- | --- |
| archflow.developer.ansi | QA-SETTINGS | [archflow-live.ansi](../projects/workspace/archflow-live.ansi) |
| archflow.developer.mybatis | QA-SETTINGS | [MyBatisConsoleFixture.java](../projects/workspace/mybatis-console-fixture/src/main/java/sample/mybatis/MyBatisConsoleFixture.java) |
| archflow.developer.icons | QA-SETTINGS | [archverity-qa.aficons](../projects/workspace/archverity-qa.aficons) |
| archflow.developer.icons.project | QA-SETTINGS | [archverity-qa.aficons](../projects/workspace/archverity-qa.aficons) |
| archflow.developer.http.environments | QA-SETTINGS | [qa-api.http](../projects/workspace/qa-api.http) |

### editorExtensions (22)

| Entry | Case | Workspace fixture |
| --- | --- | --- |
| fileEditorProvider:AnsiLogFileEditorProvider | QA-ANSI | [archflow-live.ansi](../projects/workspace/archflow-live.ansi) |
| fileType:BatsFileType:Shell Script | QA-SHELL | [deploy.bats](../projects/workspace/shell-professional/test/deploy.bats) |
| localInspection:ArchFlowContract:JAVA | QA-EDITOR | [PaymentController.java](../projects/workspace/payment-app/src/main/java/sample/payment/PaymentController.java) |
| codeInsight.lineMarkerProvider:ArchFlowImpactLineMarkerProvider:JAVA | QA-EDITOR | [PaymentController.java](../projects/workspace/payment-app/src/main/java/sample/payment/PaymentController.java) |
| psi.referenceContributor:MyBatisReferenceContributor:XML | QA-MYBATIS | [PaymentMapper.xml](../projects/workspace/payment-app/src/main/resources/mappers/PaymentMapper.xml) |
| psi.referenceContributor:MyBatisReferenceContributor:JAVA | QA-MYBATIS | [PaymentMapper.java](../projects/workspace/payment-app/src/main/java/sample/payment/PaymentMapper.java) |
| psi.referenceContributor:MyBatisReferenceContributor:kotlin | QA-MYBATIS | [PaymentNotificationMapper.kt](../projects/workspace/notification-app/src/main/kotlin/sample/notification/PaymentNotificationMapper.kt) |
| psi.referenceContributor:SpringStringReferenceContributor:JAVA | QA-SPRING | [application.yml](../projects/workspace/payment-app/src/main/resources/application.yml) |
| psi.referenceContributor:SpringStringReferenceContributor:kotlin | QA-SPRING | [PaymentListener.kt](../projects/workspace/notification-app/src/main/kotlin/sample/notification/PaymentListener.kt) |
| gotoDeclarationHandler:MyBatisGotoDeclarationHandler | QA-MYBATIS | [PaymentMapper.xml](../projects/workspace/payment-app/src/main/resources/mappers/PaymentMapper.xml) |
| gotoDeclarationHandler:SpringConfigGotoDeclarationHandler | QA-SPRING | [application.yml](../projects/workspace/payment-app/src/main/resources/application.yml) |
| multiHostInjector:SpringLanguageInjector | QA-SPRING | [application-qa.properties](../projects/workspace/payment-app/src/main/resources/application-qa.properties) |
| lang.documentationProvider:SpringConfigDocumentationProvider:Properties | QA-SPRING | [application-qa.properties](../projects/workspace/payment-app/src/main/resources/application-qa.properties) |
| lang.documentationProvider:SpringConfigDocumentationProvider:yaml | QA-SPRING | [application.yml](../projects/workspace/payment-app/src/main/resources/application.yml) |
| gotoDeclarationHandler:ShellGotoDeclarationHandler | QA-SHELL | [deploy](../projects/workspace/shell-professional/bin/deploy) |
| psi.referenceContributor:ShellReferenceContributor:Shell Script | QA-SHELL | [deploy](../projects/workspace/shell-professional/bin/deploy) |
| lang.documentationProvider:ShellDocumentationProvider:Shell Script | QA-SHELL | [deploy](../projects/workspace/shell-professional/bin/deploy) |
| gotoDeclarationHandler:AnsibleGotoDeclarationHandler | QA-ANSIBLE | [site.yml](../projects/workspace/ansible/professional/playbooks/site.yml) |
| completion.contributor:SpringConfigCompletionContributor:Properties | QA-SPRING | [application-qa.properties](../projects/workspace/payment-app/src/main/resources/application-qa.properties) |
| completion.contributor:SpringConfigCompletionContributor:yaml | QA-SPRING | [application.yml](../projects/workspace/payment-app/src/main/resources/application.yml) |
| completion.contributor:ShellCompletionContributor:Shell Script | QA-SHELL | [deploy](../projects/workspace/shell-professional/bin/deploy) |
| completion.contributor:AnsibleCompletionContributor:yaml | QA-ANSIBLE | [site.yml](../projects/workspace/ansible/professional/playbooks/site.yml) |
