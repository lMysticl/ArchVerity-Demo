# ArchVerity 5.8.2: 19 MCP-инструментов на одном проекте

[Маршрут продукта](PRODUCT_TOUR_RU.md) · [Средовые проверки](ENVIRONMENT_CHECKS_RU.md) ·
[Точки входа](ENTRY_POINTS_RU.md) · [Запись результата](RUN_RECORD.md)

Нужны современная совместимая IDEA с JetBrains MCP Server, ArchVerity 5.8.2,
активный Trial/Pro и ваш агент. Legacy-пакет для IDEA 2024.3 не предоставляет
этот MCP-маршрут. Подготовьте отдельную `workspace`-копию, импортируйте Gradle,
отсканируйте чистый HEAD. В **Agents** настройте выбранного клиента и проверьте
соединение. Агентский аккаунт, доступ к исходникам и лимиты оплачиваются/выдаются
отдельно. Таблица описывает отдельные вызовы, а не один aggregate API.

## Перед правкой, после правки и после исправления

1. Вызовите `archverity_capabilities` с `{}`. Убедитесь, что клиент видит
   возможности выбранного проекта и правильную версию/границы, затем
   `archverity_file_contracts` с
   `{"path":"payment-app/src/main/java/sample/payment/PaymentController.java","limit":10,"project_root":"<полный путь подготовленного проекта>"}`.
   Подставьте реальный путь; placeholder не является аргументом для запуска.
2. До записи файлов вызовите `archverity_simulate_change` с этим планом:

```json
{
  "edits_json": "[{\"path\":\"payment-app/src/main/java/sample/payment/PaymentController.java\",\"old\":\"@PostMapping(\\\"/{paymentId}\\\")\",\"new\":\"@PutMapping(\\\"/{paymentId}\\\")\"}]",
  "limit": 10,
  "offset": 0,
  "project_root": "<тот же полный путь>"
}
```

   `edits_json` — строка со строгим JSON array объектов `{path,old,new}`. Допускается
   до 20 замен Java/Kotlin, применяемых по порядку, и до 1 MiB JSON. На каждом
   шаге `old` должен встретиться ровно один раз после предыдущих замен того же
   файла. Путь относится к выбранному проекту. `limit` ограничивает вывод
   breaking/unproven пунктов (1–100), а не количество запланированных замен.
   Если ответ содержит `nextOffset`, продолжите чтение с этим `offset`, тем же
   планом и `project_root`; ограниченный ответ не является полным результатом.
   Изучите simulated-ответ, affected consumer и предложения; `git diff` исходников
   должен оставаться пустым. Симуляция не пишет исходники и не выдаёт commit trailer.
3. В этой же свежей копии после полного HEAD scan примените `http-method` из
   `qa-support/apply_impact.py`. Выполните подходящие тесты, затем вызовите
   `archverity_check_change` с
   `{"base_revision":"HEAD","from_merge_base":false,"limit":10,"project_root":"<тот же полный путь>"}`.
   Сверьте affected consumers и source locations с **Changes → Details** в IDEA.
   Фактический diff и intended plan должны описывать одну и ту же правку.
4. Запросите `archverity_test_plan` для HEAD. Он должен объяснить контроли,
   но `NOT_EXECUTED` не означает, что тест уже запущен. Выполните подходящий
   тест отдельно, исправьте контракт, сохраните и снова вызовите check_change.
5. Контроль маршрутизации: неверный `project_root` должен дать ошибку, а не
   результат соседнего проекта. После ещё одной правки старый commit receipt
   не подтверждает новое дерево. Пустой список контрактов не доказывает безопасность.

## Все инструменты и наблюдения

`limit: 10` ниже — небольшой бюджет для показа. Динамические IDs и identities
берутся из текущего ответа или UI; их нельзя заменять выдуманными строками.

| Инструмент | Конкретный вход / действие | Что проверять |
| --- | --- | --- |
| `archverity_capabilities` | `{}` | Реальные возможности и ограничения текущего bridge |
| `archverity_file_contracts` | Путь PaymentController.java выше | Контракты файла, другая сторона, текущий pair verdict |
| `archverity_simulate_change` | `edits_json` из примера выше, тот же `project_root` | До 20 ordered replacements в памяти; проверить источник break/Needs review, отсутствие исходного diff и commit trailer |
| `archverity_check_change` | HEAD, `from_merge_base:false`, фактический `project_root` | Решение для текущего дерева; новый receipt только для допустимого сохранённого состояния |
| `archverity_change_impact` | `{"base_revision":"HEAD","limit":10}` | Прямые HTTP/Kafka/AMQP/DTO последствия отдельно от downstream REVIEW |
| `archverity_findings` | `{"severity":"ERROR","include_suppressed":false,"limit":10}` | Фильтр и source locations совпадают с Problems |
| `archverity_contract_evidence` | `{"query":"payments","limit":10}` | Источник доказанной связи и её ограничения |
| `archverity_trace_flow` | `{"query":"payment-service","direction":"both","max_depth":3,"limit":10}` | Технический путь; повторить inbound/outbound, не придумывать бизнес-смысл |
| `archverity_explain_flow` | Те же query/direction/depth + `base_revision:"HEAD"` | Текущая inputIdentity; повторить с previous_identity после изменения контракта |
| `archverity_architecture_diagram` | Query `payment-service`, depth 3, limit 10 | Mermaid и структурированные узлы/связи относятся к тому же bounded flow; truncated не выдаётся за complete |
| `archverity_test_plan` | `{"base_revision":"HEAD","from_merge_base":false,"limit":10}` | Положительные и отрицательные проверки; статус выполнения остаётся честным |
| `archverity_kafka_migration_plan` | В свежей копии `kafka-topic`, затем `{"base_revision":"HEAD","limit":10}` | Порядок шагов, неизвестные deployment/schema факты; план ничего не разворачивает |
| `archverity_preview_rule` | `{"policy_id":"demo-no-payments","from_services":["order-service"],"to_services":["payment-service"],"protocol":"HTTP","mode":"deny","limit":10}` | YAML/наблюдаемые пути; `.archflow.yml` не меняется автоматически |
| `archverity_settings` | `{}` | Whitelisted settings и текущая inputIdentity, без секретных значений |
| `archverity_preview_settings` | identity из предыдущего вызова, `proposal_json:"{\"analysis\":{\"profiles\":[\"default\"]}}"` | Локальное preview; Apply/Undo только через явное действие Settings Assistant в IDE |
| `archverity_config_usage` | `{"query":"spring.application.name","limit":10}` | Объявления и явные usages без значений; UNUSED не означает, что настройку можно удалить |
| `archverity_context` | `kind:"NODE"`, selector — реальный ID `payment-service` из выбранного узла | Тот же выбранный объект, locations и identity; CONFIG проверяется отдельно по ключу |
| `archverity_prepare_review` | `{"scope":"CHANGES","base_revision":"HEAD","from_merge_base":false,"limit":10}` | Session/identity, manifest и реальные границы покрытия выбранного review method |
| `archverity_submit_review` | Текущий prepared session; strict protocol batch от подключённого агента | Только локальное review-state, реальные coverage/anchors; PARTIAL при неполном покрытии, отказ для stale identity |

## Контроль качества bridge

- Для simulation проверьте отсутствующий/неоднозначный `old`, более 20 edits и
  путь вне выбранного проекта: нужен явный отказ. Конфигурация всего модуля и
  неподдержанные объявления дают Needs review; после реальной правки нужен
  отдельный check_change.
- Передавайте пустой обязательный query, неверный severity/direction и
  неподходящую Git revision: нужна явная ошибка, не правдоподобный чужой ответ.
- Для preview_settings измените вход после preview: устаревшая identity должна
  быть отклонена. Изучите preview и отмените его; не применяйте настройки
  к рабочему проекту ради показа.
- Review prepare/submit — отдельный агентский протокол. Для успешного прогона
  используйте поддержанный клиент и фактически обработанные им manifest pages.
  Не отправляйте выдуманный COMPLETE. Невалидный `report_json` должен отклоняться.
- Структурированное evidence не равно передаче исходников. Собственный агент
  может читать файлы согласно своим разрешениям. `project_root`/projectRoot
  служит явной привязкой; прочие locations проверяйте как относительные.
- При недоступном MCP Server, агенте или entitlement запишите точную причину.
  Локальные HTTP, upgrade и wire-проверки остаются самостоятельными маршрутами.
