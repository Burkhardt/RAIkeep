# CURRENT_STATUS

Last updated: 2026-08-03

Current coordinated package line: `3.13.1`

## Release Truth

- The coordinated next-release line is `v3.13.1` across `OsLibCore`, `RaiUtils`, `RaiImage`, `JsonPit`, `ImgSeeder`/`iorg`, and `PitSeeder`/`pits`.
- The release order remains `OsLib -> RaiUtils -> RaiImage -> JsonPit -> ImgSeeder -> PitSeeder`.
- The GitHub workflow and local helper preserve the required `330`-second wait between published packages and verify flat-container `.nupkg` visibility, including lowercase `imgseeder`, but no publish steps were run in this task.
- Remote GitHub tag and publication state could not be re-verified from this environment because `github.com` DNS resolution failed and `gh auth status` reported an invalid token.

## Current Working Release Metadata

- All six child working trees now target `3.13.1`.
- The centralized current release notes are `doc/<Project>_RELEASE_NOTES_3.13.1.md`.
- These maintenance changes are not committed yet.

## Previous 3.13.0 Prep Baseline

- `OsLib` `5b26149` (`release: prep 3.13.0`)
- `RaiUtils` `8e8b730` (`release: prep 3.13.0`)
- `RaiImage` `1667f53` (`release: prep 3.13.0`)
- `JsonPit` `6c172c1` (`release: prep 3.13.0`)
- `ImgSeeder` `a730699` (`release: prep 3.13.0`)
- `PitSeeder` `1ba1cf4` (`release: prep 3.13.0`)

## Validation

- The 2026-08-03 umbrella run built all six projects successfully.
- After the PitSeeder process-window implementation, `OsLib` passes `65` tests and `PitSeeder` passes `7`. In JsonPit, `103` tests passed in the run excluding the separate concurrency CR; its OneDrive remote-sync test observed a transient materialization race and then passed on an immediate isolated rerun.
- Two immediate consecutive read-only WWWA exports against the configured OneDrive `AIA` pit succeeded. Both runs left distinct per-PID epoch tombstones, confirming ownership-verified release without a delete/recreate cycle.
- The full umbrella run still has one known failure: `SaveInterleavedWithAdds_SubsequentSavePersistsEveryAcceptedItem` throws during concurrent persistence snapshot materialization.
- An immediate isolated rerun failed again in `ConcurrentDictionary.ICollection.CopyTo(...)`, confirming the open race documented in [`doc/JsonPit_CR_concurrency-for-next-release-RAI-commented.md`](doc/JsonPit_CR_concurrency-for-next-release-RAI-commented.md).

The PitSeeder lifecycle request is resolved in [`doc/PitSeeder_CR_release_for_cli-resolved-in-v3.13.1.md`](doc/PitSeeder_CR_release_for_cli-resolved-in-v3.13.1.md). The separate JsonPit concurrency request remains open and was not implemented in this slice.

Existing non-blocking warning observed on JsonPit-targeted build:

- `JsonPit.cs(95,32): warning CS1574: XML comment has cref attribute 'AddPreservingModified' that could not be resolved`

## Docs And Diagrams

- Package metadata, fallback package pins, README/API/status docs, and the project-prefixed `doc/*_RELEASE_NOTES_3.13.1.md` files are aligned across all six child repositories.
- PlantUML release markers were refreshed and tracked SVG renders regenerated for `OsLib`, `RaiUtils`, `RaiImage`, `JsonPit`, and the root dependency diagrams.
- `RunReleaseChain.md` now shows the `3.13.1` explicit version example and the required `330`-second hold window guidance.

## Previously Recorded Release Blockers

The following conditions were recorded during the 2026-07-20 `3.13.0` preparation and have not been re-verified in this maintenance pass:

- `git ls-remote origin HEAD` fails with `Could not resolve host: github.com`.
- `gh auth status` reports the active `Burkhardt` token as invalid.
- `git push origin main` failed with `Could not resolve host: github.com` for `OsLib` (`5b26149`), `RaiUtils` (`8e8b730`), `RaiImage` (`1667f53`), `JsonPit` (`6c172c1`), `ImgSeeder` (`a730699`), and `PitSeeder` (`1ba1cf4`).
- `RAIkeep` `main` did push successfully at `4db644f`, so the remote parent repo now references child submodule commits that are still local-only until the six child `main` pushes succeed.
- No tags, publish actions, or `sequential-nuget-release-chain` workflow dispatch were attempted.

## Local Noise To Ignore

- Untracked root artifacts unrelated to this release prep remain present: `.tmp_africa_svg/` and `AfricaStage-multicolor-clean.svg`.

## Next Maintenance Step

- Keep the separate JsonPit concurrency CR open until it is explicitly selected for implementation.
- Commit child changes in dependency order, then commit the updated parent submodule pointers and centralized `doc/` files.
- Do not publish to NuGet or trigger the sequential release chain unless explicitly requested.
