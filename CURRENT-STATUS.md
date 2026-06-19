# CURRENT-STATUS

This file captures the current release-ready status of the RAIkeep workspace so a later session can resume without re-deriving the recent decisions.

## Current focus

The current release-and-docs alignment pass is `3.10.2`.

## 3.10.2 release decisions

- The active OsLib config contract remains `RAIkeep.json5` with PascalCase property names and lazy `dynamic` access through `Os.Config`.
- `UserHomeDir` and `AppRootDir` are intrinsic runtime values.
- `TempDir` and `LocalBackupDir` remain config-driven.
- `SyncPropagationDelayMs` is optional config and can override metadata-propagation waits.
- `CloudPathWiring` initializes `RaiPath.CloudEvaluator`, and `RaiPath` buffers its `Cloud` state.
- Directory wait logic lives in `RaiPath`; file wait logic lives in `RaiFile`.
- `RaiImage` now preserves separated and compact trailing image numbers during `EasyFileName(...)` normalization and keeps all-uppercase tokens intact in `WordCase` PascalCase output.
- `ImgSeeder` is now part of the umbrella release line and the parent sequential NuGet release chain.

## Current implementation status

Completed concepts currently in the codebase:

- `Os.Config` is lazy, internal-load, and backed by `RAIkeep.json5`
- `Os.IsConfigLoaded` exposes config lifecycle state without opening a public reload API
- `CloudPathWiring` provides the delegate bridge from `Os.Config` to `RaiPath.CloudEvaluator`
- `RaiPath` buffers its `Cloud` state and owns directory wait logic
- `RaiFile` copies the buffered `Cloud` flag and owns file wait logic
- `RaiFile.DefaultSyncPropagationDelayMs` provides the in-process fallback for metadata propagation waits
- `RaiFile.BackdateCreationTime(...)` supports deterministic remote-sync test setup without forcing one global latency for every machine
- `RAIkeep.slnx` includes `PitSeeder`, the `iorg` CLI, and the `iorg` test project
- the parent sequential NuGet release chain now includes `ImgSeeder` before `PitSeeder`

## Current result

The most recent verified umbrella command in this session is:

- `dotnet test RAIkeep.slnx --nologo -v minimal`
- result: 271 passed, 0 failed, 1 skipped

## Latest validation result

Latest directly verified results in this workspace state:

- `dotnet test OsLib/OsLib.slnx --nologo -v minimal`
- `dotnet test RaiUtils/RaiUtils.slnx --nologo -v minimal`
- `dotnet test RaiImage/RaiImage.slnx --nologo -v minimal`
- `dotnet test JsonPit/JsonPit.slnx --nologo -v minimal`
- `dotnet test ImgSeeder/ImgSeeder.slnx --nologo -v minimal`
- `dotnet test PitSeeder/PitSeeder.slnx --nologo -v minimal`
- PlantUML SVG regeneration completed with the local `plantuml` binary

## Release alignment

The workspace is aligned to version `3.10.2` across:

- `OsLib`
- `RaiUtils`
- `RaiImage`
- `JsonPit`
- `ImgSeeder`
- `PitSeeder`
- the umbrella `RAIkeep` workspace documentation and submodule references

## Current operational note

- No `3.10.2` publication was triggered in this prep pass.
- The existing release automation remains wired in the order `OsLibCore -> RaiUtils -> RaiImage -> JsonPit -> ImgSeeder -> PitSeeder`, with `ImgSeeder` immediately before `PitSeeder`.
- The parent sequential chain now includes flat-container `.nupkg` verification after each 300-second wait, using lower-case `imgseeder` for the ImgSeeder package id.
- This environment could not push the prepared child commits or dispatch the parent workflow because shell GitHub access is DNS-blocked and no workflow-dispatch tool is available in-session.

## Suggested resume prompt

```text
Please read CURRENT-STATUS.md first, then continue from the prepared `3.10.2` umbrella baseline. Push and publish require an environment with GitHub network access.
```
