# Kafka profiles and evidence lab

Producer включает Spring profile `blue`, consumer — `green`. Обе стороны
используют `orders.events` и одинаковый недоступный bootstrap `127.0.0.1:1`;
только producer зависит от внешнего `KAFKA_VALUE_SERIALIZER`. Topic name и
bootstrap address не доказывают общий кластер или совместимый контракт.

Два Gradle-модуля моделируют разные repository identities из `.archflow.yml`.
Это синтетический workspace для статического анализа без запуска Kafka.
[Общая инструкция демонстрации](../../docs/DEMO_RUNBOOK_RU.md).

## Требования к сборке

Новые `AFG-KAFKA-009/010` требуют source build ArchVerity с исправлением Kafka
profile/evidence. Номер пакета может оставаться `3.0.3`; прежняя опубликованная
Marketplace-сборка не содержит это исправление. В
[RUN_RECORD](../../docs/RUN_RECORD.md) внесите source commit, SHA-256
установленного ZIP, IDE build, путь проекта и его HEAD. Номера версии недостаточно.
Trial/Pro нужен для платного Analysis JSON export; demo не выдаёт лицензию.

Нужны Git, Python 3.10+, JDK 21 и совместимая IDEA. Fixture привязан к Spring
Boot BOM **3.5.12**, Spring Kafka **3.3.14**, kafka-clients **3.9.2**, Jackson
**2.19.4**. Это версии компиляции; версия брокера не заявлена.

## Первый сценарий

Из корня demo repo подготовьте новую самостоятельную копию:

```powershell
python -B -X utf8 suite-support/prepare_kafka_case.py --case unknown-cluster-and-override --output E:/CodexData/Temp/kafka-K01
```

Helper создаёт чистый собственный Git HEAD, сохраняет исходную лабораторию и
отказывается перезаписывать существующий output. Откройте output как Gradle
project, выберите JDK 21, дождитесь импорта обоих модулей и индексации. В терминале
созданного output проверьте compile:

```powershell
./gradlew.bat :producer:classes :consumer:classes --console=plain
```

В Linux/macOS используйте `./gradlew`. В IDEA нажмите ArchVerity → Analyze,
откройте Evidence у UNKNOWN finding. Для K01 ожидаются:

- Два разных topic nodes, `AFG-KAFKA-009/010` с disposition `UNKNOWN`.
- Оба пути: `producer/.../application-blue.yml` и `consumer/.../application-green.yml`.
- Цепочка `topics.orders → topic.alias → orders.events` и явно неразрешённый `KAFKA_VALUE_SERIALIZER`.
- Отсутствие доказанного cross-service Kafka mismatch из одного совпадающего имени.

Проверяйте disposition, а не только цвет/severity. Экспортируйте полный текущий
Analysis JSON той же копии в `work/analysis.json`. Из корня demo repo:

```powershell
python -B -X utf8 suite-support/inspect_kafka_export.py --case unknown-cluster-and-override --snapshot E:/CodexData/Temp/kafka-K01/work/analysis.json
```

Checker проверяет actual export; IDE/build/project identity оператор фиксирует
отдельно. Написанный вручную JSON не доказывает работу плагина.

## Все 12 сценариев

Имена и ожидания заданы в [cases.json](cases.json). Для каждого ID используйте
новый output; повторите prepare, compile, Analyze, export и check с тем же
`--case`. Каждая копия имеет собственные HEAD и analysis fingerprint.

| ID | `--case` | Ожидаемое наблюдение |
| --- | --- | --- |
| K01 | `unknown-cluster-and-override` | Два профиля и одинаковые topic/bootstrap: отдельные scopes, `009/010 UNKNOWN`, оба пути и missing override |
| K02 | `shared-cluster-unresolved-serializer` | Общий declared scope; DTO drift даёт `005 UNKNOWN`, binding — `010 UNKNOWN` |
| K03 | `separate-clusters-same-topic` | `east/west` и точные статические JSON bindings: два topic nodes, без cross-cluster `005/009/010` |
| K04 | `unknown-cluster-pattern` | Regex consumer остаётся отдельным pattern node и не подхватывает producer topic другого unknown scope |
| K05 | `separate-cluster-pattern` | Consumer regex из `west` не разрешается по producer topic из `east` |
| K06 | `equal-dto-unresolved-serializer` | Одинаковые DTO не скрывают отсутствующее wire proof: `010 UNKNOWN` |
| K07 | `nested-external-override` | `value-serializer → wire.serializer → KAFKA_VALUE_SERIALIZER`; вся цепочка, `005/010 UNKNOWN` |
| K08 | `fallback-is-not-deployment-proof` | Default у `${KAFKA_VALUE_SERIALIZER:...}` не доказывает effective deployment value |
| K09 | `cyclic-serializer-configuration` | Цикл явно unresolved; обход завершается, wire остаётся UNKNOWN |
| K10 | `fixed-analysis-override` | Явный analysis override закрывает свой config key; opaque factory map всё ещё даёт `010 UNKNOWN` |
| K11 | `proven-drift-control` | Общий declared scope, простые точные JSON bindings, обязательное `tenant` отсутствует у producer: `005 PROVEN_MISMATCH` |
| K12 | `compatible-static-control` | Общий scope, простые точные bindings и равная статическая DTO shape: нет `005/009/010` |

Для shared cases helper явно задаёт `kafka.defaultCluster: declared-demo` в
`.archflow.yml`; separate cases используют module/profile property
`archflow.kafka.cluster`. Логическое объявление — предпосылка статической модели.
Оно не заменяет наблюдение Kafka cluster ID и deployed configuration.
K12 означает отсутствие этих статических findings; он не обещает успешную
десериализацию, поддержку type headers, schema registration или delivery.

Восстановление — новый output из исходного набора. Process environment ради
положительного scan не изменяют: анализ читает выбранные source properties и
явные `analysis.propertyOverrides`. Fallback сохраняет unresolved external key.

## Runtime chain

Для real Actuator capture используйте отдельный
[runtime-evidence lab](../runtime-evidence/README.md). `/beans` показывает names,
types и dependencies; effective serializer/ObjectMapper, wire format и broker
cluster ID он не сообщает.

Accepted observation сохраняет вместе со static chain service, environment,
repository revision, configuration fingerprint, Actuator context, observation
time и SHA-256 raw capture. Другие identity/hash, будущая или просроченная
observation не уточняют binding. Валидный bean capture не повышает UNKNOWN wire
до доказанного контракта и не удаляет альтернативные static profile paths.
После изменения config/fingerprint нужны current export и новое наблюдение
этой же deployment identity.

Bytes/headers/schema ID, send acknowledgement, business effect и offset commit
требуют actual broker/application observations. Compile и scan не подтверждают
exactly-once, performance, ACL, lag, Streams/Connect или физический общий кластер.

## Автоматическая проверка

```powershell
python -B -X utf8 -m unittest discover -s suite-support -p test_kafka_cases.py -v
python -B -X utf8 suite-support/check_suite.py
```

Recipe tests проверяют изоляцию и отказы export checker при потере scope,
provenance или UNKNOWN. Их synthetic negative controls не считаются plugin scan.
Maintainer `KafkaProfileScanIntegrationTest` проходит loader → Java PSI → backend
scan → graph/rules → JSON. Опциональный consumer run читает 12 подготовленных
roots через `ARCHVERITY_KAFKA_CASE_INPUT` и пишет actual JSON в
`ARCHVERITY_KAFKA_CASE_OUTPUT`; exports проверяют этим же checker. Тест использует
API declarations; compile fixture отдельно проверяет настоящие библиотеки.
Ручной licensed UI run записывается отдельно.

Основания: [Spring Boot external config](https://docs.spring.io/spring-boot/3.5/reference/features/external-config.html),
[Spring Kafka 3.3 serializers](https://docs.spring.io/spring-kafka/reference/3.3/kafka/serdes.html),
[Kafka 3.9 bootstrap/serializer settings](https://kafka.apache.org/39/configuration/producer-configs/),
[Kafka 3.9 cluster ID](https://kafka.apache.org/39/javadoc/org/apache/kafka/clients/admin/DescribeClusterResult.html).
