# JsonPit 4.4.1 Release Notes

JsonPit 4.4.1 participates in the synchronized eight-package delivery
of accepted
[`CR037_AIA_to_RAIkeep_RaidSeeder_Diagram_Artifact_Management.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR037_AIA_to_RAIkeep_RaidSeeder_Diagram_Artifact_Management.md).
The coordinated release also carries accepted
[`CR037.1_AIA_to_RAIkeep_CLI_Global_Flag_and_Verb_Dispatch_Resilience.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR037.1_AIA_to_RAIkeep_CLI_Global_Flag_and_Verb_Dispatch_Resilience.md).

It implements accepted
[`CR040_AIA_to_RAIkeep_and_jsonpit_Prohibit-Read-Modify-Write.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR040_AIA_to_RAIkeep_and_jsonpit_Prohibit-Read-Modify-Write.md)
and
[`CR041_jsonpit_to_RAIkeep_Restore-Clean-Change-Filenames.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR041_jsonpit_to_RAIkeep_Restore-Clean-Change-Filenames.md).

- `SetProperty`, `ExtendWith`, and `Merge` atomically reject top-level `Id`,
  `Modified`, or `Deleted`; property tombstones reject the same protected names.
- Live `Pit.Add(...)` rejects entity-shaped/projected payloads carrying client
  lifecycle fields. Trusted canonical and change-fragment replay remains
  available through `AddHistorical(...)`.
- New change and receipt files use the clean
  `{UtcTicks}_{ExactProcessIdentity}` stem. Discovery accepts clean and legacy
  SHA-suffixed names; only legacy names retain content-hash verification.
- Live engine timestamps use a process-wide monotonic UTC-tick allocator. This
  closes the real OS-clock resolution gap under concurrent writes while keeping
  the CR041 filename equal to `{Modified.UtcTicks}_{ExactProcessIdentity}`.
- Maintenance creates receipts and applies the ten-minute cleanup protocol to
  clean names without the former unhashed-file deferral.
- Explicit historical fragments that reuse both a timestamp and an exact process
  identity fail rather than silently replacing a cloud artifact. Persistence,
  event archives, audit, temporal export, and clean-exit
  process-flag behavior otherwise remain intact.
