# Документация ArchVerity Demo

Начните с [пошаговой инструкции запуска](DEMO_RUNBOOK_RU.md): подготовка среды,
первый finding, все шесть лабораторий, остановка своих процессов и запись результатов.
[English overview](OVERVIEW_EN.md) даёт короткое описание проектов.

| Задача | Руководство |
| --- | --- |
| Провести демонстрацию с нуля | [Запуск всех лабораторий](DEMO_RUNBOOK_RU.md) |
| Изучить каждую функцию | [Все 62 функции](ALL_FUNCTIONS_RU.md) |
| Проверить конкретную кнопку, команду, настройку или editor extension | [Все 87 точек входа](ENTRY_POINTS_RU.md) |
| Найти fixture и прежний capability ID | [Каталог функций и входов](FEATURE_CATALOG.md) |
| Проверить архитектуру, baseline, Impact и Review | [Архитектурный walkthrough и 19 мутаций](ARCHITECTURE_WALKTHROUGH_RU.md) |
| Проверить submodule-only rules и семь keystore-форматов | [Иконки и crypto inputs](ICON_AND_KEYSTORE_INPUTS_RU.md) |
| Подготовить Tools/MCP/SSH/licensing/Split Mode | [Средовые инструкции](ENVIRONMENT_CHECKS_RU.md) |
| Проверить Kafka profiles, cluster scope и UNKNOWN | [12 Kafka-сценариев](../projects/kafka-profile-lab/README.md) |
| Записать actual positive/negative/recovery result | [Шаблон прогона](RUN_RECORD.md) |
| Посмотреть реально выполненные проверки | [Verification record](VERIFICATION_RU.md) |
| Понять происхождение исходников и зависимостей | [NOTICE](../NOTICE.md) |

## Документы шести проектов

- [first-result](../projects/first-result/README.md): первый HTTP mismatch и исправление.
- [workspace](../projects/workspace/README.md): основная архитектура, Impact и developer tools.
- [api-lab](../projects/api-lab/README.md): реальные HTTP/WebSocket/gRPC и scenario DSL.
- [mobile-lab](../projects/mobile-lab/README.md): RN/Expo, scripts, bundle и device prerequisites.
- [runtime-evidence](../projects/runtime-evidence/README.md): реальные Actuator/verification inputs и identity-bound capture.
- [kafka-profile-lab](../projects/kafka-profile-lab/README.md): profiles, external overrides, отдельные scopes и actual JSON oracle.

Полное руководство привязано к source inventory ArchVerity 3.0.3 и сохраняет
все 41 прежние capability recipes. `suite-support/check_suite.py` проверяет
входы и подготовленные рецепты; maintainer с исходниками добавляет
`--plugin-source <source-root> --require-source`.
Порядок source comparison также описан в
[README набора](../README.md#полная-проверка).
Actual IDEA/device/MCP/remote outcomes записываются по выбранной версии и проекту.

Kafka profile/evidence recipes требуют 3.0.4 или новее; для локальной IDEA
2024.3 существует отдельный 3.0.4-2024.3. [Запись выпуска и проверок](VERIFICATION_RU.md#выпуск-304--05102026)
фиксирует загрузку обоих обновлений и отдельно статус одобрения Marketplace.
