# CURRENT_STATUS

Last updated: 2026-07-20

Current coordinated package line: `3.12.1`

## Release Truth

- The live child version metadata at the start of this run was `3.12.0` across `OsLibCore`, `RaiUtils`, `RaiImage`, `JsonPit`, `ImgSeeder`/`iorg`, and `PitSeeder`/`pits`, so the next coordinated patch line is `v3.12.1`.
- The release order remains `OsLib -> RaiUtils -> RaiImage -> JsonPit -> ImgSeeder -> PitSeeder`.
- The GitHub workflow and local helper preserve the required `300`-second wait between published packages and verify flat-container `.nupkg` visibility, including lowercase `imgseeder`, but no publish steps were run in this task.
- Remote GitHub tag and publication state could not be re-verified from this environment because `github.com` DNS resolution failed and `gh auth status` reported an invalid token.

## Local Prep Commits

- `OsLib` `2f04769` (`release: prep 3.12.1`)
- `RaiUtils` `a3cebf8` (`release: prep 3.12.1`)
- `RaiImage` `a67d1a6` (`release: prep 3.12.1`)
- `JsonPit` `727c2e5` (`release: prep 3.12.1`)
- `ImgSeeder` `9f32fbe` (`release: prep 3.12.1`)
- `PitSeeder` `cea41b6` (`release: prep 3.12.1`)

## Validation

- `dotnet test OsLib/OsLib.Tests/OsLib.Tests.csproj --nologo -v minimal` -> `64 passed`
- `dotnet test RaiUtils/RaiUtils.slnx --nologo -v minimal` -> `21 passed`
- `dotnet test JsonPit/JsonPit.Tests/JsonPit.Tests.csproj --nologo -v minimal` -> `101 passed`, `1 skipped`
- `dotnet test RaiImage/RaiImage.slnx --nologo -v minimal` -> `94 passed`
- `dotnet test ImgSeeder/ImgSeeder.slnx --nologo -v minimal` -> `8 passed`
- `dotnet test PitSeeder/PitSeeder.slnx --nologo -v minimal` -> `4 passed`
- `dotnet test RAIkeep.slnx --nologo -v minimal` -> passed with `RaiUtils 21`, `OsLib 64`, `RaiImage 94`, `JsonPit 101 + 1 skipped`, `PitSeeder 4`, `ImgSeeder 8`

Observed only during the parallel per-repo warm-up pass, not during the sequential umbrella run:

- `RaiImage` emitted one transient reference-assembly file-lock warning against `RaiUtils/obj/Debug/net10.0/refint/RaiUtils.dll`.
- `PitSeeder` emitted one transient MSBuild copy-retry warning against `JsonPit/obj/Debug/net10.0/JsonPit.dll`.

Existing non-blocking warning observed on JsonPit-targeted build:

- `JsonPit.cs(95,32): warning CS1574: XML comment has cref attribute 'AddPreservingModified' that could not be resolved`

## Docs And Diagrams

- Package metadata, fallback package pins, README/API/status docs, and `RELEASE_NOTES_3.12.1.md` files are aligned across all six child repositories.
- PlantUML release markers were refreshed and tracked SVG renders regenerated for `OsLib`, `RaiUtils`, `RaiImage`, `JsonPit`, and the root dependency diagrams.
- `RunReleaseChain.md` now shows the `3.12.1` explicit version example and the required `300`-second hold window guidance.

## Blockers

- `git ls-remote origin HEAD` fails with `Could not resolve host: github.com`.
- `gh auth status` reports the active `Burkhardt` token as invalid.
- `git push origin main` failed with `Could not resolve host: github.com` for `OsLib` (`2f04769`), `RaiUtils` (`a3cebf8`), `RaiImage` (`a67d1a6`), `JsonPit` (`727c2e5`), `ImgSeeder` (`9f32fbe`), and `PitSeeder` (`cea41b6`).
- Because remote GitHub access is blocked here, child pushes could not complete and no tags, publish actions, or `sequential-nuget-release-chain` workflow dispatch were attempted.

## Local Noise To Ignore

- Untracked root artifacts unrelated to this release prep remain present: `.tmp_africa_svg/` and `AfricaStage-multicolor-clean.svg`.

## Resume Prompt

- Restore GitHub DNS reachability and valid `gh` auth.
- Push child `main` branches in order: `OsLib`, `RaiUtils`, `RaiImage`, `JsonPit`, `ImgSeeder`, `PitSeeder`.
- Push the parent `RAIkeep` repo with the updated submodule pointers, root dependency diagrams, and this release ledger.
- Create the required `v3.12.1` tags after each child `main` push is in place.
- Trigger `.github/workflows/sequential-nuget-release-chain.yml` from `RAIkeep` `main` with `publish_to_nuget=true`.
- Keep the strict order and the `300`-second guidance for the publish run and verify flat-container `.nupkg` URLs, including lowercase `imgseeder`.
