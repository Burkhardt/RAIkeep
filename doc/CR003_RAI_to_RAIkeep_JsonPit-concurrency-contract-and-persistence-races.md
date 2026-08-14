# Change Request — JsonPit concurrency contract and persistence races

This document captures the next-release concurrency work needed for RAIkeep and JsonPit.

Status: accepted and finalized for implementation in the coordinated `3.13.2` line.  
Finalized: 2026-08-05

Detailed implementation guidance, current code seams, sequencing pseudocode, traps, and per-agreement test designs are recorded in [`Details of CR003.md`](<https://github.com/Burkhardt/RAIkeep/blob/main/doc/Details%20of%20CR003.md>).

## Current Assessment

RAIkeep is not yet fully at the desired concurrency contract.

The project already has important concurrency-related tests and safeguards, and the test suite intentionally disables incidental xUnit test parallelism. That is appropriate while OsLib and JsonPit contain process-global state and real cloud-backed filesystem behavior.

However, disabling test-runner parallelism is not the same thing as proving product-level concurrency safety. RAIkeep needs explicit, intentional concurrency tests and a documented runtime contract for threads, processes, and machines.

## Confirmed Regression — Concurrent Save And Add

On 2026-08-03, both the umbrella test run and an immediate isolated rerun failed in `SaveInterleavedWithAdds_SubsequentSavePersistsEveryAcceptedItem`.

The failures occurred while `GetRawPersistenceModel()` applied LINQ ordering and materialization directly to `HistoricItems` as concurrent `Add` operations changed the same `ConcurrentDictionary`. The two observed exceptions were:

- `IndexOutOfRangeException` from LINQ materialization.
- `ArgumentException` from `ConcurrentDictionary.ICollection.CopyTo(...)` after the collection size changed during copying.

This is an in-process persistence snapshot race, not a cloud-storage or flag-file failure. The fix must create a stable, thread-safe persistence snapshot without losing accepted writes, and the existing regression test must pass repeatedly rather than intermittently.

### Agreed v3.13.2 persistence boundary

- Concurrent `Add` calls on one shared `Pit` remain supported; they must not be serialized unnecessarily behind cloud-file I/O.
- `Add` participates in a shared state/snapshot gate that permits multiple additions concurrently.
- `Save` takes brief exclusive access to that gate, waits for additions already inside the gate to finish, and captures one coherent point-in-time persistence snapshot.
- `Save` releases the state/snapshot gate before serialization, cloud-file I/O, and flag updates. Additions may therefore continue while the captured snapshot is being persisted.
- An addition accepted after the snapshot boundary may be deferred to a later `Save`, but its existing per-fragment dirty state must remain set until a snapshot containing that fragment is successfully persisted.
- Only fragments demonstrably included in the successfully persisted snapshot may be validated. `Save` must never validate a newer live fragment that was absent from the written snapshot.
- Reuse the existing `PitItem` dirty/valid mechanism; do not introduce a second pending-write queue or public pending-state abstraction.

## Next Release Goal

Make RAIkeep's concurrency behavior explicit, testable, and enforceable across:

1. multiple threads in one process
2. multiple processes on one machine
3. multiple machines sharing cloud-synced pit files

## Required Work

### 1. Define The Concurrency Contract

The accepted contract is:

- One shared `Pit` instance may receive concurrent `Add` calls.
- There must be no more than one live public in-memory `Pit` instance for each distinct canonical pit path in a process. Application threads share that instance through the application's container or singleton mechanism.
- Multiple processes may target the same `.pit`. Every process is identified by its PID-specific process flag, and JsonPit—not the caller—prevents overlapping processes from exercising the same master authority. Applications still provide meaningful stable subscriber identities such as `AIA` and `AfricaStage`, but callers do not invent unique subscribers merely to distinguish PIDs.
- The master is the exact process currently holding the valid `Master.flag` lease for that pit. Every other process is a non-master participant at that moment. Roles are dynamic, apply equally to local and remote processes, and may differ from pit to pit.
- A process that cannot acquire or renew exact-process master authority writes change files rather than overwriting the canonical pit.
- Ordinary application reads use the process's single shared in-memory `Pit`. A different process may load the canonical file while persistence is occurring, but JsonPit publishes replacement in-memory state only after the complete canonical snapshot has been read and parsed successfully. Transient absence, sharing errors, incomplete content, or parse failure during a known rewrite are retried without clearing or partially replacing existing state. Exhausting the bounded retry window throws a descriptive persistence exception.
- Delayed and out-of-order fragments remain valid under JsonPit's eventually persistent model and are ordered by fragment history rather than arrival time. Exact replay duplicates are ignored. Different fragments with equal timestamps remain valid and use the deterministic ordering below. Unsupported external delete/rename interference remains an operational condition that may require human repair.

Required promises are:

- reads must never publish corrupt, partial, or transiently empty pit state; JsonPit retries transient read-during-write failures and throws a useful persistence exception if bounded recovery is exhausted
- accepted writes must not silently disappear; this is addressed by the agreed brief snapshot gate and by validating only fragments contained in the successfully persisted snapshot, while later fragments retain their existing dirty state for the next `Save`
- non-master writes must not overwrite the canonical pit directly; they must use change files
- non-master changes must remain mergeable through JsonPit's established change-file representation
- merge behavior must be deterministic

### 2. Separate Test-Runner Parallelism From Product Concurrency

Keep ordinary xUnit test parallelism disabled for now.

The current non-parallel setting is a containment choice for tests that touch process-global state, real cloud roots, filesystem timing, and shared test infrastructure.

Do not use incidental xUnit parallelism as proof of concurrency safety.

Instead, add explicit concurrency suites that deliberately create controlled races:

- `InProcessConcurrencyTests`
- `MultiPitInstanceConcurrencyTests`
- `MultiProcessConcurrencyTests`
- `RemoteCloudConcurrencyTests`

These tests use real cloud-root pits under the test-environment contract below and make concurrency behavior visible instead of hiding it behind test-runner scheduling.

### 3. Harden In-Process JsonPit Write Behavior

JsonPit should guarantee safe behavior for concurrent in-process use.

Required assertions:

- concurrent `Pit.Add` calls on one `Pit` instance do not lose updates
- concurrent additions receive fresh UTC insertion timestamps; timestamp uniqueness is not promised and concurrency correctness must not depend on it
- duplicate detection remains correct under contention
- history ordering remains stable and explainable
- saving after concurrent additions produces a valid pit file
- `Save` obtains only a brief exclusive snapshot window and does not hold the state/snapshot gate throughout cloud-file I/O
- an addition accepted after the persistence snapshot remains dirty and is written by a later `Save`
- successful persistence validates the fragments in the written snapshot without validating a newer, unwritten live fragment

#### Agreed v3.13.2 equal-timestamp and replay behavior

- Replaying an exact fragment already present in the same item history is idempotent; the duplicate is ignored rather than consuming another bounded-history slot.
- Primary history order remains `Modified` descending.
- Different fragments with equal `Modified` values are both retained and are not treated as an exception.
- For equal timestamps, the fragment with fewer JSON properties sorts first and therefore has projection precedence for contradictory overlapping properties.
- A later equal-time fragment may still contribute properties not defined by the earlier fragment.
- If timestamp and property count are both equal, canonicalized fragment content supplies the final deterministic ordinal tie-break.
- Canonical-content comparison is performed only for that final double-tie case; ordinary additions and projections do not pay that cost.
- Projection continues to use first-seen property precedence. Equal-time misuse may therefore produce an arbitrary business winner, but the library produces the same deterministic winner from the same history on every participant.

Required tests cover exact replay idempotence, bounded-history protection, smaller-fragment precedence, contribution of non-overlapping properties, deterministic equal-count ordering, and identical projection regardless of fragment arrival order.

#### Agreed v3.13.2 timestamp boundary

- Live `Add` retains the established behavior of refreshing `Modified` from actual `DateTimeOffset.UtcNow` at the insertion boundary.
- `Modified` is a real UTC timestamp, not a synthetic sequence number, and is not guaranteed unique within or across processes.
- `AddHistorical` preserves the supplied historical timestamp.
- Equal timestamps are valid and use the deterministic history ordering defined above.
- Do not add a global or per-pit monotonic clock, stateful `UtcNow` getter, clock injection, or environment-controlled time source for this work.
- Replace tests that require every concurrent addition to receive a unique timestamp with tests proving that all accepted additions are preserved and project deterministically even when timestamps coincide.

Existing concurrency tests should be preserved and expanded only where they expose real behavior.

### 4. Define And Test Multiple Pit Instances In One Process

More than one live public `Pit` instance targeting the same canonical `.pit` path in one process is unsupported library use. This rule applies to writable and read-only public instances alike.

Required behavior:

- JsonPit maintains process-wide ownership of canonical pit paths by live public `Pit` instances.
- Construction of a second public instance for an already-owned canonical path throws a descriptive exception before the duplicate instance can load or mutate state.
- The exception directs the application to reuse one in-memory instance through its singleton, keyed container, or equivalent process-level store.
- `Dispose` releases path ownership so a later instance may legitimately reopen the pit.
- Constructor failure must not leave stale path ownership behind.
- JsonPit's internal persistence comparison and merge mechanics must use a private snapshot-reading mechanism rather than constructing a second public `Pit` for the same path.

Required tests prove duplicate rejection, read-only duplicate rejection, release on disposal, cleanup after constructor failure, and successful reopen after disposal. Do not implement or test competing mutations through two public instances; the required result is rejection before that state exists.

This is separate from many threads sharing one `Pit` instance. The surrounding process is responsible for registering and sharing that singleton; JsonPit is responsible for detecting conflicting public instances rather than permitting silent misuse.

### 5. Harden Multi-Process Coordination

The accepted coordination mechanism is the timed `Master.flag` lease, PID-specific `ProcessFlagFile` activity windows, and ordinary change files for non-master participants. No operating-system or distributed file lock is introduced.

Required behavior:

- writers must not corrupt the canonical `.pit`
- stale writers must not overwrite newer state
- stale locks or stale tickets must have recovery behavior
- lock/ticket failures must produce useful diagnostics
- retry behavior must be deterministic enough to test

#### Agreed v3.13.2 master ownership contract

- Keep the existing timed `Master.flag` plus PID-specific `ProcessFlagFile` protocol; do not add an operating-system file lock.
- Master ownership records both the stable participant identity (`Machine` plus `Subscriber`) and the exact owning process identity represented by its PID-specific process flag.
- Only the exact owning process may renew its active master lease directly.
- A different PID with the same stable participant must not inherit master authority while the recorded owner's process window remains active. It follows the non-master change-file path instead of writing the canonical pit.
- When the recorded owner's process window has been explicitly released or has expired, a new PID with the same stable participant may inherit the still-protected participant lease and become its exact process owner.
- Different subscribers on one machine remain distinct stable participants and use the same lease/change-file protocol as participants on different machines.
- PID-level collision detection and safe handover are JsonPit responsibilities. The library must not delegate correctness to callers by requiring every concurrent process to invent a unique subscriber value.

Required tests cover exact-owner renewal, refusal while another same-participant PID is active, change-file fallback for the refused process, inheritance after explicit process-window release, inheritance after expiry, and continued separation of different subscribers.

#### Agreed distributed lease boundary and cloud-provider role

- The `Master.flag` protocol is a cooperative cloud-backed lease, not an atomic cross-machine compare-and-swap.
- When two machines begin from independently visible expired state, arbitrary cloud synchronization delay can allow both to believe temporarily that they acquired master authority. JsonPit must not claim unconditional single-master exclusion under that condition.
- Cloud-drive providers may preserve conflicting writes by retaining the canonical name and renaming a conflicting copy, for example `Master.flag` plus `Master (1).flag`.
- JsonPit uses one provider-independent filesystem signal for Dropbox, OneDrive, Google Drive, and iCloud Drive: any file matching `Master*.flag` whose filename length is greater than `Master.flag`. It does not parse or require a provider-specific suffix.
- A provider-created conflict copy is evidence that competing master claims occurred. It detects the conflict after the fact; it does not prevent canonical writes that happened before the conflict artifact became visible.
- The same detection and recovery code applies to every configured provider root without a capability matrix, provider API, or provider-specific branch. The contract is triggered whenever the synchronized filesystem exposes the general longer-name signal; it makes no timing guarantee about when that signal appears.
- Real configured-cloud and SSH-driven tests reproduce the simultaneous-claim scenario and record the actual conflict artifacts and propagation timing of the configured provider used by the test.

#### Agreed v3.13.2 live split-master recovery

The exact recovery design is specified in [`JsonPit-CONCEPT-Live-Split-Master-Recovery.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/JsonPit-CONCEPT-Live-Split-Master-Recovery.md).

- The exact canonical `Master.flag` remains the authority record. A longer provider-created `Master*.flag` variant is a signal that the provider detected conflicting master writes; it is not a second authority record.
- When both claimant processes remain alive, each uses its own live in-memory `Pit` state. JsonPit does not hold `Object.pit` open through the lease and does not add a persistent operating-system file handle.
- Each exact-process master tenure maintains an in-memory recovery write set. Before a successful master `Save` marks snapshot fragments clean, it records the newly persisted fragments in that set. If the process retires an incoming change file, the file's fragments must first be represented in the recovery write set or the source change file must remain available.
- A live losing claimant stops canonical writes and publishes the union of its recovery write set and its currently dirty fragments as ordinary, small change files. It does not dump its complete in-memory pit into one bulk recovery file.
- The live loser identifies the longer `Master*.flag` whose exact-process content names itself. Only after every required recovery fragment has a locally materialized, hash-valid ordinary change file does it delete that longer conflicting claim. It never deletes or alters exact canonical `Master.flag`; the current master does not retire a still-live loser's conflict evidence on its behalf.
- If the exact process named by a longer conflict flag has no active PID-specific process window, only the exact current master may retire that orphaned signal. It waits for process-window expiry plus ten minutes, writes and locally validates a `Critical` event containing the conflicting filename, complete flag content, claimant identity, timestamps, and unavailable-live-recovery diagnosis, then deletes only the longer flag. It does not inspect or merge noncanonical `Object*.pit` files.
- Every ordinary change file, including non-master persistence, split-master recovery, and graceful-shutdown export, uses `{Modified.UtcTicks}_{ExactProcessIdentity}_{Sha256}.json`. The exact identity is the process-flag stem containing machine, subscriber/application, and PID. `Sha256` is the full lowercase SHA-256 of the exact canonical UTF-8 JSON payload written to the file.
- Change-file payload canonicalization recursively orders object properties by ordinal name, preserves array order, and emits invariant compact JSON without insignificant whitespace. The timestamp remains diagnostic and sortable but is not treated as unique. Distinct equal-timestamp fragments therefore cannot suppress one another; repeating the same fragment produces the same filename.
- A participant treats a materialized change file as mergeable only after its bytes match the hash encoded in its filename and the canonical payload parses completely.
- A recovery-write-set entry remains in memory while it is the fragment's only recovery representation. It may be removed immediately after its ordinary change file has been written locally, fully materialized, hash-verified, and parsed successfully. No cloud or current-master acknowledgement is required merely to release that process memory.
- Publication and write-set removal are per fragment. A failed publication retains that entry for retry; successful entries in a partially published batch may be removed independently because their filenames are idempotent.
- A live transfer of exact master authority to another process is a durability handoff even when no longer conflict flag exists. The former master enters the persistence/recovery gate, publishes its completed-tenure recovery write set plus currently dirty fragments as ordinary change files, removes only locally validated entries, and continues as a non-master. Mere lease expiry followed by reacquisition by the same exact process is not a transfer and does not trigger this export.
- Every participant that encounters those files may merge them through the ordinary deterministic change-file path. Exact replay duplicates are harmless and ignored.
- Only the exact current master may persist the reconciled canonical pit and complete recovery cleanup. That responsibility follows canonical `Master.flag` if master authority changes while recovery is in progress.
- Change-file cleanup is a current-master-only two-stage operation. The master first validates and merges a file, successfully persists a canonical snapshot that accounts for its fragment under the configured history-retention rules, and records the file's cleanup-eligibility time in memory. It must not delete the file before that canonical save.
- The file remains for a ten-minute propagation grace period measured from successful canonical persistence, not from original change-file creation. A later cleanup pass revalidates current exact-master authority and canonical health before deletion.
- Restart or master change loses the in-memory eligibility time. The new current master therefore merges/persists again and starts a fresh ten-minute grace period. No acknowledgement sidecar is required. The grace is an explicit operational safety margin, not a proof of replication under unlimited provider delay.
- Explicit disposal of a writable `Pit` is a durability boundary. Under the persistence/recovery gate it snapshots the recovery write set plus currently dirty fragments, publishes them as ordinary collision-safe change files, optionally completes a canonical save if it still owns exact master authority, and only then releases process/master authority and its watcher.
- Graceful shutdown must publish the change files before attempting the optional canonical save so the fragments remain recoverable if that canonical save fails. Finalizers do not perform this I/O. Crash, forced termination, power loss, and failure to dispose remain outside the live in-memory recovery guarantee.
- Do not remove recent fragments or manufacture timestamp-based undo. `GetAt` historical projection is not an undo implementation.

Immediate detection uses native filesystem notifications:

- Every live writable flagged `Pit` watches its pit directory for created, renamed, or changed `Master*.flag` paths.
- A filesystem callback only queues one debounced recovery evaluation; it does not perform persistence directly on the callback thread.
- The recovery worker waits for materialization, rescans the directory, reads canonical `Master.flag`, determines winner/loser role, and runs through the persistence/recovery gate.
- Filesystem notifications are signals rather than guaranteed delivery. Construction, master acquisition, `Save`, and `Reload` also scan at their normal operation boundaries; watcher errors trigger a rescan.
- There is no continuous polling loop and no cloud-provider API integration.
- Disposal stops the watcher and cancels queued recovery work.

Recovery diagnostics are structured and available both live and durably:

- Each live `Pit` exposes an immutable `LastRecoveryStatus` and an optional `RecoveryStatusChanged` event. Applications do not need to subscribe or respond for recovery correctness.
- Status stages include conflict detected, role determined, change files published, canonicalized, cleanup pending, completed, deferred for retry, and failed. JsonPit's event content includes schema version, event identity, UTC time, severity, stage, pit identity, exact local process, current master, role, affected fragment/file counts, correlation identity, source operation, message, and optional exception details.
- CR-related diagnostics use structured events instead of `Debug.WriteLine`. Filesystem-watcher callbacks never throw recovery failures on the callback thread; explicit operations still throw descriptive persistence exceptions when their bounded durability contract cannot be fulfilled.
- Durable JsonPit audit events are immutable canonical-JSON files written under the owning pit root's opinionated `Events` child directory. JsonPit supplies the logical stem `{UtcTicks}_{ExactProcessIdentity}_{Stage}` and OsLib appends `_{Sha256}.event`, where the full lowercase hash covers the canonical UTF-8 content.
- OsLib supplies `EventFile : TextFile` for one create-once event and a static `EventDirectory` aggregator. `EventDirectory` declares `public const string Name = "Events"`; both APIs accept the owning root path and derive `rootPath / EventDirectory.Name` internally.
- The first `EventFile` write creates the `Events` child. `EventDirectory.Events(RaiPath rootPath)` never creates it, returns an empty `Dictionary<string, JObject>` when absent, and freshly enumerates `*.event` on every call without cached state.
- `EventFile` accepts a `JObject` or a dynamic object that serializes to one top-level JSON object. Each `.event` file begins with `{`, ends with `}`, and contains exactly one event object. OsLib imposes no event-content schema: it canonicalizes the supplied object, computes SHA-256, and appends the hash to the caller's logical filename stem.
- The same logical stem and canonical content resolve to the same path and are an idempotent success. The same stem with different content resolves to a different hash-derived filename. If a hash-derived path already contains different bytes, the existing artifact is preserved and the new event receives an additional collision nonce; collision handling does not interrupt the operation being audited.
- `EventDirectory.Events` returns a newly constructed `Dictionary<string, JObject>` using the complete event filename as key and that file's unchanged parsed object as value. It does not interpret content fields. JsonPit and `pits`, not OsLib, own the JsonPit event schema, grouping, ordering, filtering, and presentation.
- A temporarily incomplete, unparseable, or hash-invalid `.event` file is omitted individually from the current result; it does not fail the whole directory read or hide valid events. Because every call enumerates and reads afresh, the file is reconsidered automatically after cloud materialization progresses.
- The `pits` executable produced by the PitSeeder repository exposes diagnostic audit mode as `pits -r <root> <PitName> --events`. It reads `EventDirectory.Events` directly without opening a `Pit`, creating a process flag, acquiring master authority, or writing an audit event.
- `--event-machine all|local|<machine>` filters machine identity and defaults to `all`. `--event-level <level>` is a case-insensitive inclusive minimum and defaults to `Trace`. Existing `--json` emits the filtered JsonPit event result as JSON; otherwise output is human-readable and ordered by machine, UTC time, and event identity.
- v3.13.2 requires one positional pit name for audit mode. Combining `--wwwa` with `--events` remains outside this CR.
- JsonPit uses the `Microsoft.Extensions.Logging.LogLevel` names `Trace`, `Debug`, `Information`, `Warning`, `Error`, and `Critical` in durable and live recovery status; `None` is never written as an event. Default stage levels are `ConflictDetected` → `Warning`, `RoleDetermined` → `Information`, `ChangeFilesPublished` → `Information`, `Canonicalized` → `Information`, `CleanupPending` → `Debug`, `Completed` → `Information`, `DeferredForRetry` → `Warning`, and `Failed` → `Error`. Failure to make accepted fragments durable during explicit shutdown is `Critical`.
- OsLib's existing injectable `Microsoft.Extensions.Logging` surface may later consume the same structured records; v3.13.2 does not require an application logger for durable auditing or recovery.

Required configured-cloud and SSH-driven tests reproduce two live false-master claimants, provider creation of a longer `Master*.flag` conflict copy, watcher notification on both servers, recovery of the losing tenure's write set through ordinary small change files, loser-only retirement of its longer conflict flag after all recovery files validate locally, current-master cleanup of an orphaned longer flag only after process expiry plus ten minutes and validated `Critical` evidence, durable write-set export on a live exact-master transfer without a conflict flag, no such export for same-process reacquisition, idempotent merging by all participants, canonical-save-before-delete ordering, a fresh ten-minute post-save cleanup grace after restart or master transfer, operation-boundary recovery when a notification is deliberately missed, and graceful disposal exporting all tenure-write-set and dirty fragments before releasing authority.

Required PitSeeder tests prove that `pits --events` applies all/local/named-machine and inclusive minimum-severity filters, produces the specified JSON and deterministic human ordering, and remains a read-only audit path that creates no `Pit`, process/master flag, or audit event.

#### Agreed v3.13.2 read-during-write contract

- The supported application read model is the process's single shared in-memory `Pit`; application threads do not bypass it to read the canonical file independently.
- A load in another process may overlap the exact master's canonical write.
- Loading builds and validates a candidate state separately. It replaces live `HistoricItems` only after the entire canonical snapshot has been read and parsed successfully.
- When a canonical file known to exist is transiently missing, locked, incomplete, or unparsable during a rewrite, JsonPit retries from disk without clearing the current in-memory state.
- A genuinely absent pit on initial creation remains a valid no-data case; it is distinct from disappearance during a known rewrite.
- Exhausting the bounded retry policy throws a descriptive persistence exception. It must not silently return an empty or partially replaced pit.

Required tests use configured cloud-root pits to overlap canonical writing and loading, prove that only complete snapshots become visible, prove preservation of prior in-memory state across transient failures, and verify the explicit failure after bounded retry exhaustion.

#### Agreed v3.13.2 `TextFile.Save` contract

- The no-delete persistence behavior belongs in OsLib's public `TextFile.Save` abstraction rather than in a JsonPit-specific caller workaround.
- `TextFile.Save(backup: false)` creates the pathname when absent or truncates and writes the existing pathname directly. It must not call `rm`, rename the original, or use temporary-file replacement.
- `TextFile.Save(backup: true)` copies the previous content to the configured backup location before overwriting the original pathname in place. Backup must copy rather than move so the original pathname never disappears.
- Existing materialization checks remain in both paths.
- `TextFile.SaveInPlace` remains for patch-release source and binary compatibility and delegates to the new `Save(backup: false)` behavior.
- In-place writing is not described as atomic reader visibility. JsonPit's validated candidate-load and bounded-retry behavior remains responsible for preventing incomplete content from becoming live state.
- JsonPit canonical files, flag files, change files, and other `TextFile` callers receive the same no-delete default without selecting a special method.

Required OsLib tests cover ordinary overwrite, copy-based backup before overwrite, continuous pathname presence during repeated configured-cloud writes, and retained materialization behavior. JsonPit tests cover overlapping configured-cloud canonical writes and validated loads through this shared abstraction.

### 6. Strengthen Dynamic Master And Non-Master Behavior

Mastership is a dynamic per-pit lease role, not a permanent machine or application category. Any eligible participant may acquire an available master lease. A process may be master for one pit and non-master for another.

Required behavior:

- the exact process holding the valid master lease may write the canonical `.pit`
- a participant that cannot acquire or renew master authority writes change files
- all participants may ingest change files into their in-memory representation
- only the exact master process may fold merged changes into the canonical pit and perform guarded change-file cleanup
- duplicate change files are safe
- out-of-order change arrival is safe
- delayed cloud sync is tolerated
- local and remote tests prove the dynamic master/non-master distinction

The existing remote-sync scenario should become reliable and explicit about the difference between current master behavior and non-master behavior.

### 7. Preserve Real Cloud Semantics In Tests

All concurrency tests governed by this CR use configured cloud roots. Local temporary paths are not substitutes for cloud-backed pit behavior. A purely local mechanics test requires specific justification and approval; test isolation alone is not sufficient.

#### Agreed v3.13.2 test-environment contract

- All concurrency tests in this CR operate on real pits under configured cloud roots. They must not substitute local temporary directories, environment variables, rewritten configuration, or dependency-injected filesystem/configuration stand-ins.
- Tests detect and report missing configured provider or remote-node prerequisites explicitly.
- On an ordinary machine lacking a prerequisite, the affected real-cloud test is skipped with a precise reason. A skip is neither a pass nor evidence for release acceptance.
- The coordinated `3.13.2` release is blocked until the complete applicable concurrency suite has been deliberately executed and passed against the configured cloud roots and configured remote node.
- Release evidence records the provider, participating machines/processes, exact test names, results, and any observed propagation timing.
- Purely local mechanics may use local files only after the test's relevance is specifically justified and approved; test isolation alone is not sufficient justification.

### 8. Document The Release Acceptance Bar

The coordinated release is accepted only when:

- ordinary suite remains non-parallel
- explicit in-process concurrency tests pass
- explicit multi-`Pit` same-file tests prove duplicate public instances are rejected and legitimate reopen after disposal succeeds
- explicit multi-process ownership, handoff, change-file, and recovery tests pass
- remote dynamic master/non-master and split-master recovery tests pass reliably
- docs state exactly what concurrency RAIkeep supports and its accepted crash/power-loss limitation
- no required real-cloud concurrency test remains skipped in the recorded release-acceptance run

## Non-Goals

For the next release, do not make broad architecture changes merely to satisfy test isolation.

Do not treat test-runner parallelism as a goal by itself.

Do not rewrite configuration loading as part of the concurrency work.

Do not use dependency injection or environment-variable manipulation to replace the real machine configuration model.

## Configuration And Test-Environment Guardrail

The established configuration file on each participating machine is the sole source of truth for `Os.Config`, `Os.TempDir`, cloud-root discovery, and related runtime paths. Concurrency work governed by this CR must not replace or mutate that model through dependency injection, resettable global contexts, environment variables, rewritten configuration, `RaiPath.CloudEvaluator` substitution, or local temporary directories.

Configuration loading is outside this CR except for the already approved and established configuration tests. Tests must exercise the real configured paths and the behavior under investigation rather than repeatedly retesting configuration initialization or creating isolated substitutes that remove cloud semantics.

This guardrail preserves the direction recorded by RAI on 2026-07-24.
