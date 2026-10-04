# Проверочный проект ArchVerity

В публичном наборе это основной архитектурный workspace. Начните с
[полного walkthrough](../../docs/ARCHITECTURE_WALKTHROUGH_RU.md) и
[каталога функций](../../docs/FEATURE_CATALOG.md). Здесь сохранены существующие
QA-входы и добавлены HTTP/Jackson/Kafka/AMQP примеры и 19 мутаций. Для настоящих
Metro/Expo/native команд используйте соседний `mobile-lab`, для WebSocket/gRPC —
`api-lab`, для Actuator/verification evidence — `runtime-evidence`.

Это небольшой Gradle-проект с четырьмя сервисами и отдельными входными файлами для инструментов ArchVerity. Его цель — проверять результат действий в интерфейсе, а не только наличие кнопок. Исходники, сертификат и иконки здесь синтетические. Никакого рабочего сервера, облачной учётной записи или закрытого ключа проект не требует.

**Матрица точек входа:** `QA_MATRIX_RU.md`. Она перечисляет зарегистрированные 15 экранов, 6 действий, 22 команды процессов, 7 команд отладчика, 6 экспортов, 4 MCP-инструмента, 5 страниц настроек и 22 editor extension. Из 22 process-команд здесь есть пригодные локальные входы для шести; остальные 16 требуют указанной внешней среды. `qa-support/verify_coverage.py` сверяет список с текущими исходниками плагина, проверяет тип локального входа и не засчитывает фиктивный `package.json` как Android/iOS/ADB приложение. В переносимой ZIP-копии сверка с исходниками пропускается. Запись в матрице не означает, что функция отработала в IDEA.

## Быстрый запуск

Нужны IntelliJ IDEA с проверяемой версией ArchVerity, JDK 21 как **Gradle JVM**, Python 3 и Git. Для проверки запуска React Native script дополнительно нужны Node.js и npm. Первый Gradle build загружает зависимости из Maven Central.

В PowerShell из этой папки:

```powershell
python -B -X utf8 qa-support/preflight.py
python -B -X utf8 qa-support/verify_coverage.py
python -B -X utf8 -m unittest discover -s qa-support -p test_verify_coverage.py
.\gradlew.bat classes
python -B -X utf8 qa-support/prepare_impact.py --output D:\CodexData\Temp\archverity-sample-check
```

Последняя команда создаёт **новую чистую** Git-копию и откажется перезаписать существующую. Откройте именно `D:\CodexData\Temp\archverity-sample-check` в IDEA как Gradle-проект, дождитесь импорта и индексации. Если IDEA сообщает `Invalid Gradle JDK configuration`, назначьте установленный JDK 21 в Gradle settings и повторите импорт. Откройте ArchVerity → Workspace → **Analyze project** на **чистой** версии: Impact должен показать отсутствие изменений. Это создаёт точный снимок коммита `HEAD` в `.idea/archflow/commits/`.

При запуске внутри полного дерева исходников плагина добавьте `--require-source` к `verify_coverage.py`: тогда любое расхождение с зарегистрированными entry points завершит проверку ошибкой. В переносимой копии этот source-check недоступен и явно помечается как пропущенный.

Затем в терминале созданной копии выполните:

```powershell
python -B -X utf8 qa-support/apply_impact.py --project . --scenario combined-breaking
```

Скрипт откажется работать без полного снимка чистого `HEAD`. Он меняет ровно один файл: метод провайдера `POST → PUT`, добавляет обязательный параметр запроса `mandatoryRiskToken` и удаляет обязательное поле ответа `providerReference`. Дождитесь обновления файла в IDEA; если интерфейс всё ещё показывает отсутствие изменений, выполните синхронизацию файлов проекта в IDEA. Повторите **Analyze project**, затем в Impact сравните `HEAD → WORKTREE`.

Для отдельной проверки метода, request/response DTO, добавления необязательного поля, Kafka topic, Spring profile и OpenAPI/AsyncAPI/Backstage manifests создавайте новую чистую копию и передавайте другое имя `--scenario`; полный список выводит `python qa-support/apply_impact.py --help`. Сценарий `manifest-missing` должен дать явную диагностику. Исходные `qa-openapi.json`, `qa-asyncapi.json`, `qa-backstage.json` и три готовых файла в `contracts/` позволяют повторить импорт отдельно через `archflow-tools`.

Для `combined-breaking` проверяйте конкретные изменения: несовместимость HTTP-метода, обязательного request-поля и удалённого response-поля. В таблице `PaymentResponse` удалённое поле должно отличаться от неизменённых; карта и рекомендации должны открывать соответствующие исходники. Число результатов зависит от версии анализатора и добавленных связей расширенного workspace, поэтому оно не служит критерием приёмки. Если запуск показывает только `Unknown`, проверьте полный снимок `HEAD`, состояние индексации и данные экспорта Change impact JSON; частичный анализ не подтверждает Breaking. Подробные ожидания для всех 19 сценариев приведены в [walkthrough](../../docs/ARCHITECTURE_WALKTHROUGH_RU.md).

## Что проверить в интерфейсе

| Раздел | Вход и наблюдаемый результат |
| --- | --- |
| Workspace | Три действия ведут в Impact, API Client и Spring configuration; меню открывает все разделы, назад/вперёд возвращают предыдущий экран. |
| Impact | Чистый `HEAD`, затем `POST → PUT`, обязательный токен и удалённое поле ответа; Breaking/Safe/Unknown, «Было/Стало», `Compatible`/`Incompatible`, три потребителя на карте, ссылки к четырём исходникам и Evidence. |
| Inventory | HTTP-фильтр сокращает список; элемент открывает исходный файл. |
| Topology | Выбор узла показывает детали; сброс фокуса возвращает весь граф. |
| Relations | Связь между HTTP-производителем и потребителями открывает исходники. |
| Diagnostics | Список открывается и показывает фактическое число диагностик; ноль для исправного образца допустим. |
| Spring configuration | Inspect находит `application.yml` и `application-dev.yml`; фильтр профиля `dev` меняет список ключей. |
| MyBatis SQL | Из двух строк в `MyBatisConsoleFixture.java` восстанавливается SQL с `payments`, `id = 42` и экранированным `O'Reilly`. |
| Ansible | Сканируются playbook, inventory и `ansible/professional`; строка результата ведёт к исходнику. |
| Shell and Bats | `shell-professional/lib/common.sh` проходит ShellCheck и показывает ожидаемый shfmt diff; `test/deploy.bats` содержит два проходящих теста; `qa-debug.sh` подходит для локального и подготовленного удалённого Bash debugger. Extensionless `bin/deploy` предназначен для навигации в редакторе. Запуск требует Bash/Bats в среде, где они доступны. |
| API Client | Запустите локальный API ниже. Импортируйте `qa-api.http`, `qa-openapi.json`, `qa-postman.json`, `qa-curl.txt`, отправьте запрос и проверьте HTTP 200 и тело ответа. `qa-slow.http` даёт пять секунд для проверки Cancel. |
| React Native | `rn-qa/package.json` обнаруживается; `qa:verify` действительно выполняет Node script и пишет `rn-qa/work/qa-script-result.txt`. Это проверка консоли скриптов, не сборка мобильного приложения. |
| ANSI logs | Откройте `ansible/qa.ansi` или `archflow-live.ansi`; цветные участки должны отображаться в просмотрщике. |
| Dev Icons | `archverity-qa.aficons` содержит 63 SVG, manifest и rules с отдельным ID: первый импорт добавляет пакет в настройки. `archflow-studio.aficons` проверяет встроенный стиль. Повторный импорт того же ID проверяет замену. |
| Keystore and X.509 | `qa-cert.pem` и `qa-cert.der` — один синтетический сертификат в двух форматах; `qa-public-artifacts.pem` содержит другой сертификат и подписанный им CRL с одной записью, `qa-request.csr` и `qa-public-key.pem` относятся к нему. `qa-truststore.p12` содержит только первый сертификат как `trustedCertEntry`; тестовый пароль — `archverity-qa-only`. Закрытых ключей в образце нет. |

API Client использует отдельный локальный процесс. Запустите его в терминале из созданной копии и оставьте открытым на время проверки:

```powershell
python -B -X utf8 qa-support/local_api.py
```

Адрес — `http://127.0.0.1:18427`. `GET /health` и `GET /qa-openapi` возвращают 200; `POST /qa-roundtrip` и `POST /qa-postman` отражают JSON; неизвестный путь возвращает 404. `GET /qa-slow?delay_ms=5000` возвращает 200 через пять секунд и предназначен для Cancel; задержка ограничена 0–5000 мс. Сервер слушает только `127.0.0.1` и ограничивает размер тела 32 КиБ. Preflight запускает временный сервер на случайном порту и проверяет обычные и ошибочные пути автоматически.

Для проверки **замены** уже установленного пакета сначала импортируйте `archverity-qa.aficons`, затем из созданной копии выполните:

```powershell
python -B -X utf8 qa-support/generate_icon_pack.py --version 2 --accent '#D946EF' --output work/archverity-qa-v2.aficons
```

Импортируйте `work/archverity-qa-v2.aficons` и подтвердите Replace. Результат проверяйте по версии `2` в импортированном пакете и изменённому цвету `icons/ansible.svg`, а не только по числу строк в списке: ранее старый пакет мог оставаться в списке после неудачной замены.

`preflight.py` проверяет файлы и форматы, 19 изолированных сценариев, три внешних manifest, эквивалентность PEM/DER, публичное хранилище через `keytool` при его наличии, пакет иконок, цикл HTTP включая 400/404/413 и Node script при наличии Node.js. Если доступен пакет Python `cryptography`, он дополнительно проверяет подписи CSR/CRL и соответствие публичного ключа; отсутствие пакета явно отражается в результате. `gradlew classes` доказывает, что Java/Kotlin-исходники проекта компилируются. Эти проверки **не доказывают работу кнопок IDEA**: для этого нужно пройти `QA_MATRIX_RU.md` в запущенном плагине. Отдельной средовой проверки требуют внешние Bash/Bats/Ansible, Android/iOS, SSH, MCP Server и реальные состояния Marketplace-лицензии.

Чтобы передать исходный образец без кешей IDEA/Gradle и результатов запуска, выполните `python -B -X utf8 qa-support/package_sample.py --output D:\CodexData\ArchFlow\deliverables\archverity-sample-workspace.zip`. Упаковщик проверяет ZIP и не перезаписывает существующий файл. После распаковки выполните `prepare_impact.py` уже из распакованной папки: ZIP содержит исходную версию, а не заранее изменённую рабочую копию.
