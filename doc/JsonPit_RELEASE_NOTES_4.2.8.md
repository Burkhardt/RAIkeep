# JsonPit 4.2.8 Release Notes

JsonPit 4.2.8 implements accepted
[CR021](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR021_RAI_to_RAIkeep_JsonPit_Durable_Cleanup_Receipts_and_Pits_Coordination.md),
narrowly superseding CR003's in-memory-only cleanup-eligibility rule.

- Adds immutable `ReceiptFile` evidence beside each canonically accounted hashed change file. The original UTC `Time` survives replay, restart, and master transfer without refresh.
- `Pit.Maintain(...)` provides report-only inventory or explicit application through the existing persistence/recovery gate.
- Eligible cleanup revalidates exact-master authority, change integrity, canonical health/accounting, and receipt age, then removes the change first and receipt second.
- Malformed, incomplete, unverifiable, or non-master work remains deferred and retained. Orphan receipts are safely retryable.
- `PitMaintenanceOptions` separately authorizes age-qualified PID-window pruning and content-validated extensionless flag/event repair. `Master.flag`, conflict evidence, active windows, unknown files, and recovery events are never implicitly removed.
- The finalizer contract remains unchanged: no recovery publication or filesystem I/O, and abandoned canonical paths become reopenable.

Verified by focused and package-level Release coverage, including the receipt
lifecycle on a real configured CloudDrive root, restart with unchanged receipt
time, grace-expiry cleanup, malformed/orphan evidence, explicit hygiene, legacy
repair, and the finalizer regression. The separate two-machine split-master
scenario still requires an active synchronizer on Mzansi.
