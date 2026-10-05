# Native Kafka exports · ArchVerity 3.0.4

These six files were exported with **JSON → Save analysis JSON** from installed
ArchVerity 3.0.4 in IntelliJ IDEA 2026.1.4 on Windows on 2026-10-06. They contain
the actual model; they are not expectations generated from the source fixture.
All identities, addresses and sources are synthetic.

The [Russian walkthrough](../../KAFKA_PROFILES_ARTICLE_RU.md) shows the exact
source changes. The [native recording](../../media/kafka-profiles-3.0.4.mp4) and
[recording receipt](../../media/kafka-profiles-3.0.4.proof.json) bind these exports
to the installed package, project, compilation and inspected video.

| Export | Actual result | Configuration fingerprint |
| --- | --- | --- |
| [k01-unknown.json](k01-unknown.json) | Two unresolved scopes; `009/010 UNKNOWN`; five findings | `11c4887f666120ce9eefa040` |
| [k02-shared-unknown.json](k02-shared-unknown.json) | Shared `declared-demo`; `005 UNKNOWN`, `010 UNKNOWN` | `a7027d5ed987525c5c8083a4` |
| [k11-proven-drift.json](k11-proven-drift.json) | Explicit JSON factory; required `tenant` missing; `005 PROVEN_MISMATCH` | `66f121186adcd7d9e8e272eb` |
| [k12-repaired.json](k12-repaired.json) | Producer and consumer both require `id/tenant`; zero findings | `66f121186adcd7d9e8e272eb` |
| [k03-separate.json](k03-separate.json) | `east/west` stay separate; no `005/009/010`; two observations | `81de1c6985ae900e5838b2cb` |
| [k01-recovery.json](k01-recovery.json) | Original nodes, edges, findings, DTO shapes and context restored | `11c4887f666120ce9eefa040` |

Every export has `projectId=kafka-profile-lab`, `runStatus=COMPLETE`,
`partial=false`, global selected profiles `[default]` and property sources from
both `application.yml` files plus producer `application-blue.yml` and consumer
`application-green.yml`. The DTO-only repair retains the configuration
fingerprint. Export timestamps and elapsed statistics naturally differ after
recovery; the semantic model and configuration identity match the original.

From the demo repository root:

```powershell
python -B -X utf8 suite-support/inspect_kafka_story.py
python -B -X utf8 -m unittest discover -s suite-support -p test_kafka_story.py -v
```

`KAFKA_STORY_PASS` checks each case, both repository/module identities, active
source provenance, required wire fields, topic scopes, graph edges and recovery.
The negative controls reject screenshot metadata substituted for an export,
missing/stale repaired DTOs, an edge across cluster scopes, wrong profiles and
a stale recovery fingerprint. Existing `inspect_kafka_export.py` remains the
oracle for independently prepared [12 recipes](../../../projects/kafka-profile-lab/cases.json).

This is evidence of static analysis in this installed build. No broker was
started, messages were not sent, and effective deployment configuration,
headers/type mappings, deserialization and business processing were not tested.
The prepared copy was restored to its own clean Git baseline after recording.
