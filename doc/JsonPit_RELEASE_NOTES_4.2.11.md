# JsonPit 4.2.11 Release Notes

JsonPit 4.2.11 implements accepted
[CR024](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR024_AIA_to_RAIkeep_Ephemeral_Flag_Self_Cleanup.md).

- `ProcessFlagFile.TryReleaseCurrentProcess()` ownership-checks and removes the
  exact PID-specific process flag through `RaiFile.rm()`.
- Explicit read-only and writable `Pit.Dispose()` therefore leave no process
  flag after their existing durability work completes.
- Process-window cleanup never changes or removes `Master.flag`; established
  master leases and TTL behavior are unchanged.
- Finalization remains strictly free of filesystem and recovery-publication I/O.
- Flags left by crashes remain discoverable and eligible for the existing
  explicit maintenance pruning path.

Tests cover owned and foreign flags, both disposal modes, master preservation,
and the existing finalizer/no-I/O contract.
