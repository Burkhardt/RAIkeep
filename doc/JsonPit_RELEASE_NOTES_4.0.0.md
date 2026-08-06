# Release Notes: JsonPit v4.0.0

**Date:** 2026-08-05  
**Author / Delivering Agent:** RAIkeep Dev Agent  
**Delivered Version:** v4.0.0  
**Target Consumers:** AIA, AfricaStage, PitSeeder  
**Status:** Implemented — coordinated 4.0.0 line; NuGet publication pending release authorization

---

## 1. Summary

JsonPit 4.0.0 makes RAIkeep's concurrency behavior explicit, testable, and enforceable
across threads in one process, processes on one machine, and machines sharing
cloud-synced pit files. It fixes the confirmed concurrent save-and-add persistence
race, introduces exact-process master ownership, one-live-instance path ownership,
validated candidate loads, collision-safe hashed change files, and live split-master
recovery with structured durable audit events.

## 2. Resolved Change Requests (CRs)

- [`CR003_RAI_to_RAIkeep_JsonPit-concurrency-contract-and-persistence-races.md`](CR003_RAI_to_RAIkeep_JsonPit-concurrency-contract-and-persistence-races.md) — the governing concurrency contract, together with its accepted supporting design [`JsonPit-CONCEPT-Live-Split-Master-Recovery.md`](JsonPit-CONCEPT-Live-Split-Master-Recovery.md) and implementation companion `Details of CR003.md`.

## 3. Root Cause Analysis & Technical Resolution

### Confirmed regression — concurrent save and add

`Store()` applied LINQ ordering and materialization directly to live `HistoricItems`
while concurrent `Add` operations mutated the same `ConcurrentDictionary`
(`IndexOutOfRangeException`, `ArgumentException` from `CopyTo`). It then validated the
*live latest* fragments after I/O, so a fragment accepted after the written snapshot
could be marked persisted prematurely — a silent-loss window.

**Resolution — the agreed v4.0.0 persistence boundary:**
- A `ReaderWriterLockSlim` state/snapshot gate: concurrent `Add` calls enter shared
  mode (never serialized behind cloud I/O); `Save` takes brief exclusive access,
  captures a byte-stable snapshot (fragments cloned inside the gate) plus the exact
  set of included dirty fragments and the snapshot change time, and releases the gate
  before serialization, cloud-file I/O, and flag updates.
- Only fragments demonstrably included in the persisted snapshot are validated; flag
  metadata is computed from snapshot facts, never newer live state. A later addition
  keeps its existing per-fragment dirty state until a snapshot containing it persists.
  No second pending-write queue was introduced.
- The regression test `SaveInterleavedWithAdds_SubsequentSavePersistsEveryAcceptedItem`
  passes repeatedly.

### Deterministic equal-timestamp and replay behavior

- Live `Add` refreshes `Modified` from real `DateTimeOffset.UtcNow` once at the
  insertion boundary (not restamped on CAS retries); `AddHistorical` preserves supplied
  timestamps; uniqueness is not promised and nothing depends on it. No monotonic clock
  or injected time source was added.
- History order: `Modified` descending → fewer JSON properties first → canonical
  content ordinal tie-break (computed only for the double-tie case). Exact replay of a
  fragment already in history is idempotent and consumes no bounded-history slot.
  Projection keeps first-seen precedence; every participant computes the same result
  from the same fragments in any arrival order (`PitItems.CompareFragments` is public).

### One live public `Pit` per canonical path per process

- A process-wide registry reserves the canonical path before the constructor performs
  observable pit work; a duplicate (writable or read-only) throws the descriptive
  `PitInstanceConflictException`. `Dispose` releases the reservation; constructor
  failure never leaves a stale one. Internal comparison/merge paths use private
  snapshot readers — the former internal `new Pit(...)` constructions are gone.

### Read-during-write contract

- `Load`/`Reload` build a complete validated candidate and replace live state only
  after the entire canonical snapshot parsed successfully; fragments from a validated
  canonical enter clean. Transient absence, emptiness, or unparseable content during a
  known rewrite is retried without clearing state; bounded exhaustion throws the
  descriptive `JsonPitPersistenceException`. Initial absence remains a valid no-data
  case. The former `Reload` "changed without permission" exception is obsolete under
  exact-PID ownership: a master-time advance while this exact process is the recorded
  owner is its own earlier write, handled by reloading.

### Exact-process master ownership and handoff

- `Master.flag` records `{Machine}-{Subscriber}-{PID}`; only the exact owner renews.
  A second PID of the same participant is refused while the owner's process window is
  active (change-file fallback) and inherits the still-protected lease after explicit
  release or expiry. Different subscribers remain distinct participants. No
  operating-system or distributed file lock was added.

### Collision-safe change files, merge, and cleanup

- Every ordinary change file uses `{Modified.UtcTicks}_{ExactProcessIdentity}_{Sha256}.json`
  with the hash over the exact canonical UTF-8 payload (no trailing terminator);
  republication is filename-idempotent, equal-time fragments cannot suppress one
  another, and merge requires hash+parse validation. Legacy `{ticks}_{identity}.json`
  files are still ingested (parse-validated) for upgrade compatibility but are never
  credited with the hash guarantee.
- Cleanup is a current-master-only two-stage protocol: merge → successful canonical
  save accounting for the fragment → in-memory eligibility → ten-minute grace measured
  from that save (settable `Pit.ChangeFileCleanupGrace`, production default 10 min).
  Original file age no longer counts; restart or master transfer resets eligibility.
  The former age-based delete-before-store path is removed.

### Live split-master recovery (concept)

- Per-tenure in-memory recovery write set: fragments newly persisted by a master save
  are recorded before being marked clean; entries transfer out per fragment once an
  ordinary change file is locally written, materialized, hash-verified, and parsed.
- Native `FileSystemWatcher` per live writable flagged pit for `Master*.flag`
  (provider-independent longer-name signal, no suffix parsing, no provider API);
  callbacks only debounce and queue one recovery evaluation; construction, master
  acquisition, `Save`, and `Reload` also scan — no polling loop.
- Live loser: stops canonical writes, publishes the write-set/dirty union as ordinary
  small change files, and deletes only the longer flag naming itself after all files
  validate locally. Exact `Master.flag` is never deleted or altered.
- Orphaned signal: only the exact current master retires it, after claimant window
  expiry plus `Pit.OrphanedConflictFlagGrace` (default 10 min) and a locally validated
  `Critical` evidence event. Noncanonical `Object*.pit` copies are never inspected.
- Live authority transfer to another exact process exports the completed tenure's
  write set as change files; same-process reacquisition does not.
- Explicit disposal is a durability boundary: change files first, optional canonical
  save if still exact master, then release of process authority, watcher, and path
  registration. Failure to make accepted fragments durable during explicit shutdown is
  `Critical` and throws. Finalizers perform no filesystem I/O; crash/power loss before
  export remains the explicitly accepted data-loss gap.

### Recovery diagnostics

- Immutable `Pit.LastRecoveryStatus` plus optional `RecoveryStatusChanged` event; no
  subscriber is required for correctness. Stages: ConflictDetected(Warning),
  RoleDetermined(Information), ChangeFilesPublished(Information),
  Canonicalized(Information), CleanupPending(Debug), Completed(Information),
  DeferredForRetry(Warning), Failed(Error); explicit-shutdown durability failure is
  Critical; `None` is never written.
- Durable events are canonical-JSON `.event` files under the pit's `Events` child via
  OsLib `EventFile`, stem `{UtcTicks}_{ExactProcessIdentity}_{Stage}`. `PitAudit.Read`
  provides filtered read-only access (machine all/local/named; inclusive minimum
  `LogLevel`), ordered by machine, UTC time, and event identity.

## 4. Public Contract & API / Package Changes

- New: `PitInstanceConflictException`, `JsonPitPersistenceException`,
  `RecoveryStage`, `RecoveryRole`, `RecoveryStatus`, `PitAuditEvent`, `PitAudit`,
  `ChangeFile` (naming/validation), `Pit.LastRecoveryStatus`,
  `Pit.RecoveryStatusChanged`, `Pit.ExactProcessIdentity` (public, with
  `ParticipantIdentity` now public), `Pit.ChangeFileCleanupGrace`,
  `Pit.OrphanedConflictFlagGrace`, `Pit.RecoveryDebounce`,
  `PitItems.CompareFragments` (public deterministic comparator),
  `MasterFlagFile.ParticipantOf/IsExactProcessIdentity/ConflictFlags`,
  `ProcessFlagFile.IsProcessWindowActive/ProcessWindowTime`.
- Changed behavior: `Master.flag` owner value is the exact process identity
  (legacy participant-only values are handled during upgrade); `CreateChangeFile`
  returns the created `RaiFile` and writes hashed names; a second live public `Pit`
  per canonical path throws; `Load` throws on bounded retry exhaustion instead of
  returning false; `Reload` no longer throws the "changed without permission"
  exception; `Dispose` performs the full durability sequence.
- Fallback dependency alignment: `OsLibCore 4.0.0`, `RaiUtils 3.13.1`.

## 5. Validation & Acceptance Evidence

Machine configuration is the sole source of truth; all concurrency suites run on real
configured cloud roots (no local substitutes, DI, or environment overrides). Ordinary
suites remain non-parallel (`CollectionBehavior(DisableTestParallelization = true)`).

- Umbrella `RAIkeep.slnx` (excluding the two SSH remote scenarios): **359 passed, 0 failed, 0 skipped**
  (RaiUtils 21, OsLib 80, ImgSeeder 8, pits 13, RaiImage 94, JsonPit 143).
- Recorded full acceptance run (all suites including both SSH scenarios): 361 passed,
  1 failed, 0 skipped. The single failure was `RemoteSyncTests` exhausting its 600 s
  OneDrive propagation window for the Mzansi-bound merged pit while the remaining
  suites concurrently churned the same cloud root — an environmental propagation
  variance, not a contract violation; the scenario passed standalone immediately
  before (1 m 26 s) and immediately after (2 m 0 s), and the split-master scenario
  passed inside the combined run as well.
- New explicit suites (provider OneDrive, machine Nkosikazi):
  `InProcessConcurrencyTests`, `MultiPitInstanceConcurrencyTests`,
  `MultiProcessConcurrencyTests`, `EqualTimestampOrderingTests`,
  `ReadDuringWriteTests`, `SplitMasterRecoveryTests` — 39 passed, 0 failed, 0 skipped.
- Two-server split-master scenario
  (`RemoteCloudConcurrencyTests.TwoServerSplitMaster_LiveLocalLoser_RecoversThroughProviderSyncedConflictSignal`),
  provider OneDrive, machines Nkosikazi (local claimant `Nkosikazi-cr003-82853`) and
  Mzansi (remote claimant `Mzansi-cr003-777777`): local claim reached Mzansi in 6.1 s;
  remote conflict artifacts (`Master.flag` + `Master (1).flag`) written at +9.3 s;
  conflict signal materialized locally and the live loser published its recovery write
  set as validated ordinary change files
  (`639215809514405680_Nkosikazi-cr003-82853_424fbd….json`,
  `639215809514602540_Nkosikazi-cr003-82853_715a00….json`), retired only its longer
  conflict flag, left canonical `Master.flag` naming the remote winner, and wrote 6
  durable audit events — total scenario time 19.3 s. **Passed.**
- Dynamic master/non-master remote scenario (`RemoteSyncTests.RemoteSync_MasterClient_FullScenario`,
  provider OneDrive, Nkosikazi + Mzansi running pits v4.0.0): **passed in 1 m 26 s** —
  pit creation and master claim on Nkosikazi; Mzansi as non-master producing hashed
  change files (canonical→Mzansi sync 5.8 s, change files back 0.0–13.6 s); master
  merge of both entries; exact-PID master transfer to `Mzansi-pits-1978308` after
  simulated ticket expiry (observed locally in 10.0 s); Nkosikazi reading all three
  entries; and the two-stage current-master-only cleanup (files retained through the
  post-save grace, deleted only on the later pass, data integrity preserved).
- Cross-process exact-PID inheritance proven with real separate CLI processes in
  `pits.Tests.LocalCliTicketWindowTests`.

## 6. Upgrade & Consumption Instructions

- Consume `JsonPit 4.0.0` together with `OsLibCore 4.0.0`.
- Applications must hold **one** live `Pit` per canonical pit path per process (via
  their singleton/keyed container) and `Dispose()` it before reopening; a duplicate
  now throws `PitInstanceConflictException` instead of silently misbehaving.
- `Dispose()` of a writable pit now performs the durability export; call it on
  shutdown paths (finalizers intentionally do nothing).
- Treat `JsonPitPersistenceException` from `Load`/`Reload`/`Save`/`Dispose` as an
  operational signal — prior in-memory state is preserved when loading fails.
- Mixed-version fleets: 4.0.0 reads legacy change files, but pre-4.0.0 processes can
  fail on 4.0.0 hashed change files; upgrade all participants of a shared pit
  together (the coordinated release requirement).
