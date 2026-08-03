# Change Request — JsonPit concurrency contract and persistence races

This document captures the next-release concurrency work needed for RAIkeep and JsonPit.

Status: open for the coordinated `3.13.1` line.

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

## Next Release Goal

Make RAIkeep's concurrency behavior explicit, testable, and enforceable across:

1. multiple threads in one process
2. multiple processes on one machine
3. multiple machines sharing cloud-synced pit files

## Required Work

### 1. Define The Concurrency Contract

Document the intended behavior clearly.

The contract should answer:

- Can a single `Pit` instance receive concurrent `Add` calls? RAI: yes
- Can multiple `Pit` instances in one process target the same `.pit`? RAI: no, there should be no more than one in-memory instance of each distinct pit per Process. If there are several threads running concurrently inside this one process, they should get synchronized through the used Container (i.e. ConcurrentDictionary, Keyed store in Kestrel, ...)
- Can multiple processes target the same `.pit`? RAI: yes, and each of the processes should identify themselves differently in their flag file; e.g. should two instances of Kestrel be able to run on the same machine, running different application (on different ports) but using the same WWWA pits, e.g. AIA and AfricaStage both using AfricaStage? RAI: I don't know ... should they? Do they have to? It's probably more reasonable to have the changes on AfricaStage done by the AfricaStage Kestrel instance and the changes on AIA done by the AIA Kestrel instance.
- What is the master/client distinction for remote machines? RAI: be more specific ... I do not understand what you are asking.
- When must clients write change files instead of overwriting canonical pit files? RAI: the JsonPit library must write change files always when a request to write can not get executed directly (in the MasterFile), because of the guard system that's built around the Masterflag file and the ProcessFlag files.
- What guarantees exist for reads during writes? RAI: a) in-memory: should already be covered by conditioned-critical-area handling (like in ConcurrentDictionary or other libraries); b) there is not supposed to be a mechanism to prevent concurrent read from file into the memory representation. Should not conflict under UNIX; c) while one in-memory representation is flushed, no other in-memory representation can be flushed because of the guard system around the Masterflag file and the ProcessFlag files; d) while one flush happens, the fileIO buffered read should still work, when requested from a different process - it should not work within the same process ... they have to wait; but as said before: in-memory read is the mainly supported model, there is supposed to be no direct reads allowed whatsoever from the same Process anyway. everybody reads from in-memory when inside the process and pits instances read from file or write to file but are not in-Process and can only access as permitted by the guard system.
- What happens when cloud sync is delayed, duplicated, stale, or out of order? RAI: a) delayed: this is covered in the "eventually persistent" concept of JsonPit. There is no harm in a delay of any amount of time for the system. Whenever the changes show up they will show up and considered accordingly => this is the beauty of JsonPit (or one of it). b) duplications are not a problem when they have different timestamps because then they just reflect 2 write operations at the almost same time. Even more so with real duplicates (Modified time is exactly the same), then the sorting takes care of it. c) most stale changes in my experiments were created through delete/change elsewhere/rename patterns. If nobody uses this pattern, the system should remain clean because the tested CloudDrive systems deal well with files. If any unforseen trouble occurs (mostly human or agent interaction), then human interaction will be necessary to clean up the mess.


Expected promises should include:

- reads must never observe corrupt or half-written pit files: RAI: since only one process can write at a time through the guard system, this should never happen; if it does happen, an exception should get thrown and the application that uses the library can react with their illegal use of JsonPit policy
- accepted writes must not silently disappear; RAI: I would like to know how that will be adressed before anything is implemented; in general: less is more
- client writes must not overwrite a master pit directly; RAI: well yes, clients that do not have master rights have to write ChangeFiles.
- remote/client changes must be represented in a mergeable form; RAI: no need to get into details here, the whole JsonPit system is built to support exactly this ... and yes, it should work and it does work.
- merge behavior must be deterministic; RAI: yes, I think it is and it should remain so.

### 2. Separate Test-Runner Parallelism From Product Concurrency

Keep ordinary xUnit test parallelism disabled for now.

The current non-parallel setting is a containment choice for tests that touch process-global state, real cloud roots, filesystem timing, and shared test infrastructure.

Do not use incidental xUnit parallelism as proof of concurrency safety.

Instead, add explicit concurrency suites that deliberately create controlled races:

- `InProcessConcurrencyTests`
- `MultiPitInstanceConcurrencyTests`
- `MultiProcessConcurrencyTests`
- `RemoteCloudConcurrencyTests`

These tests should use real pits where appropriate and should make the concurrency behavior visible instead of hiding it behind test-runner scheduling.
RAI: Yes, use real pits in CloudDrives, do not test in temp directories locally. We do not need irrelevant test results.

### 3. Harden In-Process JsonPit Write Behavior

JsonPit should guarantee safe behavior for concurrent in-process use.

Required assertions:

- concurrent `Pit.Add` calls on one `Pit` instance do not lose updates; RAI: yes
- concurrent additions receive fresh, unique enough `Modified` timestamps; RAI:yes
- duplicate detection remains correct under contention; RAI: well, I think it implicitely is, we'll see
- history ordering remains stable and explainable; RAI: yes, important
- saving after concurrent additions produces a valid pit file; RAI: yes

Existing concurrency tests should be preserved and expanded only where they expose real behavior.

### 4. Define And Test Multiple Pit Instances In One Process

RAI: No. I don't think we need this; I would consider it Library abuse. However, I would like an exception thrown when library abuse like this is detected by the library ... with a hint to use in-memory singletons like in the examples for Kestrel. 
Add tests for more than one `Pit` instance targeting the same `.pit` path in one process to test if the exception is thrown.

Required scenarios:

- two instances load the same pit => not allowed within the same process
- both add distinct items: RAI: do not test, do not implement
- both save or trigger persistence; RAI: do not test, do not implement
- no accepted update is lost; RAI: do not test, do not implement
- stale in-memory state does not overwrite newer file state without a merge; RAI: do not test, do not implement

This is a separate case from many threads sharing one `Pit` instance. RAI: Yes, it is and the surrounding process is responsible for making sure that a Singleton is implemented.

### 5. Harden Multi-Process Coordination

RAIkeep needs a clear production story for two processes writing the same pit.

The next release should decide and document the coordination mechanism:

- file lock
- lock file
- lease file
- master-ticket protocol
- change-file-only protocol for non-master writers
- or another explicit approach

Required behavior:

- writers must not corrupt the canonical `.pit`
- stale writers must not overwrite newer state
- stale locks or stale tickets must have recovery behavior
- lock/ticket failures must produce useful diagnostics
- retry behavior must be deterministic enough to test

This is likely the largest gap between thread-safety and real-world concurrency safety.

RAI: I agree with the goals and I believe the design of JsonPit is already fit to fulfill all those requirements ... without outlawing any of the above mentioned methods. Except file lock: I do not think we need (or can afford) this in a CLoudDrive environment. The masterflagfile and processflagfiles are the concept to solve all this.

### 6. Strengthen Remote Client Behavior

For cloud/shared-machine usage, remote clients should not overwrite the canonical master pit directly.
RAI: this is a bit simple-minded the way it's written. JsonPit does much more than this - it allows any client to take on master responsibilities temporarily under certain conditions ... the masterflagfile/processflagfile/timeWindow(lease) mechanism.

Required behavior:

- client machines write change files or another mergeable representation
- master machine merges client changes deterministically
- duplicate change files are safe
- out-of-order change arrival is safe
- delayed cloud sync is tolerated
- remote tests prove the master/client distinction

The existing remote-sync scenario should become reliable and explicit about the difference between master behavior and client behavior.

### 7. Preserve Real Cloud Semantics In Tests

Concurrency tests for cloud behavior must use the configured cloud roots when the behavior being tested is cloud behavior.
RAI: All concurrency tests should be performed within CloudRoots. Other concurrency tests are redundant or misleading.

Do not replace real cloud paths with local temp directories for tests whose purpose is to validate cloud-backed pit behavior. RAI: !!!

Local temp directories are acceptable only for tests whose subject is purely local mechanics. RAI: I would need to see a really good reason in this context to approve using local files. Test isolation is certainly not one of them.

### 8. Document The Release Acceptance Bar

The next release should not require every theoretical concurrency case to be solved, but it should clearly state what is supported.

Recommended acceptance bar:

- ordinary suite remains non-parallel
- explicit in-process concurrency tests pass
- explicit multi-`Pit` same-file tests pass or document the unsupported case
- explicit multi-process tests pass or document the unsupported case
- remote master/client test passes reliably or documents the unsupported case
- docs state exactly what concurrency RAIkeep supports and what it does not yet promise

## Non-Goals

For the next release, do not make broad architecture changes merely to satisfy test isolation.

Do not treat test-runner parallelism as a goal by itself.

Do not rewrite configuration loading as part of the concurrency work.

Do not use dependency injection or environment-variable manipulation to replace the real machine configuration model.

## RAI Warning

The above written statement "isolate Os.Config, Os.TempDir, RaiPath.CloudEvaluator, and environment mutation behind resettable or injectable context" is toxic and should be considered very carefully. Several weeks of work were created by an aggressive testing schema that first tried to use DI to isolate those static Os attributes. When the permisson to doing so was revoked, the LLM found different ways to test over and over again if the initial load of the config file was creating proper results under all kinds of strange conditions. We ended up testing the load of the config object hundreds of times in one debugging session totally hiding the real problem ... which was that the testing schema pulled the rug out from under the configuration of cloud-based pits in parts by testing them in local tempDirs instead ... which is totally irrelevant for this kind of library.

Pay attention that we are not going down this rabbit hole again - no focus on loading the config ... the config file loading is off limits except for the already approved and established tests for the config file and the before mentioned attributes in it, Os.Config, Os.TempDIr in particular. At no time, environment variables should play a role in the configuration of the library. The configuration file on every machine the library is executed on is the only source of truth and should not get tampered with for the purpose of test isolation.

RAI, 2026-07-24
