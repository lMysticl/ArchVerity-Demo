# Средовые и дополнительные сценарии

Все действия выполняйте на проекте и версии из [run record](RUN_RECORD.md).
Записывайте PASS только по непосредственному результату. Здесь находятся
предпосылки функций, которые нельзя подтвердить одной компиляцией образца.

## Команды процессов и отладчика

Все 16 RN/Expo/Gradle/iOS/ADB-команд с входом, аргументом и proof перечислены
в [mobile-lab README](../projects/mobile-lab/README.md). Native commands требуют
сгенерированных через Expo исходников, подходящего SDK/JDK и реального
симулятора/устройства. Для iOS необходим macOS. Установка APK, signing,
удаление `com.archverity.demo` и очистка его данных — отдельные явно
разрешённые оператором действия на одноразовом устройстве.

Оставшиеся шесть process-команд:

| Команда | Вход и среда | Проверяемый результат |
| --- | --- | --- |
| ANSIBLE_SYNTAX_CHECK | workspace/ansible/professional/playbooks/site.yml; ansible-playbook в backend PATH, поддерживаемая Linux/macOS/WSL среда | Exit 0, правильный inventory/roles; missing Ansible остаётся BLOCKED |
| SHELLCHECK | workspace/shell-professional/lib/common.sh; ShellCheck | Exit 0; в отдельной копии намеренная shell ошибка даёт реальный diagnostic |
| SHFMT_DIFF | Тот же common.sh; shfmt | Diff и exit 1 означают найденные formatting changes; исходный файл не меняется |
| BATS_TEST | workspace/shell-professional/test/deploy.bats; Bash + Bats | Два проходящих теста; намеренный fail в отдельной копии виден как fail |
| BASH_DEBUG | workspace/shell-professional/qa-debug.sh; настоящий Bash в backend | Break/Step/Next/Continue/Stack/Print variable/Clear breakpoints/Go to stop/Stop дают реальные состояния |
| BASH_REMOTE_DEBUG | Тот же script и заранее подготовленный, явно разрешённый SSH host с Bash | Host/path/script hash совпадают; удалённый stop/variable/stack относится к этому target |

SSH-учётные данные и private keys сюда не включены. Используйте существующий
разрешённый host; подготовьте matching remote script по своему установленному
debugger workflow. Не подменяйте удалённый результат local debugger run.
Bash/Zsh/extensionless/Bats editor completion, navigation, documentation,
rename/format проверяются отдельно в QA-SHELL. Seven debug command registrations
остаются привязаны к QA-SHELL в каталоге.

Ansible Vault: подготовленная plain YAML находится в `ansible/vault-plain.yml`.
Оператор отдельно задаёт одноразовый пароль, encrypt → Decrypt/Edit → save,
независимо decrypt и проверяет изменение `service_name`. Неверный пароль не
должен менять ciphertext. Пароль/расшифровку не включайте в evidence.
Keystore private-key metadata требует отдельно предоставленного синтетического
ключа; в набор включены только безопасные публичные certificate/CSR/CRL/key inputs.

## MCP

Включите встроенный JetBrains MCP Server, выберите **этот** отсканированный
проект, убедитесь в действительном Trial/Pro. Примеры аргументов четырёх tools:

```json
{
  "archverity_change_impact": {"base_revision":"HEAD","limit":10},
  "archverity_findings": {"severity":"ERROR","include_suppressed":false,"limit":10},
  "archverity_contract_evidence": {"query":"payments","limit":10},
  "archverity_trace_flow": {"query":"payment-service","direction":"both","max_depth":4,"limit":20}
}
```

Это четыре отдельных вызова, а не один aggregate tool. Для trace повторите
inbound/outbound/both; limit вне диапазона должен быть ограничен до поддержанного
бюджета. Negative inputs: trace query пустой, severity `INVALID`, direction
`INVALID`, неподходящий base revision. Evidence tool допускает пустой optional
query; trace требует непустой query. Ответ содержит bounded metadata и
project-relative locations, без source snippets/absolute paths. Повторите
неполный/stale scan и отсутствие entitlement: нужна явная ошибка.

## JSON, CLI и headless

Реальные IDE exports проверяйте на format и затем на текущую identity:

```powershell
python suite-support/inspect_export.py work/analysis.json --kind analysis
python suite-support/inspect_export.py work/change.impact.json --kind impact
python suite-support/inspect_export.py work/findings.sarif --kind sarif
python suite-support/inspect_export.py work/topology.svg --kind svg
python suite-support/inspect_export.py work/topology.png --kind png
python suite-support/inspect_export.py work/topology.mmd --kind mermaid
python suite-support/inspect_export.py work/review.md --kind markdown
```

Проверяйте Copy/Save JSON, все шесть форматов, JSON re-read, PNG visual inspection,
SVG root, Mermaid diagram, SARIF 2.1.0, readable Review Markdown и redaction.
Format inspection не запускает анализ и не доказывает полноту/SAFE.

**ArchVerity Tools поставляются отдельно** от этого публичного демо. Здесь нет
копии закрытых исходников плагина/Tools и не обещается несуществующий pip пакет.
С предоставленным оператором дистрибутивом `python -m archflow_tools --help`
должен работать в его Python environment. Проверяйте реальные команды:

```powershell
python -m archflow_tools import-openapi projects/workspace/qa-openapi.json --service-id qa-loopback -o work/openapi.archflow.json
python -m archflow_tools import-asyncapi projects/workspace/qa-asyncapi.json -o work/asyncapi.archflow.json
python -m archflow_tools import-backstage projects/workspace/qa-backstage.json -o work/backstage.archflow.json
python -m archflow_tools scan-amqp projects/workspace --service-id demo-amqp -o work/amqp.archflow.json
python -m archflow_tools validate-manifest work/openapi.archflow.json
python -m archflow_tools ci work/analysis.json --threshold ERROR --sarif work/ci.sarif --report work/ci.json
python -m archflow_tools ci-impact work/change.impact.json --fail-on BREAKING --require-complete -o work/ci-impact.json
python -m archflow_tools diff work/base.json work/head.json -o work/diff.json --markdown work/diff.md
```

`policy-merge` требует предоставленного policy и project YAML; `git-diff`
требует существующих committed base/head и snapshot path. Используйте
подготовленную demo Git-копию, не личный проект. Import-verification можно
повторить по raw/metadata/spec из runtime-evidence: формат
`pact-broker-verification` либо `drift-junit` и соответствующие реальные файлы.
Проверки JSON fail closed для incomplete/partial/UNKNOWN и разных scopes.

Свежий PSI producer `analyze` / `analyze-impact` требует совместимые
`--ide-home`, unpacked `--plugin-dir`, отдельный новый `--work-dir`, committed
HEAD/base и заранее provisioned **изолированный** CI IDE config с настоящим
entitlement. Конкретный пример после подстановки проверенных путей:

```text
python -m archflow_tools analyze-impact <prepared-repository> --base <committed-base> --head <committed-head> --ide-home <compatible-IDE> --plugin-dir <unpacked-plugin> --ide-config <separate-provisioned-CI-profile> --work-dir <new-task-owned-directory> -o <impact-json>
```

Лицензионные credentials не копируются автоматически. Активный GUI IDE config
нельзя использовать одновременно в headless процессе. Working-tree мутация
из apply_impact требует отдельного scoped commit перед headless comparison.
Используйте workspace без включённых runtime/verification imports: ignored
sidecar reports producer не переносит в новые Git clones. Refusal лицензии —
отдельная наблюдаемая проверка, а не успешный анализ.

## Runtime, интерфейс и лицензии

Повторите выбранные QA-сценарии в local IDEA и настоящем Split Mode, связав
frontend/backend/project identity. Проверьте JCEF graph и native fallback на
отдельно выбранном реально доступном renderer. Не объявляйте fallback
проверенным по обычному JCEF run. Смените light/dark, 200% scale, keyboard-only
и screen reader; переоткройте проект для persistence и disposal.

Free/Trial/Pro/Expired/offline проверяются на независимо предоставленных
реальных Marketplace состояниях. Проверяйте UI и backend, exports, cached
analysis/Impact, Dev Icons, Developer tools и MCP. Файл демо или JVM property
не заменяет entitlement. Отсутствующий внешний state/device/host/profile —
конкретный BLOCKED/NOT RUN в run record; другие независимые сценарии продолжаются.
