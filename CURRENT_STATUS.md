# CURRENT_STATUS

Last updated: 2026-07-06

Current coordinated minor line: `3.13.0`

## Local Version Truth

- Authoritative local child package versions at the start of this run were already `3.12.0` in all six child repo project files:
  - `OsLib/OsLib.csproj`
  - `RaiUtils/RaiUtils.csproj`
  - `RaiImage/RaiImage.csproj`
  - `JsonPit/JsonPit.csproj`
  - `ImgSeeder/ImgSeeder.csproj`
  - `PitSeeder/pits/pits.csproj`
- Therefore the next coordinated minor target prepared in this run is `3.13.0`.

## Remote / Publish Truth

- The prior umbrella ledger entry recorded `3.11.3` as the latest tagged and NuGet-published line.
- That remote truth was not reverified live in this run because GitHub access is blocked in this environment during push attempts.

## Prepared Local Child Commits

- `OsLib` `88ed2fb`
- `RaiUtils` `88a99ee`
- `RaiImage` `52b6aa2`
- `JsonPit` `09dbab6`
- `ImgSeeder` `77ff9ed`
- `PitSeeder` `596c2f2`

## Validation

- Sequential release validation passed:
  - `dotnet test RaiImage/RaiImage.slnx --nologo -v minimal` -> `94 passed`
  - `dotnet test ImgSeeder/ImgSeeder.slnx --nologo -v minimal` -> `8 passed`
  - `dotnet test PitSeeder/PitSeeder.slnx --nologo -v minimal` -> `4 passed`
  - `dotnet test RAIkeep.slnx --nologo -v minimal` -> `OsLib 64 passed`, `RaiUtils 21 passed`, `JsonPit 94 passed / 1 skipped`, `RaiImage 94 passed`, `ImgSeeder 8 passed`, `PitSeeder 4 passed`
- Existing `JsonPit` documentation warning still appears on the `ImgSeeder` solution build path:
  - `JsonPit.cs(95,32): warning CS1574: XML comment has cref attribute 'AddPreservingModified' that could not be resolved`
- `dotnet run` CLI smoke checks for `iorg` and `pits` were attempted earlier in this run but hung in this shell context, so release evidence here relies on solution tests and project metadata rather than those runtime probes.

## Blockers

- Child pushes are blocked in this environment:
  - `OsLib`: `fatal: could not read Username for 'https://github.com': Device not configured`
  - `RaiUtils`: `fatal: could not read Username for 'https://github.com': Device not configured`
  - `RaiImage`: `fatal: unable to access 'https://github.com/Burkhardt/RaiImage.git/': Could not resolve host: github.com`
  - `JsonPit`: `fatal: unable to access 'https://github.com/Burkhardt/JsonPit.git/': Could not resolve host: github.com`
  - `ImgSeeder`: `fatal: unable to access 'https://github.com/Burkhardt/ImgSeeder.git/': Could not resolve host: github.com`
  - `PitSeeder`: `fatal: unable to access 'https://github.com/Burkhardt/PitSeeder.git/': Could not resolve host: github.com`
- No NuGet publish and no Sequential NuGet Release Chain run were triggered, by request.

## Suggested Resume Prompt

```text
Please read CURRENT_STATUS.md first. Continue the prepared 3.13.0 release in an environment with working GitHub auth/DNS, push the child repos in order, then push the parent repo with the updated submodule pointers. Do not publish to NuGet or dispatch the Sequential NuGet Release Chain unless explicitly requested.
```
