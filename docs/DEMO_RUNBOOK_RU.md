# Запуск демонстрации ArchVerity: пошаговая инструкция

Этот маршрут предназначен для первого знакомства, показа плагина и повторяемого
QA на открытых исходниках. Набор описывает функции ArchVerity **3.0.3**:
[62 функции](ALL_FUNCTIONS_RU.md), [87 точек входа](ENTRY_POINTS_RU.md),
41 прежний capability recipe и 19 отдельных изменений для Impact.
Выберите нужный этап; архитектурные примеры и сетевые лаборатории запускаются
по своим инструкциям ниже. [Оглавление всей документации](README.md).

## 1. Подготовить среду и получить проекты

| Что нужно | Для какого этапа | Как проверить |
| --- | --- | --- |
| Git | Получение исходников и самостоятельный Git baseline | `git --version` |
| Python 3.10+ | Проверки набора, подготовка копий, локальные API | `python --version`; hosted CI использует 3.12 |
| JDK 21 | Gradle import/build трёх JVM-проектов | `java -version`; в IDEA отдельно выбрать Gradle JVM 21 |
| Совместимая IDEA и установленный ArchVerity 3.0.3 | Действия плагина | Settings → Plugins → ArchVerity; записать version/build |
| Настоящий Trial/Pro для соответствующих операций | Impact, paid tools/export/MCP | Записать фактически видимое состояние лицензии |
| Node 22 | Metro/Expo/JavaScript bundle | `node --version`, `npm --version`; native device пока не нужен |
| Сеть для первого download | Gradle/npm/pinned Python packages | Установка завершается с exit code 0 |

Установите плагин отдельно из [JetBrains Marketplace](https://plugins.jetbrains.com/plugin/34234-archverity),
используя IDEA, поддерживаемую именно выбранной сборкой. Публичный репозиторий
содержит примеры и инструкции; версию установленного плагина фиксируйте отдельно.
Для статического HTTP/Kafka/AMQP анализа Kafka, RabbitMQ, БД и Docker не нужны.

Если репозитория ещё нет, выполните в своей папке для проектов:

```powershell
git clone https://github.com/lMysticl/ArchVerity-Demo.git
cd ArchVerity-Demo
python -B -X utf8 suite-support/check_suite.py
```

Если clone уже есть, откройте его корень и выполните только проверку набора.
Проверка должна сообщить `INPUT_CONTRACT_PASS`, `functions=62`, `entry_points=87`.
Перед обновлением существующего clone просмотрите `git status`; локальные
изменения сохраняйте своим обычным Git-процессом.

Все команды `suite-support/...` выполняются из корня **ArchVerity-Demo**.
Пути `D:/CodexData/Temp/...` ниже — примеры новых выходных каталогов на Windows;
на Linux/macOS задайте путь своей рабочей папки. Выход не должен существовать:
helper откажется его перезаписывать. Для нового прогона выберите новый путь.
Оригинальные исходники набора сохраняются для следующих демонстраций.

## 2. Первый finding и его исправление

Из корня набора создайте отдельный проект:

```powershell
python -B -X utf8 suite-support/prepare_project.py --project first-result --output D:/CodexData/Temp/archverity-first-demo
```

1. Откройте **созданную папку** в IDEA как Gradle-проект. Выберите JDK 21 как
   Gradle JVM; дождитесь окончания import и indexing.
2. В терминале созданной папки выполните `./gradlew classes`; на Windows —
   `.\gradlew.bat classes`. Оба модуля должны компилироваться.
3. View → Tool Windows → ArchVerity → Analyze. В Findings найдите
   HTTP method mismatch, rule `AFG-HTTP-001`.
4. Откройте обе стороны: `order-app/src/main/java/demo/orders/PaymentClient.java`
   и `payment-app/src/main/java/demo/payments/PaymentController.java`.
   Клиент объявляет POST, provider принимает PUT.
5. В клиенте замените только `@PostMapping` на `@PutMapping`, сохраните файл и
   повторите Analyze. Именно этот method mismatch должен исчезнуть.

Для обратной проверки верните `@PostMapping` и повторите Analyze: тот же finding
должен вернуться. Отдельно запишите build result и наблюдение анализатора.
Если finding отсутствует изначально, проверьте import обоих модулей,
полный scope, `.archflow.yml` и alias `payments.example.test`.
[Подробности и исходные пути](../projects/first-result/README.md).

## 3. Архитектура, Impact и инструменты редактора

Вернитесь в корень набора и создайте **новую** копию:

```powershell
python -B -X utf8 suite-support/prepare_project.py --project workspace --output D:/CodexData/Temp/archverity-impact-demo
```

Откройте этот output как Gradle project, выполните import/build с JDK 21 и
Analyze на чистом HEAD. Убедитесь в complete scan; сохранённый полный HEAD
snapshot нужен для сравнения. Findings исходного образца допустимы; чистое
HEAD → WORKTREE сравнение должно показывать отсутствие изменений.

Из **терминала созданной копии** выполните:

```powershell
python -B -X utf8 qa-support/apply_impact.py --project . --scenario combined-breaking
```

Повторите Analyze/Impact HEAD → WORKTREE. Проверьте изменение method,
обязательное поле запроса и удалённое поле ответа, Было/Стало, source links
обеих сторон и downstream REVIEW. Если полного HEAD snapshot нет, helper
откажется применять изменение: завершите исходный scan и повторите команду.
Не переносите baseline из соседнего проекта.

Для остальных 18 мутаций создавайте отдельную чистую копию и сканируйте её
HEAD до изменения. Имена и точные ожидаемые результаты перечислены в
[архитектурной инструкции](ARCHITECTURE_WALKTHROUGH_RU.md).
Для Spring/MyBatis/Ansible/Shell/ANSI/Dev Icons/Keystore используйте связанные
входы в [полном руководстве](ALL_FUNCTIONS_RU.md) и
[матрице workspace](../projects/workspace/QA_MATRIX_RU.md).
Все семь keystore-форматов и настоящий icon-rule submodule имеют отдельную
[инструкцию по входам](ICON_AND_KEYSTORE_INPUTS_RU.md).

## 4. Локальные HTTP, WebSocket и gRPC

В корне набора создайте Python environment. Windows:

```powershell
python -m venv work/api-venv
work/api-venv/Scripts/python.exe -m pip install -r projects/api-lab/requirements.txt
work/api-venv/Scripts/python.exe projects/api-lab/serve.py
```

Linux/macOS — те же входы, другой путь interpreter:

```bash
python3 -m venv work/api-venv
work/api-venv/bin/python -m pip install -r projects/api-lab/requirements.txt
work/api-venv/bin/python projects/api-lab/serve.py
```

У уже подготовленного environment выполните install/start по необходимости.
Дождитесь строки `READY` с тремя endpoints; терминал остаётся занят сервером.
Откройте в IDEA корень набора или workspace copy и выберите API:

| Действие | Вход | Ожидаемый результат |
| --- | --- | --- |
| HTTP Send | GET `http://127.0.0.1:18427/health` | Status 200 |
| HTTP roundtrip | POST `/qa-roundtrip`, JSON `{"id":42}` | `received.id=42` |
| Scenario | Вставить `projects/api-lab/scenarios/dsl-types.json` | Два последовательных шага, type/null/array/pointer assertions и capture ID=42 |
| Negative scenario | `wrong-json-type.json`, затем `missing-json-pointer.json` по отдельности | Первый шаг FAIL; второй запрос цепочки не отправлен |
| WebSocket | Connect `ws://127.0.0.1:18428`, Send `ArchVerity`, Close | Эхо и завершение выбранной сессии |
| gRPC | Load `projects/api-lab/schema/echo.pb`; target `http://127.0.0.1:18429`; `archverity.demo.Echo/Health`, `{}` | Unary response `text=ok`; imported Empty разрешён |

Для error, Cancel, Limits, cookies, environments, stream и остальных imports
следуйте [API README](../projects/api-lab/README.md). Пути входов в таблице
относятся к корню набора, даже если в IDEA открыт другой demo project.
Остановите свой сервер **Ctrl+C в терминале его запуска**. Если порт занят,
задайте другой через `--http-port`, `--websocket-port`, `--grpc-port` и измените
соответствующие URLs в запросах/scenario copy. Для HTTP-only достаточно
`python projects/api-lab/serve.py --protocol http`, без сторонних пакетов.

## 5. React Native / Expo

Из корня набора подготовьте отдельное приложение:

```powershell
python -B -X utf8 suite-support/prepare_project.py --project mobile-lab --output D:/CodexData/Temp/archverity-mobile-demo
```

В терминале **созданного output**:

```powershell
npm ci --ignore-scripts
npm run qa:verify
npm run bundle:android
```

Ожидайте `RN_SCRIPT_OK` в `work/qa-script-result.txt` и JavaScript bundle с
`ARCHVERITY_DEMO_CLICK`. В IDEA откройте этот output, React Native → Detect
projects, выберите его package.json и выполните RN_SCRIPT `qa:verify`.
RN_METRO и RN_EXPO проверяйте по очереди: ready → Stop → завершение своего
процесса/освобождение порта. Terminal `npm run start` останавливается Ctrl+C.

Native Android/iOS требуют prebuild и платформенной среды по
[мобильной инструкции](../projects/mobile-lab/README.md). Для ADB_RELOAD
ожидается **development menu**, затем оператор выбирает Reload; command
использует keyevent 82. SDK/device/macOS и разрешения на install/clear/uninstall
фиксируйте отдельно. JavaScript bundle проверяется без Android SDK/device.

## 6. Runtime beans и verification evidence

Из корня набора:

```powershell
python -B -X utf8 suite-support/prepare_project.py --project runtime-evidence --output D:/CodexData/Temp/archverity-runtime-demo
```

В терминале **созданного output** запустите `python run_local.py`; дождитесь
Spring Boot на `127.0.0.1:18430`. `/demo-identity` должен принадлежать HEAD/config
этой копии. Откройте ту же папку как Gradle project в IDEA, выполните текущий
полный scan и экспортируйте Analysis JSON в `work/analysis.json`.

В другом терминале **той же копии**:

```powershell
python capture.py --snapshot work/analysis.json --format pact
```

Reanalyze/import: actual bean bindings и локальный verification outcome должны
сохранить identity, hash, context и `LOCAL_FILE`. Runtime observation имеет
max age 300 seconds. Для FAIL и Drift нужны новые копии с их собственным
current export; команды и rejection controls — в
[runtime README](../projects/runtime-evidence/README.md).
Ctrl+C в launcher terminal останавливает его приложение. Smoke использует
явно synthetic producer-test input; реальный IDEA consumer run требует
настоящего current export из выбранной копии.

## 7. Kafka profiles и UNKNOWN

Этот дополнительный lab требует **ArchVerity 3.0.4** или новее; для локальной
IDEA 2024.3 используйте **3.0.4-2024.3**. Прежний Marketplace package 3.0.3
не содержит исправления Kafka profile/evidence. Оба новых обновления загружены
05.10.2026 и ожидают одобрения; см. [запись выпуска](VERIFICATION_RU.md#выпуск-304--05102026).
Подготовьте новую копию:

```powershell
python -B -X utf8 suite-support/prepare_kafka_case.py --case unknown-cluster-and-override --output E:/CodexData/Temp/archverity-kafka-K01
```

Откройте output как Gradle project, выберите JDK 21, дождитесь двух modules и
indexing, выполните Analyze. Одинаковые `orders.events` и bootstrap из blue/green
profiles должны дать два отдельных scopes и `009/010 UNKNOWN`. Evidence содержит
оба profile paths и missing `KAFKA_VALUE_SERIALIZER`, без доказанного контракта
из совпадения имени. Сохраните current full JSON и проверьте его checker из
[Kafka README](../projects/kafka-profile-lab/README.md).
Там даны все 12 recipes, положительные контроли и runtime rejection boundaries.
Для каждого нужен новый output; source commit и SHA-256 ZIP записываются отдельно
от номера версии. Брокер для static scan не нужен.

## 8. Полный обход функций и запись результата

1. Откройте [содержание 62 функций](ALL_FUNCTIONS_RU.md) и выберите ID.
2. Подготовьте указанный input/среду. Для конкретного control используйте
   [87 точек входа](ENTRY_POINTS_RU.md); выполните positive, counterexample,
   recovery и зафиксируйте каждое наблюдение.
3. Скопируйте [RUN_RECORD](RUN_RECORD.md) в `work/` своего проекта. Запишите
   demo commit, IDE/plugin version, project path/HEAD, license state,
   function/entry ID, expected/actual result и evidence path.
4. Отмечайте фактический `PASS`, `FAIL`, `NOT RUN` или `BLOCKED` с одной точной
   недоступной предпосылкой. Независимые сценарии продолжайте.

Tools, MCP Server, лицензии, SSH, Split Mode и private inputs имеют
[отдельные средовые инструкции](ENVIRONMENT_CHECKS_RU.md).
Логи/скриншоты/results храните в `work/`, без customer credentials и raw secrets.
В public Git остаются исходные примеры и документация.

## Если демонстрация остановилась

| Наблюдение | Что проверить и как продолжить |
| --- | --- |
| Output уже существует | Выбрать новый output; helper сохраняет старую копию |
| Finding отсутствует | Дождаться import/index, проверить оба module и `.archflow.yml`, повторить Analyze |
| Impact не готов | Получить complete snapshot чистого HEAD той же копии, затем применять мутацию |
| Transport не READY | Проверить pip environment, сообщение missing dependency и занятый port; сменить свой port/URLs |
| Mobile native command недоступен | Проверить native folders/SDK/device/macOS по mobile README; JS script/bundle проверить независимо |
| Evidence UNKNOWN | Проверить actual export, revision/config/context/spec hash, max age и выбранный launcher identity |
| Paid/remote/private case недоступен | Записать реальную отсутствующую предпосылку; продолжить независимые функции |

Список уже выполненных проверок — в [VERIFICATION_RU.md](VERIFICATION_RU.md).
Для воспроизведения автоматических checks используется
[CI workflow](../.github/workflows/checks.yml); его результат относится к
конкретному commit, а ручной IDEA/device run — к записанному проекту и версии.
