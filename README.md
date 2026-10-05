# ArchVerity Demo

Open demonstration and regression projects for the ArchVerity IntelliJ plugin.
All service identities, source code and data are synthetic. You can inspect
architecture without running business services, and exercise network features
against local servers. [English project overview](docs/OVERVIEW_EN.md).

Публичный набор проектов для показа и повторяемого тестирования функций
ArchVerity. Основная демонстрация показывает Kafka profiles и границы
совместимости; небольшой HTTP-пример помогает быстро познакомиться с плагином.
Плагин устанавливается отдельно из
[JetBrains Marketplace](https://plugins.jetbrains.com/plugin/34234-archverity).

**[Kafka: profiles и границы совместимости](docs/KAFKA_PROFILES_ARTICLE_RU.md)** —
практическая статья для Java/Spring-разработчиков и
[видео настоящей IDEA с русскими пояснениями](docs/media/kafka-profiles-3.0.4.mp4).
Две repository identities, `blue/green`, неизвестный wire binding, доказанное
расхождение `tenant`, исправление и контроль разных clusters связаны в один путь.
[Шесть полных exports](docs/evidence/kafka-3.0.4/README.md) можно проверить командой
`python -B -X utf8 suite-support/inspect_kafka_story.py`.

**[Короткий HTTP-разбор](docs/FIRST_RESULT_ARTICLE_RU.md)**
разбирает пример, который компилируется при несовпадающих HTTP-методах:
finding, исходники обеих сторон, исправление и повторная проверка в 3.0.4.
В статье есть [70-секундная запись работы в IDEA](docs/media/first-result-3.0.4.mp4)
с русскими пояснениями и контрольным возвратом исходного расхождения.

**[Пошаговая инструкция запуска](docs/DEMO_RUNBOOK_RU.md)** проводит через
подготовку, первый finding, все шесть лабораторий, полную проверку и запись
результатов. **[Оглавление документации](docs/README.md)** связывает инструкции,
каталоги функций и руководства каждого проекта.

**[Все функции подробно](docs/ALL_FUNCTIONS_RU.md):** 62 пользовательские
возможности ArchVerity 3.0.3 — назначение, подготовка, конкретные действия,
ожидаемый результат, контрпример и восстановление. Отдельная
**[матрица 87 точек входа](docs/ENTRY_POINTS_RU.md)** раскрывает каждую команду,
настройку и editor extension. Прежние 41 capability recipe и 19 Impact-мутаций
сохранены.

**[Функциональная проверка 05.10.2026](docs/FUNCTIONAL_AUDIT_RU.md)** связывает
каждую функцию с выполненными тестами, перечисляет исправления и показывает
оставшиеся проверки в IDEA, на устройствах и в удалённой среде.

| Проект | Зачем открыть | Что подготовлено |
| --- | --- | --- |
| [first-result](projects/first-result/README.md) | Первый результат за несколько действий | Компилируемые Spring MVC + OpenFeign, намеренный POST/PUT mismatch, исправление до совпадающего метода |
| [workspace](docs/ARCHITECTURE_WALKTHROUGH_RU.md) | Основная демонстрация и регрессия | Java/Kotlin, HTTP/Kafka/AMQP, вложенные DTO, Spring, MyBatis, Ansible, Shell/Bats, ANSI, иконки, публичные сертификаты, 19 изолированных мутаций |
| [api-lab](projects/api-lab/README.md) | Проверка API Client | HTTP/WebSocket/gRPC loopback, descriptor с imports, сценарии, отрицательные входы, deadline и cancel |
| [mobile-lab](projects/mobile-lab/README.md) | React Native / Expo и команды устройств | Настоящее приложение, lockfile, Metro, bundle; native проекты создаются через Expo prebuild |
| [runtime-evidence](projects/runtime-evidence/README.md) | Импорт runtime и verification evidence | Запускаемый Spring Boot Actuator, реальные bean dependencies, локальные PASS/FAIL отчёты в Pact/Drift форматах |
| [kafka-profile-lab](projects/kafka-profile-lab/README.md) | Kafka UNKNOWN и границы evidence | 12 изолированных случаев: разные profiles/clusters, внешний serializer, regex, defaults/cycles, равные DTO и положительные контроли; требует ArchVerity 3.0.4 или новее |

## Быстрый показ

Нужны Git, Python 3.10+, JDK 21 и IDEA, поддерживаемая **установленной версией**
ArchVerity. Для всех шести лабораторий используйте **3.0.4** или более новую
совместимую сборку; для локальной IDEA 2024.3 нужен отдельный **3.0.4-2024.3**.
Inventory полного руководства сохраняет 62 функции и 87 точек входа версии 3.0.3.
Оба обновления 3.0.4 одобрены и доступны в Marketplace с 05.10.2026;
[запись проверки выпуска](docs/VERIFICATION_RU.md#выпуск-304--05102026)
разделяет загрузку и публичную доступность. Trial/Pro необходим для платных операций, экспорта и MCP;
этот репозиторий не выдаёт и не подменяет лицензию. Первый Gradle/npm install
требует сети; основные архитектурные примеры не требуют Kafka/RabbitMQ/БД.

```powershell
git clone https://github.com/lMysticl/ArchVerity-Demo.git
cd ArchVerity-Demo
python -B -X utf8 suite-support/check_suite.py
```

Для короткого показа сначала создайте отдельную копию из корня набора:

```powershell
python -B -X utf8 suite-support/prepare_project.py --project first-result --output D:/CodexData/Temp/archverity-first-demo
```

Откройте **созданную папку как Gradle-проект** в
IDEA, выберите JDK 21 как Gradle JVM, дождитесь индексации и нажмите
ArchVerity → Analyze. Откройте finding: клиент отправляет POST, провайдер
принимает PUT. Навигация должна открыть обе стороны. Исправьте метод клиента
на PUT, повторите Analyze и проверьте, что именно method-mismatch исчез.

Для Impact нужна отдельная чистая Git-копия **проекта**, а не просто подкаталог
этого репозитория. Из корня набора:

```powershell
python -B -X utf8 suite-support/prepare_project.py --project workspace --output D:\CodexData\Temp\archverity-demo-workspace
```

Откройте созданную папку в IDEA, выполните Analyze на чистом HEAD. Затем из
терминала этой папки:

```powershell
python -B -X utf8 qa-support/apply_impact.py --project . --scenario combined-breaking
```

Скрипт требует полный сохранённый снимок этого HEAD, меняет только заданные
файлы и сохраняет исходную копию набора. Анализ HEAD → WORKTREE должен показать
последствия POST→PUT, обязательного поля запроса и удалённого поля ответа.
Следуйте [полной инструкции](docs/ARCHITECTURE_WALKTHROUGH_RU.md) для Evidence,
двусторонней навигации, downstream review, baseline и экспорта.

## Полная проверка

- [Каталог функций](docs/FEATURE_CATALOG.md): функция → вход → действие → ожидаемое наблюдение → среда.
- [Матрица зарегистрированных действий IDEA](projects/workspace/QA_MATRIX_RU.md): 87 entry points — 15 экранов, 6 действий, 22 команды процессов, 7 команд отладчика, 6 экспортов, 4 MCP, 5 настроек и 22 editor extension.
- [Средовые сценарии](docs/ENVIRONMENT_CHECKS_RU.md): все мобильные команды, SSH debugger, MCP, Split Mode, лицензии и headless CI.
- [Запись результатов](docs/RUN_RECORD.md): отдельно фиксируйте подготовку, фактическую проверку и блокирующую предпосылку.
- [Проверенный прогон](docs/VERIFICATION_RU.md): версия среды и реально выполненные проверки этого набора.

Подготовка входов проверяется `suite-support/check_suite.py`. Maintainer может
добавить `--plugin-source <корень исходников плагина> --require-source`: тогда
появление зарегистрированной функции без сценария завершит проверку ошибкой.
Матрица относится к данным и зарегистрированным действиям; полная работоспособность
IDEA, мобильного устройства, remote и лицензии подтверждается их отдельным прогоном.

Проекты и инструкции сохраняются в Git. Кеши, отчёты, private keys, локальные
настройки и сгенерированные native каталоги исключены. [Лицензия и происхождение](NOTICE.md).
