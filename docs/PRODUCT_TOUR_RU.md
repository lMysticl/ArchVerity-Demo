# ArchVerity 5.8.2: от проблемы до проверенного исправления

Цель демонстрации — ответить на вопрос: **какой соседний сервис перестанет
работать после моего изменения и что проверить до merge?** Сборка отдельного
сервиса этого не доказывает. Здесь вы увидите обе стороны контракта, измените
конкретный вход и сравните результат до и после исправления.

[English](PRODUCT_TOUR_EN.md) · [Запуск всех лабораторий](DEMO_RUNBOOK_RU.md) ·
[Каталог функций](FEATURE_CATALOG.md) · [Запись своего результата](RUN_RECORD.md) ·
[Если вы смотрите старое видео](#как-читать-старые-записи)

## Начните с одного результата

Нужны Git, Python 3.10+, JDK 21, совместимая IDEA и отдельно установленный
[ArchVerity](https://plugins.jetbrains.com/plugin/34234-archverity) **5.8.2**
с активным Trial/Pro. В Marketplace доступен 14-дневный trial. Первое получение
Gradle/Maven-зависимостей требует сети; HTTP/Kafka-примеры не требуют серверов.
MCP-маршрут требует современную сборку с JetBrains MCP Server и вашего агента.

Из корня набора:

```powershell
python -B -X utf8 suite-support/check_suite.py
python -B -X utf8 suite-support/prepare_project.py --project first-result --output ../archverity-first-demo
```

Откройте **созданную папку**, импортируйте Gradle с JDK 21 и дождитесь индексации.
В её терминале выполните `.\gradlew.bat classes` (Linux/macOS: `./gradlew classes`).

1. **Увидеть проблему.** Откройте **Map → Analyze Project**, дождитесь анализа
   и перейдите в **Problems**. Найдите HTTP method mismatch `AFG-HTTP-001`: клиент
   `PaymentClient.java` вызывает POST, а `PaymentController.java` принимает PUT.
2. **Проверить основание.** Откройте обе стороны из результата или через Navigate
   → File. Сравните метод и `/payments/{paymentId}`. Сборка проходит, но это
   не делает два HTTP-контракта совместимыми.
3. **Исправить и повторить.** В клиенте замените `@PostMapping` на `@PutMapping`.
   Сохраните, обновите анализ. Должен исчезнуть именно этот method mismatch.
   Верните POST и пересканируйте: тот же finding должен появиться снова.

Критерий успеха — воспроизводимая смена **этого** результата, доступность обеих
исходных точек и понятная причина. Другие сообщения не нужно скрывать ради
«зелёного» экрана. Если finding отсутствует изначально, проверьте импорт обоих
модулей, корневую `.archflow.yml`, scope и лицензию.

## Увидеть последствия до правки

Из корня набора подготовьте полную рабочую модель:

```powershell
python -B -X utf8 suite-support/prepare_project.py --project workspace --output ../archverity-review-demo
```

Импортируйте эту папку и отсканируйте чистый HEAD через **Map → Analyze Project**.
В **Map** посмотрите контракты, а в **Problems** — существующие несовместимости
и связи, где потребитель не найден.
Откройте исходник каждой выбранной записи. Отсутствующий потребитель ограничивает
вывод; его нельзя считать подтверждением совместимости.

В `payment-app/src/main/java/sample/payment/PaymentController.java` поставьте
курсор на поле `providerReference` или Spring mapping. Через Find Action
вызовите **ArchVerity: What Breaks If This Changes?**. Посмотрите предложенные
варианты, затронутого потребителя, основание и рекомендуемый шаг. Затем выполните
`git diff`: исходники должны оставаться неизменными. Повторите на Java Kafka
`send` в `order-app/.../OrderPublisher.java`. Этот конкретный маршрут использует
Java; в 5.8 поддержаны также ограниченные Kotlin-формы. Изменения конфигурации
всего модуля и неподдержанные конструкции требуют фактической правки и новой проверки.

## Проверить реальное изменение и применить исправление

В терминале **подготовленной workspace-копии**, после полного анализа чистого HEAD:

```powershell
python -B -X utf8 qa-support/apply_impact.py --project . --scenario http-method
```

В **Changes → Summary** выберите **HEAD → Current files** и нажмите
**Check Changes** или **Check Again**. В **Details** откройте обе стороны.
POST провайдера стал PUT, а вызывающий контракт остался старым. Откройте
затронутого клиента и провайдера, затем доступное **Apply fix** и его описание.
Примените согласованное исправление в этой демо-копии и проверьте ещё раз:
конкретный разрыв должен исчезнуть. Проверьте `git diff` — важно понимать,
что именно исправлено и соответствует ли это намерению владельца API.

Для каждого следующего случая создавайте свежую копию и сканируйте её HEAD:

| Сценарий | Что вы оцениваете |
| --- | --- |
| `request-required` | Новый обязательный `mandatoryRiskToken` у провайдера и клиент, который его не посылает |
| `kafka-topic` | Publisher переезжает с `orders.created` на `orders.revised`, listener остаётся |
| `response-optional-added` | Контроль совместимого изменения: добавление необязательного поля не должно называться доказанным разрывом |
| `manifest-missing` | Контроль недостающего evidence: явный UNKNOWN с причиной |
| `combined-breaking` | Один diff меняет метод, обязательное поле запроса и поле ответа; частичное исправление не должно скрыть оставшуюся проблему |

Полный набор из 19 изменений, включая вложенные DTO, AMQP и scope, находится
в [архитектурном walkthrough](ARCHITECTURE_WALKTHROUGH_RU.md).
Downstream REVIEW — повод изучить последствие; он отличается от доказанного
прямого BREAKING. Не обещайте автоматическое исправление каждого типа изменения.
[Текущая проверка и сохранённая история](CURRENT_VERIFICATION_RU.md) различают
прошедший workspace-корпус 5.8.2 и старое ограничение retry listener из 5.3.2.
Исторический FAIL сохраняет свою версию. В своём прогоне проверьте конкретный
finding и записанное исправление; результат корпуса не обещает auto-fix любого listener.

## Переход на Spring Boot 4

```powershell
python -B -X utf8 suite-support/prepare_project.py --project boot-upgrade --output ../archverity-upgrade-demo
```

Откройте новую копию. После полного анализа выберите **Check Spring Boot 4 upgrade**.
В примере orders → billing проверьте `status`, `period`, `quantity` и `discount`:
enum с `toString()`, Month, nullable writer → primitive reader и отсутствующий
primitive-компонент record. Это риск обновления при неизменённых API-исходниках.

[Лаборатория](../projects/boot-upgrade/README.md) даёт точные команды для запуска
настоящих мапперов Boot 3.5.15 и 4.1.1, явного исправления и повторной проверки.
Она также содержит `mapper-unknown`: настройка маппера должна убрать
необоснованную уверенность. Не выдавайте этот HTTP-сценарий за проверку всех
Kafka-сериализаторов или всех изменений Spring Boot.

## Проверить обычный Boot Kafka

[Новая Kafka-лаборатория](../projects/kafka-boot-lab/README.md) показывает
доказательство source/configuration для Boot 3.5 и 4.0. Из корня набора:

```powershell
python -B -X utf8 suite-support/prepare_boot_kafka_case.py --boot-line 35 --case remove-required --output ../archverity-boot-kafka-demo
```

Для Boot 4 создайте другой новый output с `--boot-line 40`. Импортируйте оба
модуля с JDK 21, дождитесь индексации и выполните `.\gradlew.bat classes`
(Linux/macOS: `./gradlew classes`). Брокер не запускается.

В **Changes → Summary** сравните зафиксированный HEAD этой копии с текущими
файлами. После **Check Changes** в **Details** проверьте producer/consumer DTO,
типизированный template, listener и свойства JSON serializer/deserializer.
В `remove-required` producer больше не передаёт обязательный для reader `tenant`.
Восстановите точный producer `Event.java` из HEAD, повторите compile и
**Check Again** с тем же base: именно этот разрыв должен исчезнуть.

Для `add-optional`, `customizer-control` и `historical-reader` создавайте
отдельные копии. Первый отделяет добавочное поле от разрыва, второй сохраняет
**Needs review** с названной customization, третий показывает старую producer-форму
из Git base при совпадающей текущей паре. Пути и восстановление даны в lab README.
Git base не доказывает retained records, доставку или версию в production.
Старые K01–K12 проверяют profiles/scopes отдельно; старый экспорт не является
свежим подтверждением этого Boot-маршрута.

## Передать результат команде

1. После полного скана в **Problems** используйте **Copy for my team**. Прочитайте Markdown: сервисы,
   зависимости, риски обновления, относительные пути и ограничения должны
   соответствовать открытому проекту. Это первый полезный артефакт trial.
2. В **Changes → Export review** скопируйте/сохраните Markdown выбранного
   сравнения; JSON доступен через **More actions → Copy or save JSON…**.
   Сверьте base revision и текущий diff. Старый экспорт не подтверждает новую правку.
3. Если нужен общий реестр, подготовьте отдельный локальный Git-репозиторий
   реестра и используйте **Publish contracts to team registry…** из Export JSON.
   Проверьте preview, затем локальный diff реестра. Плагин не делает commit/push
   за вас. Исходники соседнего сервиса не нужно подменять выдуманным контрактом.
4. Для командного gate в одноразовой копии используйте Export review →
   **Add commit receipt check to CI…**. Сначала изучите preview и созданный
   `.archverity/receipt_check.py --help`; выполните показанную самой IDE команду.
   Квитанция должна относиться к проверенному дереву. Контроль: новое изменение
   после проверки не должно приниматься как проверенное. Это проверка записи
   результата, а не новый анализ исходников в CI и не криптографическая подпись.

## Подключить своего AI-агента

В **Agents** откройте подключение выбранного поддержанного клиента и выполните
проверку соединения. Приложение агента, аккаунт и лимиты предоставляете вы.
В [MCP-маршруте](MCP_TOUR_RU.md) приведены все 19 инструментов 5.8.2 и контроли.
Начните с такого задания:

> Перед изменением PaymentController.java вызови archverity_file_contracts для
> этого файла. Назови затронутые сервисы и ограничения evidence. Вызови
> archverity_simulate_change с точными планируемыми правками до записи файлов.
> После фактической правки и тестов проверь HEAD через archverity_check_change
> для этой же папки проекта. Симуляция не является commit receipt.
> Не считай UNKNOWN или NOT_EXECUTED подтверждением успешной проверки.

Связка полезна, когда агент меняет один сервис, а контракт принадлежит двум.
Review от модели и детерминированный результат ArchVerity проверяются отдельно.

## Продолжить по своей работе

| Ваша задача | Следующий конкретный вход |
| --- | --- |
| Обычный Boot 3.5/4 Kafka, required поле, исправление и старые producer-формы | [Boot Kafka lab](../projects/kafka-boot-lab/README.md) |
| Kafka profiles, clusters, serializer uncertainty | [12 случаев и проверка настоящего export](../projects/kafka-profile-lab/README.md) |
| API-запросы, cookies, captures, assertions, WebSocket/gRPC | [Локальные серверы API lab](../projects/api-lab/README.md) |
| Runtime beans и результаты выполненной проверки | [Runtime evidence](../projects/runtime-evidence/README.md) |
| Spring config, MyBatis SQL, Ansible, Shell/Bats, ANSI, icons, certificates | [Подробные функциональные рецепты](ALL_FUNCTIONS_RU.md) через вкладку Tools |
| React Native / Expo и команды устройств | [Mobile lab](../projects/mobile-lab/README.md), отдельные SDK/device prerequisites |

Во время trial повторите подход на одном своём изменении: найдите реального
потребителя, подтвердите проблему или честную границу знания, получите проверку
после исправления и пригодный для коллег отчёт. Если этот ответ нужен регулярно
при изменениях API и схем, вы оцениваете именно повторяемую пользу продукта.
Не принимайте решение по количеству пунктов меню или одному зелёному скриншоту.

## Как читать старые записи

Ролик Petclinic записан на 5.0, а первые HTTP/Kafka-статьи и видео — на 3.0.4.
В 5.8.2 основные вкладки — **Changes, Map, Problems, Agents и Tools**.
В **Changes** есть **Summary** (ответ) и **Details** (контракты и обе исходные точки).
Для названий в старой записи используйте карту:

| Старое название | Где искать в 5.8.2 |
| --- | --- |
| Overview | Changes → Summary; существующие проблемы всего проекта — Problems |
| Review / Impact | Changes → Summary / Details |
| Diagnostics / Findings | Problems |
| Architecture / Topology | Map |
| Inventory / Relations | Map → Inventory / Relations |

Вердикты тоже зависят от версии анализатора. Исторический `UNKNOWN` не задаёт
ожидаемый ответ текущего прогона: перенос HTTP-маршрута при доказанном
затронутом клиенте может дать `BREAKING`. В измеренном на 5.3.2 сценарии
[`extra-http-path`](evidence/engine-5.3.2-20261023/shipped-workspace.txt) получен
`BREAKING`; после сохранения старого маршрута доказанные разрывы исчезают,
а результат становится `REVIEW REQUIRED`. При недостатке фактов остаётся
`UNKNOWN`. Сравнивайте конкретные входы и evidence по
[текущему отчёту проверки](CURRENT_VERIFICATION_RU.md).
