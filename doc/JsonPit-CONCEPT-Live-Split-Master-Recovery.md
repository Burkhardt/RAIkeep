# JsonPit concept — live split-master recovery

**Status:** Accepted supporting design for v3.13.2  
**Governing change request:** [`CR003_RAI_to_RAIkeep_JsonPit-concurrency-contract-and-persistence-races.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR003_RAI_to_RAIkeep_JsonPit-concurrency-contract-and-persistence-races.md)
**Scope:** Automatic recovery when two still-running processes temporarily wrote as master before a cloud provider exposed the conflicting `Master.flag` write  

## 1. Purpose

JsonPit's timed flag protocol can temporarily produce two apparent masters when separate servers begin from independently visible expired state and cloud synchronization has not yet exposed either claimant to the other. A cloud-drive provider may preserve the conflicting master writes as the exact canonical `Master.flag` plus a longer conflict-copy name such as `Master (1).flag`.

This concept defines how both still-running JsonPit processes detect that signal and perform complementary recovery actions without user-directed winner selection, timestamp-based undo, continuous polling, persistent file handles, or cloud-provider APIs.

## 2. Scope And Preconditions

The live recovery protocol applies when:

1. Two processes on separate servers target the same cloud-synchronized pit.
2. Both temporarily believe they acquired master authority and may have written their local `Object.pit`.
3. The provider subsequently materializes the exact `Master.flag` and at least one longer `Master*.flag` conflict copy on both servers.
4. Both claimant processes, their in-memory `Pit` states, and their master-tenure recovery write sets are still alive when the conflict signal is detected.

The exact `Master.flag` is the authority record. A file matching `Master*.flag` whose filename length is greater than `Master.flag` is conflict evidence, not a second authority record. The suffix is opaque and is not parsed as a provider-specific pattern.

Orderly process termination is covered by the agreed graceful-disposal export to ordinary change files. An abrupt crash, forced termination, or power loss before an in-memory write-set entry has been published remains the explicitly accepted data-loss gap. This protocol does not require or interpret provider-created noncanonical `Object*.pit` copies.

## 3. State Available To JsonPit

Each live process has:

- its exact PID-specific `ProcessFlagFile` identity;
- its stable machine/subscriber identity;
- its live in-memory history and per-fragment dirty state;
- its in-memory recovery write set for the current exact-process master tenure;
- the canonical `Master.flag` once synchronized locally;
- the provider-created longer `Master*.flag` conflict signal;
- access to the local cloud-synchronized pit directory.

JsonPit does not keep `Object.pit` open for the duration of the lease. The recovery advantage comes from the still-live in-memory histories and coherent snapshots, not from an operating-system file handle.

## 4. Detection

Every live writable flagged `Pit` creates a native `FileSystemWatcher` for its own pit directory and observes created, renamed, and changed paths matching `Master*.flag`.

Dropbox, OneDrive, Google Drive, and iCloud Drive use this same filesystem rule. JsonPit contains no provider-specific conflict-name branch or provider API integration.

The callback is a lightweight signal only:

1. Debounce duplicate or partially materialized notifications.
2. Queue at most one recovery evaluation for the pit.
3. Wait for the incoming files to materialize sufficiently for validated reads.
4. Rescan the directory rather than trusting one event payload.
5. Read exact canonical `Master.flag` and determine the current process's role.
6. Enter the pit's persistence/recovery gate before changing persistence state.

Filesystem notifications may be duplicated, coalesced, or missed. They are therefore the immediate path, not the sole correctness mechanism. JsonPit also scans for longer `Master*.flag` files during:

- construction;
- master acquisition;
- `Save`;
- `Reload`;
- watcher-error recovery.

There is no recurring polling timer. No Dropbox, OneDrive, Google Drive, or iCloud API is required.

## 5. Master-Tenure Recovery Write Set

A master tenure begins when an exact process acquires canonical-write authority after not owning it. Renewals by that same exact process continue the tenure; authority moving to another exact process ends it.

During a tenure, JsonPit maintains an in-memory recovery write set containing the fragments that could otherwise exist only in canonical files written by that process:

1. Before a successful master `Save` marks snapshot fragments clean, the fragments newly persisted by that snapshot are recorded in the write set.
2. Fragments accepted after the latest successful snapshot remain dirty and therefore remain independently identifiable.
3. If the process retires an incoming change file, its fragments must first be represented in the recovery write set; alternatively, the source change file remains available.
4. Exact replay entries in the write set are deduplicated by fragment identity and canonical content.

The write set tracks disputed writes prospectively. JsonPit does not attempt to infer a false-master interval afterward from wall-clock timestamps, and it does not copy the complete losing pit merely because a conflict occurred.

A write-set entry remains in memory while it is the fragment's only recovery representation. It may be removed immediately after its ordinary change file has been written locally, fully materialized, hash-verified, and parsed successfully. Durable responsibility has then transferred from process memory to the synchronized-directory file; cloud replication or canonical-master acknowledgement is not required merely to release memory.

Publication and removal are per fragment. A failed publication retains that entry for idempotent retry. Entries whose files succeeded in a partially published batch may be removed independently.

### Live authority handoff without a conflict flag

When exact canonical master authority moves to another process while the former master remains alive, the completed tenure receives the same durable handoff even if no longer `Master*.flag` exists:

1. Enter the persistence/recovery gate.
2. Capture the completed-tenure recovery write set plus currently dirty fragments through the snapshot barrier.
3. Publish them as ordinary collision-safe change files.
4. Remove only entries whose files validate locally.
5. Continue as a non-master participant.

Mere lease expiry followed by successful reacquisition by the same exact process is not an authority transfer and does not trigger this export.

## 6. Current-Master Role

The recovery persister is whichever exact process is recorded by the valid canonical `Master.flag` at the time canonical persistence occurs. This responsibility follows master authority if the lease changes during recovery.

The current master:

1. Retains canonical-write authority.
2. Captures its current coherent in-memory state through the brief exclusive snapshot barrier.
3. Reasserts that snapshot through the canonical no-delete `TextFile.Save` path.
4. Continues observing the pit directory for ordinary change files emitted by the losing process.
5. Merges those fragments through the normal deterministic history merge.
6. Ignores exact replay duplicates and applies the agreed equal-timestamp ordering.
7. Persists the reconciled history as canonical `Object.pit` while it still owns the valid exact-process lease.
8. Alone may make successfully canonicalized change files eligible for eventual cleanup and later retire them.

The current master does not delete history or infer an undo window from timestamps.

Every non-master participant that encounters the same change files may merge them into its in-memory history through the ordinary change-file path. Such a merge improves read freshness but does not acknowledge distributed recovery or authorize canonical persistence.

### Change-file cleanup

Cleanup is a current-master-only two-stage operation:

1. Validate and merge the change file.
2. Successfully persist a canonical snapshot that accounts for the fragment under the configured history-retention rules.
3. Only after that save, record an in-memory cleanup-eligibility time for the file.
4. Retain the file for a ten-minute propagation grace period measured from that successful canonical persistence, not from the file's original creation time.
5. On a later cleanup pass, confirm that the process remains the exact current master and that canonical state is healthy before deleting the file.

A restart or master change loses the in-memory eligibility time. The new current master conservatively merges and persists again, then starts a fresh ten-minute grace period. No acknowledgement sidecar is required.

The grace period is the project's explicit operational safety margin. It reduces the chance that a provider propagates deletion before canonical content but cannot prove replication under unlimited cloud delay. Non-master participants never delete change files.

## 7. Losing-Claimant Role

A process whose identity is not the valid owner in canonical `Master.flag` is the losing claimant for this conflict.

The loser:

1. Stops exercising canonical-write authority.
2. Captures the union of its master-tenure recovery write set and its currently dirty fragments through the brief exclusive snapshot barrier.
3. Publishes that union as ordinary, small change files rather than one bulk history dump.
4. Locally materializes, hashes, and parses every required recovery change file.
5. Identifies the longer `Master*.flag` whose exact-process content names itself and deletes that conflicting claim only after step 4 succeeds.
6. Never deletes or alters exact canonical `Master.flag` and never overwrites canonical `Object.pit` as part of recovery.
7. Keeps additions accepted after the recovery snapshot dirty.
8. Uses the ordinary non-master change-file path for subsequent persistence.

The current master does not retire a still-live loser's conflict evidence on its behalf. Deletion of the longer losing claim is the loser's completion signal; it cannot occur before recovery data has transferred from memory to ordinary files.

### Orphaned conflict signal

If the exact process named by a longer conflict flag has no active PID-specific process window, the exact current master may retire the orphaned signal without claiming recovery of that process's lost memory:

1. Wait for the claimant process window to expire and then for an additional ten-minute safety grace.
2. Write a `Critical` durable event containing the conflicting filename, its complete flag content, claimant identity, relevant timestamps, and the fact that no live recovery write set was available.
3. Validate that event file locally.
4. Delete only the orphaned longer `Master*.flag`.

The current master never deletes exact `Master.flag` in this flow and never inspects or merges a noncanonical `Object*.pit` file.

Every ordinary change file uses this identity:

`{Modified.UtcTicks}_{ExactProcessIdentity}_{Sha256}.json`

- `ExactProcessIdentity` is the process-flag stem containing machine, subscriber/application, and PID.
- `Sha256` is the full lowercase SHA-256 of the exact canonical UTF-8 JSON payload written to the file.
- Canonicalization recursively orders object properties by ordinal name, preserves array order, and emits invariant compact JSON without insignificant whitespace.
- The timestamp remains diagnostic and sortable but is not treated as unique.
- A participant accepts the file for merge only after the materialized bytes match the filename hash and the canonical payload parses completely.

The contract applies equally to ordinary non-master persistence, split-master recovery, and graceful-shutdown export. Distinct equal-timestamp fragments cannot suppress one another, while repeating publication of the same fragment produces the same filename and remains idempotent.

## 8. Recovery Concurrency

- Only one recovery evaluation runs for a pit at a time.
- Watcher callbacks never perform file I/O or merge work directly.
- Snapshot capture coordinates with concurrent `Add` operations through the agreed brief state/snapshot gate.
- Persistence and recovery coordinate through the pit's persistence/recovery gate.
- Duplicate watcher notifications and repeated operation-boundary scans may repeat ordinary change-file publication safely.
- Each change file must materialize and parse completely before any participant treats it as mergeable input.

### Graceful disposal

Explicit disposal of a writable `Pit` is a durability boundary:

1. Enter the persistence/recovery gate so shutdown cannot overlap `Save` or recovery work.
2. Capture the recovery write set plus all currently dirty fragments through the snapshot barrier.
3. Publish every captured fragment as an ordinary collision-safe change file.
4. If the process still owns exact current-master authority, it may then complete a canonical save.
5. Release process/master authority only after the local change-file writes complete.
6. Dispose the filesystem watcher and finish shutdown.

Change files are published before the optional canonical save. If that save fails, another current master can still recover the fragments through the ordinary merge path. Exact replay makes fragments already present in the canonical pit harmless.

Finalizers do not attempt filesystem or cloud-root I/O. Crash, forced termination, power loss, and application failure to dispose remain outside the live in-memory recovery guarantee.

## 9. Recovery Diagnostics And Audit Events

Each live `Pit` exposes an immutable `LastRecoveryStatus` property and an optional `RecoveryStatusChanged` event. Applications do not need to subscribe or respond for recovery correctness.

Structured stages include conflict detected, role determined, change files published, canonicalized, cleanup pending, completed, deferred for retry, and failed. JsonPit's event content carries schema version, event identity, UTC time, severity, stage, pit identity, exact local process, current master, local role, affected fragment/file counts, recovery or tenure correlation identity, source operation, message, and optional exception details.

CR-related diagnostic paths write structured events instead of relying on `Debug.WriteLine`. Watcher-thread failures update status and remain available for operation-boundary retry rather than escaping from the filesystem callback. Explicit `Save`, `Reload`, or graceful `Dispose` still throws a descriptive persistence exception when its bounded durability contract cannot be fulfilled.

Durable events use OsLib filesystem abstractions:

- `EventFile : TextFile` represents and writes one immutable canonical-JSON event. It accepts a `JObject` or a dynamic object that serializes to one top-level JSON object; OsLib imposes no content schema. Each `.event` file begins with `{`, ends with `}`, and contains exactly one event object.
- The preferred extension is `.event`.
- The caller supplies a logical filename stem. `EventFile` canonicalizes the JSON, computes the full lowercase SHA-256 of its UTF-8 content, and writes `{LogicalStem}_{Sha256}.event`. JsonPit uses `{UtcTicks}_{ExactProcessIdentity}_{Stage}` as its logical stem.
- The same stem and canonical content resolve to the same path and succeed idempotently. The same stem with different content resolves to a different hash-derived path. If a hash-derived path contains different bytes, the existing artifact is preserved and the new event is written with an additional collision nonce rather than interrupting the audited operation.
- A static `EventDirectory` declares `public const string Name = "Events"`.
- Both writing and aggregation accept the owning root path and internally derive `rootPath / EventDirectory.Name`.
- The first `EventFile` write creates the `Events` child directory. Reading never creates it.
- `EventDirectory.Events(RaiPath rootPath)` returns a newly constructed `Dictionary<string, JObject>`. Each complete `.event` filename is a key and that file's unchanged parsed object is its value. When the child is absent it returns an empty dictionary; otherwise every call freshly enumerates `*.event` without interpreting content fields. It has no instances, constructor, cache, or refresh method.
- A temporarily incomplete, unparseable, or hash-invalid file is omitted individually from that call instead of failing the complete directory read. It remains on disk and is reconsidered by the next fresh call.

JsonPit and `pits`, not OsLib, own the JsonPit event schema, grouping, ordering, filtering, and presentation.

The `pits` executable produced by the PitSeeder repository reads a selected pit's audit without opening a `Pit`, creating a process flag, acquiring master authority, or writing another audit event:

`pits -r <root> <PitName> --events`

- `--event-machine all|local|<machine>` defaults to `all`.
- `--event-level <level>` is a case-insensitive inclusive minimum and defaults to `Trace`.
- Existing `--json` emits filtered JsonPit events as JSON; otherwise output is human-readable and ordered by machine, UTC time, and event identity.
- v3.13.2 audit mode requires one positional pit name. `--wwwa --events` remains outside this CR.

JsonPit uses the existing `Microsoft.Extensions.Logging.LogLevel` names `Trace`, `Debug`, `Information`, `Warning`, `Error`, and `Critical`; `None` is never written as an event. Default recovery levels are:

- `ConflictDetected` → `Warning`
- `RoleDetermined` → `Information`
- `ChangeFilesPublished` → `Information`
- `Canonicalized` → `Information`
- `CleanupPending` → `Debug`
- `Completed` → `Information`
- `DeferredForRetry` → `Warning`
- `Failed` → `Error`
- failure to make accepted fragments durable during explicit shutdown → `Critical`

OsLib already exposes injected `Microsoft.Extensions.Logging` through `Os.ConfigureDiagnostics`. A future adapter may send the same structured event there as well; durable audit and recovery do not depend on an injected logger in v3.13.2.

## 10. Required Tests

Tests use real configured cloud roots and the configured SSH-accessible remote server. They do not substitute local temporary directories.

Required scenarios:

1. Two servers begin from an expired or independently visible master state.
2. Both claim master and write distinct accepted history before synchronization reveals the conflict.
3. The provider creates canonical `Master.flag` plus a longer `Master*.flag` conflict copy.
4. Both native filesystem watchers receive or recover the signal.
5. Canonical `Master.flag` identifies exactly one current master at each canonical persistence boundary.
6. The loser publishes only its recovery write set plus currently dirty fragments as ordinary small change files, not a complete pit dump.
7. Every participant may merge the emitted files, but only the exact current master writes the reconciled canonical pit and completes cleanup.
8. Repeating the recovery produces no duplicate history and no lost accepted fragment.
9. A deliberately missed watcher notification is recovered at the next operation boundary without continuous polling.
10. Watcher disposal leaves no active callback or recovery task for a disposed pit.
11. Distinct fragments from one process with equal timestamps produce distinct change files and both survive recovery.
12. A master change during recovery transfers canonicalization responsibility without losing the emitted fragments.
13. Explicit disposal publishes all recovery-write-set and dirty fragments before authority is released, including when the optional canonical save subsequently fails.
14. A finalizer does not attempt recovery publication.
15. Canonically equivalent object-property order produces the same change-file hash, while a changed value produces a different hash.
16. A hash mismatch or incomplete payload is not merged, marked processed, or removed from the publisher's recovery write set.
17. Successful local publication transfers one entry out of the in-memory write set without waiting for cloud or canonical acknowledgement; partial batch failure retains only the failed entries.
18. A change file is never deleted before a successful canonical save that accounts for it.
19. Cleanup waits ten minutes from canonical persistence; file age before processing does not count toward that grace.
20. Restart or master transfer resets cleanup eligibility and requires another merge/persist/grace cycle.
21. Event files from multiple machines coexist without overwrite; the same logical stem and canonical JSON publish idempotently; different content under the same stem produces a different hash-derived path; and a different-content hash-path collision writes a nonce-suffixed event rather than interrupting recovery.
22. Event aggregation returns an empty dictionary without creating a missing `Events` directory. Every call reflects newly materialized files as complete-filename/`JObject` pairs, with exactly one top-level object per file, and OsLib does not require or interpret JsonPit fields.
23. One incomplete, unparseable, or hash-invalid event is omitted without hiding valid events or failing the whole read, and a later call includes it once the file materializes correctly.
24. Watcher recovery produces durable stage events and updates the in-memory status/event surface without requiring an application subscriber.
25. A live loser cannot delete its longer master-conflict flag until all required recovery change files validate locally; exact `Master.flag` remains untouched.
26. An orphaned longer flag survives claimant expiry plus ten minutes and is deleted only by the exact current master after a complete `Critical` evidence event validates locally; no noncanonical pit is merged.
27. A live transfer to another exact master exports the completed tenure's write set and dirty fragments without requiring a conflict flag, while same-process reacquisition does not.
28. `pits --events` applies the `all`, `local`, and named-machine filters and the inclusive minimum-severity filter, emits the specified JSON or deterministic human ordering, and does not open a `Pit`, create process/master flags, or write an audit event.

Release evidence records provider, servers, process identities, generated conflict filenames, timing, recovered fragment identifiers, and final canonical projection.

## 11. Non-Goals

- No persistent operating-system handle on `Object.pit`.
- No operating-system or distributed file lock.
- No continuous polling loop.
- No cloud-provider API integration.
- No timestamp-based deletion or undo.
- No full losing-pit bulk recovery file for the live-process protocol.
- No guarantee about how quickly a cloud provider exposes the longer-name conflict signal.
- No recovery guarantee for an abrupt crash, forced termination, or power loss before in-memory write-set entries have been exported. Provider-created noncanonical `Object*.pit` copies are not recovery inputs and remain untouched.
- No required injected application logger for v3.13.2 recovery or durable audit.
