# CURRENT_STATUS

Last updated: 2026-06-30

Current coordinated release line: `3.11.3`

## Release Truth (GitHub + NuGet)

- Latest NuGet-published version for all six packages is `3.11.3`.
- Latest release tag in all six child repos is `v3.11.3`.
- `3.12.0`, `3.12.1`, and `3.13.0` were prepared on child `main` branches earlier, then safely rolled back using non-destructive revert commits.

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

## Consolidated Legacy Status Notes

The former umbrella files `CURRENT-STATE.md` and `CURRENT-STATUS.md` were obsolete `3.11.2` release-prep notes. Their useful historical context is consolidated here:

- Earlier sandbox runs could not validate with `dotnet test` or `dotnet vstest` because test execution failed before running tests with `System.Net.Sockets.SocketException (13): Permission denied`.
- Earlier sandbox runs also reported stale prebuilt `iorg` and `pits` binaries showing `3.9.1`; those binaries are not valid evidence for the current package line.
- Earlier 3.11.2 prep notes mentioned blocked GitHub DNS/auth/workflow-dispatch access. That blocker is historical; subsequent 3.11.3 release and rollback operations were pushed successfully.
- The old notes referenced a release order that conflicted with later corrected release-chain practice. For the current state, no release is pending; any future release must first confirm intended/tagged/published versions here.

## Current Verification Snapshot

- All repos are clean (`git status` clean).
- All repos are synced with remote (`origin/main...HEAD` => `0 0`).
- Live version markers (`*.csproj` and top release README sections) are back on `3.11.3`.

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
Please read CURRENT_STATUS.md first and treat it as the single source of truth for umbrella release state. Confirm intended/tagged/published versions match before any new version prep, tagging, or release-chain execution.
```
