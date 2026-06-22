# CURRENT-STATUS

This file captures the current release-ready status of the `RAIkeep` workspace for the coordinated `3.11.0` line.

## Current focus

- Advance the umbrella package line from `3.10.x` to `3.11.0`.
- Keep the release order unchanged: `OsLibCore -> RaiUtils -> RaiImage -> JsonPit -> ImgSeeder -> PitSeeder`.
- Keep `ImgSeeder`/`iorg` immediately before `PitSeeder` everywhere in docs, release notes, and release-prep notes.
- Do not publish to NuGet and do not trigger the GitHub Sequential NuGet Release Chain.

## Completed in this run

- Updated package versions to `3.11.0` in `OsLib`, `RaiUtils`, `RaiImage`, `JsonPit`, `ImgSeeder`, and `PitSeeder`.
- Updated downstream fallback dependency versions, including `JsonPit`, `ImgSeeder`, `ImgSeeder.Tests`, and `PitSeeder`.
- Added `RELEASE_NOTES_3.11.0.md` to every child repo.
- Refreshed current README/API/requirements/testing notes and the root release-prep docs.
- Updated live PlantUML release/version markers and regenerated tracked SVG outputs with local `plantuml`.

## Validation

Sequential validation results from this workspace state:

- `dotnet test RaiImage/RaiImage.slnx --nologo -v minimal`
  Result: 91 passed
- `dotnet test ImgSeeder/ImgSeeder.slnx --nologo -v minimal`
  Result: 8 passed
- `dotnet test PitSeeder/PitSeeder.slnx --nologo -v minimal`
  Result: 3 passed
- `dotnet test RAIkeep.slnx --nologo -v minimal`
  Result: 280 passed, 0 failed, 1 skipped

One earlier parallel validation attempt produced transient file-lock and temp-tool failures; those did not reproduce once the same solutions were rerun sequentially.

## Git state

Child release-prep commits created in this run:

- `OsLib`: `3268fbf` pushed to `origin/main`
- `RaiUtils`: `69d2c32` pushed to `origin/main`
- `RaiImage`: `c7e9e64` local only
- `JsonPit`: `cbf0b6d` local only
- `ImgSeeder`: `54a3bd2` local only
- `PitSeeder`: `df2dc3a` local only

The last four pushes failed repeatedly with:

```text
fatal: unable to access 'https://github.com/Burkhardt/<repo>.git/': Could not resolve host: github.com
```

## Parent repo handling

- The parent repo should track the new `3.11.0` submodule pointers and updated root docs.
- The parent remote push must wait until `RaiImage`, `JsonPit`, `ImgSeeder`, and `PitSeeder` are pushed successfully, otherwise the parent would reference unreachable submodule SHAs.

## Suggested resume prompt

```text
Please read CURRENT-STATUS.md first, then continue from the prepared 3.11.0 umbrella baseline. Validation is green, but only OsLib and RaiUtils were pushed before GitHub DNS resolution started failing for the remaining child repos.
```
