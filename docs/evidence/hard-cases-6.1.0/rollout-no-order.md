# Rollout plan

Compared ` HEAD@bf714706db6c ` with ` WORKTREE@bf714706db6c `. Services deploy one at a time, so for a while the new version of one meets the previous version of another. The constraints below describe this comparison; verify the deployed versions before using them.

## Version bindings

- ` . ` (` order-service `, ` payment-service `): ` HEAD ` at ` bf714706db6cc6589ce3afb56309bd5e327b4a9d ` → HEAD ` bf714706db6cc6589ce3afb56309bd5e327b4a9d ` plus working-tree edits.

Git bases are comparison inputs, not evidence of what is deployed. A working-tree candidate has no release version until committed and released.

**As written, no deploy order is safe:** ship one side backward compatible first.

## Rollout window

- ` order-service ` and ` payment-service ` both changed ` PUT /payments/{paymentId} → PUT /v2/payments/{paymentId} `; they match only when both are new. By method and path, neither the current ` order-service ` with the new ` payment-service ` nor the reverse matches: no order keeps this call working. Keep the previous route on the server until the caller moves.

## Migration completion evidence

- **EXPAND** (completion evidence not observed): Introduce a version accepting both old and new contracts; retain the previous route or payload shape. Complete only after: Check the expanded provider with the old and new consumers, including mixed-version payloads, against the recorded repository bases.
- **MIGRATE** (completion evidence not observed): Move consumers to the new contract while the expanded provider supports both versions. Complete only after: Owners confirm the consumer versions actually deployed, and check external consumers, retained Kafka records and rollback paths.
- **CONTRACT** (completion evidence not observed): Remove the old contract only in a later reviewed change. Complete only after: Obtain owner evidence that no deployed or external consumer, retained record or rollback version needs the old contract; absence in this scan alone is insufficient.

Produced locally by [ArchVerity](https://plugins.jetbrains.com/plugin/34234) from the change review; it checks contracts, not runtime traffic.
