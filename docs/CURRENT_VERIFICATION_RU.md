# Публичное демо для ArchVerity 5.8.2 — 30.10.2026

[Текущий маршрут](PRODUCT_TOUR_RU.md) · [Boot Kafka lab](../projects/kafka-boot-lab/README.md) ·
[Исторические проверки](VERIFICATION_RU.md) · [Записать свой IDEA run](RUN_RECORD.md)

Инструкции относятся к выпущенным Stable [5.8.2](https://plugins.jetbrains.com/plugin/34234-archverity-ai/versions/stable/1206577)
и [5.8.2-2024.3](https://plugins.jetbrains.com/plugin/34234-archverity-ai/versions/stable/1206580).
Пять текущих вкладок — Changes, Map, Problems, Agents и Tools; современный пакет
предоставляет 19 MCP tools, включая `archverity_simulate_change`.

## Уже имеющееся релизное доказательство

В Jenkins №149 логического релиза 148 production source
`524bdd34047e71c8639196ffa5ff481c4c673a8a` проверил прежний публичный demo commit
`901655e6510fe615c82f909895c0042668914d21`, `projects/workspace`:

- Один `DemoMutationCorpusTest` выполнил все 19 публичных мутаций и два
  дополнительных сценария listener-topic / HTTP path; весь метод PASS.
- Все 13 сопоставленных what-if результатов совпали с фактическими правками.
- В `kafka-topic` после `KeepTopicPlan` и в дополнительном listener-topic после
  `KeepListeningPlan` осталось ноль Breaking. Это наблюдения указанного корпуса,
  а не обещание автоматического исправления любого Kafka listener.

Это результат старого входа на новом анализаторе. Свежие проверки обновлённых
Boot и profile labs приведены ниже; релизный прогон workspace сохраняет свою
отдельную идентичность.

## Проверка обновлённых Kafka labs — 30.10.2026

В отдельной Windows-копии неизменённого production source
`524bdd34047e71c8639196ffa5ff481c4c673a8a` выполнены два выбранных класса:

- `PublicBootKafka582Test`: **10/10 PASS**, пять случаев на каждой Boot-линии;
  отдельный временный test harness, SHA-256
  `b3a17b995c4af7b41b9fb07f6707b530d408eb71ec48f344379d6d735b9f78a1`.
- `KafkaProfileScanIntegrationTest.testPublicCaseK01`–`K12`: **12/12 PASS**.
- В JUnit XML обоих классов **0 failures, 0 errors, 0 skipped**. Это реальные
  PSI/source-analysis тесты с SDK IDEA **2026.1.4** и его test JVM — JBR
  **25.0.3**. Gradle/toolchain использовал JDK **21.0.12.1**; открытый
  пользовательский проект IDEA не заменялся.

### Новый Boot Kafka lab

Все **10** подготовленных Java-копий отдельно скомпилированы с настоящими BOM
**3.5.7 / 4.0.0**. Локальная Windows-компиляция использовала JDK **25.0.3**
с `release=21`; проверен class-file major **65**. Current/base source hashes
совпадают с inputs, переданными анализатору. Полные JSON exports, Git base,
project ID, SDK/JDK и hashes библиотек проверены для каждого случая.

| Case | Результат на обеих Boot-линиях |
| --- | --- |
| B01 `baseline` | Обычная Boot wire-цепочка разрешена; seeded mismatch и contract changes отсутствуют |
| B02 `remove-required` | `AFG-KAFKA-005 PROVEN_MISMATCH`, Changes — Breaking; после физического восстановления producer из того же HEAD seeded mismatch и impacts отсутствуют |
| B03 `add-optional` | Добавленное поле producer даёт `SAFE` impact в пределах этого JSON-контракта |
| B04 `customizer-control` | `UNKNOWN`, с именованным `ProducerOverrides.java`; неподтверждённый wire mismatch не повышается до proven |
| B05 `historical-reader` | Breaking для **старого producer → текущего reader**, хотя текущие DTO совпадают; activation/build inputs между Git base и working tree одинаковы |

### Прежние K01–K12 и pattern controls

Эта линия использует существующий PSI harness с синтетическими объявлениями
типов и точными публичными Java/YAML inputs. Она проверяется отдельно от Boot
lab с настоящими библиотеками. Сохраняются unknown scope, внешние/cyclic
properties, opaque factory, proven mismatch и compatible controls.

Первичная сверка exports обнаружила устаревшее ожидание K04/K05: явный
serializer был ошибочно принят за полную wire-определённость. У pattern
consumer factory/serde binding остаётся `RESOLVED`, но без конкретного
`topics` релиз 5.8.2 оставляет topic-specific `wireConfidence=INFERRED` и
`AFG-KAFKA-010 UNKNOWN`. K03 и K05 отличаются только аннотацией в
`consumer/.../Listener.java`; остальные **20** файлов package совпадают.
K06 отдельно сохраняет настоящий unresolved serializer у producer.

Текущий export checker требует для K04/K05 именно consumer pattern UNKNOWN,
разрешённые underlying factory/serde/settings и их source provenance.
Запрет ложного `010` для explicit literal-topic controls и запрет
cross-scope `005` сохранены. Все **12/12** сохранённых полных exports прошли
эту сверку; сами exports и анализируемые inputs при коррекции ожиданий не менялись.
[Cases, точные ожидания и команды](../projects/kafka-profile-lab/README.md).

Подготовка, compile и PSI-анализ показывают разные границы. Здесь не заявлены
новые UI/MCP/Remote/Split Mode runs, broker delivery или наличие исторических
records в реальном Kafka. [CI](../.github/workflows/checks.yml) отдельно
проверяет публичные inputs и компиляцию на Windows/Linux с JDK 21.

## Исторический отчёт 5.3.2

Ниже сохранены исходные дата, source, FAIL и различающий контроль 23 октября.
Они не являются текущим ожидаемым retry-listener результатом для 5.8.2.

---

# Проверка публичного демо для 5.3.2 — 23.10.2026

[Маршрут продукта](PRODUCT_TOUR_RU.md) · [Лаборатория Boot upgrade](../projects/boot-upgrade/README.md) ·
[Исторические проверки](VERIFICATION_RU.md) · [Записать свой IDEA run](RUN_RECORD.md)

Сверка с исходниками ArchVerity 5.3.2:
`15ca7a22519abbf92d8a3d7f9f59f1f17adaa9a4`. Публичный набор расширяет исходный
demo commit `de07998fb7369d099ef6267e0884baedb2ed0623`. Среда локального прогона:
Windows, Python 3.12, Temurin JDK 21.0.12+1; для engine-тестов — библиотеки
установленной IDEA 2026.1.4. Открытый IDE-проект не заменялся.

| Что проверено | Наблюдение | Граница доказательства |
| --- | --- | --- |
| Исходники и документация | 114 registrations: 18 views, 10 actions, 18 MCP, 22 process, 7 debug, 6 exports, 5 settings, 28 editor extensions; 49 recipes | Соответствие текущему коду и доступность входов, не 114 выполненных UI-прогонов |
| Python regressions | 37 tests; после изменения preparation повторены соответствующие 10; ещё 4 workspace coverage controls | Подготовка, отказ от перезаписи правок, документация, export/media boundaries |
| Настоящие Boot 3.5.15 / 4.1.1 мапперы | До исправления `WIRE_DIFFERENCES_CONFIRMED`; после — `WIRE_FIX_PASS` | Реальные библиотеки и компиляция; [исходные JSON и hashes](evidence/boot-upgrade-20261023/README.md) |
| `BootUpgradeFixtureTest` | PASS: четыре поддержанных риска; после явных исправлений рисков не осталось | Engine integration fixture из исходников плагина; не GUI-прогон нового public lab |
| `WhatIfFixtureTest` | PASS | Engine integration для pre-edit simulation |
| `DemoMutationCorpusTest` на поставляемом workspace | 19 изменений обработаны; 13 simulations совпали с реальными правками; весь тест FAIL на дополнительном retry-listener исправлении | [Полный измеренный результат](evidence/engine-5.3.2-20261023/shipped-workspace.txt); ошибка не скрыта |
| Тот же корпус, отдельная копия без `@RetryableTopic` у OrderListener | PASS, в том числе `KeepListeningPlan`, после него 0 BREAKING | [Различающий контроль](evidence/engine-5.3.2-20261023/without-retry-control.txt); исходный workspace сохранён |

Первая попытка engine-тестов offline остановилась до выполнения тестов из-за
отсутствующей Gradle plugin dependency. После её разрешения online выполнен
описанный прогон: два теста PASS, один FAIL. Повтор с изменённым входом проверял
конкретную гипотезу о retry listener, а не заменял результат исходного набора.

## Точная известная граница автоматического исправления

В `workspace/payment-app/src/main/java/sample/payment/OrderListener.java` есть
`@RetryableTopic` и `@KafkaListener(topics="orders.created",...)`. При переносе
listener на `orders.revised` анализ правильно обнаруживает BREAKING, но
исправление не создаётся: измерено `applyFix=[]`, после проверки остаётся один
BREAKING. В этом пути hint имеет `PUBLISH_BOTH`, тогда как planner для listener
принимает `LISTEN_BOTH` и изменение только topics.

В контрольной копии удалили **только `@RetryableTopic` перед начальным анализом**.
Тот же перенос получил `LISTEN_BOTH` → `KeepListeningPlan` и после применения
не оставил доказанных разрывов. Это сужает проблему до данного retry-listener
пути. Общая рекомендация «любой Kafka listener исправляется автоматически»
не подтверждена. Исправление реализации плагина и новый бинарный релиз не входят
в это обновление публичного демо.

Чтобы отдельно увидеть поддержанный plain-listener сценарий:

1. Подготовьте новую workspace-копию, удалите в ней `@RetryableTopic` у
   `OrderListener` и зафиксируйте эту учебную исходную версию обычным Git commit.
2. Импортируйте и полностью отсканируйте её чистый HEAD.
3. Вручную замените только listener topic `orders.created` на `orders.revised`.
4. Выполните Review HEAD → working tree, изучите и примените доступное Apply fix.
   Пересканируйте: конкретный разрыв должен исчезнуть. Исходный producer всё
   ещё публикует в старый topic, поэтому сохранение старой подписки существенно.

Наличие другого UNKNOWN после исправления — отдельная граница знания. Например,
в полном workspace исправление HTTP method очищает доказанный разрыв, но
общий ответ остаётся UNKNOWN из-за других неразрешённых связей. Не меняйте это
на «всё безопасно» в демонстрации. Удаление `providerReference` также требует
ручного решения владельца контракта; поле не восстанавливается этим auto-fix.

## Что подтверждается отдельным пользовательским прогоном

Новая запись работы ArchVerity 5.3.2 в установленной IDEA, реальные entitlement-состояния,
все 18 MCP-вызовов с агентом, устройства и remote/Split Mode здесь не объявлены
прошедшими. Репозиторий содержит сценарии, prerequisites и отрицательные
контроли для этих наблюдений. Старые записи 3.0.4/5.0 остаются историческими.

Для воспроизведения engine-корпуса maintainer исходников задаёт
`ARCHVERITY_DEMO_WORKSPACE=<demo>/projects/workspace`, `PYTHON=<python executable>`
и `ARCHVERITY_PRODUCT_CAPTURE_DIR=<новая папка>`, затем запускает
`:plugin-backend:test --tests '*DemoMutationCorpusTest'` по инструкции сборки
плагина. Используйте опубликованный workspace без изменения retry annotation,
если проверяете именно описанную известную проблему.
