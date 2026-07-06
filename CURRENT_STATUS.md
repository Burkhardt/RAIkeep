# CURRENT_STATUS

Last updated: 2026-07-06

Current coordinated release line: `3.11.4` (prepared locally, not yet pushed or published)

## Release Truth (GitHub + NuGet)

- Intended next coordinated release version is `3.11.4`.
- Latest NuGet-published version for all six packages is `3.11.3`.
- Latest release tag in all six child repos is `v3.11.3`.

Local 2026-07-06 release-prep commits created for the `3.11.4` line:

- `OsLib` `84ff67a`
- `RaiUtils` `8feda38`
- `RaiImage` `c47f9ff`
- `JsonPit` `e7cf593`
- `ImgSeeder` `36b051e`
- `PitSeeder` `49f922e`

## Rollback Completed (Safe, Non-Destructive)

Rollback executed on 2026-06-30 with these guarantees:

- No force-push used.
- Full audit trail preserved via `git revert` commits.
- Safety tags created before rollback:
  - `rollback-pre-20260630-121626` in `RAIkeep` and each child repo.

Child repos reverted from `v3.11.3..HEAD` and pushed:

- `OsLib`
- `RaiUtils`
- `RaiImage`
- `JsonPit`
- `PitSeeder`
- `ImgSeeder`

Umbrella repo actions:

- Reverted 3.13 prep commits:
  - `c5abe78` (`docs: refresh 3.13.0 push blockers`)
  - `6d264fc` (`chore: prepare 3.13.0 umbrella release`)
- Synced submodule pointers to the child rollback heads.
- Pushed updated `main`.

## 3.11.4 Prep Status

Prepared locally on 2026-07-06:

- Updated package and tool versions to `3.11.4` across `OsLib`, `RaiUtils`, `RaiImage`, `JsonPit`, `ImgSeeder`/`iorg`, and `PitSeeder`.
- Updated current README/API/testing/status docs and renamed active child release notes to `RELEASE_NOTES_3.11.4.md`.
- Refreshed touched PlantUML release markers and regenerated the tracked SVG artifacts where local tooling was available.
- Corrected the local `scripts/release-chain.sh` order so it now matches the authoritative GitHub chain: `OsLibCore -> RaiUtils -> RaiImage -> JsonPit -> ImgSeeder -> PitSeeder`.

## Validation Snapshot

Sequential local validation passed:

- `dotnet test RaiImage/RaiImage.slnx --nologo -v minimal` -> `94` passed, `0` failed, `0` skipped
- `dotnet test ImgSeeder/ImgSeeder.slnx --nologo -v minimal` -> `8` passed, `0` failed, `0` skipped
- `dotnet test PitSeeder/PitSeeder.slnx --nologo -v minimal` -> `4` passed, `0` failed, `0` skipped
- `dotnet test RAIkeep.slnx --nologo -v minimal` -> `285` passed, `0` failed, `1` skipped across the umbrella test projects

Observed warning during the `ImgSeeder` validation run:

- `JsonPit/JsonPit.cs(95,32): warning CS1574: XML comment has cref attribute 'AddPreservingModified' that could not be resolved`

## Current Blocker

Remote release steps are blocked in this environment:

- `git push origin main` prompts `Username for 'https://github.com':`
- `gh auth status` reports `The token in default is invalid.`
- Because no working noninteractive GitHub auth is configured here, child pushes, parent push, workflow dispatch, and NuGet publication could not continue safely.

## Consolidated Legacy Status Notes

The former umbrella files `CURRENT-STATE.md` and `CURRENT-STATUS.md` were obsolete `3.11.2` release-prep notes. Their useful historical context is consolidated here:

- Earlier sandbox runs could not validate with `dotnet test` or `dotnet vstest` because test execution failed before running tests with `System.Net.Sockets.SocketException (13): Permission denied`.
- Earlier sandbox runs also reported stale prebuilt `iorg` and `pits` binaries showing `3.9.1`; those binaries are not valid evidence for the current package line.
- Earlier 3.11.2 prep notes mentioned blocked GitHub DNS/auth/workflow-dispatch access. That blocker is historical; subsequent 3.11.3 release and rollback operations were pushed successfully.
- The old notes referenced a release order that conflicted with later corrected release-chain practice. For the current state, no release is pending; any future release must first confirm intended/tagged/published versions here.

## Current Verification Snapshot

- Child repos are locally committed for `3.11.4` but remain ahead of `origin/main` until GitHub auth is restored.
- The umbrella repo is locally committed for `3.11.4` and remains ahead of `origin/main` until GitHub auth is restored.
- Live version markers (`*.csproj` and top release README sections) now advertise `3.11.4`.

## Operating Rule (From Now On)

Use this file as the umbrella release ledger and update it for every release-related action, including:

- latest intended release version
- latest actually tagged version
- latest actually published NuGet version
- any rollback/revert operations
- blockers and next required action

If any mismatch appears between intended/tagged/published versions, record it here immediately before further release actions.

There must be only one current-state/status file at the umbrella level: `CURRENT_STATUS.md`. Do not recreate `CURRENT-STATE.md` or `CURRENT-STATUS.md`.

## Suggested Resume Prompt

```text
Please read CURRENT_STATUS.md first and treat it as the single source of truth for umbrella release state. Resume by restoring GitHub auth, pushing the local 3.11.4 child commits in release order, then pushing the parent and dispatching the sequential-nuget-release-chain workflow with publish_to_nuget=true.
```
