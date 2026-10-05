# Все функции ArchVerity: демонстрация и проверка

Source scope: ArchVerity 3.0.3; исходный inventory commit `4af095685012405a9420415a0e26c3256c5a61a6`.
62 пользовательские возможности, все 87 registered entry points и все 41 прежние capability recipes связаны с конкретными входами.
Статус ниже относится к подготовленным сценариям. Реальное выполнение отмечайте отдельно в [RUN_RECORD](RUN_RECORD.md).

## Подготовка

Для первого finding откройте `projects/first-result` с JDK 21. Для архитектуры и Impact создайте новую копию через `suite-support/prepare_project.py` и получите настоящий полный снимок чистого HEAD в IDEA.
API запускается через `projects/api-lab/serve.py`. Mobile имеет свой lockfile/native prerequisites. Runtime evidence требует настоящего current IDEA export; producer smoke явно использует synthetic test context.
При отсутствии SDK/device, SSH, real entitlement, PasswordSafe/Vault input или Tools distribution записывайте точную недоступную зависимость. Остальные независимые проверки продолжаются. Signing, credentials и device install/clear/uninstall требуют отдельного разрешения.

[Каталог входов](FEATURE_CATALOG.md) · [87 точек входа](ENTRY_POINTS_RU.md) · [Архитектура и 19 мутаций](ARCHITECTURE_WALKTHROUGH_RU.md) · [Средовые команды и MCP](ENVIRONMENT_CHECKS_RU.md)

## Содержание

| ID | Функция |
| --- | --- |
| DEV-01 | [SVG-каталог и отрисовка иконок](#dev-01) |
| DEV-02 | [Три встроенных стиля](#dev-02) |
| DEV-03 | [Глобальные и проектные настройки иконок](#dev-03) |
| DEV-04 | [Типы, приоритеты и диагностика правил иконок](#dev-04) |
| DEV-05 | [Жизненный цикл custom .aficons](#dev-05) |
| KEY-01 | [Типы хранилищ, aliases и certificate chains](#key-01) |
| KEY-02 | [Certificate, PEM/DER, CRL, CSR и key metadata](#key-02) |
| DEVS-01 | [HTTP Send, Cancel, limits и response](#devs-01) |
| DEVS-02 | [Environment variables, headers и PasswordSafe](#devs-02) |
| DEVS-03 | [DSL, captures, assertions и последовательные Scenarios](#devs-03) |
| DEVS-04 | [WebSocket и динамический gRPC](#devs-04) |
| DEVS-05 | [Четыре импорта, request exports, cookies и history](#devs-05) |
| DEVS-06 | [Spring inspect, profiles и source navigation](#devs-06) |
| DEVS-07 | [Spring completion, docs, strings и injected language](#devs-07) |
| DEVS-08 | [Spring YAML↔properties и key variants](#devs-08) |
| DEVS-09 | [Все четыре Spring live templates](#devs-09) |
| DEVS-10 | [MyBatis paste/selection → готовый SQL](#devs-10) |
| DEVS-11 | [MyBatis live capture из Run console](#devs-11) |
| DEVS-12 | [MyBatis Java/Kotlin/XML navigation и settings](#devs-12) |
| DEVS-13 | [Ansible project model и offline editor support](#devs-13) |
| DEVS-14 | [Vault encrypt и decrypt/edit/re-encrypt](#devs-14) |
| DEVS-15 | [Ansible syntax check и process lifecycle](#devs-15) |
| DEVS-16 | [ShellCheck и shfmt diff](#devs-16) |
| DEVS-17 | [Bats обнаружение и два настоящих теста](#devs-17) |
| DEVS-18 | [Shell editor, семь debugger commands и remote session](#devs-18) |
| DEVS-19 | [RN/Expo discovery и scripts](#devs-19) |
| DEVS-20 | [Metro, Expo, bundle и платформенные команды](#devs-20) |
| DEVS-21 | [ADB devices, logcat, reverse, reload и device changes](#devs-21) |
| DEVS-22 | [ANSI raw/rendered, search, wrap и source links](#devs-22) |
| DEVS-23 | [Большой ANSI-log: bounded pages и Tail](#devs-23) |
| DEVS-24 | [ANSI settings и file registration](#devs-24) |
| ARC-01 | [Анализ, обновление, отмена и индексация](#arc-01) |
| ARC-02 | [HTTP server inventory: обычные, inherited и composed mappings](#arc-02) |
| ARC-03 | [HTTP clients, route matching и условия](#arc-03) |
| ARC-04 | [Kafka contracts: topic, group, binding и orphan](#arc-04) |
| ARC-05 | [Kafka retry, DLT и reply paths](#arc-05) |
| ARC-06 | [AMQP direct/topic/fanout/default exchange](#arc-06) |
| ARC-07 | [DTO/Jackson: вложенность, коллекции, enum и Unknown](#arc-07) |
| ARC-08 | [Severity, confidence, disposition и evidence](#arc-08) |
| UI-01 | [Все 15 экранов, layouts и navigation history](#ui-01) |
| UI-02 | [Поиск, protocol filters и переход к исходнику](#ui-02) |
| UI-03 | [Topology: уровни, focus и exploration](#ui-03) |
| UI-04 | [Diagnostics и восстановление после missing input](#ui-04) |
| CFG-01 | [Scope, service IDs, profiles и aliases](#cfg-01) |
| CFG-02 | [Rules, guided alias/manifest suggestions и suppression](#cfg-02) |
| CFG-03 | [Dependency allow/deny и bounded cycles](#cfg-03) |
| IMP-01 | [Git base/HEAD → WORKTREE и unsaved edits](#imp-01) |
| IMP-02 | [Local baseline: Save, compare и Clear](#imp-02) |
| IMP-03 | [Breaking/Safe/Unknown и downstream REVIEW](#imp-03) |
| IMP-04 | [Две стороны, field table, recommendation и Markdown review](#imp-04) |
| EVD-01 | [External OpenAPI/AsyncAPI/Backstage manifests](#evd-01) |
| EVD-02 | [Настоящие Actuator beans и local runtime metadata](#evd-02) |
| EVD-03 | [Executed verification: PASS, FAIL, drift и freshness](#evd-03) |
| TEAM-01 | [Analysis JSON и Impact JSON для команды](#team-01) |
| TEAM-02 | [Mermaid, SVG, PNG и SARIF](#team-02) |
| IDE-01 | [Java inspection и Impact gutter → карточка](#ide-01) |
| CLI-01 | [Offline import adapters](#cli-01) |
| CLI-02 | [Snapshot diff, git-diff и policy merge](#cli-02) |
| CLI-03 | [CI gates findings и Impact](#cli-03) |
| CLI-04 | [Fresh headless PSI producer и committed source](#cli-04) |
| CLI-05 | [Verification converter и реальный extension provider](#cli-05) |
| MCP-01 | [Все четыре MCP tools и bounded responses](#mcp-01) |

## Иконки

<a id="dev-01"></a>
### DEV-01 — SVG-каталог и отрисовка иконок

**Зачем:** Проверить, что иконки помогают различать типы файлов и папок в настоящем Project View.

**Подготовка:** Открыть указанную лабораторию в IDEA с ArchVerity 3.0.3, JDK 21 для Gradle; дождаться import/index. Для полного показа использовать настоящий Trial/Pro. Требования отдельных инструментов перечислены ниже и в linked guides.

**Входы:** [archverity-qa.aficons](../projects/workspace/archverity-qa.aficons), [archflow-studio.aficons](../projects/workspace/archflow-studio.aficons), [generate_icon_pack.py](../projects/workspace/qa-support/generate_icon_pack.py)

1. Открыть Dev Icons → Preview и выбрать ArchVerity Studio; просмотреть Java/Kotlin, YAML, shell и folder glyphs.
   Ожидаемое наблюдение: Одинаковые семантические типы имеют разные подходящие glyphs; всего в поставляемом demo pack 63 SVG.
2. Экспортировать разрешённый pack в work/, открыть ZIP manifest и один SVG, затем проверить иконку того же типа в Project View.
   Ожидаемое наблюдение: ID и SVG соответствуют выбранному каталогу; реальная Project View использует выбранный glyph.

**Контрпример:** Импортировать копию pack с повреждённым SVG.
Ожидаемое наблюдение: Валидация отклоняет повреждённый pack; текущий рабочий набор остаётся применённым.

**Восстановление:** Работать в отдельной копии. Отменить свои изменения в редакторе, вернуть изменённую настройку, остановить только запущенный для этой проверки процесс. Для следующей мутации создать новую чистую копию; исходный набор сохраняется.

**Доказательство:** Записать ID сценария, точный plugin/IDE build, project path и HEAD, вход и результат в RUN_RECORD. Для UI приложить видимое наблюдение; для экспорта — файл и hash. Успех producer/checker не присваивает PASS плагину.

**Consumer run:** `NOT_RUN`. Capability IDs: DEV-ICONS.

<a id="dev-02"></a>
### DEV-02 — Три встроенных стиля

**Зачем:** Выбрать подходящий читаемый стиль, сохранив семантику типов файлов.

**Подготовка:** Открыть указанную лабораторию в IDEA с ArchVerity 3.0.3, JDK 21 для Gradle; дождаться import/index. Для полного показа использовать настоящий Trial/Pro. Требования отдельных инструментов перечислены ниже и в linked guides.

**Входы:** [archverity-qa.aficons](../projects/workspace/archverity-qa.aficons), [archflow-studio.aficons](../projects/workspace/archflow-studio.aficons), [generate_icon_pack.py](../projects/workspace/qa-support/generate_icon_pack.py)

1. По очереди выбрать Studio, Outline и Contrast в Dev Icons Preview.
   Ожидаемое наблюдение: Типы файлов сохраняются, визуальный стиль меняется для того же glyph.
2. Применить каждый стиль, закрыть и открыть settings; проверить один Java-файл и папку.
   Ожидаемое наблюдение: Выбор сохраняется и влияет на реальные иконки проекта, включая папки.

**Контрпример:** Проверить export/apply при реальном отсутствии paid entitlement.
Ожидаемое наблюдение: Недоступное действие даёт явное ограничение; Preview и право на изменение не смешиваются.

**Восстановление:** Работать в отдельной копии. Отменить свои изменения в редакторе, вернуть изменённую настройку, остановить только запущенный для этой проверки процесс. Для следующей мутации создать новую чистую копию; исходный набор сохраняется.

**Доказательство:** Записать ID сценария, точный plugin/IDE build, project path и HEAD, вход и результат в RUN_RECORD. Для UI приложить видимое наблюдение; для экспорта — файл и hash. Успех producer/checker не присваивает PASS плагину.

**Consumer run:** `NOT_RUN`. Capability IDs: DEV-ICONS.

<a id="dev-03"></a>
### DEV-03 — Глобальные и проектные настройки иконок

**Зачем:** Разделить личные настройки IDE и правила конкретного проекта.

**Подготовка:** Открыть указанную лабораторию в IDEA с ArchVerity 3.0.3, JDK 21 для Gradle; дождаться import/index. Для полного показа использовать настоящий Trial/Pro. Требования отдельных инструментов перечислены ниже и в linked guides.

**Входы:** [archverity-qa.aficons](../projects/workspace/archverity-qa.aficons), [archflow-studio.aficons](../projects/workspace/archflow-studio.aficons), [generate_icon_pack.py](../projects/workspace/qa-support/generate_icon_pack.py), [coverage.json](../projects/workspace/qa-support/coverage.json), [QA_MATRIX_RU.md](../projects/workspace/QA_MATRIX_RU.md)

1. Записать глобальное состояние; переключить project override INHERIT → DISABLED → ENABLED.
   Ожидаемое наблюдение: DISABLED выключает иконки в этом проекте; ENABLED включает; INHERIT использует глобальный выбор.
2. Добавить project rule только для PaymentController.java и повторно открыть проект.
   Ожидаемое наблюдение: Правило и override сохраняются в project scope; глобальная настройка остаётся прежней.

**Контрпример:** В проекте с DISABLED выбрать другой глобальный стиль.
Ожидаемое наблюдение: Project override продолжает определять состояние; чужая настройка не превращается в project rule.

**Восстановление:** Работать в отдельной копии. Отменить свои изменения в редакторе, вернуть изменённую настройку, остановить только запущенный для этой проверки процесс. Для следующей мутации создать новую чистую копию; исходный набор сохраняется.

**Доказательство:** Записать ID сценария, точный plugin/IDE build, project path и HEAD, вход и результат в RUN_RECORD. Для UI приложить видимое наблюдение; для экспорта — файл и hash. Успех producer/checker не присваивает PASS плагину.

**Consumer run:** `NOT_RUN`. Capability IDs: DEV-ICONS, IDE-SETTINGS, IDE-LICENSE.

<a id="dev-04"></a>
### DEV-04 — Типы, приоритеты и диагностика правил иконок

**Зачем:** Предсказуемо разрешать пересекающиеся правила и находить ошибочные matchers.

**Подготовка:** Открыть указанную лабораторию в IDEA с ArchVerity 3.0.3, JDK 21 для Gradle; дождаться import/index. Для полного показа использовать настоящий Trial/Pro. Требования отдельных инструментов перечислены ниже и в linked guides.

**Входы:** [archverity-qa.aficons](../projects/workspace/archverity-qa.aficons), [archflow-studio.aficons](../projects/workspace/archflow-studio.aficons), [generate_icon_pack.py](../projects/workspace/qa-support/generate_icon_pack.py), [prepare_icon_submodule.py](../suite-support/prepare_icon_submodule.py), [ICON_AND_KEYSTORE_INPUTS_RU.md](../docs/ICON_AND_KEYSTORE_INPUTS_RU.md)

1. В rules создать FILE/EXACT для PaymentController.java, FILE/GLOB для *.java и FOLDER/EXACT для payment-app; выбрать существующие icon IDs.
   Ожидаемое наблюдение: Exact, glob и folder target применяются к соответствующим элементам; результат показывает выбранное правило.
2. Для двух пересекающихся project rules поменять priority и проверить один файл; REGEX использовать Payment.*[.]java. Создать отдельную copy через prepare_icon_submodule.py и проверить FOLDER/EXACT demo-icon-module с gitSubmoduleOnly.
   Ожидаемое наблюдение: Порядок разрешается детерминированно; правило submoduleOnly применяется к настоящему gitlink demo-icon-module, но не к обычной payment-app.

**Контрпример:** Внести некорректный REGEX или неизвестный iconId.
Ожидаемое наблюдение: Появляется конкретная диагностика; ошибочное правило не вытесняет действующее.

**Восстановление:** Работать в отдельной копии. Отменить свои изменения в редакторе, вернуть изменённую настройку, остановить только запущенный для этой проверки процесс. Для следующей мутации создать новую чистую копию; исходный набор сохраняется.

**Доказательство:** Записать ID сценария, точный plugin/IDE build, project path и HEAD, вход и результат в RUN_RECORD. Для UI приложить видимое наблюдение; для экспорта — файл и hash. Успех producer/checker не присваивает PASS плагину.

**Consumer run:** `NOT_RUN`. Capability IDs: DEV-ICONS.

<a id="dev-05"></a>
### DEV-05 — Жизненный цикл custom .aficons

**Зачем:** Добавить свой pack и проверить замену, экспорт и возвращение к fallback.

**Подготовка:** Открыть указанную лабораторию в IDEA с ArchVerity 3.0.3, JDK 21 для Gradle; дождаться import/index. Для полного показа использовать настоящий Trial/Pro. Требования отдельных инструментов перечислены ниже и в linked guides.

**Входы:** [archverity-qa.aficons](../projects/workspace/archverity-qa.aficons), [archflow-studio.aficons](../projects/workspace/archflow-studio.aficons), [generate_icon_pack.py](../projects/workspace/qa-support/generate_icon_pack.py)

1. Импортировать archverity-qa.aficons, включить pack и экспортировать его в work/.
   Ожидаемое наблюдение: Pack имеет demo ID и 63 glyphs; экспорт открывается как корректный pack.
2. Сгенерировать v2 тем же ID по README, Import → Replace; проверить version 2 и новый accent в ansible.svg.
   Ожидаемое наблюдение: Заменилось содержимое pack, а не только строка списка; disable и enable изменяют фактическую иконку.

**Контрпример:** Отменить Replace; затем Remove именно импортированного demo pack.
Ожидаемое наблюдение: Cancel сохраняет первую версию; Remove убирает только выбранный pack и возвращает подходящий bundled fallback.

**Восстановление:** Работать в отдельной копии. Отменить свои изменения в редакторе, вернуть изменённую настройку, остановить только запущенный для этой проверки процесс. Для следующей мутации создать новую чистую копию; исходный набор сохраняется.

**Доказательство:** Записать ID сценария, точный plugin/IDE build, project path и HEAD, вход и результат в RUN_RECORD. Для UI приложить видимое наблюдение; для экспорта — файл и hash. Успех producer/checker не присваивает PASS плагину.

**Consumer run:** `NOT_RUN`. Capability IDs: DEV-ICONS.

## Keystore и X.509

<a id="key-01"></a>
### KEY-01 — Типы хранилищ, aliases и certificate chains

**Зачем:** Исследовать содержимое хранилища, aliases и chains без изменения ключевого материала.

**Подготовка:** Все семь public-only inputs поставляются готовыми; password archverity-qa-only защищает целостность открытых demo-файлов. Закрытых ключей и действующих credentials в них нет. Плагин поставляет BC 1.85; standalone Java verifier использует тот же jar для BKS/BCFKS/UBER.

**Входы:** [qa-cert.pem](../projects/workspace/qa-cert.pem), [qa-cert.der](../projects/workspace/qa-cert.der), [qa-public-artifacts.pem](../projects/workspace/qa-public-artifacts.pem), [qa-request.csr](../projects/workspace/qa-request.csr), [qa-public-key.pem](../projects/workspace/qa-public-key.pem), [qa-truststore.p12](../projects/workspace/qa-truststore.p12), [qa-truststore.jks](../projects/workspace/qa-truststore.jks), [qa-truststore.jceks](../projects/workspace/qa-truststore.jceks), [qa-truststore.pfx](../projects/workspace/qa-truststore.pfx), [qa-truststore.bks](../projects/workspace/qa-truststore.bks), [qa-truststore.bcfks](../projects/workspace/qa-truststore.bcfks), [qa-truststore.uber](../projects/workspace/qa-truststore.uber), [PublicTruststores.java](../suite-support/PublicTruststores.java), [public_truststores.json](../suite-support/public_truststores.json), [ICON_AND_KEYSTORE_INPUTS_RU.md](../docs/ICON_AND_KEYSTORE_INPUTS_RU.md)

1. Inspect qa-truststore.p12 с demo-паролем archverity-qa-only через Keystore и Project View action.
   Ожидаемое наблюдение: Тип PKCS12, alias, trustedCertEntry и fingerprint видны; закрытого ключа в этом input нет.
2. По очереди Inspect qa-truststore.jks/.jceks/.pfx/.bks/.bcfks/.uber с тем же demo-паролем; открыть alias/certificate.
   Ожидаемое наблюдение: Все семь файлов содержат только archverity-qa trusted certificate с одинаковым SHA-256; тип и фактический JDK/BC provider отображаются, isKeyEntry=false.

**Контрпример:** Ввести неверный пароль или открыть повреждённую копию.
Ожидаемое наблюдение: Явная ошибка без успешного пустого хранилища; другой сохранённый результат не выдаётся за новый.

**Восстановление:** Работать в отдельной копии. Отменить свои изменения в редакторе, вернуть изменённую настройку, остановить только запущенный для этой проверки процесс. Для следующей мутации создать новую чистую копию; исходный набор сохраняется.

**Доказательство:** Записать ID сценария, точный plugin/IDE build, project path и HEAD, вход и результат в RUN_RECORD. Для UI приложить видимое наблюдение; для экспорта — файл и hash. Успех producer/checker не присваивает PASS плагину.

**Consumer run:** `NOT_RUN`. Capability IDs: DEV-CRYPTO.

<a id="key-02"></a>
### KEY-02 — Certificate, PEM/DER, CRL, CSR и key metadata

**Зачем:** Сопоставить публичные криптографические артефакты и проверить их метаданные/подписи.

**Подготовка:** Открыть указанную лабораторию в IDEA с ArchVerity 3.0.3, JDK 21 для Gradle; дождаться import/index. Для полного показа использовать настоящий Trial/Pro. Требования отдельных инструментов перечислены ниже и в linked guides.

**Входы:** [qa-cert.pem](../projects/workspace/qa-cert.pem), [qa-cert.der](../projects/workspace/qa-cert.der), [qa-public-artifacts.pem](../projects/workspace/qa-public-artifacts.pem), [qa-request.csr](../projects/workspace/qa-request.csr), [qa-public-key.pem](../projects/workspace/qa-public-key.pem), [qa-truststore.p12](../projects/workspace/qa-truststore.p12)

1. Inspect qa-cert.pem и qa-cert.der; сравнить fingerprint и validity. Затем Inspect qa-public-artifacts.pem.
   Ожидаемое наблюдение: PEM/DER описывают один сертификат; bundle содержит другой сертификат и CRL с одной записью.
2. Открыть qa-request.csr и qa-public-key.pem; проверить subject/public-key relation и результат CSR signature check.
   Ожидаемое наблюдение: CSR и public key относятся к сертификату bundle; validity, signature state и Copy fingerprint доступны.

**Контрпример:** Открыть повреждённую копию PEM; private-key metadata проверять лишь на отдельном разрешённом операторском input.
Ожидаемое наблюдение: Повреждение даёт диагностику; private-key bytes не показываются и не экспортируются. Без такого input эта часть NOT RUN.

**Восстановление:** Работать в отдельной копии. Отменить свои изменения в редакторе, вернуть изменённую настройку, остановить только запущенный для этой проверки процесс. Для следующей мутации создать новую чистую копию; исходный набор сохраняется.

**Доказательство:** Записать ID сценария, точный plugin/IDE build, project path и HEAD, вход и результат в RUN_RECORD. Для UI приложить видимое наблюдение; для экспорта — файл и hash. Успех producer/checker не присваивает PASS плагину.

**Consumer run:** `NOT_RUN`. Capability IDs: DEV-CRYPTO.

## Инструменты разработчика

<a id="devs-01"></a>
### DEVS-01 — HTTP Send, Cancel, limits и response

**Зачем:** Отправлять и диагностировать запросы, ограничивать нагрузку и безопасно отменять ожидание.

**Подготовка:** Запустить python projects/api-lab/serve.py --protocol http. В API указать http://127.0.0.1:18427; если порт изменён, поменять URL во всех inputs.

**Входы:** [requests.http](../projects/api-lab/requests.http), [qa-openapi.json](../projects/workspace/qa-openapi.json), [qa-postman.json](../projects/workspace/qa-postman.json), [qa-curl.txt](../projects/workspace/qa-curl.txt)

1. Запустить api-lab; Send GET /health, POST /qa-roundtrip с {"id":42}; раскрыть Limits.
   Ожидаемое наблюдение: HTTP 200; ответ POST содержит received.id=42; status, headers и body относятся к выбранному запросу.
2. Отправить /qa-slow?delay_ms=5000, Cancel, сразу Send /health; затем /large?bytes=100000 с меньшим byte budget.
   Ожидаемое наблюдение: Поздний slow response не заменяет новый health result; лимит явно показывает truncation/ошибку вместо полного PASS.

**Контрпример:** Send /missing и /error; затем корректный /health.
Ожидаемое наблюдение: 404 и 500 видимы как ответы; следующий 200 не наследует body/status ошибки.

**Восстановление:** Работать в отдельной копии. Отменить свои изменения в редакторе, вернуть изменённую настройку, остановить только запущенный для этой проверки процесс. Для следующей мутации создать новую чистую копию; исходный набор сохраняется.

**Доказательство:** Записать ID сценария, точный plugin/IDE build, project path и HEAD, вход и результат в RUN_RECORD. Для UI приложить видимое наблюдение; для экспорта — файл и hash. Успех producer/checker не присваивает PASS плагину.

**Consumer run:** `NOT_RUN`. Capability IDs: API-HTTP.

<a id="devs-02"></a>
### DEVS-02 — Environment variables, headers и PasswordSafe

**Зачем:** Повторно использовать окружения и передавать secrets через специальное хранилище.

**Подготовка:** Открыть указанную лабораторию в IDEA с ArchVerity 3.0.3, JDK 21 для Gradle; дождаться import/index. Для полного показа использовать настоящий Trial/Pro. Требования отдельных инструментов перечислены ниже и в linked guides.

**Входы:** [requests.http](../projects/api-lab/requests.http), [qa-openapi.json](../projects/workspace/qa-openapi.json), [qa-postman.json](../projects/workspace/qa-postman.json), [qa-curl.txt](../projects/workspace/qa-curl.txt), [coverage.json](../projects/workspace/qa-support/coverage.json)

1. Environments: создать demo-local, variable DEMO=local; Send /headers с X-Demo: {{DEMO}}.
   Ожидаемое наблюдение: demoHeader=local; выбранное окружение используется этим запросом.
2. С операторским одноразовым secret использовать Set secret и запрос /headers; открыть только несекретный settings export.
   Ожидаемое наблюдение: hasAuthorization показывает присутствие header без его значения; secret хранится через PasswordSafe, а не plain project JSON.

**Контрпример:** Сослаться на {{MISSING_DEMO_VARIABLE}}.
Ожидаемое наблюдение: Запрос отклоняется с указанием отсутствующей переменной; placeholder не отправляется буквальным текстом.

**Восстановление:** Работать в отдельной копии. Отменить свои изменения в редакторе, вернуть изменённую настройку, остановить только запущенный для этой проверки процесс. Для следующей мутации создать новую чистую копию; исходный набор сохраняется.

**Доказательство:** Записать ID сценария, точный plugin/IDE build, project path и HEAD, вход и результат в RUN_RECORD. Для UI приложить видимое наблюдение; для экспорта — файл и hash. Успех producer/checker не присваивает PASS плагину.

**Consumer run:** `NOT_RUN`. Capability IDs: API-HTTP, IDE-SETTINGS.

<a id="devs-03"></a>
### DEVS-03 — DSL, captures, assertions и последовательные Scenarios

**Зачем:** Проверять API цепочками с точными assertions и передавать значения между шагами.

**Подготовка:** Открыть указанную лабораторию в IDEA с ArchVerity 3.0.3, JDK 21 для Gradle; дождаться import/index. Для полного показа использовать настоящий Trial/Pro. Требования отдельных инструментов перечислены ниже и в linked guides.

**Входы:** [happy.json](../projects/api-lab/scenarios/happy.json), [assertion-fails.json](../projects/api-lab/scenarios/assertion-fails.json), [missing-variable.json](../projects/api-lab/scenarios/missing-variable.json), [dsl-types.json](../projects/api-lab/scenarios/dsl-types.json), [wrong-json-type.json](../projects/api-lab/scenarios/wrong-json-type.json), [missing-json-pointer.json](../projects/api-lab/scenarios/missing-json-pointer.json), [unsupported-javascript.json](../projects/api-lab/scenarios/unsupported-javascript.json)

1. В Scenarios вставить dsl-types.json и запустить.
   Ожидаемое наблюдение: Шаг 1 проверяет number/string/boolean/null, массив и escaped JSON Pointer; capture ID=42 попадает в POST шага 2.
2. Повторить запуск и выполнить happy.json.
   Ожидаемое наблюдение: Captures принадлежат одному запуску; шаги исполняются последовательно, результат каждого шага виден.

**Контрпример:** По очереди выполнить wrong-json-type.json, missing-json-pointer.json, missing-variable.json и unsupported-javascript.json.
Ожидаемое наблюдение: Каждый завершается конкретной ошибкой; последующие шаги после ошибки не исполняются; Postman JS не запускается.

**Восстановление:** Работать в отдельной копии. Отменить свои изменения в редакторе, вернуть изменённую настройку, остановить только запущенный для этой проверки процесс. Для следующей мутации создать новую чистую копию; исходный набор сохраняется.

**Доказательство:** Записать ID сценария, точный plugin/IDE build, project path и HEAD, вход и результат в RUN_RECORD. Для UI приложить видимое наблюдение; для экспорта — файл и hash. Успех producer/checker не присваивает PASS плагину.

**Consumer run:** `NOT_RUN`. Capability IDs: API-SCENARIOS.

<a id="devs-04"></a>
### DEVS-04 — WebSocket и динамический gRPC

**Зачем:** Исследовать сообщения WebSocket и schema-bound gRPC вызовы с контролем lifecycle.

**Подготовка:** Открыть указанную лабораторию в IDEA с ArchVerity 3.0.3, JDK 21 для Gradle; дождаться import/index. Для полного показа использовать настоящий Trial/Pro. Требования отдельных инструментов перечислены ниже и в linked guides.

**Входы:** [websocket_server.py](../projects/api-lab/websocket_server.py), [echo.proto](../projects/api-lab/schema/echo.proto), [echo.pb](../projects/api-lab/schema/echo.pb), [grpc_server.py](../projects/api-lab/grpc_server.py)

1. Запустить все api-lab transports; WS Connect ws://127.0.0.1:18428 → Send ArchVerity → Close.
   Ожидаемое наблюдение: Входящий текст совпадает с отправленным; sequence/close состояние относится к текущей сессии.
2. gRPC: Load schema/echo.pb, target 127.0.0.1:18429; вызвать Echo/Health с {}, Echo/Say и Echo/Watch по README.
   Ожидаемое наблюдение: Imported google.protobuf.Empty разрешается; unary body корректен, server stream упорядочен, Cancel/deadline завершает вызов.

**Контрпример:** WS send error/reconnect; gRPC Fail, deadline и Upload/Chat.
Ожидаемое наблюдение: 1011 и INVALID_ARGUMENT видимы; восстановление создаёт новую сессию; client/bidi streams явно unsupported, без зависания.

**Восстановление:** Работать в отдельной копии. Отменить свои изменения в редакторе, вернуть изменённую настройку, остановить только запущенный для этой проверки процесс. Для следующей мутации создать новую чистую копию; исходный набор сохраняется.

**Доказательство:** Записать ID сценария, точный plugin/IDE build, project path и HEAD, вход и результат в RUN_RECORD. Для UI приложить видимое наблюдение; для экспорта — файл и hash. Успех producer/checker не присваивает PASS плагину.

**Consumer run:** `NOT_RUN`. Capability IDs: API-WEBSOCKET, API-GRPC.

<a id="devs-05"></a>
### DEVS-05 — Четыре импорта, request exports, cookies и history

**Зачем:** Переносить запросы между форматами и управлять session cookies/history.

**Подготовка:** Открыть указанную лабораторию в IDEA с ArchVerity 3.0.3, JDK 21 для Gradle; дождаться import/index. Для полного показа использовать настоящий Trial/Pro. Требования отдельных инструментов перечислены ниже и в linked guides.

**Входы:** [requests.http](../projects/api-lab/requests.http), [qa-openapi.json](../projects/workspace/qa-openapi.json), [qa-postman.json](../projects/workspace/qa-postman.json), [qa-curl.txt](../projects/workspace/qa-curl.txt)

1. Через Import .http / Import cURL / Import OpenAPI/Postman импортировать четыре workspace inputs и отправить по одному запросу.
   Ожидаемое наблюдение: URL, method, headers/body перенесены; все запросы идут в тот же loopback API.
2. Copy cURL, Save .http, Copy OpenAPI, Copy Postman; повторно импортировать сохранённый demo request. Затем /cookies/set → /cookies/show → Clear cookies → show; открыть history.
   Ожидаемое наблюдение: Roundtrip сохраняет семантику запроса; hasDemoCookie меняется true → false; history повторяет выбранный собственный запрос.

**Контрпример:** Импортировать повреждённую JSON-копию; Clear history.
Ожидаемое наблюдение: Import error не заменяет исправный запрос; очищается история demo-запросов, не список исходных endpoint contracts.

**Восстановление:** Работать в отдельной копии. Отменить свои изменения в редакторе, вернуть изменённую настройку, остановить только запущенный для этой проверки процесс. Для следующей мутации создать новую чистую копию; исходный набор сохраняется.

**Доказательство:** Записать ID сценария, точный plugin/IDE build, project path и HEAD, вход и результат в RUN_RECORD. Для UI приложить видимое наблюдение; для экспорта — файл и hash. Успех producer/checker не присваивает PASS плагину.

**Consumer run:** `NOT_RUN`. Capability IDs: API-HTTP.

<a id="devs-06"></a>
### DEVS-06 — Spring inspect, profiles и source navigation

**Зачем:** Понять effective Spring configuration и найти её конкретный источник.

**Подготовка:** Открыть указанную лабораторию в IDEA с ArchVerity 3.0.3, JDK 21 для Gradle; дождаться import/index. Для полного показа использовать настоящий Trial/Pro. Требования отдельных инструментов перечислены ниже и в linked guides.

**Входы:** [application.yml](../projects/workspace/payment-app/src/main/resources/application.yml), [application-qa.properties](../projects/workspace/payment-app/src/main/resources/application-qa.properties), [application-demo.properties](../projects/workspace/payment-app/src/main/resources/application-demo.properties), [application-dev.yml](../projects/workspace/payment-app/src/main/resources/application-dev.yml), [.archflow.yml](../projects/workspace/.archflow.yml), [extended_scenarios.py](../projects/workspace/qa-support/extended_scenarios.py)

1. Spring → Inspect project; поиск payment и фильтр profile dev.
   Ожидаемое наблюдение: application.yml, application-dev.yml/properties и связанные keys различимы; профиль меняет effective view.
2. Открыть строку результата; сравнить override/import с .archflow.yml и локальными application-demo.properties.
   Ожидаемое наблюдение: Навигация идёт к точному ключу; local import и выбранные profiles отражаются в context fingerprint.

**Контрпример:** На новой копии применить spring-profile или scope-change и пересканировать.
Ожидаемое наблюдение: Scope/context change не объявляет исчезнувшее finding resolved; неподдержанный import получает диагностику.

**Восстановление:** Работать в отдельной копии. Отменить свои изменения в редакторе, вернуть изменённую настройку, остановить только запущенный для этой проверки процесс. Для следующей мутации создать новую чистую копию; исходный набор сохраняется.

**Доказательство:** Записать ID сценария, точный plugin/IDE build, project path и HEAD, вход и результат в RUN_RECORD. Для UI приложить видимое наблюдение; для экспорта — файл и hash. Успех producer/checker не присваивает PASS плагину.

**Consumer run:** `NOT_RUN`. Capability IDs: DEV-SPRING, ARCH-PROPERTIES, ARCH-SCOPE.

<a id="devs-07"></a>
### DEVS-07 — Spring completion, docs, strings и injected language

**Зачем:** Редактировать конфигурацию с completion/docs и переходами из кода.

**Подготовка:** Открыть указанную лабораторию в IDEA с ArchVerity 3.0.3, JDK 21 для Gradle; дождаться import/index. Для полного показа использовать настоящий Trial/Pro. Требования отдельных инструментов перечислены ниже и в linked guides.

**Входы:** [application.yml](../projects/workspace/payment-app/src/main/resources/application.yml), [application-qa.properties](../projects/workspace/payment-app/src/main/resources/application-qa.properties), [SpringPropertyReferences.java](../projects/workspace/payment-app/src/main/java/sample/payment/SpringPropertyReferences.java), [SpringPropertyReferences.kt](../projects/workspace/notification-app/src/main/kotlin/sample/notification/SpringPropertyReferences.kt), [application-editor-demo.yml](../projects/workspace/payment-app/src/main/resources/application-editor-demo.yml)

1. В application-qa.properties и application.yml вызвать Ctrl+Space на ключе и Quick Documentation; использовать известный ключ payment из fixture.
   Ожидаемое наблюдение: Предложения и документация относятся к property/key context и доступным metadata, с источником определения.
2. В новых Java/Kotlin SpringPropertyReferences на ${server.port:8085} и ${spring.rabbitmq.virtual-host} вызвать Ctrl+B; в application-editor-demo.yml проверить sql, regex и cron value injection при наличии соответствующего language plugin.
   Ожидаемое наблюдение: Переход ведёт к определению выбранного ключа; Injection классифицируется как SQL, RegExp либо CRON по поддержанному key; SpEL/JSON/URL этим injector не поддержаны. Отсутствующий language plugin фиксируется отдельно.

**Контрпример:** Использовать неизвестный ключ и обычную несвязанную строку.
Ожидаемое наблюдение: Нет выдуманного определения или Spring injection; неразрешённость остаётся явной.

**Восстановление:** Работать в отдельной копии. Отменить свои изменения в редакторе, вернуть изменённую настройку, остановить только запущенный для этой проверки процесс. Для следующей мутации создать новую чистую копию; исходный набор сохраняется.

**Доказательство:** Записать ID сценария, точный plugin/IDE build, project path и HEAD, вход и результат в RUN_RECORD. Для UI приложить видимое наблюдение; для экспорта — файл и hash. Успех producer/checker не присваивает PASS плагину.

**Consumer run:** `NOT_RUN`. Capability IDs: DEV-SPRING.

<a id="devs-08"></a>
### DEVS-08 — Spring YAML↔properties и key variants

**Зачем:** Менять представление конфигурации, сохраняя ключи и значения.

**Подготовка:** Открыть указанную лабораторию в IDEA с ArchVerity 3.0.3, JDK 21 для Gradle; дождаться import/index. Для полного показа использовать настоящий Trial/Pro. Требования отдельных инструментов перечислены ниже и в linked guides.

**Входы:** [application.yml](../projects/workspace/payment-app/src/main/resources/application.yml), [application-qa.properties](../projects/workspace/payment-app/src/main/resources/application-qa.properties)

1. Spring config action: конвертировать копию application.yml в properties и обратным действием в YAML.
   Ожидаемое наблюдение: Ключи, значения и вложенные пути сохраняют смысл; результат расположен в выбранном demo output.
2. Выбрать key с dotted/kebab naming и просмотреть предлагаемые relaxed variants/переход.
   Ожидаемое наблюдение: Преобразование относится к выбранному key; исходник и результат сравнимы.

**Контрпример:** Конвертировать повреждённую YAML-копию либо неподдержанный неоднозначный input.
Ожидаемое наблюдение: Появляется parse/validation error; исходный файл не заменяется успешной пустой конфигурацией.

**Восстановление:** Работать в отдельной копии. Отменить свои изменения в редакторе, вернуть изменённую настройку, остановить только запущенный для этой проверки процесс. Для следующей мутации создать новую чистую копию; исходный набор сохраняется.

**Доказательство:** Записать ID сценария, точный plugin/IDE build, project path и HEAD, вход и результат в RUN_RECORD. Для UI приложить видимое наблюдение; для экспорта — файл и hash. Успех producer/checker не присваивает PASS плагину.

**Consumer run:** `NOT_RUN`. Capability IDs: DEV-SPRING.

<a id="devs-09"></a>
### DEVS-09 — Все четыре Spring live templates

**Зачем:** Быстро создавать типовые Spring declarations в правильном language context.

**Подготовка:** Открыть runtime-evidence с настоящим Spring Boot classpath. Java templates имеют JAVA_DECLARATION/JAVA_CODE contexts; afprofile имеет OTHER context и его YAML block проверяют в YAML input. Изменять только demo/scratch файлы.

**Входы:** [application.yml](../projects/workspace/payment-app/src/main/resources/application.yml), [application-qa.properties](../projects/workspace/payment-app/src/main/resources/application-qa.properties), [TemplateTargets.java](../projects/runtime-evidence/src/main/java/demo/evidence/TemplateTargets.java), [application-demo.properties](../projects/runtime-evidence/src/main/resources/application-demo.properties)

1. В Java declaration expand afcfgrecord; задать PREFIX=demo, NAME=DemoProperties, TYPE=String, PROPERTY=value.
   Ожидаемое наблюдение: Получается ConfigurationProperties record с prefix demo и компонентом value.
2. В TemplateTargets.java expand afvalue над полем; в scratch method expand afgetprop; в YAML application.yml expand afprofile.
   Ожидаемое наблюдение: afvalue создаёт @Value с key/default, afgetprop — getRequiredProperty, afprofile — spring.config.activate.on-profile block.

**Контрпример:** Попытаться раскрыть Java template в несоответствующем language/context.
Ожидаемое наблюдение: Java template не предлагается как подходящий; обычный введённый текст не выдаётся за успешное expansion. afprofile имеет общий OTHER context, поэтому проверяется отдельно.

**Восстановление:** Работать в отдельной копии. Отменить свои изменения в редакторе, вернуть изменённую настройку, остановить только запущенный для этой проверки процесс. Для следующей мутации создать новую чистую копию; исходный набор сохраняется.

**Доказательство:** Записать ID сценария, точный plugin/IDE build, project path и HEAD, вход и результат в RUN_RECORD. Для UI приложить видимое наблюдение; для экспорта — файл и hash. Успех producer/checker не присваивает PASS плагину.

**Consumer run:** `NOT_RUN`. Capability IDs: DEV-SPRING.

<a id="devs-10"></a>
### DEVS-10 — MyBatis paste/selection → готовый SQL

**Зачем:** Получать исполнимый SQL из Preparing/Parameters без ручного подставления literals.

**Подготовка:** Открыть указанную лабораторию в IDEA с ArchVerity 3.0.3, JDK 21 для Gradle; дождаться import/index. Для полного показа использовать настоящий Trial/Pro. Требования отдельных инструментов перечислены ниже и в linked guides.

**Входы:** [MyBatisConsoleFixture.java](../projects/workspace/mybatis-console-fixture/src/main/java/sample/mybatis/MyBatisConsoleFixture.java), [PaymentMapper.xml](../projects/workspace/payment-app/src/main/resources/mappers/PaymentMapper.xml), [PaymentNotificationMapper.kt](../projects/workspace/notification-app/src/main/kotlin/sample/notification/PaymentNotificationMapper.kt)

1. Скопировать обе строки Preparing/Parameters из MyBatisConsoleFixture.java в MyBatis panel → Restore.
   Ожидаемое наблюдение: Восстановлены id=42 и status='O''Reilly'; placeholders заменены в правильном порядке.
2. В Run console выделить тот же блок и вызвать Restore MyBatis SQL; проверить Format и Copy.
   Ожидаемое наблюдение: Контекстное действие и paste дают одинаковый SQL; formatting не меняет параметры.

**Контрпример:** Убрать один Parameters value либо нарушить Preparing line.
Ожидаемое наблюдение: Несовпадение параметров показано как partial/ошибка; не получается ложный полностью восстановленный SQL.

**Восстановление:** Работать в отдельной копии. Отменить свои изменения в редакторе, вернуть изменённую настройку, остановить только запущенный для этой проверки процесс. Для следующей мутации создать новую чистую копию; исходный набор сохраняется.

**Доказательство:** Записать ID сценария, точный plugin/IDE build, project path и HEAD, вход и результат в RUN_RECORD. Для UI приложить видимое наблюдение; для экспорта — файл и hash. Успех producer/checker не присваивает PASS плагину.

**Consumer run:** `NOT_RUN`. Capability IDs: DEV-MYBATIS.

<a id="devs-11"></a>
### DEVS-11 — MyBatis live capture из Run console

**Зачем:** Восстанавливать запросы непосредственно из реального запуска приложения.

**Подготовка:** Открыть указанную лабораторию в IDEA с ArchVerity 3.0.3, JDK 21 для Gradle; дождаться import/index. Для полного показа использовать настоящий Trial/Pro. Требования отдельных инструментов перечислены ниже и в linked guides.

**Входы:** [MyBatisConsoleFixture.java](../projects/workspace/mybatis-console-fixture/src/main/java/sample/mybatis/MyBatisConsoleFixture.java), [PaymentMapper.xml](../projects/workspace/payment-app/src/main/resources/mappers/PaymentMapper.xml), [PaymentNotificationMapper.kt](../projects/workspace/notification-app/src/main/kotlin/sample/notification/PaymentNotificationMapper.kt)

1. Запустить main MyBatisConsoleFixture в Run configuration; открыть MyBatis live console.
   Ожидаемое наблюдение: Реальные Preparing и Parameters захватываются в один восстановленный query.
2. Повторить Run, проверить выбранную строку, Copy/Format и доступную историю.
   Ожидаемое наблюдение: Новый query относится к новому запуску; SQL и escaped literal остаются воспроизводимыми.

**Контрпример:** Остановить процесс до Parameters либо вывести посторонние log lines.
Ожидаемое наблюдение: Частичный блок не подменяется завершённым query и не забирает параметры соседнего блока.

**Восстановление:** Работать в отдельной копии. Отменить свои изменения в редакторе, вернуть изменённую настройку, остановить только запущенный для этой проверки процесс. Для следующей мутации создать новую чистую копию; исходный набор сохраняется.

**Доказательство:** Записать ID сценария, точный plugin/IDE build, project path и HEAD, вход и результат в RUN_RECORD. Для UI приложить видимое наблюдение; для экспорта — файл и hash. Успех producer/checker не присваивает PASS плагину.

**Consumer run:** `NOT_RUN`. Capability IDs: DEV-MYBATIS.

<a id="devs-12"></a>
### DEVS-12 — MyBatis Java/Kotlin/XML navigation и settings

**Зачем:** Переходить между mapper methods и XML statements, настроив поведение console.

**Подготовка:** Открыть указанную лабораторию в IDEA с ArchVerity 3.0.3, JDK 21 для Gradle; дождаться import/index. Для полного показа использовать настоящий Trial/Pro. Требования отдельных инструментов перечислены ниже и в linked guides.

**Входы:** [MyBatisConsoleFixture.java](../projects/workspace/mybatis-console-fixture/src/main/java/sample/mybatis/MyBatisConsoleFixture.java), [PaymentMapper.xml](../projects/workspace/payment-app/src/main/resources/mappers/PaymentMapper.xml), [PaymentNotificationMapper.kt](../projects/workspace/notification-app/src/main/kotlin/sample/notification/PaymentNotificationMapper.kt), [coverage.json](../projects/workspace/qa-support/coverage.json), [PaymentNotificationMapper.xml](../projects/workspace/notification-app/src/main/resources/mappers/PaymentNotificationMapper.xml)

1. Ctrl+B на PaymentMapper.findById и XML namespace/id/include refid; повторить PaymentNotificationMapper.kt ↔ PaymentNotificationMapper.xml.
   Ожидаемое наблюдение: Каждый переход ведёт к своему mapper/statement; Java, Kotlin и XML проверены отдельно.
2. В MyBatis Assistant изменить несекретную опцию live capture/format, применить, переоткрыть и повторить один query.
   Ожидаемое наблюдение: Опция сохранена и меняет именно назначенное поведение.

**Контрпример:** В копии изменить statement id на неизвестный.
Ожидаемое наблюдение: Нет перехода к чужому похожему statement; восстановление id возвращает правильную ссылку.

**Восстановление:** Работать в отдельной копии. Отменить свои изменения в редакторе, вернуть изменённую настройку, остановить только запущенный для этой проверки процесс. Для следующей мутации создать новую чистую копию; исходный набор сохраняется.

**Доказательство:** Записать ID сценария, точный plugin/IDE build, project path и HEAD, вход и результат в RUN_RECORD. Для UI приложить видимое наблюдение; для экспорта — файл и hash. Успех producer/checker не присваивает PASS плагину.

**Consumer run:** `NOT_RUN`. Capability IDs: DEV-MYBATIS, IDE-SETTINGS.

<a id="devs-13"></a>
### DEVS-13 — Ansible project model и offline editor support

**Зачем:** Ориентироваться в Ansible roles/inventory/variables без обязательного сетевого каталога.

**Подготовка:** Открыть указанную лабораторию в IDEA с ArchVerity 3.0.3, JDK 21 для Gradle; дождаться import/index. Для полного показа использовать настоящий Trial/Pro. Требования отдельных инструментов перечислены ниже и в linked guides.

**Входы:** [site.yml](../projects/workspace/ansible/professional/playbooks/site.yml), [vault-plain.yml](../projects/workspace/ansible/vault-plain.yml)

1. Inspect ansible/professional: inventories, group_vars/host_vars, roles, collection acme.platform, Jinja template.
   Ожидаемое наблюдение: Типы и связи видны с project-relative source locations.
2. Ctrl+B на role/import_tasks/include_vars/module references; Ctrl+Space на task module и доступной variable.
   Ожидаемое наблюдение: Переходы ведут к конкретному role/task/vars; offline module catalog и project symbols различимы.

**Контрпример:** В копии сослаться на отсутствующий role/variable.
Ожидаемое наблюдение: Неизвестная ссылка обозначается, а не ведёт к случайному соседнему файлу.

**Восстановление:** Работать в отдельной копии. Отменить свои изменения в редакторе, вернуть изменённую настройку, остановить только запущенный для этой проверки процесс. Для следующей мутации создать новую чистую копию; исходный набор сохраняется.

**Доказательство:** Записать ID сценария, точный plugin/IDE build, project path и HEAD, вход и результат в RUN_RECORD. Для UI приложить видимое наблюдение; для экспорта — файл и hash. Успех producer/checker не присваивает PASS плагину.

**Consumer run:** `NOT_RUN`. Capability IDs: DEV-ANSIBLE.

<a id="devs-14"></a>
### DEVS-14 — Vault encrypt и decrypt/edit/re-encrypt

**Зачем:** Редактировать разрешённый Vault input с сохранением шифрованного состояния.

**Подготовка:** Нужны изолированная копия, отдельно разрешённый тестовый password и право на local encrypt/edit. В repository есть только synthetic plaintext; secret/ключи не создаются и не публикуются автоматически.

**Входы:** [site.yml](../projects/workspace/ansible/professional/playbooks/site.yml), [vault-plain.yml](../projects/workspace/ansible/vault-plain.yml)

1. На отдельной копии vault-plain.yml вызвать Encrypt Ansible Vault и использовать разрешённый операторский одноразовый password/vault-id.
   Ожидаемое наблюдение: Получен корректный $ANSIBLE_VAULT header; публичный fixture не изменён.
2. Decrypt/Edit, поменять синтетическое поле, сохранить; снова открыть с тем же password.
   Ожидаемое наблюдение: Изменённое значение восстановлено после re-encrypt; plaintext не сохранён отдельным project file.

**Контрпример:** Неверный password/HMAC или Cancel в editor.
Ожидаемое наблюдение: Ошибка fail-closed; Cancel сохраняет исходный encrypted input, никакого partial plaintext overwrite.

**Восстановление:** Работать в отдельной копии. Отменить свои изменения в редакторе, вернуть изменённую настройку, остановить только запущенный для этой проверки процесс. Для следующей мутации создать новую чистую копию; исходный набор сохраняется.

**Доказательство:** Записать ID сценария, точный plugin/IDE build, project path и HEAD, вход и результат в RUN_RECORD. Для UI приложить видимое наблюдение; для экспорта — файл и hash. Успех producer/checker не присваивает PASS плагину.

**Consumer run:** `NOT_RUN`. Capability IDs: DEV-ANSIBLE.

<a id="devs-15"></a>
### DEVS-15 — Ansible syntax check и process lifecycle

**Зачем:** Получать результат установленного syntax checker, а не только parse модели.

**Подготовка:** Открыть указанную лабораторию в IDEA с ArchVerity 3.0.3, JDK 21 для Gradle; дождаться import/index. Для полного показа использовать настоящий Trial/Pro. Требования отдельных инструментов перечислены ниже и в linked guides.

**Входы:** [site.yml](../projects/workspace/ansible/professional/playbooks/site.yml), [vault-plain.yml](../projects/workspace/ansible/vault-plain.yml)

1. С установленным ansible-playbook выполнить ANSIBLE_SYNTAX_CHECK для ansible/playbook.yml.
   Ожидаемое наблюдение: Реальный process output и exit code показывают syntax result.
2. В отдельной копии нарушить YAML/task syntax, повторить и исправить.
   Ожидаемое наблюдение: Неверный input получает nonzero/diagnostic; исправленный input снова проверяется.

**Контрпример:** Запустить при отсутствующем executable либо Cancel активную проверку.
Ожидаемое наблюдение: Сообщается точная недоступная зависимость; Cancel завершает свой process, а не показывает старый PASS.

**Восстановление:** Работать в отдельной копии. Отменить свои изменения в редакторе, вернуть изменённую настройку, остановить только запущенный для этой проверки процесс. Для следующей мутации создать новую чистую копию; исходный набор сохраняется.

**Доказательство:** Записать ID сценария, точный plugin/IDE build, project path и HEAD, вход и результат в RUN_RECORD. Для UI приложить видимое наблюдение; для экспорта — файл и hash. Успех producer/checker не присваивает PASS плагину.

**Consumer run:** `NOT_RUN`. Capability IDs: DEV-ANSIBLE.

<a id="devs-16"></a>
### DEVS-16 — ShellCheck и shfmt diff

**Зачем:** Находить shell diagnostics и форматировать scripts по реальному diff.

**Подготовка:** Открыть указанную лабораторию в IDEA с ArchVerity 3.0.3, JDK 21 для Gradle; дождаться import/index. Для полного показа использовать настоящий Trial/Pro. Требования отдельных инструментов перечислены ниже и в linked guides.

**Входы:** [common.sh](../projects/workspace/shell-professional/lib/common.sh), [deploy.bats](../projects/workspace/shell-professional/test/deploy.bats), [qa-debug.sh](../projects/workspace/shell-professional/qa-debug.sh)

1. SHELLCHECK для shell-professional/lib/common.sh; SHFMT_DIFF для shell-tools/format.sh.
   Ожидаемое наблюдение: Показаны реальные tool diagnostics и ожидаемый formatting diff.
2. В копии применить предлагаемое форматирование, повторить diff; проверить Ctrl+B/rename function reference.
   Ожидаемое наблюдение: Diff исчезает после исправления; символ и его ссылки относятся к одной функции.

**Контрпример:** Передать неподдержанный/отсутствующий path или отсутствующий executable.
Ожидаемое наблюдение: Явная ошибка запуска/path validation; старый успешный tool output не считается новым.

**Восстановление:** Работать в отдельной копии. Отменить свои изменения в редакторе, вернуть изменённую настройку, остановить только запущенный для этой проверки процесс. Для следующей мутации создать новую чистую копию; исходный набор сохраняется.

**Доказательство:** Записать ID сценария, точный plugin/IDE build, project path и HEAD, вход и результат в RUN_RECORD. Для UI приложить видимое наблюдение; для экспорта — файл и hash. Успех producer/checker не присваивает PASS плагину.

**Consumer run:** `NOT_RUN`. Capability IDs: DEV-SHELL.

<a id="devs-17"></a>
### DEVS-17 — Bats обнаружение и два настоящих теста

**Зачем:** Запускать Bats tests и отличать успешный process от пройденных assertions.

**Подготовка:** Открыть указанную лабораторию в IDEA с ArchVerity 3.0.3, JDK 21 для Gradle; дождаться import/index. Для полного показа использовать настоящий Trial/Pro. Требования отдельных инструментов перечислены ниже и в linked guides.

**Входы:** [common.sh](../projects/workspace/shell-professional/lib/common.sh), [deploy.bats](../projects/workspace/shell-professional/test/deploy.bats), [qa-debug.sh](../projects/workspace/shell-professional/qa-debug.sh)

1. Открыть shell-professional/test/deploy.bats; выполнить BATS_TEST с этим project-relative path.
   Ожидаемое наблюдение: Bats распознаёт test declarations и реально выполняет два fixture tests.
2. В копии изменить одно expected value и повторить; вернуть исходное значение.
   Ожидаемое наблюдение: Один test падает с понятным output; восстановление возвращает проходящий suite.

**Контрпример:** Передать extensionless bin/deploy вместо Bats input.
Ожидаемое наблюдение: Не происходит ложного Bats PASS по одному наличию shell file.

**Восстановление:** Работать в отдельной копии. Отменить свои изменения в редакторе, вернуть изменённую настройку, остановить только запущенный для этой проверки процесс. Для следующей мутации создать новую чистую копию; исходный набор сохраняется.

**Доказательство:** Записать ID сценария, точный plugin/IDE build, project path и HEAD, вход и результат в RUN_RECORD. Для UI приложить видимое наблюдение; для экспорта — файл и hash. Успех producer/checker не присваивает PASS плагину.

**Consumer run:** `NOT_RUN`. Capability IDs: DEV-SHELL.

<a id="devs-18"></a>
### DEVS-18 — Shell editor, семь debugger commands и remote session

**Зачем:** Исследовать shell execution и symbols локально или в явно выбранной remote среде.

**Подготовка:** Открыть указанную лабораторию в IDEA с ArchVerity 3.0.3, JDK 21 для Gradle; дождаться import/index. Для полного показа использовать настоящий Trial/Pro. Требования отдельных инструментов перечислены ниже и в linked guides.

**Входы:** [common.sh](../projects/workspace/shell-professional/lib/common.sh), [deploy.bats](../projects/workspace/shell-professional/test/deploy.bats), [qa-debug.sh](../projects/workspace/shell-professional/qa-debug.sh)

1. Ctrl+Space/Quick Documentation/Ctrl+B на function, source и variable в shell-professional; запустить BASH_DEBUG qa-debug.sh.
   Ожидаемое наблюдение: Определения, документация и completion относятся к реальным символам; debugger session остановлена на понятной строке.
2. В своей сессии выполнить BREAKPOINT, STEP, NEXT, PRINT_VARIABLE, STACK, CONTINUE, CLEAR_BREAKPOINTS; remote вариант — по ENVIRONMENT_CHECKS с разрешённым SSH host.
   Ожидаемое наблюдение: Каждая команда имеет наблюдаемую строку/значение/stack; локальная и remote сессии связаны с указанным script.

**Контрпример:** Команда после завершения сессии или unknown variable.
Ожидаемое наблюдение: Явное terminal/not-found состояние без возобновления чужого процесса.

**Восстановление:** Работать в отдельной копии. Отменить свои изменения в редакторе, вернуть изменённую настройку, остановить только запущенный для этой проверки процесс. Для следующей мутации создать новую чистую копию; исходный набор сохраняется.

**Доказательство:** Записать ID сценария, точный plugin/IDE build, project path и HEAD, вход и результат в RUN_RECORD. Для UI приложить видимое наблюдение; для экспорта — файл и hash. Успех producer/checker не присваивает PASS плагину.

**Consumer run:** `NOT_RUN`. Capability IDs: DEV-SHELL.

<a id="devs-19"></a>
### DEVS-19 — RN/Expo discovery и scripts

**Зачем:** Находить настоящий RN/Expo project и выполнять выбранные package scripts.

**Подготовка:** Открыть указанную лабораторию в IDEA с ArchVerity 3.0.3, JDK 21 для Gradle; дождаться import/index. Для полного показа использовать настоящий Trial/Pro. Требования отдельных инструментов перечислены ниже и в linked guides.

**Входы:** [package.json](../projects/mobile-lab/package.json), [package-lock.json](../projects/mobile-lab/package-lock.json), [index.js](../projects/mobile-lab/index.js), [App.js](../projects/mobile-lab/App.js), [app.json](../projects/mobile-lab/app.json)

1. React Native → Detect projects в mobile-lab; выбрать найденное Expo/RN package.json.
   Ожидаемое наблюдение: Выбрано настоящее приложение com.archverity.demo с pinned lockfile; не workspace detection-only rn-qa.
2. RN_SCRIPT qa:verify; проверить work/qa-script-result.txt.
   Ожидаемое наблюдение: Процесс завершился успешно; файл содержит RN_SCRIPT_OK.

**Контрпример:** Указать несуществующий script либо package без RN/Expo.
Ожидаемое наблюдение: Появляется конкретная ошибка/detection result, без выдуманного bundle.

**Восстановление:** Работать в отдельной копии. Отменить свои изменения в редакторе, вернуть изменённую настройку, остановить только запущенный для этой проверки процесс. Для следующей мутации создать новую чистую копию; исходный набор сохраняется.

**Доказательство:** Записать ID сценария, точный plugin/IDE build, project path и HEAD, вход и результат в RUN_RECORD. Для UI приложить видимое наблюдение; для экспорта — файл и hash. Успех producer/checker не присваивает PASS плагину.

**Consumer run:** `NOT_RUN`. Capability IDs: DEV-MOBILE.

<a id="devs-20"></a>
### DEVS-20 — Metro, Expo, bundle и платформенные команды

**Зачем:** Запускать dev servers, получать JS bundles и работать с подготовленными native hosts.

**Подготовка:** Открыть указанную лабораторию в IDEA с ArchVerity 3.0.3, JDK 21 для Gradle; дождаться import/index. Для полного показа использовать настоящий Trial/Pro. Требования отдельных инструментов перечислены ниже и в linked guides.

**Входы:** [package.json](../projects/mobile-lab/package.json), [package-lock.json](../projects/mobile-lab/package-lock.json), [index.js](../projects/mobile-lab/index.js), [App.js](../projects/mobile-lab/App.js), [app.json](../projects/mobile-lab/app.json)

1. После npm ci по очереди RN_METRO и RN_EXPO; для каждого дождаться ready и нажать Stop.
   Ожидаемое наблюдение: Реальный dev server отвечает packager-status:running и после Stop порт закрыт.
2. RN_BUNDLE android/ios; затем на отдельно подготовленном host проверить RN_ANDROID_RUN, RN_IOS_RUN, GRADLE_TASK, COCOAPODS_INSTALL, IOS_DEVICES по mobile table.
   Ожидаемое наблюдение: JS bundle создан из index.js; native commands выполняются только с сгенерированными android/ios и нужным SDK/device/macOS.

**Контрпример:** Выполнить native command без native folders или iOS command на Windows.
Ожидаемое наблюдение: Диагностика prerequisites; JS bundle PASS не выдаётся за установленное native app.

**Восстановление:** Работать в отдельной копии. Отменить свои изменения в редакторе, вернуть изменённую настройку, остановить только запущенный для этой проверки процесс. Для следующей мутации создать новую чистую копию; исходный набор сохраняется.

**Доказательство:** Записать ID сценария, точный plugin/IDE build, project path и HEAD, вход и результат в RUN_RECORD. Для UI приложить видимое наблюдение; для экспорта — файл и hash. Успех producer/checker не присваивает PASS плагину.

**Consumer run:** `NOT_RUN`. Capability IDs: DEV-MOBILE.

<a id="devs-21"></a>
### DEVS-21 — ADB devices, logcat, reverse, reload и device changes

**Зачем:** Диагностировать своё мобильное приложение на явно выбранном устройстве.

**Подготовка:** Нужны Android SDK/ADB и выделенный device/emulator. Установка, очистка и удаление требуют конкретного разрешения оператора; в этом наборе они не исполняются автоматически.

**Входы:** [package.json](../projects/mobile-lab/package.json), [package-lock.json](../projects/mobile-lab/package-lock.json), [index.js](../projects/mobile-lab/index.js), [App.js](../projects/mobile-lab/App.js), [app.json](../projects/mobile-lab/app.json)

1. На выделенном disposable device проверить ADB_DEVICES, ADB_LOGCAT, ADB_REVERSE и ADB_RELOAD; нажать demo counter.
   Ожидаемое наблюдение: Device serial выбран явно; ARCHVERITY_DEMO_CLICK виден в logs; reverse/reload относятся к этому приложению.
2. ADB_INSTALL_APK, ADB_CLEAR_DATA и ADB_UNINSTALL проверять только после отдельного разрешения для этого package/device.
   Ожидаемое наблюдение: Оператор наблюдает установку, очистку данных либо отсутствие com.archverity.demo; команды не переключаются на другой package.

**Контрпример:** Нет device, неверный serial либо неподготовленный APK.
Ожидаемое наблюдение: Явная ошибка; чужое устройство или приложение не выбирается автоматически.

**Восстановление:** Работать в отдельной копии. Отменить свои изменения в редакторе, вернуть изменённую настройку, остановить только запущенный для этой проверки процесс. Для следующей мутации создать новую чистую копию; исходный набор сохраняется.

**Доказательство:** Записать ID сценария, точный plugin/IDE build, project path и HEAD, вход и результат в RUN_RECORD. Для UI приложить видимое наблюдение; для экспорта — файл и hash. Успех producer/checker не присваивает PASS плагину.

**Consumer run:** `NOT_RUN`. Capability IDs: DEV-MOBILE.

<a id="devs-22"></a>
### DEVS-22 — ANSI raw/rendered, search, wrap и source links

**Зачем:** Читать цветные logs и переходить из записей к исходникам.

**Подготовка:** Открыть указанную лабораторию в IDEA с ArchVerity 3.0.3, JDK 21 для Gradle; дождаться import/index. Для полного показа использовать настоящий Trial/Pro. Требования отдельных инструментов перечислены ниже и в linked guides.

**Входы:** [qa.ansi](../projects/workspace/ansible/qa.ansi), [archflow-live.ansi](../projects/workspace/archflow-live.ansi)

1. Открыть ansible/qa.ansi и archflow-live.ansi через зарегистрированный editor; переключить raw/rendered.
   Ожидаемое наблюдение: Escape sequences превращаются в стили только в rendered view; исходный текст остаётся доступным.
2. Найти конкретный marker, включить wrap и открыть доступную source reference.
   Ожидаемое наблюдение: Поиск приводит к той же строке; wrap не меняет содержимое; ссылка открывает правильный файл.

**Контрпример:** В обычном текстовом файле поместить похожую строку без соответствующей регистрации.
Ожидаемое наблюдение: Editor selection следует extension/pattern settings; raw escape text не выдаётся за подтверждённую ANSI отрисовку.

**Восстановление:** Работать в отдельной копии. Отменить свои изменения в редакторе, вернуть изменённую настройку, остановить только запущенный для этой проверки процесс. Для следующей мутации создать новую чистую копию; исходный набор сохраняется.

**Доказательство:** Записать ID сценария, точный plugin/IDE build, project path и HEAD, вход и результат в RUN_RECORD. Для UI приложить видимое наблюдение; для экспорта — файл и hash. Успех producer/checker не присваивает PASS плагину.

**Consumer run:** `NOT_RUN`. Capability IDs: DEV-ANSI.

<a id="devs-23"></a>
### DEVS-23 — Большой ANSI-log: bounded pages и Tail

**Зачем:** Навигировать по большому log без загрузки всего текста в одну rendered страницу.

**Подготовка:** Открыть указанную лабораторию в IDEA с ArchVerity 3.0.3, JDK 21 для Gradle; дождаться import/index. Для полного показа использовать настоящий Trial/Pro. Требования отдельных инструментов перечислены ниже и в linked guides.

**Входы:** [qa.ansi](../projects/workspace/ansible/qa.ansi), [archflow-live.ansi](../projects/workspace/archflow-live.ansi), [generate_large_ansi.py](../suite-support/generate_large_ansi.py)

1. В отдельной workspace copy выполнить generate_large_ansi.py --output work/large.ansi; открыть файл.
   Ожидаемое наблюдение: Производитель сообщает 70001 строк и размер больше source threshold 5000000 bytes; используется large-log editor с bounded pages.
2. Проверить First → Next → Previous → Tail → First, затем Raw page / ANSI page.
   Ожидаемое наблюдение: Для 100-byte lines первая page начинается LINE-0000001, следующая LINE-0020001, Tail заканчивается LINE-0070001; byte offsets и navigation enabled state соответствуют странице. В ANSI page escape sequences оформлены стилями.

**Контрпример:** Быстро сменить page и закрыть только свой log tab во время загрузки; затем открыть файл снова.
Ожидаемое наблюдение: Поздняя загрузка не заменяет новую выбранную page и не пишет в закрытый editor; повторное открытие начинает текущий файл с First.

**Восстановление:** Работать в отдельной копии. Отменить свои изменения в редакторе, вернуть изменённую настройку, остановить только запущенный для этой проверки процесс. Для следующей мутации создать новую чистую копию; исходный набор сохраняется.

**Доказательство:** Записать ID сценария, точный plugin/IDE build, project path и HEAD, вход и результат в RUN_RECORD. Для UI приложить видимое наблюдение; для экспорта — файл и hash. Успех producer/checker не присваивает PASS плагину.

**Consumer run:** `NOT_RUN`. Capability IDs: DEV-ANSI.

<a id="devs-24"></a>
### DEVS-24 — ANSI settings и file registration

**Зачем:** Управлять регистрацией log editor и его resource limits.

**Подготовка:** Открыть указанную лабораторию в IDEA с ArchVerity 3.0.3, JDK 21 для Gradle; дождаться import/index. Для полного показа использовать настоящий Trial/Pro. Требования отдельных инструментов перечислены ниже и в linked guides.

**Входы:** [qa.ansi](../projects/workspace/ansible/qa.ansi), [archflow-live.ansi](../projects/workspace/archflow-live.ansi), [coverage.json](../projects/workspace/qa-support/coverage.json)

1. Записать ANSI Log Editor patterns/render limit; добавить demo extension/pattern и переоткрыть matching файл.
   Ожидаемое наблюдение: Изменился выбор editor для указанного input; значение сохраняется после Apply/reopen.
2. Изменить Maximum rendered size в диапазоне 1..100 MB и один из 16 palette colors на #00AAFF; переоткрыть цветной log, затем вернуть исходные значения.
   Ожидаемое наблюдение: Размер и цвет сохраняются после Apply/reopen; corresponding ANSI foreground меняется, остальные file associations сохранены.

**Контрпример:** Внести pattern с / либо \ и palette color #12GG34; Apply.
Ожидаемое наблюдение: ConfigurationException сообщает filename-only pattern либо требование #RRGGBB; некорректная настройка не применяется.

**Восстановление:** Работать в отдельной копии. Отменить свои изменения в редакторе, вернуть изменённую настройку, остановить только запущенный для этой проверки процесс. Для следующей мутации создать новую чистую копию; исходный набор сохраняется.

**Доказательство:** Записать ID сценария, точный plugin/IDE build, project path и HEAD, вход и результат в RUN_RECORD. Для UI приложить видимое наблюдение; для экспорта — файл и hash. Успех producer/checker не присваивает PASS плагину.

**Consumer run:** `NOT_RUN`. Capability IDs: DEV-ANSI, IDE-SETTINGS.

## Анализ контрактов

<a id="arc-01"></a>
### ARC-01 — Анализ, обновление, отмена и индексация

**Зачем:** Получать свежий анализ текущего проекта и отличать complete от interrupted scan.

**Подготовка:** Открыть указанную лабораторию в IDEA с ArchVerity 3.0.3, JDK 21 для Gradle; дождаться import/index. Для полного показа использовать настоящий Trial/Pro. Требования отдельных инструментов перечислены ниже и в linked guides.

**Входы:** [apply_impact.py](../projects/workspace/qa-support/apply_impact.py), [prepare_impact.py](../projects/workspace/qa-support/prepare_impact.py), [QA_MATRIX_RU.md](../projects/workspace/QA_MATRIX_RU.md)

1. Открыть чистый workspace → Analyze project; записать HEAD и состояние completeness.
   Ожидаемое наблюдение: Snapshot относится к текущему проекту и revision; при доступном полном анализе clean HEAD → WORKTREE не имеет изменений.
2. На новой копии поменять один контракт; Analyze/Run again, затем проверить текущий snapshot. Cancel и Dumb Mode проверять как отдельные состояния.
   Ожидаемое наблюдение: Новый результат содержит своё изменение; cancelled/partial/indexing состояние не выдаётся за complete старый результат.

**Контрпример:** Запустить до окончания index или изменить файл во время старого запроса.
Ожидаемое наблюдение: Не возникает ложного complete result для другой revision; нужно дождаться готовности и повторить текущий scan.

**Восстановление:** Работать в отдельной копии. Отменить свои изменения в редакторе, вернуть изменённую настройку, остановить только запущенный для этой проверки процесс. Для следующей мутации создать новую чистую копию; исходный набор сохраняется.

**Доказательство:** Записать ID сценария, точный plugin/IDE build, project path и HEAD, вход и результат в RUN_RECORD. Для UI приложить видимое наблюдение; для экспорта — файл и hash. Успех producer/checker не присваивает PASS плагину.

**Consumer run:** `NOT_RUN`. Capability IDs: IDE-IMPACT, IDE-RUNTIME.

<a id="arc-02"></a>
### ARC-02 — HTTP server inventory: обычные, inherited и composed mappings

**Зачем:** Видеть объявленные HTTP provider contracts и происхождение inherited mappings.

**Подготовка:** Открыть указанную лабораторию в IDEA с ArchVerity 3.0.3, JDK 21 для Gradle; дождаться import/index. Для полного показа использовать настоящий Trial/Pro. Требования отдельных инструментов перечислены ниже и в linked guides.

**Входы:** [DemoContractsController.java](../projects/workspace/payment-app/src/main/java/sample/payment/DemoContractsController.java), [DemoGet.java](../projects/workspace/payment-app/src/main/java/sample/payment/DemoGet.java), [InheritedController.java](../projects/workspace/payment-app/src/main/java/sample/payment/InheritedController.java)

1. Inventory → HTTP → поиск demo; открыть DemoContractsController.java и DemoGet.java.
   Ожидаемое наблюдение: Method/path и условия endpoint имеют locations к provider и composed annotation.
2. Найти inherited endpoint и открыть InheritedController.java/base declaration.
   Ожидаемое наблюдение: Наследуемый mapping сохраняет связь с исходной declaration; не появляется выдуманный runtime route.

**Контрпример:** Добавить неизвестный runtime path либо unsupported expression в копии.
Ожидаемое наблюдение: Неизвестное значение остаётся diagnostic/UNKNOWN, а не статически доказанным endpoint.

**Восстановление:** Работать в отдельной копии. Отменить свои изменения в редакторе, вернуть изменённую настройку, остановить только запущенный для этой проверки процесс. Для следующей мутации создать новую чистую копию; исходный набор сохраняется.

**Доказательство:** Записать ID сценария, точный plugin/IDE build, project path и HEAD, вход и результат в RUN_RECORD. Для UI приложить видимое наблюдение; для экспорта — файл и hash. Успех producer/checker не присваивает PASS плагину.

**Consumer run:** `NOT_RUN`. Capability IDs: ARCH-MVC.

<a id="arc-03"></a>
### ARC-03 — HTTP clients, route matching и условия

**Зачем:** Проверять согласованность client/provider routes и условия совместимости HTTP.

**Подготовка:** Открыть указанную лабораторию в IDEA с ArchVerity 3.0.3, JDK 21 для Gradle; дождаться import/index. Для полного показа использовать настоящий Trial/Pro. Требования отдельных инструментов перечислены ниже и в linked guides.

**Входы:** [PaymentClient.java](../projects/first-result/order-app/src/main/java/demo/orders/PaymentClient.java), [PaymentController.java](../projects/first-result/payment-app/src/main/java/demo/payments/PaymentController.java), [PaymentHttpExchange.java](../projects/workspace/order-app/src/main/java/sample/order/PaymentHttpExchange.java), [FluentPaymentClients.java](../projects/workspace/order-app/src/main/java/sample/order/FluentPaymentClients.java), [DemoContractsController.java](../projects/workspace/payment-app/src/main/java/sample/payment/DemoContractsController.java), [extended_scenarios.py](../projects/workspace/qa-support/extended_scenarios.py)

1. В first-result Analyze POST client vs PUT provider; открыть finding и обе стороны.
   Ожидаемое наблюдение: Несовместимость метода имеет provider/client source evidence; исправление client на PUT устраняет именно этот finding.
2. В workspace сравнить Feign, HttpExchange, RestTemplate/RestClient/WebClient; применить отдельно http-media-type и http-header-condition.
   Ожидаемое наблюдение: Resolved/inferred/dynamic отличаются; methods, paths, media negotiation и constraints показывают конкретную причину совместимости.

**Контрпример:** У клиента убрать известный header/target факт или оставить динамический вызов.
Ожидаемое наблюдение: Недостаток фактов остаётся UNKNOWN; не объявляется resolved runtime связь.

**Восстановление:** Работать в отдельной копии. Отменить свои изменения в редакторе, вернуть изменённую настройку, остановить только запущенный для этой проверки процесс. Для следующей мутации создать новую чистую копию; исходный набор сохраняется.

**Доказательство:** Записать ID сценария, точный plugin/IDE build, project path и HEAD, вход и результат в RUN_RECORD. Для UI приложить видимое наблюдение; для экспорта — файл и hash. Успех producer/checker не присваивает PASS плагину.

**Consumer run:** `NOT_RUN`. Capability IDs: ARCH-FEIGN, ARCH-EXCHANGE, ARCH-FLUENT, ARCH-HTTP-CONDITIONS.

<a id="arc-04"></a>
### ARC-04 — Kafka contracts: topic, group, binding и orphan

**Зачем:** Понимать Kafka producer/consumer declarations и изменения статических bindings.

**Подготовка:** Открыть указанную лабораторию в IDEA с ArchVerity 3.0.3, JDK 21 для Gradle; дождаться import/index. Для полного показа использовать настоящий Trial/Pro. Требования отдельных инструментов перечислены ниже и в linked guides.

**Входы:** [OrderPublisher.java](../projects/workspace/order-app/src/main/java/sample/order/OrderPublisher.java), [OrderListener.java](../projects/workspace/payment-app/src/main/java/sample/payment/OrderListener.java), [KafkaAdvanced.java](../projects/workspace/payment-app/src/main/java/sample/payment/KafkaAdvanced.java)

1. Inventory/Topology → Kafka; открыть send/ProducerRecord и listener/group/partition declarations.
   Ожидаемое наблюдение: Topics, producer/consumer, group и bean binding имеют source evidence.
2. На чистой сравнимой копии применить kafka-topic; открыть before/after и consumer path.
   Ожидаемое наблюдение: Отмечен конкретный topic change; internal/external topic semantics учитываются в orphan finding.

**Контрпример:** Посмотреть pattern listener или неизвестный динамический topic.
Ожидаемое наблюдение: Pattern/dynamic evidence не выдаётся за точное совпадение любого topic.

**Восстановление:** Работать в отдельной копии. Отменить свои изменения в редакторе, вернуть изменённую настройку, остановить только запущенный для этой проверки процесс. Для следующей мутации создать новую чистую копию; исходный набор сохраняется.

**Доказательство:** Записать ID сценария, точный plugin/IDE build, project path и HEAD, вход и результат в RUN_RECORD. Для UI приложить видимое наблюдение; для экспорта — файл и hash. Успех producer/checker не присваивает PASS плагину.

**Consumer run:** `NOT_RUN`. Capability IDs: ARCH-KAFKA.

<a id="arc-05"></a>
### ARC-05 — Kafka retry, DLT и reply paths

**Зачем:** Отличать retry/DLT/reply topology от обычного message flow.

**Подготовка:** Открыть указанную лабораторию в IDEA с ArchVerity 3.0.3, JDK 21 для Gradle; дождаться import/index. Для полного показа использовать настоящий Trial/Pro. Требования отдельных инструментов перечислены ниже и в linked guides.

**Входы:** [OrderPublisher.java](../projects/workspace/order-app/src/main/java/sample/order/OrderPublisher.java), [OrderListener.java](../projects/workspace/payment-app/src/main/java/sample/payment/OrderListener.java), [KafkaAdvanced.java](../projects/workspace/payment-app/src/main/java/sample/payment/KafkaAdvanced.java)

1. Открыть retry/DLT/reply declarations в PaymentListener/KafkaAdvanced и соответствующие edges.
   Ожидаемое наблюдение: Retry/DLT/reply различаются от обычной producer→consumer связи и ведут к правильным строкам.
2. Перейти по reply source и проверить partition listener отдельно.
   Ожидаемое наблюдение: Direction, declared topic и source kind согласованы; topology не утверждает реальный broker delivery.

**Контрпример:** Убрать статически известный reply topic в копии.
Ожидаемое наблюдение: Недостающий факт обозначается; старое точное reply ребро не сохраняется как доказанное.

**Восстановление:** Работать в отдельной копии. Отменить свои изменения в редакторе, вернуть изменённую настройку, остановить только запущенный для этой проверки процесс. Для следующей мутации создать новую чистую копию; исходный набор сохраняется.

**Доказательство:** Записать ID сценария, точный plugin/IDE build, project path и HEAD, вход и результат в RUN_RECORD. Для UI приложить видимое наблюдение; для экспорта — файл и hash. Успех producer/checker не присваивает PASS плагину.

**Consumer run:** `NOT_RUN`. Capability IDs: ARCH-KAFKA.

<a id="arc-06"></a>
### ARC-06 — AMQP direct/topic/fanout/default exchange

**Зачем:** Исследовать объявленную RabbitMQ маршрутизацию по exchange/binding/queue.

**Подготовка:** Открыть указанную лабораторию в IDEA с ArchVerity 3.0.3, JDK 21 для Gradle; дождаться import/index. Для полного показа использовать настоящий Trial/Pro. Требования отдельных инструментов перечислены ниже и в linked guides.

**Входы:** [AmqpPublisher.java](../projects/workspace/order-app/src/main/java/sample/order/AmqpPublisher.java), [AmqpTopology.java](../projects/workspace/payment-app/src/main/java/sample/payment/AmqpTopology.java), [AmqpListener.kt](../projects/workspace/notification-app/src/main/kotlin/sample/notification/AmqpListener.kt)

1. Inventory/Topology → AMQP; пройти AmqpPublisher → exchange → binding → queue → Java/Kotlin listener.
   Ожидаемое наблюдение: Source locations и routing keys относятся к соответствующим producer/exchange/queue declarations.
2. Сравнить direct/topic/fanout/default cases в AmqpTopology; применить amqp-binding на новой копии.
   Ожидаемое наблюдение: Default exchange, fanout и topic/direct matcher различаются; изменение binding объясняет наблюдаемую связь.

**Контрпример:** Неизвестный routingKey/queue либо dynamic broker declaration.
Ожидаемое наблюдение: Статический анализ не подменяет неизвестное реальной доставкой сообщения.

**Восстановление:** Работать в отдельной копии. Отменить свои изменения в редакторе, вернуть изменённую настройку, остановить только запущенный для этой проверки процесс. Для следующей мутации создать новую чистую копию; исходный набор сохраняется.

**Доказательство:** Записать ID сценария, точный plugin/IDE build, project path и HEAD, вход и результат в RUN_RECORD. Для UI приложить видимое наблюдение; для экспорта — файл и hash. Успех producer/checker не присваивает PASS плагину.

**Consumer run:** `NOT_RUN`. Capability IDs: ARCH-AMQP.

<a id="arc-07"></a>
### ARC-07 — DTO/Jackson: вложенность, коллекции, enum и Unknown

**Зачем:** Выявлять изменения wire shape и видеть пределы статически известного DTO.

**Подготовка:** Открыть указанную лабораторию в IDEA с ArchVerity 3.0.3, JDK 21 для Gradle; дождаться import/index. Для полного показа использовать настоящий Trial/Pro. Требования отдельных инструментов перечислены ниже и в linked guides.

**Входы:** [DemoContractsController.java](../projects/workspace/payment-app/src/main/java/sample/payment/DemoContractsController.java), [AmqpListener.kt](../projects/workspace/notification-app/src/main/kotlin/sample/notification/AmqpListener.kt), [extended_scenarios.py](../projects/workspace/qa-support/extended_scenarios.py), [BasicWireDto.java](../projects/workspace/payment-app/src/main/java/sample/payment/BasicWireDto.java), [WireController.java](../projects/workspace/payment-app/src/main/java/sample/payment/WireController.java), [UnknownContractsController.java](../projects/workspace/payment-app/src/main/java/sample/payment/UnknownContractsController.java), [AmqpPublisher.java](../projects/workspace/order-app/src/main/java/sample/order/AmqpPublisher.java)

1. Открыть DTO wire-shape в Java и Kotlin: nested object, List/Map, nullable, enum, inheritance, snake_case, JsonProperty/Ignore/access/discriminator.
   Ожидаемое наблюдение: Wire names и request/response направления объяснимы исходными аннотациями; nested path отображается как конкретное поле.
2. Отдельно применить nested-request-required, enum-response-added, response-removed и response-optional-added.
   Ожидаемое наблюдение: Before/after показывает точный path/enum change; verdict учитывает направление контракта.

**Контрпример:** Открыть generic/recursive UnknownContractsController.
Ожидаемое наблюдение: Unsupported/bounded shape обозначается UNKNOWN; нет обещания полной wire-shape там, где данных нет.

**Восстановление:** Работать в отдельной копии. Отменить свои изменения в редакторе, вернуть изменённую настройку, остановить только запущенный для этой проверки процесс. Для следующей мутации создать новую чистую копию; исходный набор сохраняется.

**Доказательство:** Записать ID сценария, точный plugin/IDE build, project path и HEAD, вход и результат в RUN_RECORD. Для UI приложить видимое наблюдение; для экспорта — файл и hash. Успех producer/checker не присваивает PASS плагину.

**Consumer run:** `NOT_RUN`. Capability IDs: ARCH-NESTED-DTO, ARCH-JACKSON, ARCH-UNKNOWN.

<a id="arc-08"></a>
### ARC-08 — Severity, confidence, disposition и evidence

**Зачем:** Принимать решение по finding с учётом severity, confidence и причины disposition.

**Подготовка:** Открыть указанную лабораторию в IDEA с ArchVerity 3.0.3, JDK 21 для Gradle; дождаться import/index. Для полного показа использовать настоящий Trial/Pro. Требования отдельных инструментов перечислены ниже и в linked guides.

**Входы:** [PaymentClient.java](../projects/first-result/order-app/src/main/java/demo/orders/PaymentClient.java), [extended_scenarios.py](../projects/workspace/qa-support/extended_scenarios.py)

1. В first-result выбрать реальный method mismatch; открыть severity, confidence, reason и evidence.
   Ожидаемое наблюдение: Показаны причина и source locations обеих сторон, а не только цвет карточки.
2. После исправления пересканировать; на отдельной копии применить suppression с reason/expiry и пересканировать.
   Ожидаемое наблюдение: Исправление и suppression имеют различимые disposition; suppression не означает resolved.

**Контрпример:** Просмотреть UNKNOWN либо partial result.
Ожидаемое наблюдение: Unknown/low confidence не превращается в доказанный Breaking/Safe только по имени сценария.

**Восстановление:** Работать в отдельной копии. Отменить свои изменения в редакторе, вернуть изменённую настройку, остановить только запущенный для этой проверки процесс. Для следующей мутации создать новую чистую копию; исходный набор сохраняется.

**Доказательство:** Записать ID сценария, точный plugin/IDE build, project path и HEAD, вход и результат в RUN_RECORD. Для UI приложить видимое наблюдение; для экспорта — файл и hash. Успех producer/checker не присваивает PASS плагину.

**Consumer run:** `NOT_RUN`. Capability IDs: IDE-FINDINGS.

## Навигация и граф

<a id="ui-01"></a>
### UI-01 — Все 15 экранов, layouts и navigation history

**Зачем:** Найти каждый инструмент и выбрать удобное представление того же результата.

**Подготовка:** Открыть указанную лабораторию в IDEA с ArchVerity 3.0.3, JDK 21 для Gradle; дождаться import/index. Для полного показа использовать настоящий Trial/Pro. Требования отдельных инструментов перечислены ниже и в linked guides.

**Входы:** [PaymentController.java](../projects/workspace/payment-app/src/main/java/sample/payment/PaymentController.java), [QA_MATRIX_RU.md](../projects/workspace/QA_MATRIX_RU.md)

1. Открыть Workspace, Impact, Inventory, Topology, Relations, Diagnostics, Spring, MyBatis, Ansible, Shell, API, React Native, ANSI, Dev Icons, Keystore.
   Ожидаемое наблюдение: Каждый экран имеет свой заголовок и рабочие actions; breadcrumbs/back/forward ведут к выбранному состоянию.
2. В Impact переключить Editor Companion, Graphite Focus, Paper Review; проверить compact/wide, reopen и настоящий Local/Split Mode отдельно.
   Ожидаемое наблюдение: Presentation меняет layout того же результата; source evidence/revision сохраняются. Runtime, license, renderer и accessibility наблюдения записываются раздельно.

**Контрпример:** Перейти back/forward после смены filter/layout.
Ожидаемое наблюдение: История не открывает карточку другого проекта или старый выбранный endpoint.

**Восстановление:** Работать в отдельной копии. Отменить свои изменения в редакторе, вернуть изменённую настройку, остановить только запущенный для этой проверки процесс. Для следующей мутации создать новую чистую копию; исходный набор сохраняется.

**Доказательство:** Записать ID сценария, точный plugin/IDE build, project path и HEAD, вход и результат в RUN_RECORD. Для UI приложить видимое наблюдение; для экспорта — файл и hash. Успех producer/checker не присваивает PASS плагину.

**Consumer run:** `NOT_RUN`. Capability IDs: IDE-NAVIGATION, IDE-RUNTIME, IDE-LICENSE.

<a id="ui-02"></a>
### UI-02 — Поиск, protocol filters и переход к исходнику

**Зачем:** Сузить результат до нужного контракта и открыть его конкретный исходник.

**Подготовка:** Открыть указанную лабораторию в IDEA с ArchVerity 3.0.3, JDK 21 для Gradle; дождаться import/index. Для полного показа использовать настоящий Trial/Pro. Требования отдельных инструментов перечислены ниже и в linked guides.

**Входы:** [.archflow.yml](../projects/workspace/.archflow.yml)

1. Inventory: filter HTTP, search payments, выбрать endpoint; затем Kafka/AMQP.
   Ожидаемое наблюдение: Список соответствует одновременно query и protocol; выбранный элемент открывает свой source.
2. Сбросить query/filter, открыть relation и проверить source locations обоих концов.
   Ожидаемое наблюдение: Полный набор восстановлен; navigation ведёт к той же relation.

**Контрпример:** Поиск без совпадений и reset.
Ожидаемое наблюдение: Пустой результат объясним query; reset возвращает элементы, без ложного исчезновения из snapshot.

**Восстановление:** Работать в отдельной копии. Отменить свои изменения в редакторе, вернуть изменённую настройку, остановить только запущенный для этой проверки процесс. Для следующей мутации создать новую чистую копию; исходный набор сохраняется.

**Доказательство:** Записать ID сценария, точный plugin/IDE build, project path и HEAD, вход и результат в RUN_RECORD. Для UI приложить видимое наблюдение; для экспорта — файл и hash. Успех producer/checker не присваивает PASS плагину.

**Consumer run:** `NOT_RUN`. Capability IDs: IDE-TOPOLOGY.

<a id="ui-03"></a>
### UI-03 — Topology: уровни, focus и exploration

**Зачем:** Исследовать graph через уровни детализации, focus и связи.

**Подготовка:** Открыть указанную лабораторию в IDEA с ArchVerity 3.0.3, JDK 21 для Gradle; дождаться import/index. Для полного показа использовать настоящий Trial/Pro. Требования отдельных инструментов перечислены ниже и в linked guides.

**Входы:** [.archflow.yml](../projects/workspace/.archflow.yml)

1. Topology: Services/Details level, HTTP/Kafka/AMQP filter; выбрать payment-service и relation.
   Ожидаемое наблюдение: Clustering/detail различаются, selection показывает связанную информацию и source evidence.
2. Включить focus на узле, пройти соседнее ребро и Reset focus; проверить graph keyboard selection.
   Ожидаемое наблюдение: Соседи соответствуют текущему graph; reset возвращает полный текущий graph, keyboard focus видим.

**Контрпример:** Выбрать node после scope change/reanalysis.
Ожидаемое наблюдение: Удалённая selection не сохраняет чужую details/card; partial scope явно обозначен.

**Восстановление:** Работать в отдельной копии. Отменить свои изменения в редакторе, вернуть изменённую настройку, остановить только запущенный для этой проверки процесс. Для следующей мутации создать новую чистую копию; исходный набор сохраняется.

**Доказательство:** Записать ID сценария, точный plugin/IDE build, project path и HEAD, вход и результат в RUN_RECORD. Для UI приложить видимое наблюдение; для экспорта — файл и hash. Успех producer/checker не присваивает PASS плагину.

**Consumer run:** `NOT_RUN`. Capability IDs: IDE-TOPOLOGY.

<a id="ui-04"></a>
### UI-04 — Diagnostics и восстановление после missing input

**Зачем:** Понять причину неполного анализа и проверить восстановление после исправления input.

**Подготовка:** Открыть указанную лабораторию в IDEA с ArchVerity 3.0.3, JDK 21 для Gradle; дождаться import/index. Для полного показа использовать настоящий Trial/Pro. Требования отдельных инструментов перечислены ниже и в linked guides.

**Входы:** [PaymentClient.java](../projects/first-result/order-app/src/main/java/demo/orders/PaymentClient.java), [extended_scenarios.py](../projects/workspace/qa-support/extended_scenarios.py)

1. На исправном workspace открыть Diagnostics и location каждого имеющегося сообщения.
   Ожидаемое наблюдение: Ноль diagnostic допустим; существующие сообщения показывают конкретный source/config факт.
2. На свежих копиях применить manifest-missing, runtime-beans-missing и verification-missing.
   Ожидаемое наблюдение: Для каждой отсутствующей зависимости есть точная причина и recovery guidance; snapshots не объявлены полностью исправными.

**Контрпример:** Вернуть нужный файл и Analyze.
Ожидаемое наблюдение: Устраняется связанная диагностика; повторное использование старого error/result не выдаётся за recovery.

**Восстановление:** Работать в отдельной копии. Отменить свои изменения в редакторе, вернуть изменённую настройку, остановить только запущенный для этой проверки процесс. Для следующей мутации создать новую чистую копию; исходный набор сохраняется.

**Доказательство:** Записать ID сценария, точный plugin/IDE build, project path и HEAD, вход и результат в RUN_RECORD. Для UI приложить видимое наблюдение; для экспорта — файл и hash. Успех producer/checker не присваивает PASS плагину.

**Consumer run:** `NOT_RUN`. Capability IDs: IDE-FINDINGS.

## Конфигурация

<a id="cfg-01"></a>
### CFG-01 — Scope, service IDs, profiles и aliases

**Зачем:** Определить границы проекта и effective profiles до сравнения контрактов.

**Подготовка:** Открыть указанную лабораторию в IDEA с ArchVerity 3.0.3, JDK 21 для Gradle; дождаться import/index. Для полного показа использовать настоящий Trial/Pro. Требования отдельных инструментов перечислены ниже и в linked guides.

**Входы:** [.archflow.yml](../projects/workspace/.archflow.yml), [extended_scenarios.py](../projects/workspace/qa-support/extended_scenarios.py), [application.yml](../projects/workspace/payment-app/src/main/resources/application.yml), [application-demo.properties](../projects/workspace/payment-app/src/main/resources/application-demo.properties), [application-dev.yml](../projects/workspace/payment-app/src/main/resources/application-dev.yml)

1. Открыть .archflow.yml: services/modulePaths/paths/profiles/aliases; сопоставить с effective config в scan.
   Ожидаемое наблюдение: Project identity, service IDs и active property sources соответствуют этому workspace.
2. На новых копиях отдельно spring-profile/scope-change; повторить scan и сравнение.
   Ожидаемое наблюдение: Context/scope fingerprint меняется по фактам, а сравнимость baseline объясняется явно.

**Контрпример:** Удалить требуемый service ID либо внести invalid profile expression.
Ожидаемое наблюдение: Конфигурация получает validation error/partial; отсутствующие элементы не считаются resolved.

**Восстановление:** Работать в отдельной копии. Отменить свои изменения в редакторе, вернуть изменённую настройку, остановить только запущенный для этой проверки процесс. Для следующей мутации создать новую чистую копию; исходный набор сохраняется.

**Доказательство:** Записать ID сценария, точный plugin/IDE build, project path и HEAD, вход и результат в RUN_RECORD. Для UI приложить видимое наблюдение; для экспорта — файл и hash. Успех producer/checker не присваивает PASS плагину.

**Consumer run:** `NOT_RUN`. Capability IDs: ARCH-SCOPE, ARCH-PROPERTIES.

<a id="cfg-02"></a>
### CFG-02 — Rules, guided alias/manifest suggestions и suppression

**Зачем:** Настраивать проверяемые правила и подавлять конкретные findings с объяснением.

**Подготовка:** Открыть указанную лабораторию в IDEA с ArchVerity 3.0.3, JDK 21 для Gradle; дождаться import/index. Для полного показа использовать настоящий Trial/Pro. Требования отдельных инструментов перечислены ниже и в linked guides.

**Входы:** [PaymentClient.java](../projects/first-result/order-app/src/main/java/demo/orders/PaymentClient.java), [extended_scenarios.py](../projects/workspace/qa-support/extended_scenarios.py), [qa-openapi.json](../projects/workspace/qa-openapi.json), [qa-asyncapi.json](../projects/workspace/qa-asyncapi.json), [qa-backstage.json](../projects/workspace/qa-backstage.json), [qa-loopback.archflow.json](../projects/workspace/contracts/qa-loopback.archflow.json), [qa-event-bus.archflow.json](../projects/workspace/contracts/qa-event-bus.archflow.json), [qa-backstage.archflow.json](../projects/workspace/contracts/qa-backstage.archflow.json)

1. Из реального finding открыть suggested alias/manifest action и проверить preview/copy.
   Ожидаемое наблюдение: Suggestion содержит подходящие service/contract IDs и источник причины; оно не применяется к чужому проекту.
2. В отдельной копии создать suppression с reason/expiry; применить rule-severity и повторить Analyze.
   Ожидаемое наблюдение: Suppression и severity rule действуют на выбранный rule/finding, с видимым конфигурационным изменением.

**Контрпример:** Invalid suppression/expiry или unknown rule.
Ожидаемое наблюдение: Validation error вместо молчаливого отключения всего анализа.

**Восстановление:** Работать в отдельной копии. Отменить свои изменения в редакторе, вернуть изменённую настройку, остановить только запущенный для этой проверки процесс. Для следующей мутации создать новую чистую копию; исходный набор сохраняется.

**Доказательство:** Записать ID сценария, точный plugin/IDE build, project path и HEAD, вход и результат в RUN_RECORD. Для UI приложить видимое наблюдение; для экспорта — файл и hash. Успех producer/checker не присваивает PASS плагину.

**Consumer run:** `NOT_RUN`. Capability IDs: IDE-FINDINGS, ARCH-MANIFESTS.

<a id="cfg-03"></a>
### CFG-03 — Dependency allow/deny и bounded cycles

**Зачем:** Контролировать разрешённые зависимости и прослеживать обнаруженные циклы.

**Подготовка:** Открыть указанную лабораторию в IDEA с ArchVerity 3.0.3, JDK 21 для Gradle; дождаться import/index. Для полного показа использовать настоящий Trial/Pro. Требования отдельных инструментов перечислены ниже и в linked guides.

**Входы:** [.archflow.yml](../projects/workspace/.archflow.yml), [extended_scenarios.py](../projects/workspace/qa-support/extended_scenarios.py)

1. Применить dependency-deny; открыть policy finding order→payment и его source.
   Ожидаемое наблюдение: Нарушение относится к явно запрещённым service IDs/protocol, а не ко всем relations.
2. На fixture reverse Payment→Order inspect cycle path и configured allow/deny precedence.
   Ожидаемое наблюдение: Цикл имеет bounded source-backed путь; policy применяется детерминированно.

**Контрпример:** Unknown/dynamic dependency либо scope без одной стороны цикла.
Ожидаемое наблюдение: Неполный путь не представляется полным доказанным циклом.

**Восстановление:** Работать в отдельной копии. Отменить свои изменения в редакторе, вернуть изменённую настройку, остановить только запущенный для этой проверки процесс. Для следующей мутации создать новую чистую копию; исходный набор сохраняется.

**Доказательство:** Записать ID сценария, точный plugin/IDE build, project path и HEAD, вход и результат в RUN_RECORD. Для UI приложить видимое наблюдение; для экспорта — файл и hash. Успех producer/checker не присваивает PASS плагину.

**Consumer run:** `NOT_RUN`. Capability IDs: ARCH-POLICIES.

## Impact и review

<a id="imp-01"></a>
### IMP-01 — Git base/HEAD → WORKTREE и unsaved edits

**Зачем:** Узнать impact текущих файлов и несохранённых document changes относительно Git base.

**Подготовка:** Открыть указанную лабораторию в IDEA с ArchVerity 3.0.3, JDK 21 для Gradle; дождаться import/index. Для полного показа использовать настоящий Trial/Pro. Требования отдельных инструментов перечислены ниже и в linked guides.

**Входы:** [apply_impact.py](../projects/workspace/qa-support/apply_impact.py), [prepare_impact.py](../projects/workspace/qa-support/prepare_impact.py), [PaymentController.java](../projects/workspace/payment-app/src/main/java/sample/payment/PaymentController.java)

1. Создать чистую workspace copy, Analyze HEAD; применить combined-breaking и сравнить HEAD → WORKTREE.
   Ожидаемое наблюдение: Before/after показывает method/request/response delta и актуальный revision/scope.
2. На новой копии изменить Java contract в editor без Save; Analyze и открыть Impact/gutter.
   Ожидаемое наблюдение: Снимок включает текущий document после корректного PSI commit; source card и gutter относятся к одной declaration.

**Контрпример:** Неверная base revision, отсутствующий полный HEAD snapshot либо invalid scope.
Ожидаемое наблюдение: Сравнение явно incomplete/unavailable; expected verdict не придумывается по имени мутации.

**Восстановление:** Работать в отдельной копии. Отменить свои изменения в редакторе, вернуть изменённую настройку, остановить только запущенный для этой проверки процесс. Для следующей мутации создать новую чистую копию; исходный набор сохраняется.

**Доказательство:** Записать ID сценария, точный plugin/IDE build, project path и HEAD, вход и результат в RUN_RECORD. Для UI приложить видимое наблюдение; для экспорта — файл и hash. Успех producer/checker не присваивает PASS плагину.

**Consumer run:** `NOT_RUN`. Capability IDs: IDE-IMPACT, IDE-UNSAVED.

<a id="imp-02"></a>
### IMP-02 — Local baseline: Save, compare и Clear

**Зачем:** Сохранить локальную точку сравнения и корректно управлять её жизненным циклом.

**Подготовка:** Открыть указанную лабораторию в IDEA с ArchVerity 3.0.3, JDK 21 для Gradle; дождаться import/index. Для полного показа использовать настоящий Trial/Pro. Требования отдельных инструментов перечислены ниже и в linked guides.

**Входы:** [.archflow.yml](../projects/workspace/.archflow.yml)

1. Analyze clean workspace → Save baseline; изменить один contract и повторить Analyze.
   Ожидаемое наблюдение: Baseline comparison показывает именно это изменение с совпадающим scope.
2. Clear baseline и снова открыть comparison controls; для Git base выбрать реальный существующий ref.
   Ожидаемое наблюдение: Local baseline убран; Git и local baseline источники не смешиваются.

**Контрпример:** Изменить profile/scope после Save baseline.
Ожидаемое наблюдение: Несравнимость объясняется; исчезнувший из scope contract не помечается resolved.

**Восстановление:** Работать в отдельной копии. Отменить свои изменения в редакторе, вернуть изменённую настройку, остановить только запущенный для этой проверки процесс. Для следующей мутации создать новую чистую копию; исходный набор сохраняется.

**Доказательство:** Записать ID сценария, точный plugin/IDE build, project path и HEAD, вход и результат в RUN_RECORD. Для UI приложить видимое наблюдение; для экспорта — файл и hash. Успех producer/checker не присваивает PASS плагину.

**Consumer run:** `NOT_RUN`. Capability IDs: IDE-BASELINE.

<a id="imp-03"></a>
### IMP-03 — Breaking/Safe/Unknown и downstream REVIEW

**Зачем:** Различать прямую несовместимость, неизвестность и последующую область review.

**Подготовка:** Открыть указанную лабораторию в IDEA с ArchVerity 3.0.3, JDK 21 для Gradle; дождаться import/index. Для полного показа использовать настоящий Trial/Pro. Требования отдельных инструментов перечислены ниже и в linked guides.

**Входы:** [apply_impact.py](../projects/workspace/qa-support/apply_impact.py), [prepare_impact.py](../projects/workspace/qa-support/prepare_impact.py), [.archflow.yml](../projects/workspace/.archflow.yml), [PaymentClient.java](../projects/workspace/notification-app/src/main/java/sample/notification/PaymentClient.java)

1. На разных чистых копиях request-required, response-optional-added и unknown shape; открыть reasons, consumers и paths.
   Ожидаемое наблюдение: Прямой verdict объяснён контрактом/направлением, Unknown — недостающим фактом.
2. Пройти downstream review path от payment через order/notification.
   Ожидаемое наблюдение: REVIEW отмечает достижимость и необходимость проверить последующие hops; не доказывает field transmission.

**Контрпример:** Попытаться трактовать REVIEW path как доказанную wire incompatibility.
Ожидаемое наблюдение: Evidence показывает границу такого вывода; direct Breaking и downstream REVIEW различимы.

**Восстановление:** Работать в отдельной копии. Отменить свои изменения в редакторе, вернуть изменённую настройку, остановить только запущенный для этой проверки процесс. Для следующей мутации создать новую чистую копию; исходный набор сохраняется.

**Доказательство:** Записать ID сценария, точный plugin/IDE build, project path и HEAD, вход и результат в RUN_RECORD. Для UI приложить видимое наблюдение; для экспорта — файл и hash. Успех producer/checker не присваивает PASS плагину.

**Consumer run:** `NOT_RUN`. Capability IDs: IDE-IMPACT, IDE-REVIEW.

<a id="imp-04"></a>
### IMP-04 — Две стороны, field table, recommendation и Markdown review

**Зачем:** Проверить изменение с двух сторон и подготовить понятный review для коллеги.

**Подготовка:** Открыть указанную лабораторию в IDEA с ArchVerity 3.0.3, JDK 21 для Gradle; дождаться import/index. Для полного показа использовать настоящий Trial/Pro. Требования отдельных инструментов перечислены ниже и в linked guides.

**Входы:** [.archflow.yml](../projects/workspace/.archflow.yml), [PaymentClient.java](../projects/workspace/notification-app/src/main/java/sample/notification/PaymentClient.java), [apply_impact.py](../projects/workspace/qa-support/apply_impact.py), [prepare_impact.py](../projects/workspace/qa-support/prepare_impact.py)

1. В изменённой карточке открыть Было/Стало, field table, evidence и оба source links.
   Ожидаемое наблюдение: Удалённое providerReference и неизменённые поля различимы; ссылки ведут к correct side/revision.
2. Review → Copy/Save Markdown в work/; открыть файл и сверить owners/consumers/unknown limits.
   Ожидаемое наблюдение: Review пригоден для передачи коллеге: известные изменения, paths и ограничения относятся к этому comparison.

**Контрпример:** Review для partial comparison или отсутствующего consumer evidence.
Ожидаемое наблюдение: Ограничение включено в review; нет обещания доказанной совместимости по всем consumers.

**Восстановление:** Работать в отдельной копии. Отменить свои изменения в редакторе, вернуть изменённую настройку, остановить только запущенный для этой проверки процесс. Для следующей мутации создать новую чистую копию; исходный набор сохраняется.

**Доказательство:** Записать ID сценария, точный plugin/IDE build, project path и HEAD, вход и результат в RUN_RECORD. Для UI приложить видимое наблюдение; для экспорта — файл и hash. Успех producer/checker не присваивает PASS плагину.

**Consumer run:** `NOT_RUN`. Capability IDs: IDE-REVIEW, IDE-IMPACT.

## Внешние evidence

<a id="evd-01"></a>
### EVD-01 — External OpenAPI/AsyncAPI/Backstage manifests

**Зачем:** Добавить известные контракты внешних репозиториев с явным file provenance.

**Подготовка:** Открыть указанную лабораторию в IDEA с ArchVerity 3.0.3, JDK 21 для Gradle; дождаться import/index. Для полного показа использовать настоящий Trial/Pro. Требования отдельных инструментов перечислены ниже и в linked guides.

**Входы:** [qa-openapi.json](../projects/workspace/qa-openapi.json), [qa-asyncapi.json](../projects/workspace/qa-asyncapi.json), [qa-backstage.json](../projects/workspace/qa-backstage.json), [qa-loopback.archflow.json](../projects/workspace/contracts/qa-loopback.archflow.json), [qa-event-bus.archflow.json](../projects/workspace/contracts/qa-event-bus.archflow.json), [qa-backstage.archflow.json](../projects/workspace/contracts/qa-backstage.archflow.json)

1. Применить manifest-import на новой копии, Analyze и найти qa-loopback, qa-event-bus, qa-catalog-service.
   Ожидаемое наблюдение: HTTP/Kafka/service declarations видны с provenance manifest и project-relative locations.
2. Отдельно выполнить offline adapters и validate-manifest по CLI guide.
   Ожидаемое наблюдение: Canonical manifests валидны; повторный import не притворяется исходным Java declaration.

**Контрпример:** manifest-missing либо unsupported raw external protocol.
Ожидаемое наблюдение: Missing/unsupported input даёт явную диагностику; scope не расширяется произвольно.

**Восстановление:** Работать в отдельной копии. Отменить свои изменения в редакторе, вернуть изменённую настройку, остановить только запущенный для этой проверки процесс. Для следующей мутации создать новую чистую копию; исходный набор сохраняется.

**Доказательство:** Записать ID сценария, точный plugin/IDE build, project path и HEAD, вход и результат в RUN_RECORD. Для UI приложить видимое наблюдение; для экспорта — файл и hash. Успех producer/checker не присваивает PASS плагину.

**Consumer run:** `NOT_RUN`. Capability IDs: ARCH-MANIFESTS.

<a id="evd-02"></a>
### EVD-02 — Настоящие Actuator beans и local runtime metadata

**Зачем:** Дополнить static bindings настоящим сохранённым наблюдением Spring beans.

**Подготовка:** Открыть указанную лабораторию в IDEA с ArchVerity 3.0.3, JDK 21 для Gradle; дождаться import/index. Для полного показа использовать настоящий Trial/Pro. Требования отдельных инструментов перечислены ниже и в linked guides.

**Входы:** [KafkaBindings.java](../projects/runtime-evidence/src/main/java/demo/evidence/KafkaBindings.java), [run_local.py](../projects/runtime-evidence/run_local.py), [capture.py](../projects/runtime-evidence/capture.py)

1. Подготовить чистую runtime-evidence copy и реальный current IDEA export; запустить run_local.py и capture.py по README.
   Ожидаемое наблюдение: /actuator/beans действительно получен из этого Spring Boot; metadata связывает source revision/config/context/environment/time.
2. Analyze/import и открыть template→producer factory, listener factory→consumer factory observation.
   Ожидаемое наблюдение: Observed bindings привязаны к current snapshot; imported file provenance отображается как LOCAL_FILE.

**Контрпример:** Подставить другой HEAD/configHash/context либо expired metadata.
Ожидаемое наблюдение: Evidence отклонено/устарело; оно не меняет текущую static contract истину.

**Восстановление:** Работать в отдельной копии. Отменить свои изменения в редакторе, вернуть изменённую настройку, остановить только запущенный для этой проверки процесс. Для следующей мутации создать новую чистую копию; исходный набор сохраняется.

**Доказательство:** Записать ID сценария, точный plugin/IDE build, project path и HEAD, вход и результат в RUN_RECORD. Для UI приложить видимое наблюдение; для экспорта — файл и hash. Успех producer/checker не присваивает PASS плагину.

**Consumer run:** `NOT_RUN`. Capability IDs: ARCH-RUNTIME.

<a id="evd-03"></a>
### EVD-03 — Executed verification: PASS, FAIL, drift и freshness

**Зачем:** Связать выполненную проверку контракта с актуальным operation/spec/context.

**Подготовка:** Открыть указанную лабораторию в IDEA с ArchVerity 3.0.3, JDK 21 для Gradle; дождаться import/index. Для полного показа использовать настоящий Trial/Pro. Требования отдельных инструментов перечислены ниже и в linked guides.

**Входы:** [capture.py](../projects/runtime-evidence/capture.py), [.archflow.yml](../projects/runtime-evidence/.archflow.yml), [payment-openapi.json](../projects/runtime-evidence/contracts/payment-openapi.json)

1. С реальным current export получить локальные Pact-shaped PASS, Pact-shaped FAIL и Drift-shaped PASS по runtime README.
   Ожидаемое наблюдение: Каждый отчёт получен именованным local HTTP verifier от реального запроса; это не vendor-authenticated run.
2. Convert/import verification, проверить operation/spec hash/version/outcome и consumer отображение.
   Ожидаемое наблюдение: PASS и FAIL различимы; verdict относится к конкретному operation и связанному spec/context.

**Контрпример:** Изменить spec bytes, service version, revision/context либо удалить report.
Ожидаемое наблюдение: Нет доверенного PASS от неверного/отсутствующего evidence; диагностирована конкретная причина.

**Восстановление:** Работать в отдельной копии. Отменить свои изменения в редакторе, вернуть изменённую настройку, остановить только запущенный для этой проверки процесс. Для следующей мутации создать новую чистую копию; исходный набор сохраняется.

**Доказательство:** Записать ID сценария, точный plugin/IDE build, project path и HEAD, вход и результат в RUN_RECORD. Для UI приложить видимое наблюдение; для экспорта — файл и hash. Успех producer/checker не присваивает PASS плагину.

**Consumer run:** `NOT_RUN`. Capability IDs: ARCH-VERIFICATION.

## Экспорты

<a id="team-01"></a>
### TEAM-01 — Analysis JSON и Impact JSON для команды

**Зачем:** Передать фактический analysis/comparison результат машинному consumer.

**Подготовка:** Открыть указанную лабораторию в IDEA с ArchVerity 3.0.3, JDK 21 для Gradle; дождаться import/index. Для полного показа использовать настоящий Trial/Pro. Требования отдельных инструментов перечислены ниже и в linked guides.

**Входы:** [inspect_export.py](../suite-support/inspect_export.py), [QA_MATRIX_RU.md](../projects/workspace/QA_MATRIX_RU.md)

1. На current scan Copy/Save analysis JSON; на реальном comparison Copy/Save Impact JSON в work/.
   Ожидаемое наблюдение: Два документа имеют свои schema/kind/context; recorded revision и completeness совпадают с UI.
2. Inspect export script, затем сопоставить один finding и один field delta с исходником.
   Ожидаемое наблюдение: Формат проверяется отдельно от смысла; одинаковая запись прослеживается до видимого результата и source.

**Контрпример:** Попытаться экспортировать неготовый/stale результат либо смешать Analysis с Impact.
Ожидаемое наблюдение: Действие не маскирует stale state; consumer определяет тип и completeness документа.

**Восстановление:** Работать в отдельной копии. Отменить свои изменения в редакторе, вернуть изменённую настройку, остановить только запущенный для этой проверки процесс. Для следующей мутации создать новую чистую копию; исходный набор сохраняется.

**Доказательство:** Записать ID сценария, точный plugin/IDE build, project path и HEAD, вход и результат в RUN_RECORD. Для UI приложить видимое наблюдение; для экспорта — файл и hash. Успех producer/checker не присваивает PASS плагину.

**Consumer run:** `NOT_RUN`. Capability IDs: IDE-EXPORTS.

<a id="team-02"></a>
### TEAM-02 — Mermaid, SVG, PNG и SARIF

**Зачем:** Поделиться graph и finding locations в пригодных для просмотра/интеграции форматах.

**Подготовка:** Открыть указанную лабораторию в IDEA с ArchVerity 3.0.3, JDK 21 для Gradle; дождаться import/index. Для полного показа использовать настоящий Trial/Pro. Требования отдельных инструментов перечислены ниже и в linked guides.

**Входы:** [inspect_export.py](../suite-support/inspect_export.py), [QA_MATRIX_RU.md](../projects/workspace/QA_MATRIX_RU.md)

1. Из текущей topology экспортировать Mermaid/SVG/PNG; открыть каждый artifact и проверить service IDs/edges.
   Ожидаемое наблюдение: Это читаемый текущий graph, PNG действительно изображение; SVG/Mermaid содержат ожидаемые узлы.
2. Export SARIF; inspect_export.py и сопоставить finding rule/location с текущим source.
   Ожидаемое наблюдение: SARIF 2.1.0 имеет правильные finding locations; source navigation и экспорт согласованы.

**Контрпример:** Пустой graph, partial scope либо повреждённая копия export.
Ожидаемое наблюдение: Пустота/ограничение обозначены; validator отвергает неверный format, а parse PASS не означает semantic PASS.

**Восстановление:** Работать в отдельной копии. Отменить свои изменения в редакторе, вернуть изменённую настройку, остановить только запущенный для этой проверки процесс. Для следующей мутации создать новую чистую копию; исходный набор сохраняется.

**Доказательство:** Записать ID сценария, точный plugin/IDE build, project path и HEAD, вход и результат в RUN_RECORD. Для UI приложить видимое наблюдение; для экспорта — файл и hash. Успех producer/checker не присваивает PASS плагину.

**Consumer run:** `NOT_RUN`. Capability IDs: IDE-EXPORTS.

## Редактор

<a id="ide-01"></a>
### IDE-01 — Java inspection и Impact gutter → карточка

**Зачем:** Увидеть finding в редакторе и перейти к связанному Impact без поиска вручную.

**Подготовка:** Открыть указанную лабораторию в IDEA с ArchVerity 3.0.3, JDK 21 для Gradle; дождаться import/index. Для полного показа использовать настоящий Trial/Pro. Требования отдельных инструментов перечислены ниже и в linked guides.

**Входы:** [PaymentController.java](../projects/workspace/payment-app/src/main/java/sample/payment/PaymentController.java), [PaymentClient.java](../projects/first-result/order-app/src/main/java/demo/orders/PaymentClient.java), [extended_scenarios.py](../projects/workspace/qa-support/extended_scenarios.py)

1. На Java mismatch открыть inspection ArchFlowContract; изменить контракт и открыть Impact marker на той же declaration.
   Ожидаемое наблюдение: Highlight/gutter привязаны к правильной строке и contract ID.
2. Перейти marker → Impact → source; восстановить contract и пересканировать.
   Ожидаемое наблюдение: Navigation совпадает с выбранной карточкой; устаревший marker исчезает после восстановления.

**Контрпример:** Во время indexing либо после удаления declaration открыть прежнее finding.
Ожидаемое наблюдение: Неразрешимая location обозначается; нет navigation к похожей чужой declaration.

**Восстановление:** Работать в отдельной копии. Отменить свои изменения в редакторе, вернуть изменённую настройку, остановить только запущенный для этой проверки процесс. Для следующей мутации создать новую чистую копию; исходный набор сохраняется.

**Доказательство:** Записать ID сценария, точный plugin/IDE build, project path и HEAD, вход и результат в RUN_RECORD. Для UI приложить видимое наблюдение; для экспорта — файл и hash. Успех producer/checker не присваивает PASS плагину.

**Consumer run:** `NOT_RUN`. Capability IDs: IDE-UNSAVED, IDE-FINDINGS.

## Tools и CI

<a id="cli-01"></a>
### CLI-01 — Offline import adapters

**Зачем:** Получать canonical manifests из поддержанных source/spec форматов.

**Подготовка:** Tools distribution устанавливается отдельно, private Tools source в public Git отсутствует. Точные имена и аргументы команд приведены в ENVIRONMENT_CHECKS_RU.md и Tools --help.

**Входы:** [qa-loopback.archflow.json](../projects/workspace/contracts/qa-loopback.archflow.json), [qa-openapi.json](../projects/workspace/qa-openapi.json), [inspect_export.py](../suite-support/inspect_export.py), [qa-asyncapi.json](../projects/workspace/qa-asyncapi.json), [qa-backstage.json](../projects/workspace/qa-backstage.json), [qa-event-bus.archflow.json](../projects/workspace/contracts/qa-event-bus.archflow.json), [qa-backstage.archflow.json](../projects/workspace/contracts/qa-backstage.archflow.json)

1. Из отдельно предоставленного Tools выполнить convert-openapi, convert-asyncapi, convert-backstage для трёх raw QA inputs, затем validate-manifest.
   Ожидаемое наблюдение: Каждый canonical output принят actual Tools validator и имеет правильные service/contract IDs.
2. import-sources для известного source language subset; результат сравнить с исходными declarations.
   Ожидаемое наблюдение: Manifest отражает заявленные поддержанные элементы и provenance; это не PSI scan произвольного runtime.

**Контрпример:** Неверный JSON/spec или неподдержанный protocol.
Ожидаемое наблюдение: Nonzero/diagnostic вместо пустого успешного manifest.

**Восстановление:** Работать в отдельной копии. Отменить свои изменения в редакторе, вернуть изменённую настройку, остановить только запущенный для этой проверки процесс. Для следующей мутации создать новую чистую копию; исходный набор сохраняется.

**Доказательство:** Записать ID сценария, точный plugin/IDE build, project path и HEAD, вход и результат в RUN_RECORD. Для UI приложить видимое наблюдение; для экспорта — файл и hash. Успех producer/checker не присваивает PASS плагину.

**Consumer run:** `NOT_RUN`. Capability IDs: TOOLS-CI, ARCH-MANIFESTS.

<a id="cli-02"></a>
### CLI-02 — Snapshot diff, git-diff и policy merge

**Зачем:** Сравнивать настоящие snapshots и объединять team/project policy.

**Подготовка:** Открыть указанную лабораторию в IDEA с ArchVerity 3.0.3, JDK 21 для Gradle; дождаться import/index. Для полного показа использовать настоящий Trial/Pro. Требования отдельных инструментов перечислены ниже и в linked guides.

**Входы:** [qa-loopback.archflow.json](../projects/workspace/contracts/qa-loopback.archflow.json), [qa-openapi.json](../projects/workspace/qa-openapi.json), [inspect_export.py](../suite-support/inspect_export.py), [team-policy.json](../suite-support/team-policy.json), [project-policy.json](../suite-support/project-policy.json)

1. Получить два настоящих same-scope exports из clean и mutated copy; выполнить diff и проверить Markdown; для git-diff использовать repository с реальными сохранёнными snapshot files.
   Ожидаемое наблюдение: Изменения и findings связываются с correct base/head; git-diff читает указанный существующий snapshot path.
2. policy-merge team-policy.json project-policy.json → work/merged-policy.json; открыть analysis.profiles и services.order-service.owner.
   Ожидаемое наблюдение: Profiles объединены в [default, demo], owner заменён на project-order-team; modules [order-app] и includeModules [*] сохранены, policyMetadata.merged=true.

**Контрпример:** Нет snapshot в одном ref или несовместимые scopes.
Ожидаемое наблюдение: Явная отсутствующая зависимость/несравнимость; ни одна сторона не подменяется текущим экспортом.

**Восстановление:** Работать в отдельной копии. Отменить свои изменения в редакторе, вернуть изменённую настройку, остановить только запущенный для этой проверки процесс. Для следующей мутации создать новую чистую копию; исходный набор сохраняется.

**Доказательство:** Записать ID сценария, точный plugin/IDE build, project path и HEAD, вход и результат в RUN_RECORD. Для UI приложить видимое наблюдение; для экспорта — файл и hash. Успех producer/checker не присваивает PASS плагину.

**Consumer run:** `NOT_RUN`. Capability IDs: TOOLS-CI.

<a id="cli-03"></a>
### CLI-03 — CI gates findings и Impact

**Зачем:** Сделать findings и completeness проверяемым условием CI.

**Подготовка:** Открыть указанную лабораторию в IDEA с ArchVerity 3.0.3, JDK 21 для Gradle; дождаться import/index. Для полного показа использовать настоящий Trial/Pro. Требования отдельных инструментов перечислены ниже и в linked guides.

**Входы:** [qa-loopback.archflow.json](../projects/workspace/contracts/qa-loopback.archflow.json), [qa-openapi.json](../projects/workspace/qa-openapi.json), [inspect_export.py](../suite-support/inspect_export.py)

1. Для настоящего export выполнить ci --threshold ERROR --sarif/--report; для comparison ci-impact --fail-on BREAKING --require-complete.
   Ожидаемое наблюдение: Exit code соответствует фактическим findings/verdict/completeness; reports читаются.
2. Повторить на исправленном source/current export и сравнить controlled failing case.
   Ожидаемое наблюдение: Исправление меняет gate outcome по реальным данным; старый report не используется как новый.

**Контрпример:** Incomplete/UNKNOWN comparison и строгий completeness gate.
Ожидаемое наблюдение: Incomplete analysis отклоняется отдельно от severity threshold; отсутствующий scan не становится success.

**Восстановление:** Работать в отдельной копии. Отменить свои изменения в редакторе, вернуть изменённую настройку, остановить только запущенный для этой проверки процесс. Для следующей мутации создать новую чистую копию; исходный набор сохраняется.

**Доказательство:** Записать ID сценария, точный plugin/IDE build, project path и HEAD, вход и результат в RUN_RECORD. Для UI приложить видимое наблюдение; для экспорта — файл и hash. Успех producer/checker не присваивает PASS плагину.

**Consumer run:** `NOT_RUN`. Capability IDs: TOOLS-CI.

<a id="cli-04"></a>
### CLI-04 — Fresh headless PSI producer и committed source

**Зачем:** Выполнить новый PSI scan committed source в подготовленной licensed CI среде.

**Подготовка:** Нужны отдельно предоставленные IDE/plugin distribution и настоящий подготовленный licensed CI config. Credentials автоматически не копируются. Без этой среды NOT RUN; offline JSON gate не заменяет fresh producer.

**Входы:** [qa-loopback.archflow.json](../projects/workspace/contracts/qa-loopback.archflow.json), [qa-openapi.json](../projects/workspace/qa-openapi.json), [inspect_export.py](../suite-support/inspect_export.py), [QA_MATRIX_RU.md](../projects/workspace/QA_MATRIX_RU.md)

1. На clean repository с JDK/IDE/plugin paths и заранее лицензированным isolated CI profile выполнить headless-ci/headless-impact по environment guide.
   Ожидаемое наблюдение: Producer открывает committed source и выдаёт свежий PSI scan с реальным context/revision.
2. Изменить committed contract в новой fixture copy, повторить с новым HEAD и проверить результат/выходной gate.
   Ожидаемое наблюдение: Result принадлежит новому commit; working-tree assumptions и старый snapshot не заменяют PSI run.

**Контрпример:** Нет entitlement/config, dirty repository или неподдержанный IDE/plugin.
Ожидаемое наблюдение: Fail-closed с точной причиной; dev license override и synthetic snapshot не считаются полноценным producer proof.

**Восстановление:** Работать в отдельной копии. Отменить свои изменения в редакторе, вернуть изменённую настройку, остановить только запущенный для этой проверки процесс. Для следующей мутации создать новую чистую копию; исходный набор сохраняется.

**Доказательство:** Записать ID сценария, точный plugin/IDE build, project path и HEAD, вход и результат в RUN_RECORD. Для UI приложить видимое наблюдение; для экспорта — файл и hash. Успех producer/checker не присваивает PASS плагину.

**Consumer run:** `NOT_RUN`. Capability IDs: TOOLS-CI, IDE-LICENSE.

<a id="cli-05"></a>
### CLI-05 — Verification converter и реальный extension provider

**Зачем:** Подключить свой manifest provider и преобразовать выполненные verification reports.

**Подготовка:** Открыть указанную лабораторию в IDEA с ArchVerity 3.0.3, JDK 21 для Gradle; дождаться import/index. Для полного показа использовать настоящий Trial/Pro. Требования отдельных инструментов перечислены ниже и в linked guides.

**Входы:** [qa-loopback.archflow.json](../projects/workspace/contracts/qa-loopback.archflow.json), [qa-openapi.json](../projects/workspace/qa-openapi.json), [inspect_export.py](../suite-support/inspect_export.py), [capture.py](../projects/runtime-evidence/capture.py), [.archflow.yml](../projects/runtime-evidence/.archflow.yml), [payment-openapi.json](../projects/runtime-evidence/contracts/payment-openapi.json), [example_provider.py](../suite-support/example_provider.py), [provider-context.json](../suite-support/provider-context.json), [provider-invalid-context.json](../suite-support/provider-invalid-context.json)

1. Convert actual runtime reports с --format, --metadata, --spec по runtime guide; сравнить canonical outcome/hash/context.
   Ожидаемое наблюдение: Importer сохраняет observed PASS/FAIL и привязку к действительному report/spec.
2. run-provider suite-support/example_provider.py --context suite-support/provider-context.json -o work/provider.archflow.json; validate-manifest work/provider.archflow.json.
   Ожидаемое наблюдение: Настоящий SDK вызывает generate_manifest(context); manifest содержит demo-extension-service и проходит actual validator.

**Контрпример:** run-provider с suite-support/provider-invalid-context.json либо повреждённым output.
Ожидаемое наблюдение: Nonzero/validation error; неизвестные или отсутствующие данные не заменяются доверенным результатом.

**Восстановление:** Работать в отдельной копии. Отменить свои изменения в редакторе, вернуть изменённую настройку, остановить только запущенный для этой проверки процесс. Для следующей мутации создать новую чистую копию; исходный набор сохраняется.

**Доказательство:** Записать ID сценария, точный plugin/IDE build, project path и HEAD, вход и результат в RUN_RECORD. Для UI приложить видимое наблюдение; для экспорта — файл и hash. Успех producer/checker не присваивает PASS плагину.

**Consumer run:** `NOT_RUN`. Capability IDs: TOOLS-CI, ARCH-VERIFICATION.

## MCP

<a id="mcp-01"></a>
### MCP-01 — Все четыре MCP tools и bounded responses

**Зачем:** Дать внешнему MCP consumer ограниченный read-only доступ к текущему результату.

**Подготовка:** Открыть указанную лабораторию в IDEA с ArchVerity 3.0.3, JDK 21 для Gradle; дождаться import/index. Для полного показа использовать настоящий Trial/Pro. Требования отдельных инструментов перечислены ниже и в linked guides.

**Входы:** [.archflow.yml](../projects/workspace/.archflow.yml), [coverage.json](../projects/workspace/qa-support/coverage.json)

1. В отсканированном same-project MCP Server вызвать change_impact и findings с параметрами из ENVIRONMENT_CHECKS_RU.md.
   Ожидаемое наблюдение: Ответы относятся к current HEAD/context, фильтры и limit соблюдены.
2. Вызвать contract_evidence с query реального contract и trace_flow inbound/outbound/both с непустым query; сопоставить paths с UI. Проверить limit=0 и завышенный limit.
   Ожидаемое наблюдение: Evidence и direction соответствуют выбранному объекту; limit ограничен до 1..100; locations project-relative без source text/absolute paths.

**Контрпример:** Неверные severity/direction, пустой trace query и отсутствие real entitlement.
Ожидаемое наблюдение: Explicit validation/entitlement error; пустой evidence ответ не превращается в выдуманный contract. Evidence optional query может быть пустым; неизвестный query допускает пустой результат.

**Восстановление:** Работать в отдельной копии. Отменить свои изменения в редакторе, вернуть изменённую настройку, остановить только запущенный для этой проверки процесс. Для следующей мутации создать новую чистую копию; исходный набор сохраняется.

**Доказательство:** Записать ID сценария, точный plugin/IDE build, project path и HEAD, вход и результат в RUN_RECORD. Для UI приложить видимое наблюдение; для экспорта — файл и hash. Успех producer/checker не присваивает PASS плагину.

**Consumer run:** `NOT_RUN`. Capability IDs: MCP-TOOLS.
