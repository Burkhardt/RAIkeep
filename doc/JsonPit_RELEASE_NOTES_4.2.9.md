# JsonPit 4.2.9 Release Notes

JsonPit 4.2.9 implements its incident correction under accepted
[CR022](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR022_RAI_to_RAIkeep_Cloud_Safe_In_Place_Filesystem_Invariant.md)
while preserving accepted [CR021](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR021_RAI_to_RAIkeep_JsonPit_Durable_Cleanup_Receipts_and_Pits_Coordination.md)
receipt-backed cleanup semantics.

- `Pit.Maintain(...)` checks the non-creating canonical parent directly.
- Report-only and apply maintenance against a missing pit return deferred
  evidence without creating a pit directory, canonical file, flag, or receipt.
- `PitMaintenanceResult` can represent a missing target without constructing a
  live `Pit` instance.
- Canonical persistence, recovery, receipt ordering, finalizer behavior, and
  explicit maintenance deletion semantics remain unchanged.

The investigation found no evidence that CR021 replaced the established AIA
`Activity`, `Person`, `Object`, or `Place` directories. Regression coverage now
protects the missing-target no-filesystem-mutation boundary explicitly.
