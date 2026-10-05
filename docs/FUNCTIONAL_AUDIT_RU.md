# Функциональная проверка демо — 05.10.2026

Сверены все 62 функции, 87 зарегистрированных точек входа, 41 прежний capability recipe,
19 Impact-мутаций и 12 Kafka-профильных сценариев. Для каждой функции ниже указан
исполненный контракт или component test. Это покрытие части сценария, а не автоматический
PASS полного пользовательского playbook. Число тестов в разных строках не суммируется:
один контракт может поддерживать несколько функций.

[Пошаговый запуск](DEMO_RUNBOOK_RU.md) · [62 подробных сценария](ALL_FUNCTIONS_RU.md) ·
[87 точек входа](ENTRY_POINTS_RU.md) · [Средовые предпосылки](ENVIRONMENT_CHECKS_RU.md) ·
[Форма фактического прогона](RUN_RECORD.md)

## Что исправлено

- Impact при отсутствии contract delta показывал пустой Selected contract, unresolved source и
  исторические поля. Дефект наблюдался в установленной 3.0.4 и воспроизведён новым тестом.
  Теперь сравнение показывает identity и следующий шаг; неполное сравнение ведёт к diagnostics.
  Все три presentation modes проходят цикл breaking → clean → incomplete → breaking.
  [Исправление исходников](https://github.com/lMysticl/ArchVerity/commit/26128c0c78d8b7c5341b38b4eee1072a1e3a3345).
  Оно проверено в компоненте и локальном unsigned build; установленный signed plugin не обновлялся.
- PNG с одной signature и фиктивными dimensions получал успех. Проверяются IHDR, chunk
  bounds/CRC, наличие IDAT и конечного IEND. Реальный rendered PNG также открыт и осмотрен.
  Это структурная проверка [по PNG specification](https://www.w3.org/TR/png-3/#5DataRep), не замена image decoder.
- Analysis/Impact JSON теперь проверяет типы, identity и status; duplicate fields, пустые identity,
  неправильные collection shapes и неверный SARIF tool отклоняются. Для полной приёмки добавлены
  require-complete/project-id options; partial export остаётся читаемым без ложного complete PASS.
- Kafka checker требует COMPLETE/partial=false/context и умеет сверять projectId. Все 12 рецептов
  имеют negative controls для missing findings, partial/failed/cancelled, wrong target и lost provenance.
  Некорректные вложенные attributes/evidence/source дают объяснимую ошибку вместо traceback.
- Добавлены проверки всех четырёх Spring live templates: IntelliJ читает shipped XML и
  разворачивает выбранные переменные, сохраняет Spring placeholder и вложенный YAML.
  Java templates не применимы к plain text. Это resource/engine contract, не проверка настроек установленной IDEA.
  [Тесты Spring-шаблонов](https://github.com/lMysticl/ArchVerity/commit/724a24dccaabe8e4443448c6e41ee60c140dce3b) также проверяют допустимость в intended Java/YAML context.
- Общий preparation CLI открывает все шесть лабораторий, включая api-lab; path traversal и повторное
  overwrite отклоняются. Для каждой лаборатории проверяется отдельный чистый Git baseline.
- Убраны устаревшие упоминания пяти лабораторий; новые documentation tests отклоняют удалённый
  путь к runbook, битую ссылку и несуществующий fragment. CI выполняет весь suite-support test set.

## Непосредственно выполнено

| Проверка | Результат и граница |
| --- | --- |
| Source correctness suite | 981 tests; 0 failures/errors/skips. Performance suite не запускалась в этой задаче. |
| Critical coverage, source audit, buildPlugin | Все требуемые gates прошли; локальный ZIP unsigned, не uploaded и не installed. |
| Python Tools | 144 tests passed, включая Windows process ownership и canonical import/CI contracts. |
| Public support tests | 21 tests passed: guides, links, exports, шесть clean projects и 12 Kafka contracts. |
| Kafka source consumer | 12 clean cases → loader → Java PSI → graph/rules → full JSON; updated public checker принял все 12 actual exports. Каждому сопоставлены input, IDE test project, context fingerprint и export. Licensed UI и Kafka broker не запускались. |
| Workspace coverage и preflight | 4 negative-control tests; 19 exact mutation anchors, manifests, local HTTP 200/400/404/413, crypto/icon/Node inputs. |
| API laboratory | 18 real TCP HTTP/WebSocket/gRPC tests: ordered messages, imports, cookies, DSL data, error, timeout, cancel и limits. |
| Gradle laboratories | first-result, workspace, runtime-evidence, kafka-profile-lab — classes compiled с JDK 21. |
| Runtime laboratory | Real Boot/Tomcat/Actuator, template→factory dependencies; pact-pass, pact-fail, drift-pass; canonical Tools importer MATCH. Synthetic producer-test context, не IDEA scan/vendor run. |
| Mobile laboratory | npm tree соответствует lockfile; RN_SCRIPT_OK; real Android JS bundle; Metro/Expo status и закрытие собственных child processes подтверждены. Native/device не запускались. |
| Public keystores | JKS/JCEKS/PKCS12/PFX/BKS/BCFKS/UBER: matching trusted certificate, no key entry, wrong password rejected; JDK 21 + BC 1.85. |
| Visual proof | Original installed 3.0.4 empty branch captured; corrected native Swing component rendered and inspected. Это разные build boundaries. |

## Покрытие каждой функции

Полный actual IDEA/device/remote playbook во всех строках пока **NOT RUN**. Test classes ниже
доказывают только названный source/component contract. Полную границу проверяют с положительными
шагами, контрпримером и восстановлением из соответствующей строки ALL_FUNCTIONS_RU.

| ID / функция | Исполненные source/component contracts | Полный consumer playbook |
| --- | --- | --- |
| [DEV-01 — SVG-каталог и отрисовка иконок](ALL_FUNCTIONS_RU.md#dev-01) | `BuiltinDevIconCatalogTest`, `DevIconSerializableIconFactoryTest` | NOT RUN |
| [DEV-02 — Три встроенных стиля](ALL_FUNCTIONS_RU.md#dev-02) | `BuiltinDevIconCatalogTest`, `DevIconRegistryTest` | NOT RUN |
| [DEV-03 — Глобальные и проектные настройки иконок](ALL_FUNCTIONS_RU.md#dev-03) | `DevIconConfigurableAccessibilityTest`, `DevIconAccessTest` | NOT RUN |
| [DEV-04 — Типы, приоритеты и диагностика правил иконок](ALL_FUNCTIONS_RU.md#dev-04) | `DevIconRegistryTest`, `DevIconPackValidatorTest` | NOT RUN |
| [DEV-05 — Жизненный цикл custom .aficons](ALL_FUNCTIONS_RU.md#dev-05) | `DevIconPackArchiveTest`, `DevIconPanelTest` | NOT RUN |
| [KEY-01 — Типы хранилищ, aliases и certificate chains](ALL_FUNCTIONS_RU.md#key-01) | `KeystoreInspectionEngineTest`, `KeystoreInspectorDialogTest` | NOT RUN |
| [KEY-02 — Certificate, PEM/DER, CRL, CSR и key metadata](ALL_FUNCTIONS_RU.md#key-02) | `X509ArtifactInspectorTest`, `SecurityArtifactInspectionUiTest` | NOT RUN |
| [DEVS-01 — HTTP Send, Cancel, limits и response](ALL_FUNCTIONS_RU.md#devs-01) | `BoundedHttpExecutorTest`, `ApiResponsePresentationTest` | NOT RUN |
| [DEVS-02 — Environment variables, headers и PasswordSafe](ALL_FUNCTIONS_RU.md#devs-02) | `EnvironmentTemplateResolverTest`, `ApiEnvironmentServiceTest`, `ApiEnvironmentConfigurableTest` | NOT RUN |
| [DEVS-03 — DSL, captures, assertions и последовательные Scenarios](ALL_FUNCTIONS_RU.md#devs-03) | `ApiScriptEngineTest`, `ApiScenarioTest`, `ApiRequestScriptTest`, `ApiResponseScriptTest` | NOT RUN |
| [DEVS-04 — WebSocket и динамический gRPC](ALL_FUNCTIONS_RU.md#devs-04) | `BoundedWebSocketExecutorTest`, `BoundedGrpcExecutorTest`, `GrpcDescriptorSchemaTest`, `ApiTransportRpcContractTest` | NOT RUN |
| [DEVS-05 — Четыре импорта, request exports, cookies и history](ALL_FUNCTIONS_RU.md#devs-05) | `ApiCollectionImporterTest`, `ApiCollectionExporterTest`, `ApiTransferPreparationTest`, `HttpRequestFileCodecTest`, `CurlCommandCodecTest` | NOT RUN |
| [DEVS-06 — Spring inspect, profiles и source navigation](ALL_FUNCTIONS_RU.md#devs-06) | `SpringConfigDocumentParserTest`, `SpringProfileDocumentScannerTest`, `SpringConfigPanelTest` | NOT RUN |
| [DEVS-07 — Spring completion, docs, strings и injected language](ALL_FUNCTIONS_RU.md#devs-07) | `SpringConfigCompletionContextTest`, `SpringConfigUsageScannerTest`, `SpringLanguageInjectionClassifierTest` | NOT RUN |
| [DEVS-08 — Spring YAML↔properties и key variants](ALL_FUNCTIONS_RU.md#devs-08) | `SpringConfigFormatConverterTest`, `SpringConfigFuzzyMatcherTest` | NOT RUN |
| [DEVS-09 — Все четыре Spring live templates](ALL_FUNCTIONS_RU.md#devs-09) | `SpringLiveTemplateIntegrationTest` | NOT RUN |
| [DEVS-10 — MyBatis paste/selection → готовый SQL](ALL_FUNCTIONS_RU.md#devs-10) | `MyBatisSqlReconstructorTest`, `SqlPresentationTest` | NOT RUN |
| [DEVS-11 — MyBatis live capture из Run console](ALL_FUNCTIONS_RU.md#devs-11) | `MyBatisLogStreamSessionTest`, `MyBatisCaptureRetentionTest` | NOT RUN |
| [DEVS-12 — MyBatis Java/Kotlin/XML navigation и settings](ALL_FUNCTIONS_RU.md#devs-12) | `MyBatisKotlinMapperScannerTest`, `MyBatisMapperXmlScannerTest`, `MyBatisConsoleSettingsServiceTest` | NOT RUN |
| [DEVS-13 — Ansible project model и offline editor support](ALL_FUNCTIONS_RU.md#devs-13) | `AnsibleProjectScannerTest`, `AnsibleOfflineCatalogTest`, `AnsibleProjectSymbolIndexTest`, `AnsibleVariableIndexTest` | NOT RUN |
| [DEVS-14 — Vault encrypt и decrypt/edit/re-encrypt](ALL_FUNCTIONS_RU.md#devs-14) | `AnsibleVaultEngineTest`, `AnsibleVaultEditorDialogTest`, `ProjectCryptoInspectorVaultTest` | NOT RUN |
| [DEVS-15 — Ansible syntax check и process lifecycle](ALL_FUNCTIONS_RU.md#devs-15) | `DeveloperCommandResolverAnsibleTest`, `DeveloperProcessExitPolicyTest`, `BoundedProcessRunnerTest` | NOT RUN |
| [DEVS-16 — ShellCheck и shfmt diff](ALL_FUNCTIONS_RU.md#devs-16) | `DeveloperExecutableResolverTest`, `ShellProfessionalCorpusTest` | NOT RUN |
| [DEVS-17 — Bats обнаружение и два настоящих теста](ALL_FUNCTIONS_RU.md#devs-17) | `BatsTapParserTest`, `ShellProfessionalCorpusTest` | NOT RUN |
| [DEVS-18 — Shell editor, семь debugger commands и remote session](ALL_FUNCTIONS_RU.md#devs-18) | `ShellDocumentScannerTest`, `ShellIndexCompletionTest`, `BashDebugHarnessIntegrationTest`, `RemoteBashDebugTunnelCommandIntegrationTest` | NOT RUN |
| [DEVS-19 — RN/Expo discovery и scripts](ALL_FUNCTIONS_RU.md#devs-19) | `ReactNativeProjectScannerTest`, `DeveloperCommandResolverReactNativeTest`, `ReactNativeConsolePanelTest` | NOT RUN |
| [DEVS-20 — Metro, Expo, bundle и платформенные команды](ALL_FUNCTIONS_RU.md#devs-20) | `DeveloperCommandResolverReactNativeTest`, `DeveloperProcessPollingTest` | NOT RUN |
| [DEVS-21 — ADB devices, logcat, reverse, reload и device changes](ALL_FUNCTIONS_RU.md#devs-21) | `AdbDevicesParserTest`, `DeveloperCommandResolverAdbTest` | NOT RUN |
| [DEVS-22 — ANSI raw/rendered, search, wrap и source links](ALL_FUNCTIONS_RU.md#devs-22) | `AnsiParserTest`, `LogLinkScannerTest` | NOT RUN |
| [DEVS-23 — Большой ANSI-log: bounded pages и Tail](ALL_FUNCTIONS_RU.md#devs-23) | `BoundedLogPageReaderTest`, `AnsiLargeLogStatusComponentTest` | NOT RUN |
| [DEVS-24 — ANSI settings и file registration](ALL_FUNCTIONS_RU.md#devs-24) | `AnsiFilePatternMatcherTest` | NOT RUN |
| [ARC-01 — Анализ, обновление, отмена и индексация](ALL_FUNCTIONS_RU.md#arc-01) | `ScanRequestQueueTest`, `ScanFreshnessTest`, `WorkingTreeFreshnessIntegrationTest` | NOT RUN |
| [ARC-02 — HTTP server inventory: обычные, inherited и composed mappings](ALL_FUNCTIONS_RU.md#arc-02) | `JavaSourceAnalyzerTest`, `KotlinSourceAnalyzerTest`, `InheritedSourceScanIntegrationTest` | NOT RUN |
| [ARC-03 — HTTP clients, route matching и условия](ALL_FUNCTIONS_RU.md#arc-03) | `HttpRouteGraphTest`, `HttpConditionsTest`, `HttpProtocolTest` | NOT RUN |
| [ARC-04 — Kafka contracts: topic, group, binding и orphan](ALL_FUNCTIONS_RU.md#arc-04) | `KafkaRuleTest`, `KafkaContractScopeTest`, `KafkaProfileScanIntegrationTest` | NOT RUN |
| [ARC-05 — Kafka retry, DLT и reply paths](ALL_FUNCTIONS_RU.md#arc-05) | `KafkaRuleTest`, `KafkaEvidenceTest` | NOT RUN |
| [ARC-06 — AMQP direct/topic/fanout/default exchange](ALL_FUNCTIONS_RU.md#arc-06) | `AmqpGraphTest`, `JavaAmqpSourceAdapterTest`, `KotlinAmqpSourceAdapterTest`, `AmqpChangeImpactTest` | NOT RUN |
| [ARC-07 — DTO/Jackson: вложенность, коллекции, enum и Unknown](ALL_FUNCTIONS_RU.md#arc-07) | `NestedDtoShapesTest`, `DtoComparatorTest`, `DtoPolymorphismTest`, `DtoEnumWireCompatibilityTest`, `DtoPropertyDirectionTest` | NOT RUN |
| [ARC-08 — Severity, confidence, disposition и evidence](ALL_FUNCTIONS_RU.md#arc-08) | `FindingDispositionTest`, `RuleEngineTest`, `FindingActionPlannerTest` | NOT RUN |
| [UI-01 — Все 15 экранов, layouts и navigation history](ALL_FUNCTIONS_RU.md#ui-01) | `ArchFlowSurfaceDeckTest`, `DeveloperSuitePresentationTest`, `Workspace30RegressionTest` | NOT RUN |
| [UI-02 — Поиск, protocol filters и переход к исходнику](ALL_FUNCTIONS_RU.md#ui-02) | `ArchFlowInspectorTest`, `ProjectRelativeSourceNavigationTest` | NOT RUN |
| [UI-03 — Topology: уровни, focus и exploration](ALL_FUNCTIONS_RU.md#ui-03) | `GraphProjectionTest`, `NativeGraphLayoutTest`, `NativeGraphAccessibilityTest` | NOT RUN |
| [UI-04 — Diagnostics и восстановление после missing input](ALL_FUNCTIONS_RU.md#ui-04) | `WorkspaceReadinessTest`, `ProjectEvidenceCoexistenceTest` | NOT RUN |
| [CFG-01 — Scope, service IDs, profiles и aliases](ALL_FUNCTIONS_RU.md#cfg-01) | `ConfigParserTest`, `AnalysisScopePolicyTest`, `ProjectConfigLoaderIntegrationTest` | NOT RUN |
| [CFG-02 — Rules, guided alias/manifest suggestions и suppression](ALL_FUNCTIONS_RU.md#cfg-02) | `ConfigSuppressionEditorTest`, `FindingActionPlannerTest`, `ProjectConfigLoaderTest` | NOT RUN |
| [CFG-03 — Dependency allow/deny и bounded cycles](ALL_FUNCTIONS_RU.md#cfg-03) | `DependencyConfigParserTest`, `DependencyPolicyScanIntegrationTest`, `DownstreamImpactTest` | NOT RUN |
| [IMP-01 — Git base/HEAD → WORKTREE и unsaved edits](ALL_FUNCTIONS_RU.md#imp-01) | `ContractImpactDemoTest`, `GitSnapshotDiffServiceTest`, `WorkingTreeHiddenIndexImpactIntegrationTest` | NOT RUN |
| [IMP-02 — Local baseline: Save, compare и Clear](ALL_FUNCTIONS_RU.md#imp-02) | `SnapshotPersistenceIntegrationTest`, `ImpactWorkspaceTest` | NOT RUN |
| [IMP-03 — Breaking/Safe/Unknown и downstream REVIEW](ALL_FUNCTIONS_RU.md#imp-03) | `ChangeImpactEngineTest`, `ChangeImpactTruthfulnessTest`, `DownstreamImpactPresentationTest` | NOT RUN |
| [IMP-04 — Две стороны, field table, recommendation и Markdown review](ALL_FUNCTIONS_RU.md#imp-04) | `HttpImpactDetailTest`, `ImpactActionButtonTest`, `ChangeImpactReviewMarkdownTest`, `Workspace30RegressionTest` | NOT RUN |
| [EVD-01 — External OpenAPI/AsyncAPI/Backstage manifests](ALL_FUNCTIONS_RU.md#evd-01) | `ExternalManifestAdapterTest`, `AmqpManifestIntegrationTest` | NOT RUN |
| [EVD-02 — Настоящие Actuator beans и local runtime metadata](ALL_FUNCTIONS_RU.md#evd-02) | `ProjectRuntimeEvidenceLoaderTest`, `SpringRuntimeBeanEvidenceTest`, `KafkaProfileScanIntegrationTest` | NOT RUN |
| [EVD-03 — Executed verification: PASS, FAIL, drift и freshness](ALL_FUNCTIONS_RU.md#evd-03) | `VerificationScanIntegrationTest`, `ProjectVerificationEvidenceLoaderTest`, `VerificationPayloadBoundaryTest` | NOT RUN |
| [TEAM-01 — Analysis JSON и Impact JSON для команды](ALL_FUNCTIONS_RU.md#team-01) | `ArchitectureExportFileTest`, `SnapshotSanitizationIntegrationTest` | NOT RUN |
| [TEAM-02 — Mermaid, SVG, PNG и SARIF](ALL_FUNCTIONS_RU.md#team-02) | `GraphProjectionTest`, `ChangeImpactReviewMarkdownTest`, `ArchitectureExportFileTest` | NOT RUN |
| [IDE-01 — Java inspection и Impact gutter → карточка](ALL_FUNCTIONS_RU.md#ide-01) | `ImpactReportSourceMatcherTest`, `ImpactSourceMatcherTest` | NOT RUN |
| [CLI-01 — Offline import adapters](ALL_FUNCTIONS_RU.md#cli-01) | `ExternalManifestAdapterTest` | NOT RUN |
| [CLI-02 — Snapshot diff, git-diff и policy merge](ALL_FUNCTIONS_RU.md#cli-02) | `DiffEngineTest`, `GitSnapshotDiffServiceTest` | NOT RUN |
| [CLI-03 — CI gates findings и Impact](ALL_FUNCTIONS_RU.md#cli-03) | `ChangeImpactTruthfulnessTest`, `VerificationEvidenceTest` | NOT RUN |
| [CLI-04 — Fresh headless PSI producer и committed source](ALL_FUNCTIONS_RU.md#cli-04) | `HeadlessCheckoutTest`, `HeadlessProjectOpenTest`, `HeadlessPsiScanTest`, `HeadlessContractTest` | NOT RUN |
| [CLI-05 — Verification converter и реальный extension provider](ALL_FUNCTIONS_RU.md#cli-05) | `VerificationScanIntegrationTest`, `VerificationEvidenceTest` | NOT RUN |
| [MCP-01 — Все четыре MCP tools и bounded responses](ALL_FUNCTIONS_RU.md#mcp-01) | `ArchVerityMcpProjectionTest`, `DownstreamMcpProjectionTest`, `McpCompatibilityTest` | NOT RUN |

## Оставшаяся граница

QA decision: **CONDITIONAL**. Полная приёмка всех функций требует ещё фактических
IDEA actions с установленным исправлением, editor/settings/reload cycles, native Android/iOS
и выделенного device/SDK/macOS, ShellCheck/shfmt/Bats/Ansible executables, подготовленного SSH
target, MCP Server и client, Split Mode, operator-supplied disposable PasswordSafe/Vault/key inputs,
реальных entitlement states и отдельного inactive entitled headless profile. Ничего из этого
не заменено passing unit test, synthetic producer context или названием кнопки.

Прямые receipts, XML, logs, screenshots и подготовленные project copies сохранены как
EVIDENCE_ONLY под `E:\CodexData\Temp\ArchVerity-demo-audit-20261005`. В публичный Git
попадают исходники проверок и этот отчёт; тяжёлые результаты, кеши и customer evidence не включаются.
