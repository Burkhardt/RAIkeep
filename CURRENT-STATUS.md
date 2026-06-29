# CURRENT-STATUS

This file captures the current release-ready status of the `RAIkeep` workspace for the coordinated `3.13.0` minor line.

## Current focus

- Move the live child/package line from `3.12.1` to the next coordinated minor, `3.13.0`.
- Keep the release order unchanged: `OsLibCore -> RaiUtils -> RaiImage -> JsonPit -> ImgSeeder -> PitSeeder`.
- Keep `ImgSeeder`/`iorg` immediately before `PitSeeder` everywhere in docs, release notes, and release-prep notes.

## Completed in this run

- Added `RELEASE_NOTES_3.13.0.md` to every child repo/package.
- Refreshed live package docs, current package metadata, and fallback dependency versions to `3.13.0`.
- Updated the active PlantUML release markers and regenerated the tracked SVG renders that changed in this run.
- Local child repo heads are now:
  - `OsLib`: `de3807c`
  - `RaiUtils`: `e163c67`
  - `RaiImage`: `7c7e98b`
  - `JsonPit`: `e9d9b9f`
  - `ImgSeeder`: `b43185a`
  - `PitSeeder`: `af5eae6`

## Validation

Sequential validation passed in this workspace:

- `dotnet test RaiImage/RaiImage.slnx --nologo -v minimal` -> `94 passed`
- `dotnet test ImgSeeder/ImgSeeder.slnx --nologo -v minimal` -> `8 passed`
- `dotnet test PitSeeder/PitSeeder.slnx --nologo -v minimal` -> `4 passed`
- `dotnet test RAIkeep.slnx --nologo -v minimal` -> `285 passed`, `1 skipped`

Observed non-blocking warning:

```text
/Users/rsb/Project2026/GitHub/RAIkeep/JsonPit/JsonPit.cs(95,32): warning CS1574: XML comment has cref attribute 'AddPreservingModified' that could not be resolved
```

Additional note:

- Existing prebuilt `iorg` and `pits` binaries still report `3.9.1`, so they are stale artifacts and not valid `3.13.0` verification.

## Git and publishing state

- Child repo commits were created locally in release order, but every push failed with:

```text
fatal: unable to access 'https://github.com/Burkhardt/<repo>.git/': Could not resolve host: github.com
```

- The parent repo now carries the corresponding submodule-pointer update and release-doc refresh locally, but `git push` there fails with:

```text
fatal: could not read Username for 'https://github.com': Device not configured
```

- `gh auth status` reports the active `github.com` token for `Burkhardt` is invalid.
- No `3.13.0` Sequential NuGet Release Chain run was dispatched.
- No NuGet publish was attempted, by request.

## Suggested resume prompt

```text
Please read CURRENT-STATUS.md first, then continue the prepared 3.13.0 umbrella minor release in an environment with working GitHub DNS/network access. Push the child repos in order, push the parent repo with the updated submodule pointers, and do not publish to NuGet or dispatch the Sequential NuGet Release Chain unless explicitly requested.
```
