# Архитектура и Impact: полный walkthrough

`workspace` — компилируемый проект анализа исходников, с четырьмя service IDs:
order-service, payment-service, notification-service, analytics-service.
Kafka/RabbitMQ/HTTP business services здесь не запускаются. Для сетевой
демонстрации есть отдельные `api-lab` и `runtime-evidence`.

## Исходный проект и чистая копия

В корне набора выполните проверки и создайте отдельный Git-root:

```powershell
python -B -X utf8 suite-support/check_suite.py
python -B -X utf8 projects/workspace/qa-support/preflight.py
python -B -X utf8 suite-support/prepare_project.py --project workspace --output D:\CodexData\Temp\archverity-demo-impact
```

Из полученной папки `gradlew.bat classes` компилирует Java и Kotlin. На
Linux/macOS используйте `./gradlew classes`. В IDEA откройте именно эту папку
как Gradle-проект; Gradle JVM — JDK 21. Дождитесь импорта/индексации, откройте
View → Tool Windows → ArchVerity и нажмите Analyze. На неизменённом HEAD
Impact должен сообщать отсутствие изменений. Обычные findings при этом
допустимы: набор намеренно содержит Kafka DTO mismatch и orphan topic.

Снимок чистого HEAD нужен в `.idea/archflow/commits/<HEAD>.json`. Скрипт мутации
проверяет точный commit, полный runStatus, отсутствие partial и unsupported
features. Он не создаёт выдуманный анализ и не меняет исходный публичный набор.
Каждый сценарий запускайте в **новой** копии; существующие папки не перезаписываются.

## Показ архитектуры

| Вход | Что открыть/наблюдать |
| --- | --- |
| `PaymentController.java` ↔ три `PaymentClient.java` | Сопоставленные HTTP стороны, service/owner/repository, ссылки к исходникам |
| `DemoContractsController.java`, `DemoGet.java`, `InheritedController.java` | Обычные, composed и inherited mappings; media types и query/header conditions |
| `PaymentHttpExchange.java` | GET/POST декларации Spring HTTP interface; факты о клиенте отделены от неизвестных значений |
| `FluentPaymentClients.java` | RestTemplate/RestClient/WebClient с фиксированными targets; inference имеет явную confidence |
| `BasicWireDto.java` / `WireController.java` | Jackson wire names, inherited/read-only/write-only/ignored fields, explicit polymorphic `kind` |
| Java `Address/PaymentView`, Kotlin `OrderNotification` | Вложенные поля, nullable/required, enum, List и Map; тип связывается внутри своего сервиса |
| `UnknownContractsController.java` | Generic/recursive boundary остаётся UNKNOWN с причиной |
| `OrderPublisher.java` / `OrderListener.java` и Kafka factory classes | `orders.created`, несовпадающий required field, JsonSerializer/JsonDeserializer bean chains, retry/DLT |
| `KafkaAdvanced.java` | ProducerRecord, partitions 0/1, reply topic, pattern/group и orphan topic |
| `AmqpPublisher.java` / `AmqpTopology.java` / `AmqpListener.kt` | Java/Kotlin topic/direct/fanout/default topology; cluster `demo-broker`, vhost `/archverity-demo`; dynamic key неизвестен |
| `OrderStatusController.java` / `OrderStatusClient.java` | Конкретная обратная payment→orders HTTP-зависимость для cycle exercise |
| `application.yml`, `application-dev.yml`, `application-demo.properties` | Profiles, local group, локальный optional import и навигация к ключу |

В Inventory смените protocol/service/search; в Topology выберите узел,
включите one-hop focus и сбросьте его; в Relations откройте обе стороны.
Число узлов/находок сверяйте с реальным экспортом своей версии, не с
историческим скриншотом. AMQP edges показывают декларации/статическое
соответствие, а не факт доставки сообщения брокером.

## Мутации

Из терминала **созданной копии**:

```powershell
python -B -X utf8 qa-support/apply_impact.py --project . --scenario combined-breaking
```

Синхронизируйте изменённые файлы в IDEA, повторите Analyze и сравните
HEAD → WORKTREE. `--help` выводит все имена; ожидаемые наблюдения:

| Сценарий | Изменение | Наблюдение для приёмки |
| --- | --- | --- |
| combined-breaking | POST→PUT, required request field, required response field removed | Раздельные последствия и две стороны evidence; не один недоказанный общий verdict |
| http-method | Только POST→PUT | Метод-провайдер и неизменённый клиент видны в comparison |
| request-required | Добавлен mandatoryRiskToken | Required request shape рассматривается в направлении клиент→провайдер |
| response-removed | Удалён providerReference | Required consumer response field сопоставляется с удалённым provider field |
| response-optional-added | Добавлен auditNote | Optional addition отделён от доказанного breaking; неполный клиент остаётся UNKNOWN |
| kafka-topic | orders.created→orders.revised | Изменение topic и затронутые существующие listeners/source |
| spring-profile | feature.enabled true→false | Изменение эффективной конфигурации; UI показывает фактическую область анализа |
| manifest-import | Подключены 3 canonical manifests | HTTP/Kafka/catalog declarations и provenance; границы external sources явные |
| manifest-missing | Файл manifest отсутствует | Явная диагностика; такой ввод не даёт ложный полный зелёный результат |
| nested-request-required | Address.postalCode становится NotNull | Вложенный путь и directed request compatibility; unresolved client shapes явные |
| enum-response-added | Provider добавляет REFUNDED | Possible response enum value сравнивается с клиентским enum; неизвестные serializer факты не угадываются |
| http-media-type | JSON→XML consumes | Media compatibility/unknown зависит от фактов о клиенте |
| http-header-condition | X-Demo local→changed | Изменение условия; отсутствующее значение клиента не считается доказанным совпадением |
| amqp-binding | orders.*→payments.* | Binding/routes change имеет source evidence; полнота bindings и runtime delivery не выдумываются |
| dependency-deny | Запрет order→payment и cycle detection | AFG-DEPENDENCY policy/cycle observation; это отдельное понятие от wire breaking |
| rule-severity | Kafka orphan rule severity INFO | Настройка меняет severity реального finding, а не скрывает UNKNOWN другими правилами |
| scope-change | Только default profile | Scope fingerprint меняется; исчезнувшие данные помечаются unobserved |
| runtime-beans-missing | Включён importer без отчётов | Явный UNKNOWN для отсутствующих runtime inputs; положительный случай — runtime-evidence |
| verification-missing | Включён verifier без отчёта | Явный UNKNOWN; положительный/FAIL случай — runtime-evidence |

Не фиксируйте одинаковое число Breaking/Safe/Unknown для всех версий и сред.
Проверяйте конкретное изменение, его direct consumer, before/after, source
location и reason. Generic/custom/dynamic случаи требуют честного UNKNOWN.

## Review, редактор и экспорт

На одном выбранном изменении переключите Editor Companion, Graphite Focus
и Paper Review. Проверьте сохранение выбора и Git comparison. Откройте source
inspector, обе стороны Evidence, affected-consumer и owner/repository.
Impact → Review должен дать читаемый Markdown с comparison, consumers,
неизвестными фактами и пределами downstream review. Сохраните его в `work/`.
Downstream REVIEW — ограниченная достижимость; она сама не доказывает передачу
изменённого поля или поломку каждого косвенного потребителя.

В отдельной чистой копии измените mapping **без сохранения** и вызовите Impact
из Java gutter. Результат должен учитывать editor text. После сохранения
проверьте, что source/source inspector и выбранный change согласованы.
Back/Forward, breadcrumb и Alt+Left/Alt+Right должны вернуться к правильному экрану.

Сохраните clean comparison baseline, измените контракт, сравните и выполните
Clear comparison baseline. При смене profiles не называйте потерянные findings
resolved. Экспортируйте JSON, Impact JSON, Mermaid, SVG, PNG, SARIF и Review
Markdown; сохранённые файлы должны быть читаемыми и относиться к текущему
run/project/base/head. Используйте `suite-support/inspect_export.py` для формата,
затем отдельно проверьте content/identity и redaction.

Остальные developer/editor/settings функции проходят по
[QA_MATRIX_RU.md](../projects/workspace/QA_MATRIX_RU.md).
Для сетей используйте [API lab](../projects/api-lab/README.md), для реального
RN/Expo — [mobile lab](../projects/mobile-lab/README.md).
