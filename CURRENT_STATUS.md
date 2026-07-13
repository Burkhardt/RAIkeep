# CURRENT_STATUS

Last updated: 2026-07-13

Current coordinated package line: `3.12.0`

## Release Truth

- The published/common remote baseline remains the completed `v3.11.4` line.
- The live child version metadata at the start of this run was `3.11.5` across `OsLibCore`, `RaiUtils`, `RaiImage`, `JsonPit`, `ImgSeeder`/`iorg`, and `PitSeeder`/`pits`, so the next coordinated minor line is `v3.12.0`.
- The release order remains `OsLib -> RaiUtils -> RaiImage -> JsonPit -> ImgSeeder -> PitSeeder`.
- The GitHub workflow and local helper preserve the required `330`-second wait between published packages and verify flat-container `.nupkg` visibility, including lowercase `imgseeder`, but no publish steps were run in this task.

## Local Prep Commits

- `OsLib` `4eb07dd` (`release: prep 3.12.0`)
- `RaiUtils` `d83821e` (`release: prep 3.12.0`)
- `RaiImage` `f4bec86` (`release: prep 3.12.0`)
- `JsonPit` `1487f6f` (`release: prep 3.12.0`)
- `ImgSeeder` `e69772b` (`release: prep 3.12.0`)
- `PitSeeder` `8ed2698` (`release: prep 3.12.0`)

## Validation

- `dotnet test OsLib/OsLib.Tests/OsLib.Tests.csproj --nologo -v minimal` -> `64 passed`
- `dotnet test RaiUtils/RaiUtils.slnx --nologo -v minimal` -> `21 passed`
- `dotnet test JsonPit/JsonPit.Tests/JsonPit.Tests.csproj --nologo -v minimal` first surfaced one transient `RAIkeepConcurrencyRegressionTests.SaveInterleavedWithAdds_SubsequentSavePersistsEveryAcceptedItem` failure with `IndexOutOfRangeException` from `Pit.GetRawPersistenceModel()`
- `dotnet test JsonPit/JsonPit.Tests/JsonPit.Tests.csproj --filter FullyQualifiedName~SaveInterleavedWithAdds_SubsequentSavePersistsEveryAcceptedItem --nologo -v minimal` -> `1 passed`
- `dotnet test JsonPit/JsonPit.Tests/JsonPit.Tests.csproj --nologo -v minimal` immediate rerun -> `101 passed`, `1 skipped`
- `dotnet test RaiImage/RaiImage.slnx --nologo -v minimal` -> `94 passed`
- `dotnet test ImgSeeder/ImgSeeder.slnx --nologo -v minimal` -> `8 passed`
- `dotnet test PitSeeder/PitSeeder.slnx --nologo -v minimal` -> `4 passed`
- `dotnet test RAIkeep.slnx --nologo -v minimal` -> passed with `RaiUtils 21`, `OsLib 64`, `RaiImage 94`, `JsonPit 101 + 1 skipped`, `PitSeeder 4`, `ImgSeeder 8`

Existing non-blocking warning observed on JsonPit-targeted build:

- `JsonPit.cs(95,32): warning CS1574: XML comment has cref attribute 'AddPreservingModified' that could not be resolved`

## Docs And Diagrams

- Package metadata, fallback package pins, README/API/status docs, and `RELEASE_NOTES_3.12.0.md` files are aligned across all six child repositories.
- PlantUML release markers were refreshed and tracked SVG renders regenerated for `OsLib`, `RaiUtils`, `RaiImage`, `JsonPit`, and the root dependency diagrams.
- `RunReleaseChain.md` now shows the `3.12.0` explicit version example and the required `330`-second hold window guidance.

## Blockers

- `git ls-remote origin HEAD` fails with `Could not resolve host: github.com`.
- `gh auth status` reports the active `Burkhardt` token as invalid.
- `git push origin main` failed with `Could not resolve host: github.com` for `OsLib`, `RaiUtils`, `RaiImage`, `JsonPit`, `ImgSeeder`, and `PitSeeder`.
- Because remote GitHub access is blocked here, child pushes could not complete and no tags, publish actions, or `sequential-nuget-release-chain` workflow dispatch were attempted.

## Local Noise To Ignore

- Untracked root artifacts unrelated to this release prep remain present: `.tmp_africa_svg/` and `AfricaStage-multicolor-clean.svg`.

## Resume Prompt

- Restore GitHub DNS reachability and valid `gh` auth.
- Push child `main` branches in order: `OsLib`, `RaiUtils`, `RaiImage`, `JsonPit`, `ImgSeeder`, `PitSeeder`.
- Push the parent `RAIkeep` repo with the updated submodule pointers, root dependency diagrams, and this release ledger.
- Do not publish to NuGet and do not trigger `.github/workflows/sequential-nuget-release-chain.yml` as part of this prep task.
- Keep the strict order and the `330`-second guidance for any later publish run.
