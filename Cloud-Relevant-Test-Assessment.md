# Cloud-Relevant Test Assessment

Date: 2026-03-13

## Historical note for 3.7.5

This assessment was written against the earlier provider-root API surface.

Where it mentions `Os.GetCloudStorageRoot(...)` or similar helpers, read that as historical context. The current OsLib model uses `Os.Config`, `CloudPathWiring`, `RaiPath.CloudEvaluator`, and buffered `RaiPath.Cloud` / `RaiFile.Cloud` state instead.

## Scope

This note assesses how well the current RAIkeep test suite detects problems that only show up in real cloud-backed sync environments, especially in the context of the core RAIkeep idea: several servers synchronized through one of the supported cloud providers.

Supported providers in scope:

- Dropbox
- OneDrive
- GoogleDrive
- ICloudDrive

The `3.5.0` package line named `Dropbox`, `OneDrive`, and `GoogleDrive`. The current configured-root contract also recognizes `ICloudDrive`.

## Honest Bottom Line

The current suite is useful, but it is not yet a strong detector of the most important real CloudDrive failure modes.

It is strong for:

- config-driven provider discovery
- provider-aware path classification
- cloud-root selection behavior
- local backup path normalization
- basic local file operations inside a cloud-managed folder on one machine

It is only moderate for:

- timing-related local provider behavior on a single machine
- catching obvious regressions in file operations under real provider roots

It is weak for:

- multi-machine synchronization correctness
- propagation delay across machines
- conflicting concurrent edits on different machines
- stale reads after remote writes
- provider-specific placeholder and hydration behavior
- rename and delete races across synchronized nodes
- recovery from offline or partially synced states

If the product claim is essentially "works across several servers synchronized via cloud storage", then the current suite does not yet validate that claim deeply enough.

## What Is Actually Real Today

The most cloud-relevant tests currently in the suite are:

- `OsLib/OsLib.Tests/CloudStorageRealWorldIntegrationTests.cs`
  - `RaiFile_RoundTrip_WorksAgainstRealWritableCloudProvider(...)`
  - `TextFile_SaveAndRead_WorksAgainstRealWritableCloudProvider(...)`
- `OsLib/OsLib.Tests/CloudStorageMachineStateTests.cs`
  - `MachineCloudState_PrintsDiscoveryInputs_AndProviderStatus_WithoutFailingForMissingRoots()`

These tests matter because they use actual provider roots discovered on the machine, not just temporary directories pretending to be cloud roots.

That is already better than a purely synthetic setup.

## What These Real Tests Do Well

### 1. They verify real provider-root discovery on an actual machine

The suite did exercise provider-root resolution against the machine's actual state.

That is important because discovery logic is exactly the kind of thing that often fails due to path conventions, machine-specific setups, and provider installation differences.

### 2. They verify that core file abstractions still operate inside real cloud-managed folders

The real-world integration tests create directories and files, copy files, move files, remove files, and read content back while operating under a real provider root.

That gives confidence that:

- the cloud-path classification is correct
- `RaiFile.Cloud` is being set correctly
- local wait logic does not immediately break in a real provider directory
- the abstractions are not only working in temp folders

### 3. They keep the suite connected to reality

Without these tests, the cloud support would mostly be validated by hermetic simulations. That would be too weak for a library whose value depends on behavior in provider-managed directories.

## Where the Current Suite Is Still Not Realistic Enough

### 1. Most cloud tests are still hermetic and config-driven

Many tests create local folders like `DropboxRoot`, `OneDriveRoot`, `GoogleDriveRoot`, and `ICloudDriveRoot` under a temp test root and then inject those paths into config.

Those tests are still useful, but they are not real cloud tests. They are local SSD tests with provider names attached.

Examples include:

- `CloudStorageDiscoveryTests`
- `CloudStorageProviderPathTests`
- `CloudStorageAgreementTests`

These tests are good for correctness of logic, but they do not reproduce provider timing, hydration, sync lag, or distributed conflict behavior.

### 2. The real-world tests are still single-machine tests

This is the biggest gap.

The current real tests prove that file operations work in a local folder that happens to be managed by a cloud provider on one machine.

They do not prove that:

- another server sees the change in time
- another server sees the same final content
- concurrent writes settle correctly
- provider conflict semantics are handled safely
- deletes, renames, and backups behave correctly across synchronized nodes

That means the most important distributed risks are still untested.

### 3. The assertions are mostly immediate local assertions

The real tests typically perform an operation and then immediately assert local existence and local content.

That catches some local timing issues, but not the hard cloud problems. Real cloud failures often involve delayed propagation, temporarily missing files, stale reads, conflicting versions, partially hydrated files, or provider-generated conflict copies.

### 4. Real-provider coverage can silently disappear through skip behavior

The integration tests skip when a provider root is not discoverable or writable on the current machine.

That is practical, but it means the most realistic tests do not form a guaranteed safety net unless they are run intentionally on machines with the right provider setup.

### 5. The suite does not yet stress the wait logic in a meaningful way

The code includes logic for cloud-aware materializing and vanishing behavior, but the current tests do not systematically provoke the failure patterns that normally justify such code.

There is no serious attempt yet to trigger:

- delayed appearance
- delayed deletion visibility
- rename lag
- provider lag under load
- conflict windows between writers

## Practical Rating

If this suite is judged specifically by how well it protects a cloud-synchronized multi-server product promise, the rating today is:

- Strong for local cloud-related logic
- Moderate for single-machine real-provider smoke coverage
- Weak for real distributed cloud synchronization behavior

That is the honest assessment.

## Why This Matters For RAIkeep

If RAIkeep depends on multiple servers coordinating through cloud-backed files, then the dominant risk is not usually path parsing or config loading.

The dominant risk is distributed timing and provider behavior:

- when does a change become visible elsewhere?
- what happens if two machines update the same file?
- what if one node reads while another node is mid-write or mid-rename?
- what if the provider leaves placeholder state or conflict artifacts?

The current suite gives some confidence around the library plumbing. It does not yet give strong confidence around these distributed behaviors.

## Recommended Next Work

The next high-value work should focus on real synchronization semantics, not more synthetic provider-name tests.

### Priority 1: Two-node real sync tests

Create a test harness that assumes two participating machines or nodes under the same provider root.

Minimum scenarios:

- Node A writes, Node B eventually sees the file and correct content
- Node A renames, Node B eventually sees the rename and no stale original
- Node A deletes, Node B eventually sees deletion

This is the single most important missing class of tests.

### Priority 2: Conflict tests

Introduce controlled concurrent write scenarios from two nodes and verify the observed outcomes.

Minimum scenarios:

- simultaneous writes to the same file
- write versus rename race
- write versus delete race

These tests should not assume ideal behavior. They should record actual provider outcomes and validate what RAIkeep can reliably guarantee.

### Priority 3: Bounded wait tests

Introduce tests that verify eventual consistency within explicit time windows instead of immediate local assertions only.

Examples:

- wait for appearance within a bounded timeout
- wait for vanishing within a bounded timeout
- wait for content change visibility on another node

This would finally exercise the kind of conditions that the cloud-aware wait logic is meant to handle.

### Priority 4: Provider-specific smoke profile

Keep a dedicated set of provider-specific smoke tests that can run on selected machines where all four providers are available.

These should be clearly separated from hermetic tests so failures mean something operationally real.

### Priority 5: Diagnostic output and traceability

When real-cloud tests fail, the output should capture:

- provider
- machine/node identity
- relevant root path
- operation timing
- whether failure was discoverability, writability, visibility lag, conflict, or content mismatch

That will make the failures actionable instead of anecdotal.

## Recommended Interpretation Of The Current Suite

What the suite currently justifies saying:

- cloud discovery logic is reasonably well covered
- provider-aware path logic is reasonably well covered
- OsLib can perform basic local file operations inside real provider-managed directories on one machine

What the suite does not yet justify saying confidently:

- RAIkeep is robust against real cross-machine cloud synchronization timing problems
- RAIkeep is robust against provider conflict behavior
- RAIkeep is well-tested for the real distributed scenarios that are central to its purpose

## Conclusion

The suite is not fake, but it is still too close to a local-filesystem test suite with some real-provider smoke coverage layered on top.

That is a solid base, but it is not yet enough for strong confidence in the actual cloud-synchronized multi-server behavior that matters most.

The next phase of testing should move decisively toward real-node, real-provider, eventual-consistency, and conflict-oriented integration coverage.
