# CURRENT_STATUS

Last updated: 2026-07-13

Current coordinated package line: `3.11.5`

## Release Truth

- The published/common remote baseline remains the completed `v3.11.4` line.
- This run prepares the next coordinated patch line `v3.11.5` locally across `OsLibCore`, `RaiUtils`, `RaiImage`, `JsonPit`, `ImgSeeder`/`iorg`, and `PitSeeder`/`pits`.
- The release order remains `OsLib -> RaiUtils -> RaiImage -> JsonPit -> ImgSeeder -> PitSeeder`.
- The GitHub workflow and local helper now both preserve the required `300`-second wait between published packages and verify flat-container `.nupkg` visibility, including lowercase `imgseeder`.

## Local Prep Commits

- `OsLib` `e155406` (`chore: prepare 3.11.5 release`)
- `RaiUtils` `d462c1d` (`chore: prepare 3.11.5 release`)
- `RaiImage` `65ac2dd` (`chore: prepare 3.11.5 release`)
- `JsonPit` `b712cb8` (`chore: prepare 3.11.5 release`)
- `ImgSeeder` `df159b3` (`chore: prepare 3.11.5 release`)
- `PitSeeder` `e693c6c` (`chore: prepare 3.11.5 release`)

## Validation

- `dotnet test RaiUtils/RaiUtils.slnx --nologo -v minimal` -> `21 passed`
- `dotnet test JsonPit/JsonPit.Tests/JsonPit.Tests.csproj --filter FullyQualifiedName~DeletePropertyProjectionTests --nologo -v minimal` -> `7 passed`
- `dotnet test JsonPit/JsonPit.Tests/JsonPit.Tests.csproj --nologo -v minimal` -> `101 passed`, `1 skipped`
- `dotnet test RaiImage/RaiImage.slnx --nologo -v minimal` -> `94 passed`
- `dotnet test ImgSeeder/ImgSeeder.slnx --nologo -v minimal` -> `8 passed`
- `dotnet test PitSeeder/PitSeeder.slnx --nologo -v minimal` -> `4 passed`
- `dotnet test RAIkeep.slnx --nologo -v minimal` -> passed with `RaiUtils 21`, `OsLib 64`, `RaiImage 94`, `JsonPit 101 + 1 skipped`, `PitSeeder 4`, `ImgSeeder 8`

Existing non-blocking warning observed on JsonPit-targeted build:

- `JsonPit.cs(95,32): warning CS1574: XML comment has cref attribute 'AddPreservingModified' that could not be resolved`

## Docs And Diagrams

- Package metadata, fallback package pins, README/API/status docs, and `RELEASE_NOTES_3.11.5.md` files are aligned across all six child repositories.
- PlantUML release markers were refreshed and tracked SVG renders regenerated for `OsLib`, `RaiUtils`, `RaiImage`, and `JsonPit`.
- `RunReleaseChain.md` and `scripts/release-chain.sh` now match the required `300`-second hold window and flat-container verification guidance.

## Blockers

- `git -C OsLib ls-remote origin HEAD` fails with `Could not resolve host: github.com`.
- `gh auth status` reports the active `Burkhardt` token as invalid.
- Because remote GitHub access is blocked here, no child pushes, tags, or `sequential-nuget-release-chain` workflow dispatch were attempted from this environment.

## Local Noise To Ignore

- Untracked root artifacts unrelated to this release prep remain present: `.tmp_africa_svg/` and `AfricaStage-multicolor-clean.svg`.

## Resume Prompt

- Restore GitHub DNS reachability and valid `gh` auth.
- Push child `main` branches in order: `OsLib`, `RaiUtils`, `RaiImage`, `JsonPit`, `ImgSeeder`, `PitSeeder`.
- Tag each child `v3.11.5` only after the pushed `main` commit is confirmed.
- Commit and push the parent `RAIkeep` repo with the updated submodule pointers and release ledger.
- From `RAIkeep main`, start `.github/workflows/sequential-nuget-release-chain.yml` with `publish_to_nuget=true`.
- Keep the strict order, the `300`-second waits, and flat-container verification for `oslibcore`, `raiutils`, `raiimage`, `jsonpit`, `imgseeder`, and `pitseeder`.
