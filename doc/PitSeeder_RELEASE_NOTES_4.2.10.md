# PitSeeder 4.2.10 Release Notes

PitSeeder 4.2.10 exposes JsonPit's RAI-authorized recovery-event compaction
through the operational CLI.

- `pits maintain (<PitName> | --wwwa) --archive-events --json` is a strictly
  non-mutating preview of the exact archive name, UTC range, selected count, and
  deferred evidence.
- Adding `--apply` creates the immutable same-directory archive and retires only
  exact validated loose copies.
- `pits audit` transparently reads remaining loose events and archive entries
  with its established machine/severity filters and deterministic ordering.
- Corrupt archives, invalid events, and conflicting event identities produce
  diagnostics and a nonzero audit result without deleting evidence.

Single-pit and WWWA command-level tests cover preview, apply, missing-pit
non-creation, archive visibility through audit, and exact JSON reporting.
Fallback references align to `JsonPit 4.2.10` and `OsLibCore 4.2.10`; the CLI
reports `pits v4.2.10`.
