# Проверка набора 05.10.2026

Проверено на Windows, Python 3.12, Temurin JDK 21.0.12 и Node 22.23.2.
Это запись подготовки и локального исполнения демонстрационных проектов.
Она не является общим PASS для всех действий установленного плагина.

| Проверка | Непосредственное наблюдение |
| --- | --- |
| Registered-entry contract | 87 записей совпадают с descriptor/enums/MCP текущих исходников ArchVerity 3.0.2: 15 surfaces, 6 actions, 22 processes, 7 debugger commands, 6 exports, 4 MCP, 5 settings, 22 editor extension |
| Feature catalog | 41 capability recipe имеет существующий вход, действие, ожидаемое наблюдение и guide; все 19 мутаций имеют точные anchors в исходном baseline |
| first-result compile | Gradle classes: оба Java-модуля успешно компилируются с JDK 21 |
| workspace compile | Java/Kotlin classes, включая HTTP/Jackson/Kafka/AMQP расширения; deprecation/compiler checks включены |
| runtime-evidence compile/run | Gradle installDist и настоящий Spring Boot/Tomcat на loopback; реальный /actuator/beans и /payments/42 |
| Runtime producer cases | Pact-shaped PASS, Pact-shaped FAIL, Drift-shaped PASS от именованного локального HTTP verifier; реальные template/factory dependencies; canonical outcome/context/hash совпали с отдельно предоставленным Tools importer |
| Workspace preflight | 19 мутаций, 3 canonical manifests, HTTP 200/400/404/413, Node script, оба 63-icon пакета; certificate PEM/DER equality, CSR/CRL signatures и public-only trustedCertEntry |
| Coverage negative controls | 4 unittest: фиктивный bundle input, неправильный shell input и отсутствие внешней предпосылки отклоняются |
| API transports | 17 unittest с настоящими TCP HTTP/WebSocket/gRPC roundtrips, cookies/header, ordered stream, errors, byte bounds, deadline/cancel и descriptor imports |
| Mobile script/bundle | RN_SCRIPT_OK; React Native CLI создал Android JavaScript bundle 1 050 866 bytes с ARCHVERITY_DEMO_CLICK; SHA-256 6013199253f605141b8e6ef3e29bd43287586a138441f06473a6437dfe4cf73f |
| Metro / Expo lifecycle | Оба реальных loopback dev servers ответили packager-status:running; после остановки их собственных child processes порты перестали отвечать |

Мобильный lockfile фиксирует совместимые SDK 54 / RN 0.81.5 / CLI 20.0.2 и
Metro/metro-config 0.83.3 для Expo и RN CLI. Upstream npm зависимости выводят
deprecation warnings; они не заменены произвольным обновлением всей SDK семьи.
В compiler builds включён deprecation check. Bundle предупреждает об отсутствующем
assets destination; демонстрационный экран не содержит image assets.
CI workflow определён для Linux и Windows; наличие workflow не доказывает
успех hosted run. Эта запись касается локально наблюдавшихся результатов.

Runtime smoke использует явно помеченный synthetic producer-test context,
поскольку он проверяет producer, а не запускает IDEA. Реальный import-consumer
run требует свежего JSON export из работающего плагина на том же checkout.
LOCAL_FILE — это provenance файлов; он не означает аутентификацию vendor run.

Требуют отдельного фактического прогона и остаются NOT RUN здесь: все UI-кнопки
в установленной IDEA, native Android/iOS/device действия, SSH remote debugger,
Ansible/Shell/Bats executables, private-key/Vault/PasswordSafe inputs,
MCP Server, реальные Free/Trial/Pro/Expired/offline состояния, Split Mode,
JCEF/native renderer переключение, screen reader и licensed headless producer.
Для каждого подготовлены входы/шаги и точные предпосылки в каталоге и guides.

Локальные отчёты, logs, bundles и runtime captures остаются evidence-only либо
ignored result files. Публичная поставка содержит исходные примеры, descriptor,
безопасные public certificate/icon inputs, инструкции и проверки.
