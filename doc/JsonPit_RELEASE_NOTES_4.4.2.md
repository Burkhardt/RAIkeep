# JsonPit 4.4.2 Release Notes

JsonPit 4.4.2 implements accepted
[`CR040_AIA_to_RAIkeep_and_jsonpit_Prohibit-Read-Modify-Write.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR040_AIA_to_RAIkeep_and_jsonpit_Prohibit-Read-Modify-Write.md)
and
[`CR041_jsonpit_to_RAIkeep_Restore-Clean-Change-Filenames.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR041_jsonpit_to_RAIkeep_Restore-Clean-Change-Filenames.md).

- `SetProperty`, `ExtendWith`, and `Merge` atomically reject top-level `Id`,
  `Modified`, or `Deleted`; property tombstones reject the same protected names.
- Live `Pit.Add(...)` rejects projected payloads carrying client lifecycle
  fields. Trusted canonical and change-fragment replay uses `AddHistorical(...)`.
- New change and receipt files use
  `{Modified.UtcTicks}_{ExactProcessIdentity}.{json|receipt}`. Discovery accepts
  both clean CR041 names and legacy SHA-suffixed CR003 names.
- Live mutations receive process-monotonic UTC ticks so concurrent writes retain
  distinct clean filenames despite ordinary OS clock resolution.
- Clean names use strict JSON validation; legacy names retain SHA verification.
  Receipt creation and the established ten-minute cleanup grace apply to both.
- Equal-time historical fragments using the same exact process identity fail
  explicitly instead of replacing an existing cloud artifact.

The finalizer remains free of recovery publication and filesystem I/O, and the
canonical path becomes reopenable after forced collection.
