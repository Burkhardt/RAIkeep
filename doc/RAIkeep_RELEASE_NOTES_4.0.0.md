# Release Notes: RAIkeep v4.0.0

**Date:** 2026-08-06  
**Author / Delivering Agent:** RAIkeep Dev Agent  
**Delivered Version:** v4.0.0  
**Target Consumers:** AIA (Bob, Adele), AfricaStage  
**Status:** Publishing in progress (NuGet)

---

## 1. Summary

RAIkeep v4.0.0 delivers the coordinated CR003 concurrency and persistence contract
across the core package line (`OsLibCore`, `RaiUtils`, `RaiImage`, `JsonPit`,
`ImgSeeder`, `PitSeeder`).

Primary outcome:
- The confirmed concurrent save/add persistence race is fixed.
- Multi-thread, multi-process, and multi-machine cloud-synced behavior is now
  explicitly defined and tested.
- Exact-process master ownership, deterministic merge ordering, and durable
  recovery/audit paths are implemented.

---

## 2. Resolved Change Requests (CRs)

- [`CR003_RAI_to_RAIkeep_JsonPit-concurrency-contract-and-persistence-races.md`](CR003_RAI_to_RAIkeep_JsonPit-concurrency-contract-and-persistence-races.md) — fully addressed in coordinated v4.0.0 implementation and release line.

---

## 3. Root Cause Analysis & Technical Resolution

### Root cause confirmed

Concurrent `Save` and `Add` operations could race during persistence snapshot
materialization, producing unstable read/serialization behavior and a silent-loss
window when newer live fragments were validated against older persisted snapshots.

### Resolution implemented

- Introduced a brief state/snapshot gate for safe point-in-time persistence capture.
- Released the gate before cloud I/O so concurrent writers are not serialized behind
  file operations.
- Validated only fragments actually included in the successfully persisted snapshot.
- Enforced exact-PID master ownership semantics for lease renewal and handoff.
- Added deterministic equal-timestamp ordering and idempotent replay handling.
- Added collision-safe hashed change-file naming and two-stage cleanup grace.
- Added live split-master recovery with durable, structured event evidence.
- Standardized OsLib in-place save contract to avoid delete/rename path gaps during
  rewrite cycles.

Detailed technical implementation is documented in component release notes:
- [`OsLib_RELEASE_NOTES_4.0.0.md`](OsLib_RELEASE_NOTES_4.0.0.md)
- [`RaiUtils_RELEASE_NOTES_4.0.0.md`](RaiUtils_RELEASE_NOTES_4.0.0.md)
- [`RaiImage_RELEASE_NOTES_4.0.0.md`](RaiImage_RELEASE_NOTES_4.0.0.md)
- [`JsonPit_RELEASE_NOTES_4.0.0.md`](JsonPit_RELEASE_NOTES_4.0.0.md)
- [`ImgSeeder_RELEASE_NOTES_4.0.0.md`](ImgSeeder_RELEASE_NOTES_4.0.0.md)
- [`PitSeeder_RELEASE_NOTES_4.0.0.md`](PitSeeder_RELEASE_NOTES_4.0.0.md)

---

## 4. Public Contract & API / Package Changes

### Package line delivered

- `OsLibCore` v4.0.0
- `RaiUtils` v4.0.0
- `RaiImage` v4.0.0
- `JsonPit` v4.0.0
- `ImgSeeder` v4.0.0
- `PitSeeder` v4.0.0

### Contract-level changes of note

- JsonPit persistence boundary and validation semantics are now explicit and
  enforced under concurrency.
- One live public `Pit` instance per canonical path per process is enforced.
- Exact-process master lease behavior is enforced across process windows.
- `pits --events` audit mode exposes durable recovery events in a read-only path.

### Breaking/operational compatibility note

- Shared-pit participants must be upgraded together to v4.0.0 package/tool line.
  Pre-4.0.0 participants can fail on v4.0.0 hashed change-file artifacts.

---

## 5. Validation & Acceptance Evidence

- Umbrella acceptance run (non-SSH scope): **359 passed, 0 failed, 0 skipped**.
- Release build completed with **0 warnings**.
- Two-server split-master cloud scenario (OneDrive; Nkosikazi <-> Mzansi): passed,
  including loser recovery via validated hashed change files and durable event trail.
- Dynamic master/non-master remote scenario: passed standalone repeatedly.
- New explicit concurrency suites added and passing, including:
  `InProcessConcurrencyTests`, `MultiPitInstanceConcurrencyTests`,
  `MultiProcessConcurrencyTests`, `ReadDuringWriteTests`,
  `SplitMasterRecoveryTests`, `RemoteCloudConcurrencyTests`,
  `EventsAuditModeTests`, `TextFileSaveContractTests`, `EventFileTests`.

---

## 6. Upgrade & Consumption Instructions

1. Update AIA package references in `Directory.Packages.props` to the coordinated
   v4.0.0 line.
2. Restore and execute:
   - `dotnet test AIA.slnx`
   - `pnpm --dir aia-workbench build`
3. Validate CR003 acceptance criteria against live behavior, contract semantics,
   and operational notes above.
4. If accepted, create the formal consumer signoff artifact using the agreed
   evaluation template (`CR003_Accepted_<Topic>.md`).

---

## Publication Notice

RAIkeep will notify AIA immediately when all six v4.0.0 NuGet packages are
visible and the sequential publication chain has completed.