# Проверка набора 05.10.2026

Проверено на Windows, Python 3.12, Temurin JDK 21.0.12 и Node 22.23.2.
Это запись подготовки и локального исполнения демонстрационных проектов.
Она не является общим PASS для всех действий установленного плагина.

| Проверка | Непосредственное наблюдение |
| --- | --- |
| Registered-entry contract | 87 записей совпадают с descriptor/enums/MCP текущих исходников ArchVerity 3.0.3: 15 surfaces, 6 actions, 22 processes, 7 debugger commands, 6 exports, 4 MCP, 5 settings, 22 editor extension |
| Feature catalog | 41 capability recipe имеет существующий вход, действие, ожидаемое наблюдение и guide; все 19 мутаций имеют точные anchors в исходном baseline |
| Полное раскрытие функций | 62 source capabilities совпадают с feature inventory 3.0.3; каждая содержит purpose, setup, действия/наблюдения, контрпример, восстановление и capture; все 87 entry points имеют отдельную привязку. Полное руководство и таблица entry points сгенерированы из проверяемых canonical JSON |
| Guide negative controls | 4 unittest отклоняют пропущенную icon subfeature, потерянный Kotlin entry point, действие без ожидаемого наблюдения и выдуманный consumer PASS; старый сокращённый каталог не принимается как полное руководство |
| first-result compile | Gradle classes: оба Java-модуля успешно компилируются с JDK 21 |
| workspace compile | Java/Kotlin classes, включая HTTP/Jackson/Kafka/AMQP расширения; deprecation/compiler checks включены |
| runtime-evidence compile/run | Gradle installDist и настоящий Spring Boot/Tomcat на loopback; реальный /actuator/beans и /payments/42 |
| Runtime producer cases | Pact-shaped PASS, Pact-shaped FAIL, Drift-shaped PASS от именованного локального HTTP verifier; реальные template/factory dependencies; canonical outcome/context/hash совпали с отдельно предоставленным Tools importer |
| Workspace preflight | 19 мутаций, 3 canonical manifests, HTTP 200/400/404/413, Node script, оба 63-icon пакета; certificate PEM/DER equality, CSR/CRL signatures и public-only trustedCertEntry |
| Coverage negative controls | 4 unittest: фиктивный bundle input, неправильный shell input и отсутствие внешней предпосылки отклоняются |
| API transports | 18 unittest с настоящими TCP HTTP/WebSocket/gRPC roundtrips, cookies/header, ordered stream, errors, byte bounds, deadline/cancel, descriptor imports и реальными различимыми number/string/boolean/null/missing/escaped-pointer inputs для scenario DSL |
| Политики и extension SDK | Реальный canonical archflow_tools CLI исполнил run-provider и validate-manifest, отклонил пустой serviceId; policy-merge объединил profiles в default/demo, заменил owner и сохранил остальные поля |
| Все keystore-форматы | Java KeyStore с JDK 21 и BC 1.85 открыл 7 public-only файлов JKS/JCEKS/PKCS12/PFX/BKS/BCFKS/UBER: один matching trusted certificate, no key entries; все 7 отвергли неправильный пароль. javac -Xlint:all -Werror прошёл |
| Настоящий submodule input | Helper создал отдельный clean Git workspace с demo-icon-module, index mode 160000; это вход для gitSubmoduleOnly, а не описание отсутствующего child repository |
| Большой ANSI input | Производитель создал 70 001 строк, 7 000 100 bytes, SHA-256 bc04d4f3bedfda13a56f9f99205d1869a431300ce6f3451202d09024c279196b; first/last markers проверены. Реальный paged editor отдельно требует IDEA consumer run |
| Mobile script/bundle | RN_SCRIPT_OK; React Native CLI создал Android JavaScript bundle 1 050 866 bytes с ARCHVERITY_DEMO_CLICK; SHA-256 6013199253f605141b8e6ef3e29bd43287586a138441f06473a6437dfe4cf73f |
| Metro / Expo lifecycle | Оба реальных loopback dev servers ответили packager-status:running; после остановки их собственных child processes порты перестали отвечать |

Мобильный lockfile фиксирует совместимые SDK 54 / RN 0.81.5 / CLI 20.0.2 и
Metro/metro-config 0.83.3 для Expo и RN CLI. Upstream npm зависимости выводят
deprecation warnings; они не заменены произвольным обновлением всей SDK семьи.
В compiler builds включён deprecation check. Bundle предупреждает об отсутствующем
assets destination; демонстрационный экран не содержит image assets.
CI workflow выполняет эти публично воспроизводимые checks на Linux и Windows,
включая guide negative controls, JDK truststores и actual submodule input.
Standalone BC-форматы в CI отмечаются NOT_RUN без отдельного BC jar; все семь
проверены локально с той же версией, что у плагина. Конкретный commit и hosted
результат проверяйте в [Actions](https://github.com/lMysticl/ArchVerity-Demo/actions/workflows/checks.yml).
Таблица выше фиксирует непосредственно наблюдавшиеся локальные результаты.

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
