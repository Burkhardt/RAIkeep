# PitSeeder 4.2.9 Release Notes

PitSeeder 4.2.9 implements the CLI correction required by accepted
[CR022](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR022_RAI_to_RAIkeep_Cloud_Safe_In_Place_Filesystem_Invariant.md)
while retaining accepted [CR021](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR021_RAI_to_RAIkeep_JsonPit_Durable_Cleanup_Receipts_and_Pits_Coordination.md)
maintenance behavior.

- `pits maintain` validates the resolved subscriber root before constructing any
  `Pit` and fails without mutation when that root is absent.
- Single-pit maintenance requires the canonical `<PitName>.pit` file to exist.
- WWWA maintenance requires at least one canonical pit; missing peers are
  reported as deferred and are not materialized.
- Report-only maintenance of a wrong or partial tree leaves directory inventory
  and timestamps unchanged.

An applied maintenance run that includes `--prune-process-flags` or
`--repair-legacy-extensions` may intentionally retire many obsolete files.
OneDrive can present its mass-deletion confirmation for that explicit cleanup;
operators should compare the reported removal counts with the `pits maintain`
result before confirming the provider action. Canonical `.pit` files and
unexpired/unvalidated evidence are not cleanup targets.

Fallback references align to `JsonPit 4.2.9` and `OsLibCore 4.2.9`; the CLI
reports `pits v4.2.9`.
