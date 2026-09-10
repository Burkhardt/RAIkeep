# PitSeeder 4.2.8 Release Notes

PitSeeder 4.2.8 implements the CLI portion of accepted
[CR021](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR021_RAI_to_RAIkeep_JsonPit_Durable_Cleanup_Receipts_and_Pits_Coordination.md).

- Adds `pits maintain (<PitName> | --wwwa)` with a non-mutating report-only default.
- `--apply` performs JsonPit's validated receipt-backed maintenance and emits human or `--json` results.
- Aged process-window removal requires the additional `--prune-process-flags --older-than <duration>` authorization.
- Content-valid extensionless process-flag/event repair requires the additional `--repair-legacy-extensions` authorization.
- Maintenance handles WWWA in `Person`, `Object`, `Place`, `Activity` order and suppresses disposal recovery publication so retired changes are not recreated.
- Existing seed, export, point-in-time export, audit, and delete behavior remains compatible.

Fallback references align to `JsonPit 4.2.8` and `OsLibCore 4.2.8`; the CLI reports
`pits v4.2.8`.
