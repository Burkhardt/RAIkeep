# CURRENT_STATUS

Current coordinated minor line: `3.13.0`

- Starting baseline was the live `3.12.1` line across all six child repos/packages.
- Local child repo prep commits for `3.13.0` are:
  - `OsLib` `de3807c`
  - `RaiUtils` `e163c67`
  - `RaiImage` `7c7e98b`
  - `JsonPit` `e9d9b9f`
  - `ImgSeeder` `b43185a`
  - `PitSeeder` `af5eae6`
- Sequential validation passed:
  - `dotnet test RaiImage/RaiImage.slnx --nologo -v minimal` -> `94 passed`
  - `dotnet test ImgSeeder/ImgSeeder.slnx --nologo -v minimal` -> `8 passed`
  - `dotnet test PitSeeder/PitSeeder.slnx --nologo -v minimal` -> `4 passed`
  - `dotnet test RAIkeep.slnx --nologo -v minimal` -> `285 passed`, `1 skipped`
- `JsonPit` emitted one existing documentation warning during the `ImgSeeder` solution build path:
  - `JsonPit.cs(95,32): warning CS1574: XML comment has cref attribute 'AddPreservingModified' that could not be resolved`
- Existing `iorg` and `pits` binaries still report `3.9.1`, so they are stale and not valid `3.13.0` verification.
- Child pushes are blocked here by shell DNS failure to `github.com`.
- The parent `RAIkeep` push currently fails later with:
  - `fatal: could not read Username for 'https://github.com': Device not configured`
- `gh auth status` reports the active `github.com` token for `Burkhardt` is invalid.
- No NuGet publish and no Sequential NuGet Release Chain run were triggered, by request.

Suggested resume prompt:

```text
Please read CURRENT_STATUS.md first. Continue the prepared 3.13.0 release in an environment with working GitHub DNS/network access, push the child repos in order, then push the parent repo with the updated submodule pointers. Do not publish to NuGet or dispatch the Sequential NuGet Release Chain unless explicitly requested.
```
