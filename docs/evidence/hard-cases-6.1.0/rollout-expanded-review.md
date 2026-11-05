# Rollout plan

Compared ` HEAD@bf714706db6c ` with ` WORKTREE@bf714706db6c `. Services deploy one at a time, so for a while the new version of one meets the previous version of another. The constraints below describe this comparison; verify the deployed versions before using them.

## Version bindings

- ` . ` (` order-service `, ` payment-service `): ` HEAD ` at ` bf714706db6cc6589ce3afb56309bd5e327b4a9d ` → HEAD ` bf714706db6cc6589ce3afb56309bd5e327b4a9d ` plus working-tree edits.

Git bases are comparison inputs, not evidence of what is deployed. A working-tree candidate has no release version until committed and released.

**Order not proven:** no service has to wait for another, but both sides of a link changed; resolve them and confirm the order with the affected teams.

## Rollout window

- ` order-service ` and ` payment-service ` both changed ` PUT /payments/{paymentId} → PUT /v2/payments/{paymentId} `, ` PUT /v2/payments/{paymentId} `; they match only when both are new. This review checked only the new versions together: confirm that whichever goes first also works with the other's current version.

Produced locally by [ArchVerity](https://plugins.jetbrains.com/plugin/34234) from the change review; it checks contracts, not runtime traffic.
