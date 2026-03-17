# API-Level Remote Test Design

Date: 2026-03-13

## Purpose

This document defines the next quality level for RAIkeep remote testing.

The goal is to move beyond:

- local-only tests
- synthetic cloud-root tests
- remote disk visibility tests only

and toward API-level propagation testing.

The key idea is simple:

1. a change is written on Nkosikasi
2. the change is synchronized through the cloud provider to Mzansi
3. the change becomes visible on disk on Mzansi
4. the change becomes visible through the server API on Mzansi

That final step is the highest-value signal because it reflects what the real system exposes to callers.

## Testing Levels

The intended layered model is:

### 1. Logic-level tests

Purpose:

- verify pure logic
- verify path handling
- verify model behavior
- verify serialization and transformation rules

Characteristics:

- hermetic
- fast
- deterministic

### 2. Integration tests

Purpose:

- verify file, process, provider-root, and local cloud behavior
- verify library interaction under real provider-managed directories

Characteristics:

- may use real cloud roots
- may use real disk
- may still be single-machine

### 3. API-level propagation tests

Purpose:

- verify that a local change becomes visible at the remote application boundary
- measure how long it takes to become visible on disk and then through the API
- detect cases where synchronization succeeded but the server did not catch up

Characteristics:

- multi-layer
- cross-machine
- timing-aware
- operationally meaningful

This document focuses on level 3.

## Immediate Scope

First provider in scope:

- GoogleDrive

First source node in scope:

- Nkosikasi

First remote observer node in scope:

- Mzansi

First remote application target in scope:

- the OpenAPI of the `otw.software` server running on Mzansi

First domain target in scope:

- JsonPit-backed API-visible data

## Architectural Note: Asynchronously Persisted With Eventual Durability

JsonPit should be understood here as following a model of asynchronous persistence with eventual durability.

This is preferred over the looser phrase "eventually persistent".

Meaning:

- a change is not guaranteed to be durably visible everywhere immediately after the local write returns
- but the system is designed so that the change should become durably visible over time
- the key engineering question is therefore not only correctness of the final state, but also the timing and observability of convergence toward that state

This model is not suitable for every database workload.

It is not a strong-immediate-consistency model.

But it is suitable for more application domains than many people initially assume, especially when:

- temporary lag is acceptable
- convergence matters more than instant global visibility
- the system can tolerate asynchronous propagation between writer, synchronized storage, and application surface

That is exactly why API-level propagation tests matter here.

They verify not only that JsonPit can eventually become durable on remote infrastructure, but also how quickly and reliably that durability becomes observable through the application API.

## Design Decision: No Shell Variables As Primary Configuration

Shell variables were acceptable for the initial spike, but they are not the intended long-term setup.

For API-level remote tests, the setup should be typed, documented, and loaded through reusable config infrastructure.

### Decision

Use a dedicated typed remote test config file.

Do not overload `osconfig.json` with remote observer topology and API endpoint metadata.

### Reason

`osconfig.json` is machine-local runtime configuration.

Remote test topology is a different concern:

- remote observers
- ssh targets
- remote cloud roots
- API endpoints
- polling strategy
- scenario-specific identifiers

That belongs in a separate test-oriented config model.

## Proposed Config File

Proposed file name:

- `remote-test-config.json`

Proposed default location:

- macOS / Linux: `~/.config/RAIkeep/remote-test-config.json`
- Windows: `%APPDATA%\RAIkeep\remote-test-config.json`

This keeps it aligned with the existing OsLib config location model while separating concerns cleanly.

## Proposed Config Schema

```json
{
	"observers": {
		"mzansi": {
			"sshTarget": "rsb@Mzansi",
			"cloudRoots": {
				"googledrive": "/home/rsb/GoogleDrive-Mzansi/"
			}
		}
	},
	"apis": {
		"otwSoftware": {
			"baseUrl": "https://otw.software",
			"itemLookupPathTemplate": "/api/items/{id}",
			"timeoutSeconds": 180,
			"expectedStatusCode": 200
		}
	},
	"scenarios": {
		"jsonPitGoogleDriveMzansi": {
			"provider": "GoogleDrive",
			"observer": "mzansi",
			"api": "otwSoftware",
			"diskTimeoutSeconds": 120,
			"apiTimeoutSeconds": 180,
			"pollIntervalMilliseconds": 1000
		}
	}
}
```

## Proposed Typed Models

Suggested OsLib types:

- `RemoteTestConfigFile : ConfigFile<RemoteTestConfigModel>`
- `RemoteTestConfigModel`
- `RemoteObserverModel`
- `RemoteApiModel`
- `RemoteScenarioModel`

Suggested supporting abstractions:

- `RemoteTestEnvironment`
- `RemoteApiProbe`
- `RemoteCloudSyncProbe`

`RemoteCloudSyncProbe` already exists in first form.

The next major addition should be `RemoteApiProbe`.

## Proposed Reusable API Abstraction

Suggested responsibility of `RemoteApiProbe`:

- perform HTTP GET against the configured API endpoint
- return structured status/body/timing results
- poll until an expected state is visible
- support "exists", "contains value", and "gone" checks

This should be reusable and typed, not just ad hoc `curl` strings buried in tests.

Likely building blocks:

- `HttpClient`
- typed URL templates
- response predicate callbacks
- structured diagnostics object

## What The New Test Actually Verifies

A successful API-level remote test should tell us three distinct things:

### 1. Local persistence succeeded

The local writer finished its operation on Nkosikasi.

### 2. Remote disk propagation succeeded

The synchronized data became visible on disk on Mzansi under Google Drive.

### 3. Remote application propagation succeeded

The server-side application on Mzansi consumed or reflected the change and exposed it through the OpenAPI.

The distinction between 2 and 3 is crucial.

## First Explicit Scenario: CRUURD

The first high-value scenario should be:

- Create
- Read
- Update
- Update
- Read
- Delete

Abbreviation used here:

- CRUURD

This is intentionally richer than CRUD because two sequential updates plus a second read are more likely to expose lag, stale cache, out-of-order processing, or delayed indexing.

## Proposed CRUURD JsonPit Scenario

### Create

1. Create a new `PitItem` locally on Nkosikasi.
2. Save the `Pit`.
3. Record local save completion timestamp.
4. Wait until the JsonPit file or relevant content is visible on disk on Mzansi.
5. Poll the OpenAPI until the created entity is visible.

### Read

1. Perform an explicit API read.
2. Assert the expected item state.
3. Record API read timing.

### Update 1

1. Update one or more fields locally.
2. Save locally.
3. Wait for remote disk visibility of the updated content.
4. Poll API until update 1 is visible.

### Update 2

1. Update again with a distinct value set.
2. Save locally.
3. Wait for remote disk visibility of update 2.
4. Poll API until update 2 is visible.

### Read Again

1. Perform another explicit API read.
2. Assert the final post-update state.
3. Ensure no stale values remain visible.

### Delete

1. Delete the item locally.
2. Wait until the backing file or content is gone on Mzansi disk.
3. Poll API until the entity is absent or returns the expected not-found response.

## Timing Model

For each stage, capture:

- local completion time
- remote disk visible time
- remote API visible time

Suggested per operation metrics:

- `LocalWriteCompletedAt`
- `RemoteDiskVisibleAt`
- `RemoteApiVisibleAt`
- `DiskPropagationLatency`
- `ApiPropagationLatency`
- `TotalEndToEndLatency`

This gives clear diagnostic separation:

- sync lag
- application lag
- combined lag

## Assertions

The test should not just verify success. It should verify stage order.

Expected ordering:

1. local completion
2. remote disk visibility
3. remote API visibility

If API visibility happens before disk visibility according to measured timestamps, that usually indicates a flawed measurement path or incorrect test wiring.

## Failure Categories

The test result should categorize failure explicitly.

Suggested categories:

- local write failed
- remote disk timeout
- remote disk content mismatch
- API timeout
- API status mismatch
- API payload mismatch
- delete not reflected on disk
- delete not reflected on API

This matters because the whole point is to distinguish filesystem sync problems from application/API propagation problems.

## Proposed First Implementation Order

### Step 1

Add typed `RemoteTestConfigFile` support.

### Step 2

Refactor `RemoteCloudSyncProbe` to load from remote test config rather than shell variables.

### Step 3

Add `RemoteApiProbe` with:

- GET request support
- polling support
- structured result object

### Step 4

Implement first API-level JsonPit Create test.

### Step 5

Extend to full CRUURD scenario.

## Why Start With Create First

Although the end goal is CRUURD, the first executable API-level scenario should probably be Create only.

Reason:

- shortest end-to-end path
- easiest to diagnose
- lowest ambiguity
- validates config, SSH, disk propagation, and API polling before layering more complexity on top

Once Create is stable, add:

1. Read
2. Update 1
3. Update 2
4. final Read
5. Delete

## Proposed Names

Suggested class names:

- `RemoteTestConfigFile`
- `RemoteTestConfigModel`
- `RemoteObserverModel`
- `RemoteApiModel`
- `RemoteScenarioModel`
- `RemoteApiProbe`
- `JsonPitApiLevelRemoteTests`

Suggested first test names:

- `Pit_Create_PropagatesToMzansiDisk_And_OtwSoftwareApi_OverGoogleDrive()`
- later: `Pit_CRUURD_PropagatesToMzansiDisk_And_OtwSoftwareApi_OverGoogleDrive()`

## Documentation Consequence

Once implemented, `RemoteTestSetup.md` should be updated to reflect that remote observer and API settings are config-driven rather than shell-variable-driven.

## Conclusion

The next meaningful quality step is not merely more remote disk testing.

It is API-level propagation testing.

The best first implementation path is:

1. separate remote test config file
2. reusable API probe
3. first create-only end-to-end JsonPit API-level test
4. then full CRUURD scenario

That would materially raise confidence in the real operational behavior of RAIkeep.