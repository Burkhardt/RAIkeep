# JsonPit Release Notes 3.x

## 3.13.2

**Date:** 2026-08-05  
**Author / Delivering Agent:** RAIkeep Dev Agent  
**Delivered Version:** v3.13.2  
**Target Consumers:** AIA, AfricaStage, PitSeeder  
**Status:** Implemented — coordinated 3.13.2 line; NuGet publication pending release authorization

---

### 1. Summary

JsonPit 3.13.2 makes RAIkeep's concurrency behavior explicit, testable, and enforceable
across threads in one process, processes on one machine, and machines sharing
cloud-synced pit files. It fixes the confirmed concurrent save-and-add persistence
race, introduces exact-process master ownership, one-live-instance path ownership,
validated candidate loads, collision-safe hashed change files, and live split-master
recovery with structured durable audit events.

### 2. Resolved Change Requests (CRs)

- [`CR003_RAI_to_RAIkeep_JsonPit-concurrency-contract-and-persistence-races.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR003_RAI_to_RAIkeep_JsonPit-concurrency-contract-and-persistence-races.md) — the governing concurrency contract, together with its accepted supporting design [`JsonPit-CONCEPT-Live-Split-Master-Recovery.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/JsonPit-CONCEPT-Live-Split-Master-Recovery.md) and implementation companion `Details of CR003.md`.

### 3. Root Cause Analysis & Technical Resolution

#### Confirmed regression — concurrent save and add

`Store()` applied LINQ ordering and materialization directly to live `HistoricItems`
while concurrent `Add` operations mutated the same `ConcurrentDictionary`
(`IndexOutOfRangeException`, `ArgumentException` from `CopyTo`). It then validated the
*live latest* fragments after I/O, so a fragment accepted after the written snapshot
could be marked persisted prematurely — a silent-loss window.

**Resolution — the agreed v3.13.2 persistence boundary:**
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

#### Deterministic equal-timestamp and replay behavior

- Live `Add` refreshes `Modified` from real `DateTimeOffset.UtcNow` once at the
  insertion boundary (not restamped on CAS retries); `AddHistorical` preserves supplied
  timestamps; uniqueness is not promised and nothing depends on it. No monotonic clock
  or injected time source was added.
- History order: `Modified` descending → fewer JSON properties first → canonical
  content ordinal tie-break (computed only for the double-tie case). Exact replay of a
  fragment already in history is idempotent and consumes no bounded-history slot.
  Projection keeps first-seen precedence; every participant computes the same result
  from the same fragments in any arrival order (`PitItems.CompareFragments` is public).

#### One live public `Pit` per canonical path per process

- A process-wide registry reserves the canonical path before the constructor performs
  observable pit work; a duplicate (writable or read-only) throws the descriptive
  `PitInstanceConflictException`. `Dispose` releases the reservation; constructor
  failure never leaves a stale one. Internal comparison/merge paths use private
  snapshot readers — the former internal `new Pit(...)` constructions are gone.

#### Read-during-write contract

- `Load`/`Reload` build a complete validated candidate and replace live state only
  after the entire canonical snapshot parsed successfully; fragments from a validated
  canonical enter clean. Transient absence, emptiness, or unparseable content during a
  known rewrite is retried without clearing state; bounded exhaustion throws the
  descriptive `JsonPitPersistenceException`. Initial absence remains a valid no-data
  case. The former `Reload` "changed without permission" exception is obsolete under
  exact-PID ownership: a master-time advance while this exact process is the recorded
  owner is its own earlier write, handled by reloading.

#### Exact-process master ownership and handoff

- `Master.flag` records `{Machine}-{Subscriber}-{PID}`; only the exact owner renews.
  A second PID of the same participant is refused while the owner's process window is
  active (change-file fallback) and inherits the still-protected lease after explicit
  release or expiry. Different subscribers remain distinct participants. No
  operating-system or distributed file lock was added.

#### Collision-safe change files, merge, and cleanup

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

#### Live split-master recovery (concept)

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

#### Recovery diagnostics

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

### 4. Public Contract & API / Package Changes

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
- Fallback dependency alignment: `OsLibCore 3.13.2`, `RaiUtils 3.13.1`.

### 5. Validation & Acceptance Evidence

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
  provider OneDrive, Nkosikazi + Mzansi running pits v3.13.2): **passed in 1 m 26 s** —
  pit creation and master claim on Nkosikazi; Mzansi as non-master producing hashed
  change files (canonical→Mzansi sync 5.8 s, change files back 0.0–13.6 s); master
  merge of both entries; exact-PID master transfer to `Mzansi-pits-1978308` after
  simulated ticket expiry (observed locally in 10.0 s); Nkosikazi reading all three
  entries; and the two-stage current-master-only cleanup (files retained through the
  post-save grace, deleted only on the later pass, data integrity preserved).
- Cross-process exact-PID inheritance proven with real separate CLI processes in
  `pits.Tests.LocalCliTicketWindowTests`.

### 6. Upgrade & Consumption Instructions

- Consume `JsonPit 3.13.2` together with `OsLibCore 3.13.2`.
- Applications must hold **one** live `Pit` per canonical pit path per process (via
  their singleton/keyed container) and `Dispose()` it before reopening; a duplicate
  now throws `PitInstanceConflictException` instead of silently misbehaving.
- `Dispose()` of a writable pit now performs the durability export; call it on
  shutdown paths (finalizers intentionally do nothing).
- Treat `JsonPitPersistenceException` from `Load`/`Reload`/`Save`/`Dispose` as an
  operational signal — prior in-memory state is preserved when loading fails.
- Mixed-version fleets: 3.13.2 reads legacy change files, but pre-3.13.2 processes can
  fail on 3.13.2 hashed change files; upgrade all participants of a shared pit
  together (the coordinated release requirement).

---

## 3.13.1

### Summary

`JsonPit 3.13.1` separates per-process activity windows from the stable master-writer lease and adds ownership-verified cleanup for finite clients such as PitSeeder.

### Flag-file lifecycle

- Process activity files now use `{Machine}-{Subscriber}-{PID}.flag`, giving each OS process its own activity window in every pit it opens.
- The stable `{Machine}-{Subscriber}` participant identity remains the value used in the single `Master.flag` writer lease for each pit.
- Added `ProcessFlagFile.CurrentFlagName(...)`, `IsOwnedByCurrentProcess`, and `TryReleaseCurrentProcess()`.
- Added `Pit.TryReleaseProcessWindow()`. It expires only a flag whose content still identifies the current process and never modifies `Master.flag`.
- Explicit release writes the Unix epoch in place. The expired flag remains as a diagnostic tombstone instead of causing a cloud-sensitive delete/recreate cycle.
- Successful flagged loads refresh process activity with the current time.
- Constructor failures attempt to release any process activity window created before construction failed.

### File handling

- Master and process flag updates now use `TextFile.SaveInPlace()` through OsLib.
- Canonical pit modification time is read through `RaiFile.LastWriteTimeUtc`; JsonPit no longer performs a direct `System.IO.FileInfo` read.
- Physical last-write time remains the real filesystem/cloud write time and is not rewritten to a logical item timestamp.

### Other carried-forward behavior

- Fallback dependencies are aligned to `OsLibCore 3.13.1` and `RaiUtils 3.13.1`.
- `PitItem.DeleteProperty(...)` retains its top-level tombstone projection behavior.
- Corrected the XML API reference for historical replay to `AddHistorical(PitItem)`.

### Compatibility and operational notes

- Process flag filenames change from a stable subscriber filename to a per-PID filename. Monitoring or cleanup tools that inspect flag names must account for the PID suffix.
- Expired process flag tombstones can accumulate; this is an accepted trade-off to avoid delete/recreate synchronization races.
- `Master.flag` remains a timed participant lease, not a per-PID mutex. Releasing a process activity window does not return or release master ownership.
- The existing flag mechanism and its current concurrency boundary are documented in [`JsonPit-FlagFiles-And-Concurrency.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/JsonPit-FlagFiles-And-Concurrency.md).
- The separate annotated concurrency CR remains open and is not implemented by this release work.

### Validation

- Umbrella `RAIkeep.slnx` build succeeds with `0` warnings and `0` errors after the XML reference correction.
- JsonPit local selection: `103` passed, `0` failed, excluding the test owned by the separate open concurrency CR and the external remote-sync scenario.
- The external OneDrive remote-sync scenario passed on its immediate isolated rerun.
- Master-ticket coverage verifies per-PID naming, ownership rejection, epoch release, and preservation of `Master.flag`.

### Release sequencing

`JsonPit` is fourth in the coordinated release chain. Its GitHub push/tag must wait for RaiImage workflow success, flat-container visibility, and the full `330`-second hold. `ImgSeeder` must wait for the same checks after JsonPit publishes.

---

## 3.12.1

### Summary

- Releases `JsonPit` version `3.12.1`.
- Aligns fallback package references to `OsLibCore 3.12.1` and `RaiUtils 3.12.1`.
- Carries forward the current concurrency coverage, packaged docs, and class-diagram release markers for the coordinated package line.
- Carries forward `PitItem.DeleteProperty(...)` projection semantics: top-level null fragments act as attribute tombstones, so projected reads omit the deleted property instead of exposing a permanent null shadow.
- No public API changes from `3.12.0`.

### Validation

- `dotnet test JsonPit.Tests/JsonPit.Tests.csproj --nologo -v minimal`
- NuGet publishing remains wired through the parent sequential release chain and the tag-triggered `publish-nuget.yml` workflow.

---

## 3.12.0

### Summary

- Releases `JsonPit` version `3.12.0`.
- Aligns fallback package references to `OsLibCore 3.12.0` and `RaiUtils 3.12.0`.
- Carries forward the current concurrency coverage, packaged docs, and class-diagram release markers for the coordinated package line.
- Carries forward `PitItem.DeleteProperty(...)` projection semantics: top-level null fragments act as attribute tombstones, so projected reads omit the deleted property instead of exposing a permanent null shadow.
- No public API changes from `3.11.5`.

### Validation

- `dotnet test JsonPit.Tests/JsonPit.Tests.csproj --nologo -v minimal`
- NuGet publishing remains wired through the parent sequential release chain and the tag-triggered `publish-nuget.yml` workflow.

---

## 3.11.4

### Summary

- Releases `JsonPit` version `3.11.4`.
- Aligns fallback package references to `OsLibCore 3.11.4` and `RaiUtils 3.11.4`.
- Carries forward the current concurrency coverage, packaged docs, and class-diagram release markers for the coordinated package line.
- Fixes `PitItem.DeleteProperty(...)` projection semantics: top-level null fragments now act as attribute tombstones, so projected reads omit the deleted property instead of exposing a permanent null shadow.
- No public API changes from `3.11.3`.

### Validation

- `dotnet test JsonPit.Tests/JsonPit.Tests.csproj --filter FullyQualifiedName~DeletePropertyProjectionTests --nologo -v minimal`
- `dotnet test JsonPit.Tests/JsonPit.Tests.csproj --nologo -v minimal`
- NuGet publishing remains wired through the parent sequential release chain and the tag-triggered `publish-nuget.yml` workflow.

---

## 3.11.2

### Summary

- Releases `JsonPit` version `3.11.2`.
- Aligns fallback package references to `OsLibCore 3.11.2` and `RaiUtils 3.11.2`.
- Carries forward the current concurrency coverage, packaged docs, and class-diagram release markers for the coordinated package line.
- No public API changes from `3.11.1`.

### Validation

- `dotnet build JsonPit.csproj --nologo -v minimal`
- NuGet publishing remains wired through the parent sequential release chain and the tag-triggered `publish-nuget.yml` workflow.

---

## 3.11.1

### Summary

- Releases `JsonPit` version `3.11.1`.
- Aligns fallback package references to `OsLibCore 3.11.1` and `RaiUtils 3.11.1`.
- Carries forward the current concurrency coverage, packaged docs, and class-diagram release markers for the coordinated package line.
- Fixes ticket ownership to use participant identity (`Machine-Subscriber`) so same-machine peers (for example `Neo-pits` and `Neo-AfricaStage.Api`) no longer collapse into one master owner.
- Ensures non-owner writers within the active ticket window persist change files instead of writing the canonical pit directly.
- Adds regression coverage for same-machine API/CLI ticket-window handoff and change-file fallback behavior.

### Validation

- `dotnet build JsonPit.csproj --nologo -v minimal`
- NuGet publishing remains wired through the parent sequential release chain and the tag-triggered `publish-nuget.yml` workflow.

---

## 3.11.0

### Summary

- Releases `JsonPit` version `3.11.0`.
- Aligns fallback package references to `OsLibCore 3.11.0` and `RaiUtils 3.11.0`.
- Carries forward the current concurrency coverage, packaged docs, and class-diagram release markers for the coordinated package line.
- No JsonPit API changes from `3.10.2`.

### Validation

- `dotnet build JsonPit.csproj --nologo -v minimal`
- NuGet publishing remains wired through the parent sequential release chain and the tag-triggered `publish-nuget.yml` workflow.

---

## 3.10.2

### Summary

- Releases `JsonPit` version `3.10.2`.
- Adds and tightens concurrency regression test coverage.
- Aligns fallback package references to `OsLibCore 3.10.2` and `RaiUtils 3.10.2`.
- Refreshes current package metadata, docs, and class-diagram release markers for the coordinated package line.

### Validation

- `dotnet build JsonPit.csproj --nologo -v minimal`
- NuGet publishing remains wired through the parent sequential release chain and the tag-triggered `publish-nuget.yml` workflow.

---

## 3.10.1

### Summary

- Releases `JsonPit` version `3.10.1`.
- Aligns fallback package references to `OsLibCore 3.10.1` and `RaiUtils 3.10.1`.
- Refreshes current package metadata, docs, and class diagram release markers for the coordinated package line.
- No public API changes from `3.10.0`.

### Validation

- `dotnet build JsonPit.csproj --nologo -v minimal`
- NuGet publishing remains wired through the parent sequential release chain and the tag-triggered `publish-nuget.yml` workflow.

---

## 3.10.0

### Summary

- Releases `JsonPit` version `3.10.0`.
- Aligns fallback package references to `OsLibCore 3.10.0` and `RaiUtils 3.10.0`.
- Refreshes package metadata, docs, and class diagram release markers for the coordinated minor line.
- No public API changes from `3.9.1`.

### Validation

- `dotnet build JsonPit.csproj --nologo -v minimal`
- NuGet publishing remains wired through the tag-triggered `publish-nuget.yml` workflow.

---

## 3.9.1

### Summary

- Releases `JsonPit` version `3.9.1`.
- Aligns fallback package references to `OsLibCore 3.9.1` and `RaiUtils 3.9.1`.
- Refreshes package metadata, docs, and class diagram release markers for the coordinated patch line.
- No public API changes from `3.9.0`.

### Validation

- `dotnet build JsonPit.csproj --nologo -v minimal`
- NuGet publishing is handled by the tag-triggered `publish-nuget.yml` workflow.

---

## 3.9.0

### Summary

- Releases `JsonPit` version `3.9.0`.
- Aligns fallback package references to `OsLibCore 3.9.0` and `RaiUtils 3.9.0`.
- Refreshes markdown docs and class-diagram release markers for the coordinated minor line.
- No JsonPit API changes from `3.8.15`.

### Validation

- `dotnet test JsonPit.Tests/JsonPit.Tests.csproj --nologo -v minimal`
- NuGet publishing is handled by tag-triggered `publish-nuget.yml`.

---

## 3.8.15

### Summary

- Releases `JsonPit` version `3.8.15`.
- Aligns fallback package references to `OsLibCore 3.8.15` and `RaiUtils 3.8.15`.
- Refreshes markdown docs and class-diagram release markers for the coordinated chain.

### Validation

- `dotnet test JsonPit.Tests/JsonPit.Tests.csproj --nologo -v minimal`
- NuGet publishing is handled by tag-triggered `publish-nuget.yml`.

---

## 3.8.14

### Summary

- Releases `JsonPit` version `3.8.14`.
- Aligns fallback package references to `OsLibCore 3.8.14` and `RaiUtils 3.8.14`.
- Refreshes markdown docs and class-diagram release markers for the coordinated chain.

### Validation

- `dotnet test JsonPit.Tests/JsonPit.Tests.csproj --nologo -v minimal`
- NuGet publishing is handled by tag-triggered `publish-nuget.yml`.

---

## 3.8.12

### Summary

- Releases `JsonPit` version `3.8.12`.
- Aligns fallback package references to `OsLibCore 3.8.12` and `RaiUtils 3.8.12`.
- Refreshes live README links and PlantUML release markers for the coordinated `RAIkeep` patch line.
- No JsonPit API or persistence behavior changes from `3.8.11`.

### Validation

- `dotnet test RAIkeep.slnx --nologo -v minimal`: 243 passed, 0 failed, 1 skipped.
- NuGet publishing is handled by the RAIkeep Sequential NuGet Release Chain.

---

## 3.8.11

### Summary

- Releases `JsonPit` version `3.8.11`.
- Aligns fallback package references to `OsLibCore 3.8.11` and `RaiUtils 3.8.11`.
- Refreshes live markdown release-line references and tracked PlantUML release markers for the `3.8.11` line.

### Validation

- Release published through GitHub Actions tag workflow.
- NuGet visibility is verified in the sequential release chain.

---

## 3.8.6

### Summary

- Coordinated release for `JsonPit` version `3.8.6`.
- Refreshes markdown release-line references (including `README.md`) via automated scan.
- Refreshes all tracked PlantUML (`.puml`) release/version markers found in scope.

### Validation

- Release published through GitHub Actions tag workflow.
- NuGet visibility is verified in the sequential release chain.

---

## 3.8.1

### Summary

- Coordinated release for `JsonPit` version `3.8.1`.
- Aligns fallback package references with `OsLibCore 3.8.1` and `RaiUtils 3.8.1`.
- Keeps the packaged README in the NuGet payload.
- Refreshes current docs and class-diagram headers without changing the `PitItem.Id` contract or persistence behavior.

### Documentation

- Updated `README.md`, `GettingStarted.md`, and `Requirements.md` to the `3.8.1` package line.
- Refreshed `JsonPit-ClassDiagram.puml` so the current diagram header matches the live release line.

### Validation

- `dotnet test JsonPit.slnx --nologo -v minimal`
- Result: 84 passed, 0 failed, 0 skipped.

---

## 3.8.0

### Summary

- Coordinated release for `JsonPit` version `3.8.0`.
- Aligns fallback package references with `OsLibCore 3.8.0` and `RaiUtils 3.8.0`.
- Keeps the packaged README in the NuGet payload.
- Refreshes current docs and class-diagram headers without changing the `PitItem.Id` contract or persistence behavior.

### Documentation

- Updated `README.md`, `GettingStarted.md`, and `Requirements.md` to the `3.8.0` package line.
- Refreshed `JsonPit-ClassDiagram.puml` so the current diagram header matches the live release line.

### Validation

- `dotnet test JsonPit.slnx --nologo -v minimal`
- Result: 83 passed, 0 failed, 1 skipped.

---

## 3.7.9

### Summary

- Patch release for `JsonPit` version `3.7.9`.
- Aligns fallback package references with `OsLibCore 3.7.9` and `RaiUtils 3.7.9`.
- Refreshes current docs and class-diagram headers without changing the `PitItem.Id` contract or persistence behavior.

### Documentation

- Updated `README.md`, `GettingStarted.md`, and `Requirements.md` to the `3.7.9` package line.
- Refreshed `JsonPit-ClassDiagram.puml` so the current diagram header matches the live release line.

### Validation

- `dotnet test RAIkeep.slnx --nologo -v minimal`
- Result: 220 passed, 0 failed, 0 skipped.

---

## 3.7.7

### Summary

- Patch release for `JsonPit` version `3.7.7`.
- Aligns fallback package references with `OsLibCore 3.7.7` and `RaiUtils 3.7.7`.
- Refreshes current docs and class-diagram headers without changing the `PitItem.Id` contract or persistence behavior.

### Documentation

- Updated `README.md`, `GettingStarted.md`, and `Requirements.md` to the `3.7.7` package line.
- Refreshed `JsonPit-ClassDiagram.puml` so the current diagram header matches the live release line.

### Validation

- `dotnet test RAIkeep.slnx --nologo -v minimal`
- Result: 214 passed, 0 failed, 0 skipped.

---

## 3.7.6

### Summary

- Patch release for `JsonPit` version `3.7.6`.
- Aligns fallback package references with `OsLibCore 3.7.6` and `RaiUtils 3.7.6`.
- Keeps the current `PitItem.Id` identifier contract and supported cloud-provider claim intact.

### Documentation

- Current docs now align on `RAIkeep.json5` for shared config.
- Remote-sync guidance now reflects OsLib's configurable metadata propagation delay handling.

---

## 3.7.3

**Date:** March 31, 2026
**Scope:** Full code review and rewrite of `JsonPit.cs` — correctness, thread safety, cloud drive safety, and structural improvements.

---

### Summary

This release is the result of a comprehensive review of `JsonPit.cs` conducted collaboratively between Rainer and Claude (Anthropic). Every class in the file was examined for correctness, thread safety, adherence to OsLib conventions, and compatibility with cloud-synced filesystems. The changes strengthen JsonPit's core promise of
[*asynchronous persistence with eventual durability*](https://github.com/Burkhardt/RAIkeep/blob/main/MANIFESTO.md#asynchronous-persistence-with-eventual-durability)
across multiple machines sharing a cloud-synced filesystem.

---

### Bug Fixes

#### `GetLatestItemChanged` returned the oldest item, not the newest

The previous implementation sorted descending then called `.Last()`, which returned the minimum rather than the maximum. Replaced with `.Max()` for clarity and correctness. Method also renamed from `GetLastestItemChanged` to `GetLatestItemChanged` (typo fix).

#### `DiskHasNewerChanges` renamed for clarity

Formerly `FileHasChangedOnDisk`. The logic was correct — returns `false` if the file doesn't exist on disk, and `true` if the disk timestamp is newer than memory — but the old name suggested "has the file changed" rather than "does disk have newer data than memory."

#### Duplicate `CreateChangeFile` methods consolidated

Two `CreateChangeFile` methods existed: a private one writing `.json` and a public one writing `.pit` in nested subdirectories. Consolidated into a single public method that writes `.json` files flat in the `Changes` directory. The method accepts an optional `machineName` parameter for testability (simulating change files from other machines).

#### `EnumerateChangeFiles` now searches for `*.json`

Previously searched for `*.pit`, which was inconsistent with the new `CreateChangeFile` implementation. Renamed from `EnumerateChangePitFiles` to `EnumerateChangeFiles` and updated the search pattern to `*.json`.

#### `Invalid()` uses `.Any()` instead of `.Count() > 0`

Minor but avoids full enumeration when only existence is needed.

---

### Thread Safety Improvements

#### `_locker` and `usingPersistence` moved from static to instance-level

Previously, all `Pit` instances across the entire process shared a single lock and semaphore. This meant unrelated Pit files would block each other — including the read-only compare instance created inside `CreateChangeFiles`. Both are now instance fields.

#### `MasterFlagFile.Locker` moved from static to instance-level

Same issue as above. The lock is still used to serialize writes to individual flag files, but no longer blocks unrelated flag file instances.

#### Redundant inner lock removed from `CreateChangeFiles`

`Save()` already acquires `_locker` before calling `CreateChangeFiles()`. The inner `lock(_locker)` was redundant (though not harmful due to `Monitor` reentrancy). Removed for clarity.

#### `PitItems.MaxCount` changed to `init` setter

`PitItems` is designed as an immutable type (all mutation returns new instances via `Push`). The `MaxCount` property had a public setter that broke this contract. Changed to `init` so it can only be set during construction.

---

### Cloud Drive Safety

#### `Store` no longer uses tmp-file-then-rename pattern

**This is a critical change.** The previous implementation wrote to a temporary file and then moved it to replace the original — a pattern that is standard for local filesystems but dangerous on cloud-synced directories.

When a file is deleted (or renamed away) and a new file appears in its place, the cloud provider sees the original file disappear. The milliseconds between deletion and replacement are often enough for the provider to detect a conflict, producing duplicate files like `"MyJsonPit (1).pit"`. This has been confirmed through years of production experience with Dropbox-backed infrastructure.

The fix: write directly to the original file handle via `TextFile`. The file never disappears from the cloud provider's perspective. The master/client philosophy already prevents simultaneous writes from multiple machines, so the atomicity guarantee of rename is unnecessary.

**This pattern must never be reintroduced in any code that writes to cloud-synced filesystem areas.**

#### `ExportJson` updated to use `TextFile`

Previously used `File.WriteAllText` directly. Now uses `TextFile` consistent with the OsLib abstraction layer and cloud drive safety.

---

### Structural Improvements

#### `PitItem` implements `IEquatable<PitItem>`

The previous `PitItemExtensions.Equals` extension method shadowed `object.Equals` and was never called as an extension — only explicitly via `PitItemExtensions.Equals(d1, d2)`. Equality is now implemented directly on `PitItem` with proper `Equals`, `GetHashCode`, and `IEquatable<PitItem>` support.

**Note:** `GetHashCode` uses exact ticks (not fuzzy `isLike` matching) to maintain the contract that equal objects must produce equal hash codes. The `isLike` extension remains available for explicit use cases that need timestamp tolerance.

#### `ChangeDir` renamed to `ChangesDir` with lazy initialization

The property previously called `mkdir()` on every access — surprising side-effect behavior for a property getter. Now uses a cached backing field, creating the directory only on first access.

#### `Pit` implements `IDisposable`, replacing the finalizer

Finalizers run on the GC thread non-deterministically. Calling `Save` from `~Pit()` could fail silently or encounter already-collected dependencies. The class now implements `IDisposable` with the standard dispose pattern. The finalizer remains as a safety net but only calls `Dispose(false)`.

#### `MergeChanges` deletes individual files, not directory trees

Previously used `rmdir(depth: 10, deleteFiles: true)` on the parent directory of each change file, which could delete the entire `Changes` directory including pending change files from other machines. Now deletes individual change files after processing (master only, after 600-second grace period).

#### `Item` class marked `[Obsolete]`

`Item` and `PitItem` had nearly identical interfaces (Id, Modified, Deleted, Note, Dirty, Delete, Invalidate, Validate) but no inheritance relationship. `PitItem` extends `JObject` and is strictly more capable. `Item` is now marked obsolete with guidance to use `PitItem` instead.

#### `CompareToOtherHistory` rewritten for correctness

The original implementation used `Enumerable.Except` which relied on reference equality for `PitItem` objects (since `PitItem` extends `JObject`). This meant the diff would almost always return everything from the left side regardless of actual differences. The rewrite uses an explicit `HashSet<(string Id, DateTimeOffset Modified)>` for fast, correct identity matching.

---

### OsLib Compliance

JsonPit now uses OsLib abstractions (`RaiFile`, `RaiPath`, `TextFile`, `RaiDir`) instead of `System.IO` direct calls wherever possible. Three remaining `System.IO` usages are marked with `// TODO: Rainerquest` for future OsLib additions:

- `System.IO.FileInfo` for `LastWriteTimeUtc` in `GetFileChanged()`
- `System.IO.Directory.GetFiles` in `EnumerateChangeFiles()`
- `System.IO.File.SetLastWriteTimeUtc` in `Store()`

---

### Test Impact

The following test updates were required (applied by Codex agent):

| Test File | Change |
|---|---|
| `PitChangeMergeTests` | `ChangeDir` → `ChangesDir`; `.pit` assertions → `.json`; subdirectory assertions → flat file |
| `CloudRemoteSyncTests` | `ChangeDir` → `ChangesDir` |
| `PitSnapshotTests` | `ExportJson(string)` → `ExportJson(RaiPath)` |
| `PitAddConcurrencyTests` | `MaxCount` post-construction assignment → `PitItems.Create(key, 0)` |

All tests pass after updates. Build succeeds with zero errors.

---

### Architecture Reminder

JsonPit follows a model of
[**asynchronous persistence with eventual durability**](https://github.com/Burkhardt/RAIkeep/blob/main/MANIFESTO.md#asynchronous-persistence-with-eventual-durability):

- A change is not guaranteed to be durably visible everywhere immediately after the local write returns.
- The system is designed so that changes become durably visible over time.
- The master/client philosophy ensures only the master writes the main pit file; all other machines persist their state as ChangeFiles in the `Changes` subdirectory.
- The master consumes and deletes ChangeFiles during `MergeChanges`, writing the consolidated state back to the pit file.
- Convergence matters more than instant global visibility.

---

### Migration Notes

- If you access `ChangeDir` on a `Pit` instance, rename to `ChangesDir`.
- If you call `CreateChangeFile` with a machine name parameter, the method is now public with the signature `CreateChangeFile(PitItem item, string machineName = null)`.
- If you set `MaxCount` on a `PitItems` instance after construction, pass it to the constructor or `PitItems.Create(key, maxCount)` instead.
- If you use the `Item` class, plan migration to `PitItem`. `Item` is now `[Obsolete]`.
- If you implement `IDisposable`-aware lifetime management, `Pit` now supports `using` blocks and explicit `Dispose()`.
- Change files are now `.json` format. Any tooling that scans for `.pit` in the Changes directory should be updated.

---

## 3.7.2

### Highlights

- Aligns JsonPit package version with the 3.7.2 release line.
- Updates fallback package references to `OsLibCore 3.7.2` and `RaiUtils 3.7.2`.
- Keeps the WWWA integration quick-start onboarding in `GettingStarted.md`.

### Notes

- Publish order remains: `OsLibCore` -> `RaiUtils` -> `RaiImage` -> `JsonPit`.

---

## 3.7.1

### Highlights

- Adds a WWWA-based quick-start section to [GettingStarted.md](https://github.com/Burkhardt/JsonPit/blob/main/GettingStarted.md) for creating and seeding a pit in cloud-backed storage.
- Documents the `SyncSamplesToCloud` test target that copies `sample/**` files to the cloud sample directory.
- Keeps package alignment with `OsLibCore 3.7.1` and `RaiUtils 3.7.1` for coordinated release flow.

### Reference

- Integration test source: [JsonPit.Tests/JsonPitRealWorldIntegrationTests.cs](https://github.com/Burkhardt/RAIkeep/blob/main/doc/JsonPit.Tests/JsonPitRealWorldIntegrationTests.cs#L22)
- Test project copy target: [JsonPit.Tests/JsonPit.Tests.csproj](https://github.com/Burkhardt/RAIkeep/blob/main/doc/JsonPit.Tests/JsonPit.Tests.csproj)

---

## 3.6.1

### Highlights

- Patch release following `3.6.0`.
- Aligns JsonPit with `OsLibCore 3.6.1` and `RaiUtils 3.6.1` in the correct NuGet publish order.
- Fallback `PackageReference` versions updated to `3.6.1`.
- No API or persistence changes.

### Validation

- JsonPit should be validated with the local `JsonPit` test suite and package build before publishing.

---

## 3.6.0

### Highlights

- Version bumped to `3.6.0`.
- Aligns JsonPit with the shared `3.6.0` package line across `RAIkeep`.
- Fallback package references now align with `OsLibCore 3.6.0` and `RaiUtils 3.6.0`.

### Compatibility

- No API or persistence changes in this release.
- All existing `PitItem.Id`-based contracts are unchanged.

### Validation

- JsonPit should be validated with the local `JsonPit` test suite and package build before publishing.

---

## 3.5.2

### Highlights

- Version bumped to `3.5.2`.
- JsonPit now aligns with the shared `3.5.2` package line across `RAIkeep`.
- Fallback package references now align with `OsLibCore 3.5.2` and `RaiUtils 3.5.2`.
- The fallback utility package id is now `RaiUtils` rather than `RaiUtilsCore`.

### Compatibility

- Legacy persisted payloads that still contain `Name` without `Id` are normalized internally to `Id`.
- During normalization, `Name` is copied into `Id` when `Id` is missing, and the original `Name` value is preserved.
- Future use of `Name` as an application-defined custom field remains supported.

### Documentation

- `README.md`, `GettingStarted.md`, and `Requirements.md` were updated for the `3.5.2` package line.
- Package installation examples now reference `JsonPit 3.5.2`, `RaiUtils 3.5.2`, and `OsLibCore 3.5.2`.
- JsonPit guidance now uses `Os.CloudStorageRootDir` in its path-composition examples.

### Validation

- JsonPit should be validated with the local `JsonPit` test suite and package build before publishing.

---

## 3.5.0

### Highlights

- Version bumped to `3.5.0`.
- JsonPit now documents the supported cloud-backed provider claim as `OneDrive`, `GoogleDrive`, and `Dropbox`.
- `PitItem.Id` replaces `Name` as the canonical framework identifier.
- JsonPit package metadata and fallback package references were aligned with the shared `3.5.0` package line.

### Compatibility

- Legacy persisted payloads that still contain `Name` without `Id` are normalized internally to `Id`.
- During normalization, `Name` is copied into `Id` when `Id` is missing, and the original `Name` value is preserved.
- Future use of `Name` as an application-defined custom field remains supported.

### Documentation

- `README.md`, `GettingStarted.md`, and `Requirements.md` were updated for the `3.5.0` package line.
- The package installation examples now reference `3.5.0`.
- The cloud-storage guidance now reflects the supported provider claim used across the `RAIkeep` package stack.
- JsonPit guidance now references `Os.CloudStorageRootDir`, `Os.UserHomeDir`, and the current `RaiPath`-based OsLib path helpers.

### Validation

- JsonPit remained green in the full workspace validation run for `3.5.0`.

---

## 3.4.0

### Highlights

- Version bumped to `3.4.0`.
- JsonPit now aligns with the shared `3.4.0` package set used together with `OsLibCore` and `RaiUtilsCore`.
- Public onboarding documentation was expanded substantially in `GettingStarted.md` so another implementation agent can use JsonPit from NuGet packages with the current APIs and usage model.
- The recommended server-side mental model is now documented explicitly as long-lived in-memory pit usage with asynchronous persistence and eventual durability.

### Packaging and Publish Automation

- JsonPit's standalone package build path now works correctly outside the umbrella workspace.
- The project now falls back to NuGet package references for `OsLibCore` and `RaiUtilsCore` when sibling source repositories are not present locally.
- The NuGet publish workflow was aligned with the other package repositories and updated to restore/build `JsonPit.csproj` directly in standalone CI.

### Practical Usage Guidance

- `GettingStarted.md` now covers package installation, current `Pit` and `PitItem` APIs, update patterns, enumeration/query patterns, and a practical `PersonPit` example for OTW / AfricaStage style backend work.
- The docs now describe JsonPit more accurately as a file-backed, synchronized in-memory working model rather than a database-table abstraction.

### Compatibility

- Existing `Pit` / `PitItem` application code remains stable.
- JsonPit remains suitable for cloud-backed shared storage scenarios when used with explicit OsLib configuration.
- Cross-server behavior should be understood as
  [asynchronous persistence with eventual durability](https://github.com/Burkhardt/RAIkeep/blob/main/MANIFESTO.md#asynchronous-persistence-with-eventual-durability)
  rather than immediate real-time synchronization.

### Validation

- The standalone `JsonPit.csproj` restore/build path was validated successfully after the packaging fix.
- JsonPit's publish workflow was corrected so it can run reliably from the standalone repository.

---

## 3.3.0

### Highlights

- Version bumped to `3.3.0`.
- JsonPit now aligns with OsLib's `Os.Config` and `osconfig.json` configuration model.
- Test environment setup was updated to configure cloud roots through config files instead of custom override variables.

### Compatibility

- Existing `Pit` usage remains stable.
- Cloud-backed usage now follows OsLib's config-driven root resolution and cache behavior.
- JsonPit remains aligned with the shared package set used in the RAIkeep workspace.

### Validation

- Full solution validation remained green after the version bump.
