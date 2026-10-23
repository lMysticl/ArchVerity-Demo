# Документация ArchVerity Demo

**Начните с [маршрута ArchVerity 5.3.2](PRODUCT_TOUR_RU.md)**: первый finding, What-if, Apply fix, Boot upgrade, отчёт для команды и агент. [English tour](PRODUCT_TOUR_EN.md).

Начните с [пошаговой инструкции запуска](DEMO_RUNBOOK_RU.md): подготовка среды,
первый finding, все семь лабораторий, остановка своих процессов и запись результатов.
[English overview](OVERVIEW_EN.md) даёт короткое описание проектов.

| Задача | Руководство |
| --- | --- |
| Провести демонстрацию с нуля | [Запуск всех лабораторий](DEMO_RUNBOOK_RU.md) |
| Проследить Kafka profiles, UNKNOWN → доказанное расхождение → исправление и разные cluster scopes | [Kafka: статья, видео и шесть native exports](KAFKA_PROFILES_ARTICLE_RU.md) |
| Разобрать компилируемый POST/PUT пример и проверить исправление в 3.0.4 | [Практическая статья для Java/Spring-разработчиков](FIRST_RESULT_ARTICLE_RU.md) |
| Изучить каждую функцию | [Все 62 функции](ALL_FUNCTIONS_RU.md) |
| Проверить конкретную кнопку, команду, настройку или editor extension | [Все 114 точек входа](ENTRY_POINTS_RU.md) |
| Найти fixture и прежний capability ID | [Каталог функций и входов](FEATURE_CATALOG.md) |
| Проверить архитектуру, baseline, Impact и Review | [Архитектурный walkthrough и 19 мутаций](ARCHITECTURE_WALKTHROUGH_RU.md) |
| Проверить submodule-only rules и семь keystore-форматов | [Иконки и crypto inputs](ICON_AND_KEYSTORE_INPUTS_RU.md) |
| Подготовить Tools/MCP/SSH/licensing/Split Mode | [Средовые инструкции](ENVIRONMENT_CHECKS_RU.md) |
| Проверить Kafka profiles, cluster scope и UNKNOWN | [12 Kafka-сценариев](../projects/kafka-profile-lab/README.md) |
| Записать actual positive/negative/recovery result | [Шаблон прогона](RUN_RECORD.md) |
| Посмотреть реально выполненные проверки | [Verification record](VERIFICATION_RU.md) |
| Проверки текущего обновления и точная граница retry-listener auto-fix | [Результаты для 5.3.2](CURRENT_VERIFICATION_RU.md) |
| Связать каждую функцию с тестами, исправлениями и оставшимися проверками | [Функциональная проверка](FUNCTIONAL_AUDIT_RU.md) |
| Понять происхождение исходников и зависимостей | [NOTICE](../NOTICE.md) |

## Документы семи проектов

- [first-result](../projects/first-result/README.md): первый HTTP mismatch и исправление.
- [workspace](../projects/workspace/README.md): основная архитектура, Impact и developer tools.
- [api-lab](../projects/api-lab/README.md): реальные HTTP/WebSocket/gRPC и scenario DSL.
- [mobile-lab](../projects/mobile-lab/README.md): RN/Expo, scripts, bundle и device prerequisites.
- [runtime-evidence](../projects/runtime-evidence/README.md): реальные Actuator/verification inputs и identity-bound capture.
- [kafka-profile-lab](../projects/kafka-profile-lab/README.md): profiles, external overrides, отдельные scopes и actual JSON oracle.

Полное руководство сохраняет 62 исторические группы из inventory 3.0.3;
рецепты и 114 зарегистрированных controls сверены с исходниками **5.3.2**.
Все 41 прежние capability recipes сохранены, добавлено восемь текущих.
`suite-support/check_suite.py` проверяет
входы и подготовленные рецепты; maintainer с исходниками добавляет
`--plugin-source <source-root> --require-source`.
Порядок source comparison также описан в
[README набора](../README.md#полная-проверка).
Actual IDEA/device/MCP/remote outcomes записываются по выбранной версии и проекту.

Для текущего маршрута используйте 5.3.2 и поддерживаемую им IDEA.
[Историческая запись 3.0.4](VERIFICATION_RU.md#выпуск-304--05102026)
относится к старым Kafka-видео и exports; это не текущая инструкция установки.

## Лаборатория Spring Boot upgrade

[boot-upgrade](../projects/boot-upgrade/README.md) — седьмой проект: настоящие Boot 3/4 мапперы, четыре риска, явное исправление и mapper-unknown control. Подготовка: `python -B -X utf8 suite-support/prepare_project.py --project boot-upgrade --output ../archverity-upgrade-demo`.
