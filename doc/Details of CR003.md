# Details of CR003

**Status:** Detailed implementation companion to the accepted CR003 contract  
**Date:** 2026-08-05  
**Nature:** Specification and implementation guidance only; this document does not implement or modify product code  
**Governing change request:** [`CR003_RAI_to_RAIkeep_JsonPit-concurrency-contract-and-persistence-races.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR003_RAI_to_RAIkeep_JsonPit-concurrency-contract-and-persistence-races.md)
**Supporting recovery design:** [`JsonPit-CONCEPT-Live-Split-Master-Recovery.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/JsonPit-CONCEPT-Live-Split-Master-Recovery.md)

## 1. Purpose And Reading Order

This document records the implementation-level meaning, rationale, sequencing, code seams, pseudocode, test ideas, and rejected approaches behind every substantial agreement in CR003. It exists so that an implementation agent does not mistake the concise language of the Change Request for a shallow change.

This is not a new Change Request and does not broaden CR003. The documents should be read in this order:

1. `CR003_RAI_to_RAIkeep_JsonPit-concurrency-contract-and-persistence-races.md` is the governing contract and release boundary.
2. `JsonPit-CONCEPT-Live-Split-Master-Recovery.md` is the accepted distributed-recovery protocol.
3. This document explains how those agreements fit the present code and where apparently easy implementations would violate them.
4. `JsonPit-FlagFiles-And-Concurrency.md` describes the 3.13.1 baseline from which CR003 proceeds.

If this companion ever appears to contradict the governing CR or concept, stop and resolve the discrepancy with RAI; do not silently choose one interpretation.

The source references below describe the working tree as observed on 2026-08-05. Some CR003 implementation work was already in progress in the JsonPit and OsLib child repositories when this companion was written. The implementation agent must re-read the live source rather than assuming that line numbers or partial classes remain unchanged.

### Test approach for document authority

The implementation review should use a requirements trace rather than treating a successful build as proof of completion. Every agreement heading in this document should map to at least one decisive automated test or configured-cloud acceptance scenario, and every numbered scenario in section 10 of the recovery concept must map back to an implementation path. A reviewer should be able to start at a CR sentence, find the corresponding source seam, find the decisive test, and identify the recorded release evidence. A missing link is an incomplete implementation even if all existing tests pass.

## 2. The Mental Model: Four Different Coordination Problems

CR003 separates four mechanisms that are easy to conflate:

| Mechanism | Scope | What it protects | What it does not claim |
|---|---|---|---|
| State/snapshot gate | One live `Pit` in one process | A coherent boundary between concurrent `Add` operations and snapshot capture | It is not held during serialization or filesystem I/O |
| Persistence/recovery gate | One live `Pit` in one process | Ordering among `Save`, `Reload`, merge, recovery, cleanup, and explicit disposal | It is not a cross-process or distributed lock |
| Live-instance path registry | One process | At most one public `Pit` per canonical pit path | It does not coordinate separate processes |
| Flag/change-file protocol | Multiple processes and machines | Cooperative master authority, non-master durability, handoff, and after-the-fact recovery | It is not an atomic distributed compare-and-swap |

The current `JsonPitBase._locker` is only an object-local monitor. It can serialize persistence work performed by that object, but it neither admits concurrent readers like a state/snapshot gate nor coordinates another `Pit` or another process. Likewise, `ConcurrentDictionary` prevents corruption of its own internal buckets; it does not turn a multi-step enumeration, sort, serialization, validation, and flag update into a coherent transaction.

The intended lock ordering is:

1. Enter the persistence/recovery gate for a persistence operation.
2. Briefly enter the state/snapshot gate exclusively to capture or publish coherent in-memory state.
3. Release the state/snapshot gate before serialization, cloud I/O, flag I/O, event I/O, retry delay, or cleanup grace handling.
4. Retain the persistence/recovery gate only for as long as necessary to prevent another persistence/recovery operation from invalidating the operation's assumptions.

`Add` enters only the shared side of the state/snapshot gate. It must not queue behind cloud I/O. A filesystem-watcher callback enters neither gate; it only coalesces and queues an evaluation that later uses the normal recovery gate.

### Test approach for the coordination model

Use explicit tasks and barriers rather than incidental xUnit scheduling. One test should hold a save between snapshot capture and file writing while multiple `Add` calls complete, proving that the state gate was released before I/O. A separate test should overlap two persistence operations and prove they do not both perform canonicalization or cleanup concurrently. A third should run the same path in two OS processes and prove that an in-process monitor is not being credited as cross-process protection. These tests should assert state transitions and persisted fragment identities, not merely that no exception occurred.

## 3. Current Code Map And Known Refactoring Seams

The principal existing and in-progress seams are:

| Component | File and symbols | CR003 relevance |
|---|---|---|
| JsonPit public state and persistence | `JsonPit/JsonPit.cs`: `Pit.AddCore`, `Load`, `Store`, `GetRawPersistenceModel`, `Save`, `CreateChangeFiles`, `MergeChanges`, `Reload`, constructors, `Dispose` | Main snapshot, load, merge, disposal, registry, and recovery integration point |
| Per-item dirty state | `JsonPit/PitItem.cs`: `Dirty`, `Valid`, `Validate`, `Invalidate`, `Modified` | Existing pending/persisted marker; no second public pending-state model is wanted |
| Immutable per-ID history | `JsonPit/PitItems.cs`: `History`, `Push`, `CompareFragments`, `ProjectState` | Exact replay, equal-time ordering, bounded history, deterministic projection |
| Master and process coordination | `JsonPit/JsonPitBase.cs`: `ParticipantIdentity`, `ExactProcessIdentity`, `TryAcquireMaster`, `ForeignChangesAvailable`, `EnumerateChangeFiles` | Stable versus exact identity, dynamic role, operation-boundary scans |
| Flag formats | `JsonPit/FlagFile.cs`: `MasterFlagFile`, `ProcessFlagFile` | Lease ownership, activity window, longer conflict-flag discovery |
| Change-file identity | `JsonPit/ChangeFile.cs` | In-progress canonical naming, hashing, parsing, and validation seam |
| Recovery status and audit interpretation | `JsonPit/Recovery.cs` | In-progress status, severity, JsonPit schema, and read-only event interpretation seam |
| Persistence exceptions | `JsonPit/Exceptions.cs` | In-progress descriptive bounded-read and duplicate-instance exceptions |
| Shared file-save behavior | `OsLib/TextFile.cs`: `Save`, `SaveInPlace` | No-delete/no-rename persistence behavior for all callers |
| Canonical JSON | `OsLib/CanonicalJson.cs` | In-progress generic recursive canonicalization and SHA-256 seam |
| Generic event storage | `OsLib/EventFile.cs`: `EventFile`, `EventDirectory` | In-progress create-once event files and stateless aggregation |
| CLI argument and execution routing | `PitSeeder/pits/Program.cs`: `Main`, `SwitchesWithValues`, `PositionalArg`, export helpers, active-pit cleanup | `--events` must branch before any `Pit` construction or flag lifecycle |
| Existing decisive regression | `JsonPit/JsonPit.Tests/RAIkeepConcurrencyRegressionTests.cs`: `SaveInterleavedWithAdds_SubsequentSavePersistsEveryAcceptedItem` | Reproduces the live enumeration/snapshot failure |
| Existing coordination tests | `JsonPit/JsonPit.Tests/MasterTicketTests.cs`, `PitChangeMergeTests.cs`, `RemoteSyncTests.cs` | Baseline to preserve and expand |
| Configured-cloud test routing | `JsonPit/JsonPit.Tests/RAIkeepTestEnvironment.cs` | Must continue using real configured roots and explicit prerequisites |
| CLI process-window tests | `PitSeeder/pits.Tests/LocalCliTicketWindowTests.cs` | Baseline for audit-mode noninterference and graceful disposal tests |

Several current paths are specifically unsafe to carry forward unchanged:

- `GetRawPersistenceModel()` enumerates live `HistoricItems`, which caused the confirmed `ConcurrentDictionary.ICollection.CopyTo` and LINQ materialization failures.
- `Store()` validates the current live latest fragments after I/O, so a fragment accepted after the written snapshot can be marked persisted prematurely.
- `Store()` derives flag time from the live state after writing, which can describe a newer state than the bytes actually written.
- `CreateChangeFiles()` creates another public `Pit` for comparison; CR003 requires a private snapshot reader because duplicate public instances must be rejected.
- `CompareToOtherHistory()` compares only `(Id, Modified)`, which collapses distinct equal-time content.
- `MergeChanges()` creates public `Pit` objects to parse change files and currently uses `Debug.WriteLine` for CR-related diagnostics.
- `MergeChanges()` currently deletes old change files before the canonical `Store`; CR003 requires canonical persistence first and a new ten-minute grace beginning at that successful save.
- `Load()` currently replaces `HistoricItems` before the candidate is fully parsed and can return `false` when a known file disappears during retry. Both behaviors violate the read contract.
- `Dispose()` currently saves but does not implement the recovery-write-set export, watcher shutdown, authority release, and path-registry sequence.
- A `lock` inside one `MasterFlagFile` instance does not coordinate another object or process and must never be described as a file lock.

### Test approach for the code-map refactoring

Preserve the confirmed regression as a permanent test and add targeted tests for every unsafe seam above. Mutation testing by temporarily restoring each old behavior is useful: restoring live enumeration should fail the snapshot test; validating live latest fragments should fail the late-add test; comparing only `(Id, Modified)` should fail the equal-time collision test; deleting before canonical save should fail the cleanup-order test; constructing a public comparison `Pit` should fail the path-registry test. This makes the suite resistant to a superficial rewrite that happens to pass once.

## 4. Agreement: Concurrent `Add` And Coherent `Save` Snapshots

### Exact meaning

Many threads may call `Add` on the one shared live `Pit`. Each accepted fragment remains represented by the existing `PitItem` dirty flag until a successful persistence operation has written a snapshot containing that exact fragment. A save may omit an addition that crosses the snapshot boundary; that is deliberate deferral, not data loss, provided the fragment stays dirty for a later save.

The state/snapshot gate should provide shared admission for additions and brief exclusive admission for snapshot capture. The persistence/recovery gate continues to serialize the larger persistence workflows. Do not solve the race by placing `Add` under `_locker`, because that would unnecessarily queue additions behind serialization and cloud filesystem delays.

The snapshot must contain both:

- an immutable/deeply stable persistence model used to generate the bytes; and
- the exact set of dirty live fragments whose state may be validated only after those bytes have been materialized successfully.

`PitItems.History` being an `ImmutableList<PitItem>` is helpful but not sufficient: each `PitItem` is a mutable `JObject`. A list snapshot that still points at objects being mutated is not a stable byte snapshot. Either clone the fragments while holding the exclusive snapshot boundary or establish and enforce immutability of stored fragments. CR003 does not authorize silently relying on callers never mutating a retained `PitItem` reference.

The explanatory sequence is:

```text
Add:
  enter shared state gate
  assign real UTC Modified once at the live insertion boundary
  perform duplicate check and CAS history replacement
  leave shared state gate

Save:
  enter persistence/recovery gate
  determine current exact-process role
  enter exclusive state gate briefly
  capture stable serialized histories + included dirty-fragment identities + snapshot change time
  leave exclusive state gate
  serialize and write without holding the state gate
  after successful local materialization, validate only the captured included fragments
  leave persistence/recovery gate
```

The snapshot's change time—not `GetLatestItemChanged()` queried against newer live state after I/O—must be used for any flag update describing the snapshot. `force: true` changes whether an otherwise clean snapshot is written; it does not permit validation of fragments outside the snapshot.

Do not introduce a second public pending queue. The private master-tenure recovery write set has a different purpose: it protects fragments that were made clean by canonical persistence but might later prove to have been written by a false master. It does not replace dirty state.

### Test approach

The decisive test has three phases. First, create enough configured-cloud data to keep save I/O observable. Second, block or repeatedly exercise save after its coherent snapshot boundary while adding uniquely identifiable fragments from several tasks; prove those `Add` calls finish before the save finishes. Third, inspect the first saved bytes and dirty state, then perform a second save and reload in a separate process. The assertions are: no materialization exception; the first file is one complete valid snapshot; every fragment in it was eligible for validation; every accepted late fragment remained dirty after the first save; and every accepted fragment appears after the second save. Repeat the race enough times to expose scheduling variance. A mere final item count without the intermediate dirty-state assertion would miss premature validation.

## 5. Agreement: Real UTC Timestamps, Not A Synthetic Clock

### Exact meaning

`Pit.Add` refreshes `Modified` from actual `DateTimeOffset.UtcNow` at the live insertion boundary. `AddHistorical` preserves the supplied historical timestamp. Timestamp uniqueness is neither promised nor required.

Do not create `Os.UtcNow`, a static last-value cache, a per-pit logical clock, or a rule that adds one tick when wall time repeats. The discussion rejected that pattern because a third wall-clock call can naturally be later, equal, or even appear earlier under clock adjustment; manufacturing a sequence makes timestamps dependent on how many internal getter calls happened. The same logical operation could then receive different values after an innocent refactor or on another machine.

Within one public `Add` invocation, read UTC once for the accepted insertion attempt rather than repeatedly restamping the fragment on CAS retries. The timestamp is metadata about the insertion boundary, not a retry counter. Historical merge, canonical load, and change-file replay must never route through the live `Add` timestamp refresh.

### Test approach

Replace any test requiring unique timestamps with a test that deliberately supplies or obtains equal timestamps and proves no accepted fragment disappears. A live-add test should start with a stale inherited `Modified`, call `Add`, and assert that the stored time was refreshed into the real call interval. An `AddHistorical` test should assert exact tick preservation. A contention test should prove deterministic history and projection without asserting `Distinct(Modified) == Count`. Tests must not replace the clock through environment variables, dependency injection, or a new time service.

## 6. Agreement: Exact Replay And Deterministic Equal-Timestamp Projection

### Exact meaning

An exact replay is the same fragment content, including the same identity and `Modified`, already present in that item's history. It is ignored and must not consume a bounded-history slot. Two fragments with the same `Id` and `Modified` but different content are not duplicates and do not cause an exception.

The deterministic history order is:

1. `Modified` descending.
2. For equal timestamps, JSON property count ascending.
3. For equal timestamps and equal property counts, canonical fragment content in ordinal order.

Projection keeps first-seen property precedence. Therefore, if `pi0` contains `p1..p10` and `pi1` at the same timestamp contains `p1..p11`, `pi0` sorts first because it has fewer properties. Its overlapping `p10` wins, while `pi1` can still contribute new `p11`. This accepts abusive read-modify-add use without throwing, yet every participant computes the same result from the same set of fragments.

Property count means the complete JSON object's property count. Shared metadata properties do not affect the comparison between otherwise comparable fragments because they occur in both. Canonicalization is paid only for the final time-and-count tie. It recursively orders object properties ordinally, preserves array order, and emits compact invariant JSON.

The current `PitItems.CompareFragments`, `Push`, and `ProjectState` are the natural implementation seam. The current `CompareToOtherHistory` `(Id, Modified)` key is not sufficient and must not be reused for exact replay.

### Test approach

Build the same history in every permutation of arrival order and compare both the ordered canonical fragments and projected result. Include: an exact replay that does not reduce useful bounded history; equal-time smaller-versus-larger fragments with a contradictory `p10` and new `p11`; equal-time/equal-count fragments whose original object-property order differs; equal-time/equal-count fragments whose values differ; and arrays whose order differs and must therefore remain distinct. The decisive assertion is identical projection and retained fragment set across permutations, not simply a stable sort in one insertion order.

## 7. Agreement: One Live Public `Pit` Per Canonical Path Per Process

### Exact meaning

Writable and read-only public instances are governed by the same rule: one live public in-memory `Pit` owns a distinct canonical pit path in a process. Threads share that object through an application singleton or keyed container. JsonPit detects misuse; it does not provide the application container.

A process-wide registry should reserve the canonical path before the constructor can load, create flags, merge, or mutate state. Constructor failure must remove only its own reservation. `Dispose` must release only the reservation owned by that instance, and repeated disposal must remain harmless. A second constructor must throw a descriptive `PitInstanceConflictException` before it performs observable pit work.

Path normalization should be centralized and based on the canonical `PitFile.FullName` used for persistence. Use the platform-appropriate path comparison and avoid having different constructors register a directory in one form and the canonical `.pit` file in another. The registry is not a reason to resolve cloud aliases, symlinks, or provider identities beyond the filesystem path contract already used by RAIkeep.

Internal comparison, load-candidate, and change-file parsing paths must be plain private readers/builders. In particular, the current `CreateChangeFiles()` and `MergeChanges()` construction of undercover/unflagged public `Pit` objects must disappear from those internal operations; flags such as `undercover` are not loopholes in the one-public-instance rule.

### Test approach

Construct a writable pit, then attempt writable and read-only duplicates using every public constructor form (`RaiPath`, `PitFile`, and `JArray` where applicable). Assert the same canonical path and exception message, and assert that no new process flag, master update, event, or data mutation occurred. Dispose the first instance and prove a new one opens successfully. Force a constructor failure after reservation and prove a later valid constructor succeeds. Race several constructors against the same path and assert exactly one succeeds. Finally, exercise save comparison and change-file merge on the valid instance to prove internal readers no longer trip the public registry.

## 8. Agreement: `TextFile.Save` Never Deletes Or Renames The Original Path

### Exact meaning

The behavior belongs to OsLib because JsonPit canonical files, flags, events, change files, and other coordination consumers need the same path-stability rule.

- `Save(backup: false)` creates the file if absent or truncates and writes the existing path directly.
- `Save(backup: true)` copies the old bytes to the configured backup location, then overwrites the original path directly.
- Neither path deletes, moves, renames, or performs temporary-file replacement of the original.
- Existing materialization checks remain.
- `SaveInPlace()` remains as a source/binary compatibility alias delegating to `Save(backup: false)`.

This contract provides pathname continuity, not atomic reader visibility. `File.WriteAllLines` or an equivalent direct overwrite can expose incomplete bytes while writing. JsonPit's candidate-read protocol is what prevents those bytes from becoming live state.

Do not add a file lock to compensate. A local `lock` in `MasterFlagFile.Save` only coordinates calls through that one object and does not become cross-process protection. The accepted design deliberately combines no-delete writes with validation and retry.

### Test approach

OsLib tests should attach a `FileSystemWatcher` to a configured cloud directory, repeatedly overwrite a file, and assert that no delete or rename event for the original path is generated while the path remains continuously discoverable. Backup tests should record old and new contents and prove the backup is a copy while the original path never vanishes. A concurrent reader should be allowed to observe a transient incomplete candidate; the corresponding JsonPit test must prove that candidate is rejected and never published. Retain existing materialization assertions. Local mechanics may supplement this only with the specific approval required by CR003; they do not replace configured-cloud evidence.

## 9. Agreement: Candidate-Based Load And Bounded Retry

### Exact meaning

`Load` and `Reload` must build a complete candidate independently of live `HistoricItems`. Only after the entire canonical payload has been read, structurally validated, parsed, and transformed into a complete candidate dictionary may an exclusive state boundary replace the live dictionary.

The implementation must distinguish:

- genuinely absent canonical file during initial creation: valid no-data result;
- a file known to exist that is transiently missing during overwrite or sync: retryable failure;
- empty, incomplete, sharing-violating, or temporarily unparsable content during a known rewrite: retryable failure;
- structurally incompatible content after a complete read: descriptive non-transient format failure;
- bounded retry exhaustion: `JsonPitPersistenceException`, while the prior live state remains intact.

The current `Load()` clears `HistoricItems` before `JArray.Parse` succeeds and returns `false` when the file disappears between retries. Both details must change. Retry diagnostics belong in the structured event/status path rather than `Debug.WriteLine`. The synchronous API may use bounded synchronous delay, but it must not hold the state/snapshot gate while waiting.

Fragments reconstructed from a successfully validated canonical pit represent already-persisted state and should enter the published candidate as clean. This must be explicit because the current `PitItem(JObject)` constructor initializes its private dirty state as dirty. Fragments ingested from an ordinary change file are durable in that file but are not thereby proven present in the canonical pit; their canonical-persistence/cleanup responsibility follows the merge protocol rather than being inferred from the constructor default.

The explanatory sequence is:

```text
remember whether the canonical file was known to exist
for each bounded attempt:
  read complete bytes into a local value
  parse and construct a separate candidate history
  on success, briefly publish the complete candidate under the state gate
  on a transient failure, retain live state and retry
after exhaustion, retain live state and throw a descriptive persistence exception
```

### Test approach

Seed a known live state, then have another process repeatedly overwrite a large configured-cloud canonical pit in place. During the overlap, call `Load`/`Reload` and continuously read the in-memory projection. Assert that every observed state equals either the complete old snapshot or the complete new snapshot—never empty, partial, or mixed. Separately make a known file transiently unavailable and assert retry rather than `false`. Force bounded exhaustion and assert the exception includes path, attempts, and underlying cause while the original in-memory state remains queryable. Finally, test initial absence separately so creation still returns the valid no-data outcome.

## 10. Agreement: Stable Participant Identity And Exact Process Master Ownership

### Exact meaning

`ParticipantIdentity` remains stable across process restarts: `{Machine}-{Subscriber}`. `ExactProcessIdentity` is the PID-specific process-flag stem: `{Machine}-{Subscriber}-{PID}`. The exact identity contains the stable identity and is what active `Master.flag` ownership records in v3.13.2.

Only the exact PID recorded in the valid canonical `Master.flag` may renew directly. A second PID with the same stable participant must use change files while the recorded PID-specific process window remains active. Once that process window is explicitly tombstoned or expires, the new PID may inherit the still-protected participant lease. Different subscribers on one machine remain distinct stable participants and follow the same protocol.

Every authority decision must reread the canonical flag sufficiently close to the protected operation. `RunningOnMaster()` is only a quick observation and must not authorize a canonical write without current lease validation. Roles are dynamic and per pit; one process may be master for one pit and non-master for another.

The current in-progress `JsonPitBase.TryAcquireMaster`, `MasterFlagFile.ParticipantOf`, `IsExactProcessIdentity`, and `ProcessFlagFile.IsProcessWindowActive` are the natural seams. Be wary of legacy participant-only master content during upgrade: it has no PID to prove active exact ownership. Compatibility handling must not let two live PIDs silently treat themselves as the same master.

No application is asked to invent subscriber names containing PIDs. Correct PID-level exclusion and handoff belong inside JsonPit.

### Test approach

Use helper processes, not two objects in one test process. Process A acquires and renews; process B uses the same subscriber and must create change files while A's process window is active. Tombstone A's window and repeat, then separately let it expire; B must inherit in both cases. Run two different subscribers on the same machine and prove they remain distinct. Verify the exact PID content of `Master.flag` after each boundary. A decisive test must inspect whether canonical bytes changed versus a change file being written; a boolean return from `TryAcquireMaster` alone is insufficient.

## 11. Agreement: The Lease Is Cooperative, Not A File Lock

### Exact meaning

The timed `Master.flag` protocol is deliberately not an operating-system file lock, distributed mutex, or atomic cloud compare-and-swap. Arbitrary cloud delay can allow two servers starting from independently visible expired state to write locally as apparent masters. CR003 handles this honestly through after-the-fact detection and live recovery rather than claiming perfect exclusion.

Do not add `FileStream` exclusive sharing, persistent open handles, lock files, named mutexes presented as distributed locks, or provider APIs. A process-local C# `lock` is useful for an object's own state but must not be treated as evidence that another process was blocked or queued in FIFO order. Waiting threads need no FIFO guarantee; correctness depends only on coherent boundaries and eventual completion.

The cloud provider's role is narrow but essential: when it detects conflicting writes to `Master.flag`, it may preserve the canonical name and create a longer conflict copy. JsonPit consumes that synchronized filesystem reality after the fact. It does not delegate recovery to the user.

### Test approach

The remote test should intentionally create the false-master window by coordinating two configured servers through the existing SSH-accessible remote environment. Both must record locally accepted writes before synchronization exposes the conflict. Evidence must include both process identities, the canonical and longer flag filenames, write timing, and eventual recovered fragments. The test must not pass merely because the provider synchronized quickly enough to avoid the race; it must reproduce the longer conflict artifact or report the prerequisite as unsatisfied for release acceptance.

## 12. Agreement: Collision-Safe Ordinary Change Files

### Exact meaning

Every ordinary change file—routine non-master persistence, live split-master recovery, normal master handoff, and graceful disposal—uses:

`{Modified.UtcTicks}_{ExactProcessIdentity}_{Sha256}.json`

The payload remains the established one-fragment JsonPit history container, currently represented as an outer array containing one history array containing one fragment. The full lowercase SHA-256 covers the exact canonical UTF-8 payload written to disk. Canonicalization recursively sorts object properties ordinally, preserves array order, and emits compact invariant JSON.

Avoid an ambiguous newline contract. Prefer writing exactly the canonical UTF-8 JSON bytes whose hash appears in the filename. If a shared text abstraction necessarily appends a line terminator, the reader and writer must agree whether those bytes are part of the hashed payload; trimming an arbitrary amount of whitespace after reading would weaken the “exact bytes” guarantee. Event and change files should have one documented byte-level convention and tests over the actual bytes on disk.

The timestamp is diagnostic and sortable, not unique. Exact process identity distinguishes publishers, and the hash distinguishes equal-time fragments from the same publisher. Re-publishing the same canonical fragment yields the same filename and is idempotent.

Before merge, retirement from a recovery write set, or any claim of durability, a reader/publisher must:

1. observe the complete materialized file;
2. read its exact bytes/content according to the writer's newline contract;
3. verify the filename hash;
4. parse the complete payload;
5. validate that the payload shape contains acceptable PitItem history data.

The filename parser should split at the first timestamp separator and final hash separator so hyphens inside machine/subscriber identity do not cause ambiguity. Compatibility with legacy `{ticks}_{identity}.json` files may be retained for upgrade ingestion, but legacy files cannot be credited with the new hash guarantee. Do not silently delete them merely because they cannot satisfy a v3.13.2 filename check.

The current in-progress `CanonicalJson` and `ChangeFile` classes are appropriate shared seams. OsLib owns generic canonical JSON and hashing; JsonPit owns the change-file payload shape and identity.

### Test approach

Publish two distinct fragments with identical `Modified` and exact process identity; assert different filenames and successful merge of both. Publish the same fragment repeatedly; assert one stable filename and no duplicate history. Reorder object properties and assert the same canonical hash; change a value and assert a different hash; reorder an array and assert a different hash. Write a partial file and a wrong-hash file and prove neither is merged, deleted, or removed from the publisher's in-memory responsibility. Complete the partial file and prove a later scan accepts it without a restart.

## 13. Agreement: Merge By Everyone, Canonicalize And Clean Only By The Current Master

### Exact meaning

Every participant may validate and merge ordinary change files into its in-memory history. This improves local read freshness and is safe because exact replay is idempotent. Such a merge is not a distributed acknowledgement and does not authorize canonical persistence.

Only the exact current master may write the reconciled canonical pit or delete change files. Authority must be revalidated at the canonical-persistence and cleanup boundaries; if `Master.flag` changes, responsibility follows the new exact master.

Cleanup is a strict two-stage protocol:

1. Validate and merge a change file.
2. Successfully persist a canonical snapshot accounting for its fragment under history retention.
3. Record an in-memory cleanup-eligibility timestamp for that file after the successful canonical save.
4. Keep it for ten minutes measured from that save.
5. On a later pass, revalidate exact master authority and canonical health, then delete.

Original file age does not count. Restart or master transfer loses the in-memory eligibility map, deliberately forcing another merge, canonical save, and fresh ten-minute grace. There is no acknowledgement sidecar.

The current `MergeChanges()` order—deleting files older than ten minutes before `Store()`—is the exact trap to remove. Its broad catch-and-ignore cleanup behavior must also become structured diagnostics; silent deletion failure may be retryable, but silent pre-save deletion is data loss.

### Test approach

Start with an old change file so its filesystem age already exceeds ten minutes. Merge it and prove it survives until after a successful canonical save plus a new ten-minute grace. Make the canonical save fail and prove the change file remains. Restart or transfer master during the grace and prove the new master starts a new merge/save/grace cycle. Have a non-master merge the same file and prove it neither writes the canonical pit nor deletes the file. Release acceptance should exercise the real ten-minute configured-cloud grace; a fast local substitute or injected clock does not prove the operational contract.

## 14. Agreement: Per-Master-Tenure In-Memory Recovery Write Set

### Exact meaning

The recovery write set is private in-memory state for one exact-process master tenure. It is not persisted, is not synchronized by the cloud provider, is not another public dirty flag, and is not a copy of the full pit.

A tenure begins when an exact process acquires canonical authority after not owning it. Renewals by that same exact process continue the tenure. Authority moving to another exact process ends it. Mere expiry followed by reacquisition by the same exact process does not create a handoff.

Before a successful master save marks snapshot fragments clean, every newly persisted fragment that could otherwise exist only in this process's canonical write must enter the tenure write set. If a master retires an incoming change file, that file must remain present or its fragments must first be represented in the write set. This preserves the ability to recover if the process is later revealed as the losing false master.

An entry stays in memory while it is its fragment's only recovery representation. It can be removed after its ordinary change file is locally written, fully materialized, hash-verified, and parsed. Cloud replication and current-master acknowledgement are not required to release the memory entry. Publication/removal is per fragment, so partial batch success removes only successful entries and retains failed ones for idempotent retry.

When authority moves to another exact process without a conflict flag, the former live master still exports its completed-tenure set plus current dirty fragments through ordinary change files, then continues as a non-master. This is the normal durable handoff path.

The explanatory lifecycle is:

```text
canonical snapshot succeeds:
  first record newly persisted snapshot fragments in current tenure write set
  then validate only those snapshot fragments

tenure ends or live loser is detected:
  snapshot union(write set, currently dirty fragments)
  publish one ordinary change file per fragment
  validate each local file independently
  remove only successfully represented entries
```

### Test approach

Let a master make several canonical saves during one tenure, with additions between them, and inspect the private behavior through outcomes rather than exposing a public queue. Transfer authority and assert that only tenure-written plus dirty fragments are exported—not the entire historical pit. Induce one file-write failure in a batch and prove successful siblings are released while the failed fragment is retried. Reacquire with the same exact process after expiry and prove no handoff export occurs; transfer to another PID and prove it does. Finally, simulate a later split-master loss and prove clean fragments from earlier saves are still recoverable because they had entered the tenure set before validation.

## 15. Agreement: Detect Longer `Master*.flag` Conflict Signals Without Polling Or Provider APIs

### Exact meaning

The detection pattern is provider-independent: enumerate `Master*.flag` and select filenames whose complete filename length is greater than `Master.flag`. The exact canonical name is never returned as a conflict. The suffix is opaque; do not encode Dropbox `(1)`, OneDrive naming, Google Drive naming, or iCloud naming rules.

Every live writable flagged `Pit` owns a native `FileSystemWatcher` on its pit directory for create, rename, and change signals relevant to `Master*.flag`. The callback only debounces/coalesces and queues at most one recovery evaluation. It does not read, parse, merge, delete, save, raise persistence exceptions, or invoke cloud APIs on the callback thread.

Notifications can be duplicated, coalesced, or missed. Correctness therefore also scans at construction, master acquisition, `Save`, `Reload`, and watcher-error recovery. There is no recurring polling timer.

Dispose must stop new callbacks, cancel or await queued recovery safely, and prevent a callback from operating on a disposed pit. Read-only or unflagged pits do not need the writable split-master watcher.

### Test approach

On each configured provider, materialize a longer conflict flag through the provider where possible and assert the same general detection path. Generate duplicate create/change/rename notifications and prove only one recovery evaluation is active. Deliberately disable or miss one watcher notification, then call an operation boundary and prove the scan recovers it. Dispose during a queued event and assert no callback or recovery task touches the disposed instance afterward. A test that manually calls the recovery method without exercising watcher and boundary-scan routing is not sufficient.

## 16. Agreement: Complementary Live Split-Master Recovery

### Exact meaning

The exact canonical `Master.flag` is the cloud-synchronized authority record. A longer conflict flag is evidence and contains the losing claimant's identity; it is never treated as another master. `Object.pit` filesystem reality on each live server supplies that process's local state, but JsonPit does not keep a persistent handle on it. The stronger recovery source is the still-live process's in-memory state, dirty fragments, and tenure write set.

The current-master role is:

1. retain canonical-write authority;
2. capture and reassert a coherent local canonical snapshot;
3. observe ordinary change files from the loser;
4. validate and merge them deterministically;
5. revalidate authority and persist the reconciled canonical pit;
6. apply the post-save cleanup protocol.

The live-loser role is:

1. stop canonical writes immediately after role determination;
2. snapshot the union of the tenure write set and dirty fragments;
3. publish ordinary small change files, never one bulk pit dump;
4. locally materialize, hash-check, and parse every required file;
5. delete only the longer conflict flag whose content names this exact process;
6. never modify exact `Master.flag` or canonical `Object.pit` as recovery master;
7. continue through the ordinary non-master path.

Both sides eventually see the same ordinary change files. All participants may merge, but whichever process is the exact master at the moment of canonical persistence owns the canonical step. Recovery must tolerate a master change mid-protocol.

Do not inspect, merge, delete, or infer authority from provider-created `Object (1).pit` or other noncanonical pit names. The discussion explicitly chose prospective live-memory recovery rather than guessing which noncanonical file contains which server's complete bytes.

### Test approach

The decisive two-server scenario must make both live processes write distinct clean and dirty fragments before the conflict appears. After detection, assert from durable evidence that the canonical owner never publishes as loser, the loser stops canonical writes, only its tenure/dirty union becomes small ordinary files, the longer losing flag remains until every required file validates, and the final canonical projection contains both sides. Change `Master.flag` during recovery and prove the new exact master completes canonicalization. Compare final histories—not only projections—to ensure no fragment was silently dropped or duplicated.

## 17. Agreement: Orphaned Conflict Evidence Is Retired Conservatively

### Exact meaning

If the exact process named in a longer conflict flag is no longer active, its in-memory write set is unavailable. CR003 accepts that abrupt-crash data-loss gap; it does not fabricate recovery from a noncanonical pit.

Only the exact current master may retire the orphan signal, and only after:

1. the claimant's PID-specific process window has expired or been released;
2. an additional ten-minute safety grace has elapsed;
3. a `Critical` durable event has been written containing the full conflicting filename and content, claimant identity, relevant timestamps, and the fact that no live write set was available;
4. that event has been locally materialized, hash-validated, and parsed.

Only then may the longer flag be deleted. Exact `Master.flag` and every noncanonical `Object*.pit` remain untouched.

### Test approach

Create a longer flag naming a helper process, terminate that process without graceful disposal, and prove the current master leaves the flag in place through process-window expiry and the additional real ten-minute grace. Make event writing or validation fail and prove the flag still remains. After a valid `Critical` event exists, assert that only the longer flag disappears, its full evidence remains readable, exact `Master.flag` is unchanged, and no noncanonical pit was opened or merged. Run the same scenario with a still-live claimant to prove the current master does not retire that claimant's flag on its behalf.

## 18. Agreement: Explicit Disposal Is A Durability Boundary; Finalization Is Not

### Exact meaning

Explicit disposal of a writable `Pit` is a coordinated durability operation:

1. enter the persistence/recovery gate so shutdown cannot overlap save/recovery;
2. snapshot the tenure write set plus dirty fragments;
3. publish and locally validate their ordinary change files;
4. optionally perform a canonical save if still exact master;
5. release process/master authority only after the ordinary files are durable;
6. stop the watcher and queued recovery;
7. release the in-process path registry reservation.

Change files come before the optional canonical save. If the canonical save fails, another master can still merge them. If accepted fragments cannot be made durable during explicit shutdown, record `Critical` status/event where possible and throw a descriptive persistence exception; do not report successful disposal while silently losing them.

A clean shutdown of a losing server is therefore treated like ordinary non-master persistence. An abrupt crash, forced termination, power loss, or application failure to dispose may lose the in-memory write set; that gap is explicitly accepted.

The finalizer must not perform filesystem, cloud-root, event, flag, save, or recovery I/O. It may release purely in-process bookkeeping if safely designed, but it cannot pretend to provide durability. PitSeeder's existing process-exit path currently calls `TryReleaseProcessWindow`; CR003 requires normal finite operations to dispose the `Pit` through the full durability sequence rather than only tombstoning the activity flag.

### Test approach

For a writable master, add clean tenure fragments and dirty fragments, dispose, and assert that ordinary change files validate before the process window is released. Force the optional canonical save to fail after change publication and prove disposal reports failure while the files remain mergeable. For a non-master, prove disposal publishes without touching canonical bytes. For a read-only pit, prove no persistence occurs but watcher/registry/process ownership is cleaned up as applicable. A finalizer test should abandon an object, force collection, and assert no files, flags, or events were created or modified by finalization.

## 19. Agreement: Generic OsLib Event Files And Stateless Event Aggregation

### Exact meaning

OsLib owns storage mechanics, not JsonPit event meaning.

`EventFile : TextFile` accepts an owning root path, a logical filename stem, and either a `JObject` or dynamic value that serializes to exactly one top-level `JObject`. It derives `rootPath / EventDirectory.Name`, creates the `Events` directory on the first write, canonicalizes the object, hashes the canonical UTF-8 content, and writes one immutable file:

`{LogicalStem}_{Sha256}.event`

The constructor usage agreed in the discussion is intentionally convenient: constructing an `EventFile` with non-null content performs the create-once write following the existing `TextFile(path, name, ext, content)` spirit. An implementation may factor private helpers, but it should not require every caller to remember a separate public `Write()` merely to obtain the agreed `new EventFile(..., content)` behavior.

Same stem plus same canonical content is an idempotent success. Same stem plus different content naturally gets a different hash filename. If the computed hash path already contains different bytes, preserve the existing file and write the new content under a collision-nonce suffix. A filename/content collision must not interrupt the operation being audited.

`EventDirectory` is a static class with `public const string Name = "Events"`. `EventDirectory.Events(RaiPath rootPath)` derives the child path internally, creates nothing, and returns a fresh `Dictionary<string, JObject>` on every call. The complete filename including `.event` is the key; the unchanged parsed single object is the value. There are no instances, constructor state, cache, watcher, or refresh method.

OsLib does not group by machine, sort by time, demand JsonPit fields, or know a JsonPit schema. Filename-hash validation is storage integrity, not content interpretation. An incomplete, unparseable, or hash-invalid individual event is omitted for the current call and reconsidered on the next fresh enumeration without hiding valid siblings.

The current in-progress `OsLib/EventFile.cs` already embodies much of this design, but its current constructor documentation says nothing is written until a separate `Write()` call. That is a detail to reconcile with the constructor-write agreement above; this report does not alter the in-progress code.

### Test approach

Construct an event and immediately assert the directory and file exist without an extra caller action. Construct the identical event again and assert no rewrite or duplicate. Use the same stem with changed content and assert two hash-derived files. Precreate a different-content file at the expected hash path and assert both old and nonce-suffixed new artifacts survive. Call `EventDirectory.Events` before the directory exists and prove it returns empty without creating anything; call again after adding files and prove it refreshes. Mix valid, incomplete, malformed, and wrong-hash files and assert only valid complete-filename/unchanged-`JObject` pairs are returned. Include arbitrary non-JsonPit objects to prove OsLib has no schema dependency.

## 20. Agreement: JsonPit Recovery Status, Events, And Error Semantics

### Exact meaning

Every live `Pit` exposes an immutable `LastRecoveryStatus` and an optional `RecoveryStatusChanged` event. Recovery correctness cannot depend on a subscriber. Each meaningful stage also writes durable JsonPit event content through OsLib `EventFile` rather than relying on `Debug.WriteLine`.

The required stages are `ConflictDetected`, `RoleDetermined`, `ChangeFilesPublished`, `Canonicalized`, `CleanupPending`, `Completed`, `DeferredForRetry`, and `Failed`. Event content includes schema version, event ID, UTC, severity, stage, pit identity, exact local process, current master, role, affected fragment/file counts, correlation or tenure ID, source operation, message, and optional exception detail.

Severity uses `Microsoft.Extensions.Logging.LogLevel` names:

| Stage/condition | Level |
|---|---|
| `ConflictDetected` | `Warning` |
| `RoleDetermined` | `Information` |
| `ChangeFilesPublished` | `Information` |
| `Canonicalized` | `Information` |
| `CleanupPending` | `Debug` |
| `Completed` | `Information` |
| `DeferredForRetry` | `Warning` |
| `Failed` | `Error` |
| Explicit-shutdown durability failure | `Critical` |

`None` is never persisted. Status publication should update the immutable current value before notifying observers. A subscriber is optional and must not become a hidden durability dependency. Watcher-thread failures become status/events and queued retry, never exceptions escaping the callback. Explicit `Save`, `Reload`, and graceful `Dispose` throw descriptive persistence exceptions when their bounded durability promise cannot be fulfilled.

Ordinary event-recording collision handling must not block the audited operation. The orphan-cleanup case is deliberately stricter: its validated `Critical` event is a prerequisite to deleting conflict evidence, so inability to produce that durable evidence defers cleanup.

### Test approach

Run recovery with no subscriber and assert complete correctness plus durable stages. Subscribe and record immutable status objects; assert ordered stage/correlation data and that `LastRecoveryStatus` always equals the latest published value. Exercise watcher failure and prove no callback-thread exception escapes while `DeferredForRetry` is visible. Exercise explicit save/reload/dispose failure and assert a descriptive exception plus `Failed`/`Critical` evidence as appropriate. Verify every default level and prove `None` is rejected. Finally, make ordinary event-name collision handling occur without failing recovery, then make orphan evidence unwritable and prove cleanup is correctly blocked.

## 21. Agreement: `pits --events` Is A Read-Only Audit Path

### Exact meaning

The PitSeeder-produced CLI adds:

`pits -r <root> <PitName> --events`

`--event-machine all|local|<machine>` defaults to `all`. `--event-level <level>` is a case-insensitive inclusive minimum and defaults to `Trace`. Existing `--json` emits filtered JsonPit events as JSON; otherwise output is human-readable and ordered by machine, UTC, and event identity. `--wwwa --events` is outside CR003.

Audit routing must happen before any `Pit` construction. It reads `EventDirectory.Events`/JsonPit's interpretation directly from `pitRoot / PitName`. It must not call `TrackPit`, create a `ProcessFlagFile`, touch `Master.flag`, acquire a lease, merge change files, write an event about reading events, or participate in normal CLI process-window cleanup.

In `PitSeeder/pits/Program.cs`, both value-taking options must be added to the argument parser's value-switch set so their values are not mistaken for the positional pit name. `--events` itself must qualify as execution intent even without `--json` or `-e`. Invalid levels, missing option values, missing pit name/root, and the unsupported `--wwwa` combination should produce clear CLI errors without side effects.

### Test approach

Create several `.event` files for multiple machines and levels, snapshot every pit-directory filename and timestamp, run the CLI in human and JSON modes, then compare the filesystem snapshot. Assert correct all/local/named-machine filtering, inclusive severity (`Warning` includes Warning/Error/Critical), case-insensitive parsing, and deterministic ordering. Assert JSON is parseable and human output follows the same event order. Most importantly, assert no process flag, master flag, change file, canonical change, or new audit event appears. Invalid-argument tests must make the same no-side-effect assertion.

## 22. Agreement: Real Configured-Cloud And Remote Tests Are Release Evidence

### Exact meaning

The established configuration file on each machine remains the sole source of truth for `Os.Config`, `Os.TempDir`, cloud roots, and SSH-accessible remote prerequisites. CR003 must not add dependency-injected filesystem/configuration contexts, reset global configuration, rewrite config files, manipulate environment variables, substitute `RaiPath.CloudEvaluator`, or move concurrency tests into local temporary directories to make them easier.

Ordinary xUnit parallelism stays disabled because process-global and real-cloud tests share infrastructure. Product concurrency is proven by explicit tasks/processes/servers inside named tests, not by allowing the runner to schedule unrelated tests concurrently.

Missing configured prerequisites cause a precise skip on an ordinary developer machine. A skip is not a pass and cannot satisfy coordinated 3.13.2 release acceptance. The deliberate release run must execute all applicable tests against configured cloud roots and the configured remote node and record provider, machines/processes, exact tests, outcomes, conflict artifacts, and observed timing.

Purely local mechanics require the specific justification and approval described by CR003. They can supplement but never replace the configured-cloud scenario whose semantics matter.

### Test approach

Organize explicit suites named `InProcessConcurrencyTests`, `MultiPitInstanceConcurrencyTests`, `MultiProcessConcurrencyTests`, and `RemoteCloudConcurrencyTests`. Each test should report the actual configured root/provider and exact process identities in its evidence. Add a release-evidence script or documented command sequence that fails acceptance when a required test is skipped, even if the test runner's numerical result is otherwise green. Preserve the existing non-parallel assembly setup and run the full suite repeatedly enough to expose cloud propagation variance.

## 23. End-To-End Operation Sequences

These sequences summarize the intended ordering. They are explanatory pseudocode, not prescribed C# structure.

### Master save with concurrent additions

```text
persistence gate
  operation-boundary conflict scan
  validate exact master authority
  exclusive state snapshot
    capture stable histories, included dirty fragments, snapshot timestamp
  release state snapshot gate
  add newly persisted fragments to tenure recovery set
  serialize/write/materialize canonical bytes
  update exact master/process flags from snapshot facts
  validate only included snapshot fragments
release persistence gate

concurrent Add uses shared state gate and may finish during file I/O;
its fragment remains dirty if it missed the snapshot.
```

### Non-master save

```text
persistence gate
  operation-boundary conflict scan
  fail exact-master acquisition
  exclusive state snapshot of dirty/local fragments
  release state gate
  compare against a private validated disk candidate, never a public Pit
  publish each missing fragment as a validated hash-named change file
  clear responsibility only per successfully materialized fragment
release persistence gate
```

### Master merge and cleanup

```text
persistence gate
  enumerate and validate complete change files
  merge exact non-replays under state gate
  revalidate exact authority
  persist canonical snapshot containing merged fragments
  mark those files cleanup-eligible now
release persistence gate

on a later pass after ten minutes:
  revalidate exact authority and canonical health
  delete only still-eligible files
```

### Live split-master loser

```text
watcher/boundary scan queues recovery
persistence gate
  read exact Master.flag
  determine that this exact process lost
  stop canonical writes
  snapshot tenure write set + dirty fragments
  publish/validate ordinary files per fragment
  if every required fragment is represented:
    delete only the longer conflict flag naming this process
  otherwise retain evidence and retry
release persistence gate
```

### Graceful writable disposal

```text
persistence gate
  stop accepting conflicting persistence/recovery work
  snapshot tenure set + dirty fragments
  publish/validate ordinary files first
  optionally canonical-save if still exact master
  release process authority/window
  stop watcher and queued work
  release path registry
release persistence gate and finish disposal
```

### Test approach for end-to-end ordering

For each sequence, capture durable event stages and filesystem observations so the test can prove order rather than infer it. Assertions should include “A existed before B” relationships: change file before process-window release; canonical bytes before cleanup eligibility; eligibility before ten-minute deletion; critical evidence before orphan-flag deletion; snapshot capture before late `Add`; and loser file validation before longer-flag removal. Timestamped logs alone are not enough when timestamps can tie; use event IDs/correlation and direct filesystem barriers where possible.

## 24. Explicit Traps And Rejected Shortcuts

The implementation is not complete if it uses any of these shortcuts:

- Treating `ConcurrentDictionary` enumeration as a stable multi-step snapshot.
- Locking `Add` behind all save/cloud I/O.
- Validating the live latest fragment after writing an older snapshot.
- Computing flag metadata from live state newer than the written snapshot.
- Adding a global/per-pit monotonic clock or injected time source.
- Rejecting different equal-time fragments or comparing them only by `(Id, Modified)`.
- Allowing two read-only public pits for the same path because they appear harmless.
- Constructing undercover/unflagged public `Pit` objects as internal readers.
- Treating `lock`, `Monitor`, `ConcurrentDictionary`, an open `FileStream`, or a lock file as distributed master exclusion.
- Requiring callers to encode PID uniqueness into subscriber names.
- Deleting, renaming, or temporary-replacing a `TextFile` path during save.
- Returning empty/false when a known canonical file transiently disappears during rewrite.
- Publishing a partial load candidate into live state.
- Naming change files only by timestamp and machine/participant.
- Trusting a hash-named file without checking both exact bytes and complete parse.
- Removing a failed fragment from the recovery write set because siblings succeeded.
- Dumping the complete losing pit instead of publishing its bounded tenure/dirty union.
- Using provider-specific conflict suffixes, cloud APIs, a provider matrix, or continuous polling.
- Reading longer conflict flags as authority or reading `Object (1).pit` as recovery input.
- Letting the current master delete a still-live loser's conflict flag.
- Deleting a change file based on original age or before canonical persistence.
- Keeping cleanup eligibility across restart or master transfer.
- Performing recovery or filesystem I/O in a finalizer.
- Using `Debug.WriteLine` as the CR003 diagnostic record.
- Giving OsLib knowledge of JsonPit event fields, machine grouping, severity, or stage semantics.
- Caching `EventDirectory.Events` or requiring a refresh call.
- Putting multiple event objects in one `.event` file or copying the filename into its JSON content.
- Making ordinary audit reads open a `Pit` or create their own audit event.
- Replacing real configuration/cloud roots with dependency injection, environment variables, rewritten config, or temporary directories.
- Counting a skipped configured-cloud test as release acceptance.

### Test approach for rejected shortcuts

During review, select representative negative mutations or temporary branches that reintroduce these shortcuts and confirm the corresponding test fails. At minimum, exercise live enumeration, live-fragment validation, timestamp-only filenames, cleanup-before-save, public comparison pits, missed watcher notification, event-directory caching, and `pits --events` constructing a `Pit`. This is especially valuable for concurrency behavior, where a happy-path test can remain green while the implementation has quietly lost the agreed invariant.

## 25. Suggested Implementation Order Without Scope Expansion

1. Finish generic OsLib primitives: canonical JSON, no-delete `TextFile.Save`, `EventFile`, and `EventDirectory`, with OsLib-owned tests.
2. Finish deterministic JsonPit fragment ordering/replay and collision-safe change-file identity/validation.
3. Add the one-public-pit registry and private candidate readers so later work cannot depend on duplicate public instances.
4. Introduce state/snapshot and persistence/recovery gate topology; repair `Add`, `Save`, `Store`, `Load`, and `Reload` around coherent snapshots.
5. Finish exact-process master ownership and normal handoff.
6. Add tenure write-set lifecycle, merge/persist/cleanup ordering, and graceful disposal.
7. Add watcher/boundary conflict detection and live/orphan recovery.
8. Integrate immutable status and durable JsonPit events.
9. Add read-only `pits --events` routing and filters.
10. Execute component tests, explicit in-process/multi-process tests, then configured-cloud/SSH acceptance scenarios; update coordinated release notes only from actual evidence.

This order minimizes circular dependencies. It is not permission to publish packages, create a version tag, or trigger NuGet workflows. Release operations remain separate and require explicit authorization.

### Test approach for incremental implementation

At each step, run the owning component's tests plus all already-completed downstream contract tests. OsLib changes should be proven before JsonPit relies on them; JsonPit behavior should be proven before PitSeeder exposes it. Keep a trace table showing which CR agreement became green at each step. Do not postpone all concurrency validation until the end, because a late failure would make it difficult to identify whether the defect belongs to snapshotting, coordination, recovery, or CLI routing.

## 26. Completion Checklist For The Implementation Agent

Before describing CR003 as implemented, verify all of the following:

- The governing CR and recovery concept were read completely.
- Every public or behavioral contract has XML/API documentation where appropriate.
- One shared `Pit` supports concurrent `Add`; a second public same-path `Pit` is rejected.
- Save captures stable bytes and validates only included fragments.
- Late additions remain dirty and persist later.
- Live timestamps use one real UTC boundary without uniqueness assumptions.
- Equal-time distinct fragments survive and project deterministically.
- `TextFile.Save` never deletes/renames the original and backup copies first.
- Load candidates never partially replace live state and bounded exhaustion throws descriptively.
- `Master.flag` authority is exact-process and dynamic.
- Ordinary change filenames contain ticks, exact process identity, and full canonical SHA-256.
- Every change file is hash/parse validated before use or responsibility transfer.
- Tenure write-set and dirty-fragment handoff cover conflict, normal transfer, and graceful disposal.
- Every participant may merge; only current exact master canonicalizes and cleans.
- Cleanup begins its grace after successful canonical save and resets on restart/transfer.
- Watcher plus operation-boundary scans detect general longer `Master*.flag` evidence.
- Loser and orphan evidence deletion rules are enforced exactly.
- Noncanonical `Object*.pit` copies remain untouched.
- Finalizer performs no filesystem I/O.
- JsonPit statuses/events and OsLib generic event mechanics remain correctly separated.
- `EventFile` preserves the agreed constructor-write convenience.
- `EventDirectory.Events` is static, fresh, and schema-agnostic.
- `pits --events` is filtered, deterministic, and side-effect-free.
- Every substantial agreement has a decisive owned test and every recovery-concept scenario is covered.
- The required configured-cloud/SSH release run contains no required skip.
- Release evidence names exact providers, machines/processes, tests, artifacts, timings, and outcomes.
- Release notes reference `CR003_RAI_to_RAIkeep_JsonPit-concurrency-contract-and-persistence-races.md` by its exact immutable filename.

Passing compilation and the legacy suite alone does not satisfy this checklist. CR003 is complete only when its concurrency and recovery invariants are demonstrated under the explicit thread, process, machine, and configured-cloud conditions for which they were designed.

## 27. Trace Of The 28 Required Recovery Scenarios

This table restates the recovery concept's numbered scenarios as decisive implementation evidence. It does not replace the fuller test explanations above.

| # | Scenario | Decisive proof |
|---:|---|---|
| 1 | Two servers begin from expired or independently visible master state | Recorded preconditions show both configured servers saw claimable state before either saw the other's claim |
| 2 | Both claim and write distinct accepted history | Each live process records a unique fragment accepted and canonically written during its apparent tenure |
| 3 | Provider creates canonical plus longer conflict flag | Release evidence includes exact `Master.flag` and actual longer `Master*.flag` filenames from the configured provider |
| 4 | Both watchers receive or recover the signal | Each process records conflict detection, whether by watcher or the documented boundary fallback |
| 5 | One canonical owner at each persistence boundary | Every canonical write is correlated with a fresh read validating the exact PID in canonical `Master.flag` |
| 6 | Loser publishes only write-set plus dirty fragments | Published IDs equal that union and exclude unrelated older pit history |
| 7 | Everyone may merge; only current master canonicalizes/cleans | Non-master projections update without canonical or deletion side effects; exact master performs those side effects |
| 8 | Recovery is idempotent | Repeating scans/publication/merge leaves one exact fragment each and loses none |
| 9 | Missed watcher signal is recovered | Suppress or miss the notification, invoke the next operation boundary, and observe recovery without a polling timer |
| 10 | Watcher disposal is complete | After dispose returns, no callback, queued task, status, event, or filesystem mutation occurs for that pit |
| 11 | Equal-time fragments get distinct change files | Same publisher and ticks with different canonical content yield different hashes and both histories survive |
| 12 | Master changes during recovery | The former master stops canonical work and the newly recorded exact master completes it without fragment loss |
| 13 | Explicit disposal exports before authority release | Validated ordinary files are observable before the process-window/authority release; optional canonical failure does not remove them |
| 14 | Finalizer performs no publication | Forced collection without explicit dispose produces no file, flag, event, watcher, or recovery I/O |
| 15 | Canonical object order hashes equally | Reordered object properties hash identically; changed values and reordered arrays do not |
| 16 | Invalid/incomplete change file is not credited | It is not merged, processed, deleted, or removed from in-memory responsibility |
| 17 | Per-fragment responsibility transfer | Successful siblings leave the write set after local validation while a failed sibling remains retryable without cloud acknowledgement |
| 18 | No deletion before canonical save | A forced canonical failure leaves every processed change file present |
| 19 | Grace starts at canonical persistence | A pre-aged change file still remains for the full ten minutes after the successful save |
| 20 | Restart/master transfer resets eligibility | New process/master repeats merge and persistence and begins a fresh grace rather than inheriting old memory |
| 21 | Event filename collision behavior | Multi-machine coexistence, idempotent same content, different-content hash names, and nonce collision preservation all succeed |
| 22 | Fresh schema-agnostic event aggregation | Missing directory stays absent/empty; later calls discover new complete files as filename/unchanged-object pairs |
| 23 | Bad event isolation and reconsideration | One bad event does not hide valid siblings; completing it makes it appear on a later fresh call |
| 24 | Durable and live status need no subscriber | Recovery completes without a handler while durable stages and `LastRecoveryStatus` remain available |
| 25 | Live loser owns its evidence deletion | Longer losing flag remains until all of that loser's required files validate; exact `Master.flag` never changes through this deletion |
| 26 | Orphan deletion requires critical evidence | Exact current master waits expiry plus ten minutes, validates full `Critical` evidence, deletes only the longer flag, and never merges noncanonical pit data |
| 27 | Normal master transfer exports; reacquisition does not | Different exact PID receives ordinary handoff files even without conflict evidence; same exact PID renewal/reacquisition produces none |
| 28 | `pits --events` filters and remains read-only | All/local/named machine and inclusive severity outputs are correct in JSON/human form, with a before/after filesystem proof of zero pit/flag/event side effects |

### Test approach for trace completeness

The final test report should cite the exact automated test name and result beside every row. Remote/provider-dependent rows should additionally cite the configured provider, machine names, exact process identities, conflict filenames, and propagation timing. No row may be closed by a skipped test, a manual assumption, or another row's broad “end-to-end passed” statement.
