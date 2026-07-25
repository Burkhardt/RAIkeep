# TODO Next Release RAIkeep

This document captures the next-release concurrency work needed for RAIkeep and JsonPit.

## Current Assessment

RAIkeep is not yet fully at the desired concurrency contract.

The project already has important concurrency-related tests and safeguards, and the test suite intentionally disables incidental xUnit test parallelism. That is appropriate while OsLib and JsonPit contain process-global state and real cloud-backed filesystem behavior.

However, disabling test-runner parallelism is not the same thing as proving product-level concurrency safety. RAIkeep needs explicit, intentional concurrency tests and a documented runtime contract for threads, processes, and machines.

## Next Release Goal

Make RAIkeep's concurrency behavior explicit, testable, and enforceable across:

1. multiple threads in one process
2. multiple processes on one machine
3. multiple machines sharing cloud-synced pit files

## Required Work

### 1. Define The Concurrency Contract

Document the intended behavior clearly.

The contract should answer:

- Can a single `Pit` instance receive concurrent `Add` calls?
- Can multiple `Pit` instances in one process target the same `.pit`?
- Can multiple processes target the same `.pit`?
- What is the master/client distinction for remote machines?
- When must clients write change files instead of overwriting canonical pit files?
- What guarantees exist for reads during writes?
- What happens when cloud sync is delayed, duplicated, stale, or out of order?

Expected promises should include:

- reads must never observe corrupt or half-written pit files
- accepted writes must not silently disappear
- client writes must not overwrite a master pit directly
- remote/client changes must be represented in a mergeable form
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

These tests should use real pits where appropriate and should make the concurrency behavior visible instead of hiding it behind test-runner scheduling.

### 3. Harden In-Process JsonPit Write Behavior

JsonPit should guarantee safe behavior for concurrent in-process use.

Required assertions:

- concurrent `Pit.Add` calls on one `Pit` instance do not lose updates
- concurrent additions receive fresh, unique enough `Modified` timestamps
- duplicate detection remains correct under contention
- history ordering remains stable and explainable
- saving after concurrent additions produces a valid pit file

Existing concurrency tests should be preserved and expanded only where they expose real behavior.

### 4. Define And Test Multiple Pit Instances In One Process

Add tests for more than one `Pit` instance targeting the same `.pit` path in one process.

Required scenarios:

- two instances load the same pit
- both add distinct items
- both save or trigger persistence
- no accepted update is lost
- stale in-memory state does not overwrite newer file state without a merge

This is a separate case from many threads sharing one `Pit` instance.

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

### 6. Strengthen Remote Client Behavior

For cloud/shared-machine usage, remote clients should not overwrite the canonical master pit directly.

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

Do not replace real cloud paths with local temp directories for tests whose purpose is to validate cloud-backed pit behavior.

Local temp directories are acceptable only for tests whose subject is purely local mechanics.

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
