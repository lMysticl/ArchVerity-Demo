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

Новая запись работы в установленной IDEA 5.3.2, реальные entitlement-состояния,
все 18 MCP-вызовов с агентом, устройства и remote/Split Mode здесь не объявлены
прошедшими. Репозиторий содержит сценарии, prerequisites и отрицательные
контроли для этих наблюдений. Старые записи 3.0.4/5.0 остаются историческими.

Для воспроизведения engine-корпуса maintainer исходников задаёт
`ARCHVERITY_DEMO_WORKSPACE=<demo>/projects/workspace`, `PYTHON=<python executable>`
и `ARCHVERITY_PRODUCT_CAPTURE_DIR=<новая папка>`, затем запускает
`:plugin-backend:test --tests '*DemoMutationCorpusTest'` по инструкции сборки
плагина. Используйте опубликованный workspace без изменения retry annotation,
если проверяете именно описанную известную проблему.
