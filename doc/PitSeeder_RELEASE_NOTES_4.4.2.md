# PitSeeder 4.4.2 Release Notes

PitSeeder and `pits` 4.4.2 implement the CLI boundary of accepted
[`CR040_AIA_to_RAIkeep_and_jsonpit_Prohibit-Read-Modify-Write.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR040_AIA_to_RAIkeep_and_jsonpit_Prohibit-Read-Modify-Write.md)
and interoperate with accepted
[`CR041_jsonpit_to_RAIkeep_Restore-Clean-Change-Filenames.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR041_jsonpit_to_RAIkeep_Restore-Clean-Change-Filenames.md).

- `pits seed` parses and validates every input object before opening the target
  pit, rejecting client-supplied `Modified` or `Deleted` without flags,
  directories, or partial state.
- `pits delete-property` emits a sparse tombstone fragment and rejects `Id`,
  `Modified`, or `Deleted`; callers use `delete-item` for lifecycle deletion.
- Domain exceptions produce concise CLI errors and nonzero exit status.
- Maintenance discovers, merges, receipts, and cleans both clean CR041 and
  legacy SHA-suffixed change artifacts during rolling upgrades.

Seed, export, audit, temporal projection, event archiving, and clean process-flag
release remain intact. Dependencies align to JsonPit and OsLibCore 4.4.2.
