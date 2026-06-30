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

## Suggested Resume Prompt

```text
Please read CURRENT_STATUS.md first and treat it as the single source of truth for umbrella release state. Confirm intended/tagged/published versions match before any new version prep, tagging, or release-chain execution.
```
