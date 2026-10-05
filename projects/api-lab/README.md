# API Client laboratory

[Пошаговый запуск этой лаборатории](../../docs/DEMO_RUNBOOK_RU.md#4-локальные-http-websocket-и-grpc)
включён в общую инструкцию демонстрации всех шести проектов.

HTTP, WebSocket and gRPC use real loopback servers. No remote service is needed.

Подробные действия API Client, environments/secrets, DSL, WebSocket/gRPC,
imports/exports/cookies раскрыты в [полном руководстве](../../docs/ALL_FUNCTIONS_RU.md#devs-01).
Все остальные возможности плагина доступны через содержание этого руководства.
Use the commands from the repository root; Python 3.10+ is required.

For a separate clean Git project, prepare all API inputs with
`python suite-support/prepare_project.py --project api-lab --output <new-directory>`.
Run `serve.py` from that copy and use its `schema/` and `scenarios/` files.

```powershell
python -m venv work/api-venv
work/api-venv/Scripts/python.exe -m pip install -r projects/api-lab/requirements.txt
work/api-venv/Scripts/python.exe projects/api-lab/serve.py
```

On Linux/macOS replace `work/api-venv/Scripts/python.exe` with
`work/api-venv/bin/python`. Stop the process with Ctrl+C. HTTP alone can run
without third-party packages: `python projects/api-lab/serve.py --protocol http`.
If a port is occupied, use the corresponding `--http-port`, `--websocket-port`
or `--grpc-port` argument and update the request/scenario URL.

| Transport | Input in ArchVerity | Observable result |
| --- | --- | --- |
| HTTP | Import `requests.http`; send `/health` and POST `/qa-roundtrip` | 200 and the exact submitted JSON under `received` |
| HTTP imports | The workspace's `qa-api.http`, `qa-openapi.json`, `qa-postman.json`, `qa-curl.txt` | Every imported request reaches this same server; no public internet target |
| HTTP errors/cancel | `/error`, `/missing`, `/qa-slow?delay_ms=5000`; press Cancel, then send `/health` | 500/404 remain visible; cancelled slow request cannot replace the later health result |
| HTTP response limit | `/large?bytes=100000` with a lower response budget | Truncation/limit is explicit; no complete successful result |
| Cookies | GET `/cookies/set`, then `/cookies/show`; Clear cookies; repeat show | hasDemoCookie becomes true, then false after clearing; fixed demo cookie has no authentication role |
| Environment headers | Set nonsecret env variable DEMO=local; X-Demo: {{DEMO}} on GET `/headers` | demoHeader=local; Authorization presence is only a boolean and its value is never echoed |
| WebSocket | `ws://127.0.0.1:18428`; Connect; send `ArchVerity` | Identical incoming text with sequence number; Close terminates this session |
| WebSocket error | Send `error`; reconnect and send `close` | Error close 1011, then normal close 1000; connection can be reopened |
| gRPC unary | `http://127.0.0.1:18429`, `archverity.demo.Echo/Say`, load `schema/echo.pb`, body `{"text":"demo"}` | `{"text":"demo","sequence":1}`, terminal OK |
| gRPC server stream | `archverity.demo.Echo/Watch`, server-stream mode, `{"text":"demo","count":3}` | Ordered sequence 1, 2, 3, then OK |
| gRPC imported message | `archverity.demo.Echo/Health`, unary, body `{}` | `text=ok`; descriptor imports `google/protobuf/empty.proto` |
| gRPC error/deadline | `Echo/Fail`; or `Echo/Say` with `{"delayMs":5000}` and deadline 100 ms | INVALID_ARGUMENT or DEADLINE_EXCEEDED |
| gRPC cancel/budget | Watch with count 1000 and delayMs 50; Cancel; or lower message limit to 2 | Cancelled/partial/error is explicit; subsequent unary succeeds |
| Unsupported streams | `Echo/Upload` and `Echo/Chat` | API Client rejects client/bidi streaming; it never treats them as supported unary calls |
| Scenarios | Paste contents of `scenarios/happy.json` into Scenarios | Two passing steps; captured `ID=42` reaches the second request |
| Failed assertion | `scenarios/assertion-fails.json` | First step fails; second step is not sent |
| Missing variable | `scenarios/missing-variable.json` | Explicit unresolved-variable error before sending |

For gRPC use the exact method string `archverity.demo.Echo/Fail`, and similarly
for all other methods. JSON field names follow protobuf JSON (`delayMs`).
Descriptor loading accepts the binary `.pb`, not the text `.proto`.

The example DSL is ArchVerity's declarative language, with structural JSON
assertions and captures. It contains no Postman `pm.*` or arbitrary JavaScript.
Environment variables, PasswordSafe secrets, cookies and import/export UI use
the [workspace QA matrix](../workspace/QA_MATRIX_RU.md#инструменты-разработчика-и-контекстные-действия).
PasswordSafe checks require a separate operator-supplied disposable secret.

Rebuild and verify the descriptor after changing the source:

```powershell
work/api-venv/Scripts/python.exe projects/api-lab/build_schema.py
work/api-venv/Scripts/python.exe -m unittest discover -s projects/api-lab -p test_protocols.py -v
```

These tests send actual HTTP/WebSocket/gRPC traffic and verify errors, sizes,
deadlines, cancellation and import completeness. They prove the laboratory's
servers; the ArchVerity UI steps above need their own IDEA run.

Additional scenario inputs:

- `scenarios/dsl-types.json`: numbers versus strings, boolean/null, arrays,
  RFC 6901 escaped keys and capture → next HTTP request, using `/dsl-shapes`.
- `scenarios/wrong-json-type.json`: number `42` compared to string `"42"` fails.
- `scenarios/missing-json-pointer.json`: a missing field differs from JSON null.
- `scenarios/unsupported-javascript.json`: Postman JavaScript is rejected.

The negative chains must stop before their second step. These are ArchVerity DSL
consumer recipes; the protocol tests separately verify their actual server input.
