# CURRENT_STATUS

Current coordinated release-prep line: `3.11.0`.

- `OsLib`, `RaiUtils`, `RaiImage`, `JsonPit`, `ImgSeeder`/`iorg`, and `PitSeeder` were updated to `3.11.0`.
- Live package metadata, fallback dependency defaults, current README/API notes, `RELEASE_NOTES_3.11.0.md` files, and PlantUML release markers were aligned across the workspace.
- The carried-forward behavior includes the current RaiImage filename-normalization and `WordCase` guidance plus the `iorg` `-rmc` cache-delete alias.

Validation completed sequentially in this workspace:

- `dotnet test RaiImage/RaiImage.slnx --nologo -v minimal`: 91 passed
- `dotnet test ImgSeeder/ImgSeeder.slnx --nologo -v minimal`: 8 passed
- `dotnet test PitSeeder/PitSeeder.slnx --nologo -v minimal`: 3 passed
- `dotnet test RAIkeep.slnx --nologo -v minimal`: 280 passed, 1 skipped

Git push state from this environment:

- pushed: `OsLib` `3268fbf`, `RaiUtils` `69d2c32`
- local-only due DNS failure: `RaiImage` `c7e9e64`, `JsonPit` `cbf0b6d`, `ImgSeeder` `54a3bd2`, `PitSeeder` `df2dc3a`

The parent `RAIkeep` repo can carry the new submodule pointers locally, but its remote push must wait until those four child commits are reachable on GitHub.

Suggested resume prompt:

```text
Please read CURRENT_STATUS.md first. The coordinated 3.11.0 release-prep line is validated locally, two child repos are pushed, and the remaining child pushes plus the parent push are blocked by intermittent DNS resolution to github.com.
```
