# PitSeeder Release Notes 3.x

## 3.13.2

**Date:** 2026-08-05  
**Author / Delivering Agent:** RAIkeep Dev Agent  
**Delivered Version:** v3.13.2  
**Target Consumers:** AIA, AfricaStage, RAIkeep operators  
**Status:** Implemented — coordinated 3.13.2 line; NuGet publication pending release authorization

---

### 1. Summary

`pits` 3.13.2 aligns the CLI with the coordinated JsonPit concurrency contract: it adds
the strictly read-only `--events` audit mode for JsonPit recovery events and routes
finite CLI shutdown through JsonPit's full durability boundary.

### 2. Resolved Change Requests (CRs)

- [`CR003_RAI_to_RAIkeep_JsonPit-concurrency-contract-and-persistence-races.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR003_RAI_to_RAIkeep_JsonPit-concurrency-contract-and-persistence-races.md) — PitSeeder share of the coordinated v3.13.2 work (`pits --events` audit mode; CR003 disposal boundary for finite CLI runs).

### 3. Root Cause Analysis & Technical Resolution

- Recovery diagnostics were previously invisible to operators. `pits --events` now
  reads a pit's durable audit events through JsonPit's `PitAudit` (backed by OsLib's
  `EventDirectory`) **without** opening a `Pit`, creating a process flag, touching
  `Master.flag`, merging change files, or writing an audit event. Audit routing runs
  before any `Pit` construction.
- Finite CLI runs previously only tombstoned their activity window. They now dispose
  each opened `Pit` through the CR003 durability boundary (change-file export first,
  optional canonical save while still exact master, then window/watcher/registry
  release). `--retain-window` still opts out and keeps the activity window until its
  normal timeout.

### 4. Public Contract & API / Package Changes

- New: `pits -r <root> <PitName> --events`
  - `--event-machine all|local|<machine>` (default `all`)
  - `--event-level <level>` — case-insensitive inclusive minimum
    (`Trace|Debug|Information|Warning|Error|Critical`, default `Trace`)
  - with `--json`: emits the filtered events as a JSON array; otherwise human-readable
    lines ordered deterministically by machine, UTC time, and event identity.
  - Audit mode requires one positional pit name; `--wwwa --events` is rejected
    (outside CR003). Invalid levels and missing values produce clear CLI errors with
    zero side effects.
- Package/tool version 3.13.2; consumes `JsonPit 3.13.2` and `OsLibCore 3.13.2`.

### 5. Validation & Acceptance Evidence

- `pits.Tests`: 13 passed, 0 failed, 0 skipped — including the new
  `EventsAuditModeTests` (all/local/named-machine filters, inclusive severity,
  case-insensitivity, deterministic ordering, JSON parseability, and before/after
  filesystem snapshots proving zero side effects) and the updated
  `LocalCliTicketWindowTests`, which exercise real separate CLI processes and prove
  exact-PID master inheritance after the previous CLI process released its window.
- Deployed and verified on the configured remote node Mzansi (`pits v3.13.2`,
  self-contained linux-x64), including seeding against the OneDrive-backed root.

### 6. Upgrade & Consumption Instructions

- Install/update the `pits` tool to 3.13.2 on **every** machine sharing a pit
  (pre-3.13.2 binaries can fail when merging 3.13.2 hashed change files).
- Inspect recovery activity with, for example:
  `pits -n -r <root> Person --events --event-level warning`
  or `pits -n -r <root> Person --events --json | jq`.

---

## 3.13.1

### Summary

`PitSeeder 3.13.1` prevents a completed finite `pits` command from unnecessarily retaining its JsonPit process activity window while preserving the separate master-writer lease.

### CLI lifecycle

- Finite seed, single-pit export, JSON stdout, and WWWA export operations track every `Pit` they open.
- On normal completion, each tracked pit attempts an ownership-verified release of the current CLI process activity window.
- Exception unwinding performs the same cleanup.
- Ctrl+C and process exit perform best-effort cleanup of any pits still tracked by the CLI.
- Cleanup expires only `{Machine}-pits-{PID}.flag`; it never releases or modifies `Master.flag`.
- Cleanup failures do not turn an otherwise successful command into a failed export; process-exit cleanup retains an opportunity to retry.

### New option

- Added `--retain-window` to keep the CLI process activity window until the normal JsonPit timeout.
- Immediate ownership-verified release is the default for finite CLI operations.
- The option is included in `pits --help` and documented in the PitSeeder README.

### Cloud behavior and writer safety

- Per-PID activity flags prevent consecutive CLI processes from targeting the same process-flag filename.
- Release writes an expired Unix-epoch tombstone in place instead of deleting and recreating the OneDrive-backed path.
- A successful writer retains its timed `Master.flag` lease. A participant that cannot acquire that lease continues to write mergeable change files rather than overwriting the canonical pit.
- The resolved lifecycle CR is [`PitSeeder_CR_release_for_cli-resolved-in-v3.13.1.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/PitSeeder_CR_release_for_cli-resolved-in-v3.13.1.md).

### Dependency alignment

- Package version is `3.13.1`.
- Fallback package references are aligned to `JsonPit 3.13.1` and `OsLibCore 3.13.1`.
- PitSeeder remains last in the coordinated release order.

### Validation

- `PitSeeder.Tests`: `7` passed, `0` failed.
- Two immediate consecutive read-only WWWA exports against the configured OneDrive `AIA` pit succeeded.
- The resulting process flags used distinct PIDs and contained expired epoch timestamps after completion.
- Coverage includes immediate consecutive execution, `--retain-window`, exception cleanup, foreign-process ownership rejection, and master-ticket preservation.

### Release sequencing

`PitSeeder` is sixth and last in the coordinated release chain. Its GitHub push/tag must wait for ImgSeeder workflow success, flat-container visibility, and the full `330`-second hold. After PitSeeder publishes, perform the final flat-container verification for all six packages before declaring the chain complete.

---

## 3.12.1

### Summary

- Releases `PitSeeder` version `3.12.1`.
- Aligns CLI package metadata and fallback package references to `JsonPit 3.12.1` and `OsLibCore 3.12.1`.
- Keeps `PitSeeder` last in the coordinated release order, immediately after `ImgSeeder`/`iorg`.
- Carries forward `pits` subscriber identity behavior and local ticket-window regression coverage from `3.12.0`.

### Validation

- `dotnet test PitSeeder.slnx --nologo -v minimal`
- NuGet publishing remains wired through the parent sequential release chain and the tag-triggered `publish-pitseeder-nuget.yml` workflow in `RAIkeep`.

---

## 3.12.0

### Summary

- Releases `PitSeeder` version `3.12.0`.
- Aligns CLI package metadata and fallback package references to `JsonPit 3.12.0` and `OsLibCore 3.12.0`.
- Keeps `PitSeeder` last in the coordinated release order, immediately after `ImgSeeder`/`iorg`.
- Carries forward `pits` subscriber identity behavior and local ticket-window regression coverage from `3.11.5`.

### Validation

- `dotnet test PitSeeder.slnx --nologo -v minimal`
- NuGet publishing remains wired through the parent sequential release chain and the tag-triggered `publish-pitseeder-nuget.yml` workflow in `RAIkeep`.

---

## 3.11.4

### Summary

- Releases `PitSeeder` version `3.11.4`.
- Aligns CLI package metadata and fallback package references to `JsonPit 3.11.4` and `OsLibCore 3.11.4`.
- Keeps `PitSeeder` last in the coordinated release order, immediately after `ImgSeeder`/`iorg`.
- Carries forward `pits` subscriber identity behavior and local ticket-window regression coverage from `3.11.3`.

### Validation

- `dotnet build pits/pits.csproj --nologo -v minimal`
- NuGet publishing remains wired through the parent sequential release chain and the tag-triggered `publish-pitseeder-nuget.yml` workflow in `RAIkeep`.

---

## 3.11.2

### Summary

- Releases `PitSeeder` version `3.11.2`.
- Aligns CLI package metadata and fallback package references to `JsonPit 3.11.2` and `OsLibCore 3.11.2`.
- Keeps `PitSeeder` last in the coordinated release order, immediately after `ImgSeeder`/`iorg`.
- Carries forward `pits` subscriber identity behavior and local ticket-window regression coverage from `3.11.1`.

### Validation

- `dotnet build pits/pits.csproj --nologo -v minimal`
- NuGet publishing remains wired through the parent sequential release chain and the tag-triggered `publish-pitseeder-nuget.yml` workflow in `RAIkeep`.

---

## 3.11.1

### Summary

- Releases `PitSeeder` version `3.11.1`.
- Aligns CLI package metadata and fallback package references to `JsonPit 3.11.1` and `OsLibCore 3.11.1`.
- Keeps `PitSeeder` last in the coordinated release order, immediately after `ImgSeeder`/`iorg`.
- Uses explicit `pits` subscriber identity for JsonPit participation, so CLI writes claim and validate master tickets as `Machine-pits` consistently (including `dotnet pits.dll` execution).
- Adds a process-level local ticket-window regression test that verifies API/CLI short-sequence conflict handling and change-file merge safety.

### Validation

- `dotnet build pits/pits.csproj --nologo -v minimal`
- NuGet publishing remains wired through the parent sequential release chain and the tag-triggered `publish-pitseeder-nuget.yml` workflow in `RAIkeep`.

---

## 3.11.0

### Summary

- Releases `PitSeeder` version `3.11.0`.
- Aligns CLI package metadata and fallback package references to `JsonPit 3.11.0` and `OsLibCore 3.11.0`.
- Keeps `PitSeeder` last in the coordinated release order, immediately after `ImgSeeder`/`iorg`.
- No CLI behavior changes from `3.10.2`.

### Validation

- `dotnet build pits/pits.csproj --nologo -v minimal`
- NuGet publishing remains wired through the parent sequential release chain and the tag-triggered `publish-pitseeder-nuget.yml` workflow in `RAIkeep`.

---

## 3.10.2

### Summary

- Releases `PitSeeder` version `3.10.2`.
- Aligns CLI package metadata and fallback package references to `JsonPit 3.10.2` and `OsLibCore 3.10.2`.
- Keeps `PitSeeder` last in the coordinated release order, immediately after `ImgSeeder`/`iorg`.
- No CLI behavior changes from `3.10.1`.

### Validation

- `dotnet build pits/pits.csproj --nologo -v minimal`
- NuGet publishing remains wired through the parent sequential release chain and the tag-triggered `publish-pitseeder-nuget.yml` workflow in `RAIkeep`.

---

## 3.10.1

### Summary

- Releases `PitSeeder` version `3.10.1`.
- Aligns CLI package metadata and fallback package references to `JsonPit 3.10.1` and `OsLibCore 3.10.1`.
- Keeps `PitSeeder` last in the coordinated release order, immediately after `ImgSeeder`/`iorg`.
- No CLI behavior changes from `3.10.0`.

### Validation

- `dotnet build pits/pits.csproj --nologo -v minimal`
- NuGet publishing remains wired through the parent sequential release chain and the tag-triggered `publish-pitseeder-nuget.yml` workflow in `RAIkeep`.

---

## 3.10.0

### Summary

- Releases `PitSeeder` version `3.10.0`.
- Aligns CLI package metadata and fallback package references to `JsonPit 3.10.0` and `OsLibCore 3.10.0`.
- Keeps `PitSeeder` last in the coordinated release order, immediately after `ImgSeeder`/`iorg`.
- No CLI behavior changes from `3.9.1`.

### Validation

- `dotnet build pits/pits.csproj --nologo -v minimal`
- NuGet publishing remains wired through the tag-triggered `publish-pitseeder-nuget.yml` workflow in `RAIkeep`.

---

## 3.9.1

### Summary

- Releases `PitSeeder` version `3.9.1`.
- Aligns CLI package metadata and fallback package references to `JsonPit 3.9.1` and `OsLibCore 3.9.1`.
- Refreshes release-note pointers in the packaged README for the coordinated patch line.
- No CLI behavior changes from `3.9.0`.

### Validation

- `dotnet build pits/pits.csproj --nologo -v minimal`
- NuGet publishing is handled by the tag-triggered `publish-pitseeder-nuget.yml` workflow in `RAIkeep`.

---

## 3.9.0

### Summary

- Releases `PitSeeder` version `3.9.0`.
- Aligns CLI package metadata and fallback package references to `JsonPit 3.9.0` and `OsLibCore 3.9.0`.
- Refreshes release-note pointers in the packaged README for the coordinated minor line.
- No CLI behavior changes from `3.8.15`.

### Validation

- `dotnet build pits/pits.csproj --nologo -v minimal`
- NuGet publishing is handled by the tag-triggered `publish-pitseeder-nuget.yml` workflow in `RAIkeep`.

---

## 3.8.15

### Summary

- Releases `PitSeeder` version `3.8.15`.
- Aligns CLI package metadata and fallback package references to `JsonPit 3.8.15` and `OsLibCore 3.8.15`.
- Refreshes release-note pointers in the packaged README for the coordinated chain.

### Validation

- `dotnet build pits/pits.csproj --nologo -v minimal`
- NuGet publishing is handled by the tag-triggered `publish-pitseeder-nuget.yml` workflow in `RAIkeep`.

---

## 3.8.14

### Summary

- Releases `PitSeeder` version `3.8.14`.
- Aligns CLI package metadata and fallback package references to `JsonPit 3.8.14` and `OsLibCore 3.8.14`.
- Refreshes release-note pointers in the packaged README for the coordinated chain.

### Validation

- `dotnet build pits/pits.csproj --nologo -v minimal`
- NuGet publishing is handled by the tag-triggered `publish-pitseeder-nuget.yml` workflow in `RAIkeep`.

---

## 3.8.12

### Summary

- Releases `PitSeeder` version `3.8.12`.
- Aligns CLI package metadata with `JsonPit 3.8.12` and `OsLibCore 3.8.12`.
- Refreshes live README release-note links for the coordinated `RAIkeep` patch line.
- No CLI behavior changes from `3.8.11`.

### Validation

- `dotnet test RAIkeep.slnx --nologo -v minimal`: 243 passed, 0 failed, 1 skipped.
- NuGet publishing is handled by the RAIkeep Sequential NuGet Release Chain.

---

## 3.8.11

### Summary

- Releases `PitSeeder` version `3.8.11`.
- Aligns the CLI package line with `JsonPit 3.8.11` and `OsLibCore 3.8.11`.
- Refreshes umbrella-workspace markdown and PlantUML release markers for the coordinated `3.8.11` release.

### Validation

- Release published through GitHub Actions tag workflow.
- NuGet visibility is verified in the sequential release chain.

---

## 3.8.10

### Summary

- Fixes cloud-relative pitroot resolution in the `pits` CLI.
- When `-c <provider>` and `-r <pitroot>` are used together, `-r` is now resolved as a provider-relative `RaiRelPath` under the configured cloud root.
- Preserves non-cloud `-r` behavior, so absolute/local pitroot usage remains supported when `-c` is absent.
- Preserves the previously working cloud shorthand with a leading slash, such as `-r /LiveAfricaStage`.

### Fixed

The following commands now resolve to the same configured OneDrive pit root:

```bash
pits -h -c OneDrive -r LiveAfricaStage
pits -h -c OneDrive -r LiveAfricaStage/
pits -h -c OneDrive -r /LiveAfricaStage
```

Expected resolved root:

```text
/Users/RSB/Library/CloudStorage/OneDrive/OneDriveData/LiveAfricaStage/
```

### Validation

- Added `PitSeeder/pits.Tests` with regression coverage for the three cloud-relative pitroot forms.
- `dotnet test PitSeeder/PitSeeder.slnx --nologo -v minimal`
- `dotnet test RAIkeep.slnx --nologo -v minimal`

---

## 3.8.6

### Summary

- Coordinated release for `PitSeeder` version `3.8.6`.
- Refreshes markdown release-line references (including `README.md`) via automated scan.
- Refreshes all tracked PlantUML (`.puml`) release/version markers found in scope.

### Validation

- Release published through GitHub Actions tag workflow.
- NuGet visibility is verified in the sequential release chain.

---

## 3.8.1

### Summary

- Release for the `PitSeeder` .NET tool package version `3.8.1`.
- Publishes the NuGet tool package from the `RAIkeep` repository via GitHub Actions.
- Publishes self-contained `pits` binaries for `osx-arm64`, `osx-x64`, `linux-x64`, and `win-x64` as GitHub release assets.
- Aligns fallback package version defaults with `JsonPit 3.8.1` and `OsLibCore 3.8.1`.

### CI/CD

- Workflow: `.github/workflows/publish-pitseeder-nuget.yml`
- Trigger: push a tag in format `v*`
- Guardrail: tag version must match `<Version>` in `PitSeeder/pits/pits.csproj`
- NuGet publish target: `https://api.nuget.org/v3/index.json`
- Self-contained targets: `osx-arm64`, `osx-x64`, `linux-x64`, and `win-x64`
- Self-contained outputs are uploaded as GitHub release assets on the matching tag

### Validation

- `dotnet pack PitSeeder/pits/pits.csproj --configuration Release`
- `dotnet publish PitSeeder/pits/pits.csproj --configuration Release --runtime osx-arm64 --self-contained true /p:PublishSingleFile=true`
- `dotnet publish PitSeeder/pits/pits.csproj --configuration Release --runtime osx-x64 --self-contained true /p:PublishSingleFile=true`
- `dotnet publish PitSeeder/pits/pits.csproj --configuration Release --runtime linux-x64 --self-contained true /p:PublishSingleFile=true`
- `dotnet publish PitSeeder/pits/pits.csproj --configuration Release --runtime win-x64 --self-contained true /p:PublishSingleFile=true`
- Result: tool package packed successfully with `README.md`, `HardCastle.png`, and `DotnetToolSettings.xml`; self-contained single-file publishes succeeded for `osx-arm64`, `osx-x64`, `linux-x64`, and `win-x64`.

---

## 3.8.0

### Summary

- Release for the `PitSeeder` .NET tool package version `3.8.0`.
- Publishes the NuGet tool package from the `RAIkeep` repository via GitHub Actions.
- Publishes self-contained `pits` binaries for `osx-arm64`, `osx-x64`, `linux-x64`, and `win-x64` as GitHub release assets.
- Aligns fallback package version defaults with `JsonPit 3.8.0` and `OsLibCore 3.8.0`.

### CI/CD

- Workflow: `.github/workflows/publish-pitseeder-nuget.yml`
- Trigger: push a tag in format `v*`
- Guardrail: tag version must match `<Version>` in `PitSeeder/pits/pits.csproj`
- NuGet publish target: `https://api.nuget.org/v3/index.json`
- Self-contained targets: `osx-arm64`, `osx-x64`, `linux-x64`, and `win-x64`
- Self-contained outputs are uploaded as GitHub release assets on the matching tag

### Validation

- `dotnet pack PitSeeder/pits/pits.csproj --configuration Release`
- `dotnet publish PitSeeder/pits/pits.csproj --configuration Release --runtime osx-arm64 --self-contained true /p:PublishSingleFile=true`
- `dotnet publish PitSeeder/pits/pits.csproj --configuration Release --runtime osx-x64 --self-contained true /p:PublishSingleFile=true`
- `dotnet publish PitSeeder/pits/pits.csproj --configuration Release --runtime linux-x64 --self-contained true /p:PublishSingleFile=true`
- `dotnet publish PitSeeder/pits/pits.csproj --configuration Release --runtime win-x64 --self-contained true /p:PublishSingleFile=true`
- Result: tool package packed successfully with `README.md`, `HardCastle.png`, and `DotnetToolSettings.xml`; self-contained single-file publishes succeeded for `osx-arm64`, `osx-x64`, `linux-x64`, and `win-x64`.

---

## 3.7.9

### Summary

- Patch release for the `PitSeeder` .NET tool package version `3.7.9`.
- Publishes the NuGet tool package from the `RAIkeep` repository via GitHub Actions.
- Publishes self-contained `pits` binaries for `osx-arm64`, `osx-x64`, `linux-x64`, and `win-x64` as GitHub release assets.
- Aligns fallback package version defaults with `JsonPit 3.7.9` and `OsLibCore 3.7.9`.

### CI/CD

- Workflow: `.github/workflows/publish-pitseeder-nuget.yml`
- Trigger: push a tag in format `v*`
- Guardrail: tag version must match `<Version>` in `PitSeeder/pits/pits.csproj`
- NuGet publish target: `https://api.nuget.org/v3/index.json`
- Self-contained targets: `osx-arm64`, `osx-x64`, `linux-x64`, and `win-x64`
- Self-contained outputs are uploaded as GitHub release assets on the matching tag

### Validation

- `dotnet publish PitSeeder/pits/pits.csproj --configuration Release --runtime linux-x64 --self-contained true /p:PublishSingleFile=true --output PitSeeder/artifacts/publish/linux-x64-ci-smoke-nooverride`
- Result: local self-contained publish succeeded.

---

## 3.7.8.1

### Summary

- Patch release for the `PitSeeder` .NET tool package version `3.7.8.1`.
- Adds automated publication from the `RAIkeep` repository via GitHub Actions tag workflow.
- Keeps fallback package version alignment with `JsonPit 3.7.8` and `OsLibCore 3.7.8`.

### CI/CD

- New workflow: `.github/workflows/publish-pitseeder-nuget.yml`
- Trigger: push a tag in format `v*`
- Guardrail: tag version must match `<Version>` in `PitSeeder/pits/pits.csproj`
- Publish target: `https://api.nuget.org/v3/index.json`
- Self-contained targets: `osx-arm64`, `linux-x64`, and `win-x64`
- Self-contained outputs are uploaded as GitHub release assets on the matching tag

### Validation

- `dotnet test PitSeeder/PitSeeder.slnx --nologo -v minimal`

---

## 3.7.8

### Summary

- Patch release for the `PitSeeder` .NET tool package version `3.7.8`.
- This is a version-symmetry release aligned with `JsonPit 3.7.8` and `OsLibCore 3.7.8`.
- No breaking CLI changes.

### Package Alignment

- `pits/pits.csproj` now defaults to:
  - `JsonPitPackageVersion = 3.7.8`
  - `OsLibPackageVersion = 3.7.8`
- Tool package version updated to `3.7.8`.

### CLI Contract

- Tool command name remains `pits`.
- Existing options and WWWA behavior are unchanged.

### Validation

- `dotnet test PitSeeder.slnx --nologo -v minimal`

---

## 3.7.7

Built and validated against:

- OsLib 3.7.7
- JsonPit 3.7.7
- .NET 10.0

### Summary

- Keeps the current CLI feature set intact.
- Aligns fallback package references with `JsonPit 3.7.7` and `OsLibCore 3.7.7`.
- Refreshes current package docs for the `3.7.7` release line.

### Packaging

- `pits.csproj` now points its fallback package versions at the `3.7.7` line.
- `README.md` now points at the `3.7.7` release notes.

### Validation

- `dotnet test RAIkeep.slnx --nologo -v minimal`
- Result: 214 passed, 0 failed, 0 skipped.

---

## 3.7.6

Built and validated against:

- OsLib 3.7.6
- JsonPit 3.7.6
- .NET 10.0

### Summary

- Keeps the current CLI feature set intact.
- Adds explicit NuGet package icon metadata so the published package can display the RAIkeep logo.
- Aligns fallback package references with `JsonPit 3.7.6` and `OsLibCore 3.7.6`.

### Packaging Changes

- `pits.csproj` now emits `<icon>HardCastle.png</icon>` in the package manifest.
- `HardCastle.png` is packed into the root of the `.nupkg` so NuGet can render the logo.
- `Authors` metadata is emitted correctly for the package manifest.

### Validation

- `dotnet pack PitSeeder/pits/pits.csproj --configuration Release --nologo -v minimal`
- Verified packaged contents include:
  - `PitSeeder.nuspec`
  - `README.md`
  - `HardCastle.png`

---

## 3.7.5

Built and validated against:

- OsLib 3.7.5
- JsonPit 3.7.5
- .NET 10.0 (SDK 10.0.102)

### Breaking Changes

#### `-d` / `--destination` removed

The destination parameter has been replaced by `-r` / `--pitroot`. The pit root is the base directory containing one or more canonical pits. For seeding, the pit name is derived from the source file; for export, it is given as a positional argument.

**Migration:**

```bash
# Old
pits -s Person.json5 -d output/Person.pit
pits -s sample/ -d output/ --wwwa

# New
pits -s Person.json5 -r output/
pits -s sample/ -r output/ --wwwa
```

### New Features

#### Export to file (`-e`)

Export a pit's current state as a flat JSON file:

```bash
pits -r /pitroot/ Person -e ~/export/
```

Writes `Person.json` to the given directory using the `Pit.ExportJson` method.

#### Export to stdout (`--json`)

Export a pit's current state directly to stdout for piping to tools like `jq` or `grep`:

```bash
pits -r /pitroot/ Person --json
pits -r /pitroot/ Person --json | jq '.[] | select(.Id == "Nomsa")'
```

#### Positional pit name argument

The pit to operate on can be specified as a bare positional argument without a switch:

```bash
pits -r /pitroot/ Person --json
pits -r /pitroot/ Person -e /tmp/
```

#### Pit root parameter (`-r` / `--pitroot`)

Replaces `-d`. Specifies the root directory containing canonical pits. All pit operations are resolved relative to this root.

```bash
pits -r /cloud/RAIkeep/WwwaTests/ Person --json
```

When combined with `-c` (cloud provider), the cloud storage root is prepended:

```bash
pits -c OneDrive -r RAIkeep/WwwaTests/ Person --json
```

#### PitRoot inference from `-s`

When `-s` points to a `.pit` file and no `-r` is given, the pit root is inferred by stripping the canonical folder from the source path:

```bash
pits -s /cloud/WwwaTests/Person/Person.pit --json
# Infers pitroot as /cloud/WwwaTests/
```

#### WWWA resolved export

Export all four WWWA pits with foreign key references resolved one level deep:

```bash
pits -r /pitroot/ --wwwa -e ~/export/     # writes wwwa.json
pits -r /pitroot/ --wwwa --json            # writes to stdout
```

Foreign key sections (`Who`, `What`, `Where`, `Activity`) are resolved against their corresponding pits (Person, Object, Place, Activity). When all references in a section resolve successfully, the wrapper dissolves and its contents are promoted to the item level. Unresolved wrappers remain unchanged.

Example: an Activity item referencing `Who: { Performer: "Nomsa" }` and `Where: { Venue: "SDZSafariPark" }` produces:

```json
{
  "Id": "SDZSP26",
  "Title": "Nomsa performing in the Elephant Valley",
  "Performer": { "Id": "Nomsa", "Name": "Nomsa Burkhardt", "Instruments": ["Voice", "Percussion", "Dance"] },
  "Venue": { "Id": "SDZSafariPark", "Name": "San Diego Zoo Safari Park", "Homepage": "https://sdzsafaripark.org/" }
}
```

#### Cleaned-up help display

The help output now shows:

- All parameters with descriptions
- Resolved PitRoot path with existence status
- Status of all four WWWA pits under the given root
- Removed redundant `--source:` / `--destination:` summary lines

### Bug Fixes

#### PitFile(string) path handling

Fixed `PitFile(string fullName)` constructor which was passing a full filename (e.g., `Person.pit`) to `new RaiPath()`, causing the filename to be treated as a directory segment. The resulting path would be `.../Person.pit/Person/Person.pit` instead of `.../Person/Person.pit`. Fixed by delegating to the `CanonicalFile(string)` base constructor, which properly separates the path from the filename.

#### JsonPitPersistenceTests path handling

Fixed `new RaiPath(persistedFileFullName)` in the persistence test, which had the same issue as the PitFile constructor. Changed to `RaiPath.SplitRaiPathAndName(persistedFileFullName).path` to extract only the directory portion.

#### Removed deleted Cloud enum and RemoteCloudSyncProbe references

Removed `CloudRemoteSyncTests.cs` and cleaned up `JsonPitRealWorldIntegrationTests.cs` to remove all references to the `Cloud` enum and `RemoteCloudSyncProbe` class, which were removed from OsLib as part of the RaiPath refactoring. The remaining cloud integration test now discovers providers via `Os.Config?.Cloud` directly.

#### NuGet restore performance

Added `Directory.Build.props` at the repo root with `NuGetAudit=false` and `NuGetAuditMode=direct` to address extremely slow restore times (300-500 seconds) caused by .NET 10's new default of `NuGetAuditMode=all` for transitive dependency scanning.

### Test Results

All tests pass:

- OsLib: 56 passed, 0 failed
- JsonPit: 83 passed, 0 failed
