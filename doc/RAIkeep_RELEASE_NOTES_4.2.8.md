# RAIkeep 4.2.8 Release Notes

RAIkeep 4.2.8 is the coordinated seven-package delivery of accepted
[CR021 — JsonPit Durable Cleanup Receipts and `pits` Coordination](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR021_RAI_to_RAIkeep_JsonPit_Durable_Cleanup_Receipts_and_Pits_Coordination.md).

## Delivered

- JsonPit cleanup eligibility is durable across restart and master transfer through immutable `.receipt` files.
- Cleanup remains crash-safe and conservative: canonical accounting and current exact-master authority are revalidated, then the change file is removed before its receipt.
- `Pit.Maintain(...)` and `pits maintain` expose report-only and explicit-apply administration without timers, finalizer work, or `Os.Config` mutation.
- Expired PID-window pruning and legacy extension repair each require separate explicit authorization.
- Dotted logical process names retain their requested `.flag` / `.event` extensions.
- Typed `PitsCommand` calls serialize same-target child invocations within one host process while preserving exact child PID authority and the distributed JsonPit protocol.

## Compatibility and release boundary

- CR021 changes no AIA source and introduces no identity-management subsystem.
- CR003 remains authoritative except for its superseded in-memory-only cleanup-eligibility rule.
- All seven package versions and fallback dependency properties align on 4.2.8.
- Tagging, GitHub labels, and NuGet publication remain behind RAI's manual `scripts/release-chain.sh 4.2.8` gate.
