# CR087 provider review

Implemented in coordinated 4.6.4 and included in 4.6.5. JsonPit, pits and Umgodi include the correction. Umgodi 0.1.0 and the frozen jsonpit 4.6.3 runtime, including its documentation-only 4.6.3.post1 distribution, predate it.

## Verification on November 18, 2026

Re-read the original AIA CR087 and checked R1–R3 against the current source. The current implementation renews the master lease at publication time, preserves historical fragment timestamps, and revalidates ownership before eligible change retirement.

- 96 C# library tests passed across receipt maintenance, master tickets, live references, reference identity, sparse deltas, and split-master recovery.
- 56 C# CLI tests passed across subcommands and local ticket windows, including historical maintenance that requires Store.
- All 220 Umgodi tests passed. Added direct Save coverage for five-minute-old and eight-day-old histories, plus CLI coverage that forces historical persistence while retiring an elapsed receipt and retaining a fresh one.
- The Python cross-engine tests required access to OsLib's configured temporary directory outside the workspace sandbox. They passed with that access after rebuilding the local C# CLI.
- A disposable fixture reproduced immediate lease expiry in the frozen Python implementation. RAI confirmed on November 18 that jsonpit remains frozen and that this verification covers C# JsonPit and active Umgodi.

These checks cover the CR087 acceptance behavior through local library and CLI entry points. The live remote replication suites were outside this verification run.

## Reproduction

On a disposable local pit, the C# CLI merged a day-old fragment and issued a receipt. After aging the receipt by eleven minutes, a second distinct historical fragment forced canonical persistence during the next maintenance pass. The CLI reported current master, canonical persisted, one eligible change, zero changes removed, zero receipts removed and a cleanup revalidation deferral. A control pass with every change already accounted for skipped Store and retired the eligible pair. Including a pending historical fragment is essential for a CLI regression that exercises the faulty Store branch.

In an independent Python fixture, a flagged Umgodi pit persisted a day-old fragment. Immediately afterwards the on-disk master named the calling process and reported an expired lease. The Python cleanup loop formerly deleted eligible files without rechecking ownership or canonical accounting. The jpit apply command also opened its target unflagged.

## Verified behavior

Store signals a successful snapshot publication with the current UTC lease time and gives the writer the same checkpoint. Historical fragment times remain intact. C# continues to validate exactly the dirty fragments included in its snapshot. A checkpoint older than publication observes the write even when it is newer than every stored fragment.

Tests in JsonPit.Tests, pits.Tests and Umgodi cover historical canonical writes, the ten-minute receipt grace, foreign takeover, canonical accounting and retention of a newly receipted change. The Python apply command now participates in the same master protocol as a normal writer.

## Where accumulated changes go

Both ordinary C# constructors and the Python writable open path reconcile pending changes. The regression starts with 102 already-imported change files. One ordinary writable open retires the 100 with elapsed receipts, retains the fresh pair and issues a first receipt for the last file. The canonical file retains all 102 histories and its modification time. Both real CLI seed entry points also retire an eligible pair. Read-only inspection preserves the files. Grace starts at durable receipt issuance, so a day-old change may still have a fresh receipt.

AIA's checked-out API uses JsonPit 4.6.3. It creates four long-lived writable PersistentPit instances at startup. A request can reuse an instance many times without reopening it. Its explicit reload service calls Load to adopt the canonical snapshot. Its separate prune service calls Maintain under the application's persistence gate. Elapsed time alone does not schedule a cleanup pass. This explains how a backlog can persist. The live AIA directories and deployment were outside this investigation.

[Requested change and acceptance criteria](https://github.com/Burkhardt/AIA/blob/main/doc/CR087_AIA_to_RAIkeep_JsonPit_Store_MasterFlag_Lease_Backdating.md)
