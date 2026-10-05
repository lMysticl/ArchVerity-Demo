# Workspace: архитектура, Impact и developer tools

[Общая пошаговая инструкция](../../docs/DEMO_RUNBOOK_RU.md#3-архитектура-impact-и-инструменты-редактора)
показывает подготовку этого проекта и переходы ко всем шести лабораториям.

Это Java/Kotlin Gradle-проект для анализа исходников четырёх service IDs:
order-service, payment-service, notification-service, analytics-service.
Используйте JDK 21; HTTP business services, Kafka/RabbitMQ и БД здесь не запускаются.
Локальные сетевые примеры находятся в соседних api-lab и runtime-evidence.

Из корня ArchVerity-Demo создайте новый самостоятельный Git-root:

```powershell
python -B -X utf8 suite-support/prepare_project.py --project workspace --output D:/CodexData/Temp/archverity-workspace-demo
```

Откройте output как Gradle project, дождитесь import/index, выполните Analyze
на clean HEAD. Получите complete HEAD snapshot, затем применяйте одну мутацию
из терминала этой копии. Для каждого другого сценария нужна новая copy/baseline.

- [Архитектура и все 19 Impact-мутаций](../../docs/ARCHITECTURE_WALKTHROUGH_RU.md).
- [Все 62 функции](../../docs/ALL_FUNCTIONS_RU.md) и [87 точек входа](../../docs/ENTRY_POINTS_RU.md).
- [QA matrix workspace](QA_MATRIX_RU.md): исходные примеры и наблюдения для UI/editor/settings.
- [Real submodule / public-only keystores](../../docs/ICON_AND_KEYSTORE_INPUTS_RU.md).
- [Средовые команды](../../docs/ENVIRONMENT_CHECKS_RU.md) и [запись прогона](../../docs/RUN_RECORD.md).

Для более раннего fixture-specific preflight сохранён [README_RU.md](README_RU.md).
Общий runbook и полный каталог выше задают маршрут текущего публичного набора.
