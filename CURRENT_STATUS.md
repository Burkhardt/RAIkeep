# CURRENT_STATUS

Last updated: 2026-07-20

Current coordinated package line: `3.13.0`

## Release Truth

- The live child version metadata at the start of this run was `3.12.0` across `OsLibCore`, `RaiUtils`, `RaiImage`, `JsonPit`, `ImgSeeder`/`iorg`, and `PitSeeder`/`pits`, so the next coordinated minor line is `v3.13.0`.
- The release order remains `OsLib -> RaiUtils -> RaiImage -> JsonPit -> ImgSeeder -> PitSeeder`.
- The GitHub workflow and local helper preserve the required `330`-second wait between published packages and verify flat-container `.nupkg` visibility, including lowercase `imgseeder`, but no publish steps were run in this task.
- Remote GitHub tag and publication state could not be re-verified from this environment because `github.com` DNS resolution failed and `gh auth status` reported an invalid token.

## Local Prep Commits

- `OsLib` `5b26149` (`release: prep 3.13.0`)
- `RaiUtils` `8e8b730` (`release: prep 3.13.0`)
- `RaiImage` `1667f53` (`release: prep 3.13.0`)
- `JsonPit` `6c172c1` (`release: prep 3.13.0`)
- `ImgSeeder` `a730699` (`release: prep 3.13.0`)
- `PitSeeder` `1ba1cf4` (`release: prep 3.13.0`)

## Validation

- The direct per-command test invocations needed `--disable-build-servers -maxcpucount:1 -nodeReuse:false -p:UseSharedCompilation=false -p:BuildInParallel=false` in this sandbox to avoid local `vstest` socket and MSBuild named-pipe permission failures.
- `dotnet test OsLib/OsLib.Tests/OsLib.Tests.csproj --nologo -v minimal --disable-build-servers -maxcpucount:1 -nodeReuse:false -p:UseSharedCompilation=false -p:BuildInParallel=false` -> `64 passed`
- `dotnet test RaiUtils/RaiUtils.slnx --nologo -v minimal --disable-build-servers -maxcpucount:1 -nodeReuse:false -p:UseSharedCompilation=false -p:BuildInParallel=false` -> `21 passed`
- `dotnet test JsonPit/JsonPit.Tests/JsonPit.Tests.csproj --nologo -v minimal --disable-build-servers -maxcpucount:1 -nodeReuse:false -p:UseSharedCompilation=false -p:BuildInParallel=false` -> `101 passed`, `1 skipped`
- `dotnet test RaiImage/RaiImage.slnx --nologo -v minimal --disable-build-servers -maxcpucount:1 -nodeReuse:false -p:UseSharedCompilation=false -p:BuildInParallel=false` -> `94 passed`
- `dotnet test ImgSeeder/ImgSeeder.slnx --nologo -v minimal --disable-build-servers -maxcpucount:1 -nodeReuse:false -p:UseSharedCompilation=false -p:BuildInParallel=false` -> `8 passed`
- `dotnet test PitSeeder/PitSeeder.slnx --nologo -v minimal --disable-build-servers -maxcpucount:1 -nodeReuse:false -p:UseSharedCompilation=false -p:BuildInParallel=false` -> `4 passed`
- `dotnet test RAIkeep.slnx --nologo -v minimal --disable-build-servers -maxcpucount:1 -nodeReuse:false -p:UseSharedCompilation=false -p:BuildInParallel=false` -> passed with `RaiUtils 21`, `OsLib 64`, `RaiImage 94`, `JsonPit 101 + 1 skipped`, `PitSeeder 4`, `ImgSeeder 8`

Existing non-blocking warning observed on JsonPit-targeted build:

- `JsonPit.cs(95,32): warning CS1574: XML comment has cref attribute 'AddPreservingModified' that could not be resolved`

## Docs And Diagrams

- Package metadata, fallback package pins, README/API/status docs, and `RELEASE_NOTES_3.13.0.md` files are aligned across all six child repositories.
- PlantUML release markers were refreshed and tracked SVG renders regenerated for `OsLib`, `RaiUtils`, `RaiImage`, `JsonPit`, and the root dependency diagrams.
- `RunReleaseChain.md` now shows the `3.13.0` explicit version example and the required `330`-second hold window guidance.

## Blockers

- `git ls-remote origin HEAD` fails with `Could not resolve host: github.com`.
- `gh auth status` reports the active `Burkhardt` token as invalid.
- `git push origin main` failed with `Could not resolve host: github.com` for `OsLib` (`5b26149`), `RaiUtils` (`8e8b730`), `RaiImage` (`1667f53`), `JsonPit` (`6c172c1`), `ImgSeeder` (`a730699`), and `PitSeeder` (`1ba1cf4`).
- Because remote GitHub access is blocked here, child pushes could not complete and no tags, publish actions, or `sequential-nuget-release-chain` workflow dispatch were attempted.

## Local Noise To Ignore

- Untracked root artifacts unrelated to this release prep remain present: `.tmp_africa_svg/` and `AfricaStage-multicolor-clean.svg`.

## Resume Prompt

- Restore GitHub DNS reachability and valid `gh` auth.
- Push child `main` branches in order: `OsLib`, `RaiUtils`, `RaiImage`, `JsonPit`, `ImgSeeder`, `PitSeeder`.
- Push the parent `RAIkeep` repo with the updated submodule pointers, root dependency diagrams, and this release ledger.
- Do not publish to NuGet and do not trigger `.github/workflows/sequential-nuget-release-chain.yml` as part of this prep task.
- Keep the strict order and the `330`-second guidance available for a later publish run, including flat-container `.nupkg` verification with lowercase `imgseeder`.
