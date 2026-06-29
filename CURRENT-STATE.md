# CURRENT-STATE

This file captures the current working state of the `RAIkeep` umbrella workspace after the coordinated `3.13.0` minor-release prep pass.

## Active line

The active coordinated line is `3.13.0` for:

- `OsLib`
- `RaiUtils`
- `RaiImage`
- `JsonPit`
- `ImgSeeder`
- `PitSeeder`

## What changed in this run

- Added `RELEASE_NOTES_3.13.0.md` to all six child repos/packages.
- Preserved the coordinated package order `OsLibCore -> RaiUtils -> RaiImage -> JsonPit -> ImgSeeder -> PitSeeder`.
- Refreshed live package metadata and fallback dependency versions to `3.13.0`.
- Regenerated the tracked SVG renders for the PlantUML files changed in this run.
- Updated the root dependency diagrams so the current package overviews stay aligned with the live release markers.

## Local child heads

- `OsLib` -> `de3807c`
- `RaiUtils` -> `e163c67`
- `RaiImage` -> `7c7e98b`
- `JsonPit` -> `e9d9b9f`
- `ImgSeeder` -> `b43185a`
- `PitSeeder` -> `af5eae6`

These heads are local-only from the perspective of this run. Child pushes failed because `github.com` DNS resolution failed in the shell, and the later parent `git push` failed with `fatal: could not read Username for 'https://github.com': Device not configured`.

## Validation note

- `dotnet test RaiImage/RaiImage.slnx --nologo -v minimal` -> `94 passed`
- `dotnet test ImgSeeder/ImgSeeder.slnx --nologo -v minimal` -> `8 passed`
- `dotnet test PitSeeder/PitSeeder.slnx --nologo -v minimal` -> `4 passed`
- `dotnet test RAIkeep.slnx --nologo -v minimal` -> `285 passed`, `1 skipped`
- Existing prebuilt `iorg` and `pits` binaries still report `3.9.1`, so they are not suitable evidence for the new line.

## Parent repo note

- The parent repo can carry the updated submodule pointers and refreshed release docs locally.
- The parent remote push still requires working GitHub credentials; `gh auth status` reports the active `github.com` token for `Burkhardt` is invalid in this session.
- No NuGet publish and no Sequential NuGet Release Chain run were triggered in this prep pass.

## Suggested resume prompt

```text
Please read CURRENT-STATE.md first. Continue the local 3.13.0 release-prep pass in an environment that allows GitHub network access, then push the child repos in order and push the parent repo with the updated submodule pointers. Do not publish to NuGet or dispatch the Sequential NuGet Release Chain unless explicitly requested.
```
