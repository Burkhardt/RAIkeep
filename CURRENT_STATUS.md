# CURRENT_STATUS

Last updated: 2026-08-03

Current coordinated package line: `3.13.1`

## Release Truth

- The coordinated next-release line is `v3.13.1` across `OsLibCore`, `RaiUtils`, `RaiImage`, `JsonPit`, `ImgSeeder`/`iorg`, and `PitSeeder`/`pits`.
- The local release order is now `RAIkeep umbrella label -> OsLib -> RaiUtils -> RaiImage -> JsonPit -> ImgSeeder -> PitSeeder`.
- The GitHub workflow and local helper now both enforce the required `330`-second wait between published packages and verify flat-container `.nupkg` visibility, including lowercase `imgseeder`, but no publish steps were run in this task.
- GitHub authentication and all six remotes were re-verified successfully on 2026-08-03. No `v3.13.1` tag exists in any child repository.

## Current Working Release Metadata

- All six child working trees now target `3.13.1`.
- The centralized current release notes are `doc/<Project>_RELEASE_NOTES_3.13.1.md`.
- The earlier documentation-centralization commits exist locally; the functional `3.13.1` changes and latest release-document refinements are not committed yet.

## Previous 3.13.0 Prep Baseline

- `OsLib` `5b26149` (`release: prep 3.13.0`)
- `RaiUtils` `8e8b730` (`release: prep 3.13.0`)
- `RaiImage` `1667f53` (`release: prep 3.13.0`)
- `JsonPit` `6c172c1` (`release: prep 3.13.0`)
- `ImgSeeder` `a730699` (`release: prep 3.13.0`)
- `PitSeeder` `1ba1cf4` (`release: prep 3.13.0`)

## Validation

- The 2026-08-03 umbrella run built all six projects successfully.
- After the PitSeeder process-window and RaiFile timestamp implementation, `OsLib` passes `66` tests and `PitSeeder` passes `7`. In JsonPit, `103` tests passed in the run excluding the separate concurrency CR and external remote-sync scenario; the OneDrive remote-sync test passed on its immediate isolated rerun.
- Two immediate consecutive read-only WWWA exports against the configured OneDrive `AIA` pit succeeded. Both runs left distinct per-PID epoch tombstones, confirming ownership-verified release without a delete/recreate cycle.
- The full umbrella run still has one known failure: `SaveInterleavedWithAdds_SubsequentSavePersistsEveryAcceptedItem` throws during concurrent persistence snapshot materialization.
- An immediate isolated rerun failed again in `ConcurrentDictionary.ICollection.CopyTo(...)`, confirming the open race documented in [`doc/JsonPit_CR_concurrency-for-next-release-RAI-commented.md`](doc/JsonPit_CR_concurrency-for-next-release-RAI-commented.md).

The PitSeeder lifecycle request is resolved in [`doc/PitSeeder_CR_release_for_cli-resolved-in-v3.13.1.md`](doc/PitSeeder_CR_release_for_cli-resolved-in-v3.13.1.md). The separate JsonPit concurrency request remains open and was not implemented in this slice.

The stale `AddPreservingModified` XML documentation reference was corrected to `AddHistorical(PitItem)`; the current umbrella build succeeds with `0` warnings and `0` errors.

## Docs And Diagrams

- Package metadata, fallback package pins, README/API/status docs, and the project-prefixed `doc/*_RELEASE_NOTES_3.13.1.md` files are aligned across all six child repositories.
- `doc/JsonPit-FlagFiles-And-Concurrency.md` documents the ProcessFlagFile activity window, stable `Master.flag` lease, canonical-write decision, and current coordination boundary.
- PlantUML release markers were refreshed and tracked SVG renders regenerated for `OsLib`, `RaiUtils`, `RaiImage`, `JsonPit`, and the root dependency diagrams.
- `RunReleaseChain.md`, `scripts/release-chain.sh`, and the umbrella sequential workflow now agree on the required `330`-second hold. The local script additionally applies the passed version to the prepared RAIkeep umbrella first, after verifying that it records the exact six child release commits.

## Remote Release Readiness

- `gh auth status` succeeds for the active `Burkhardt` account with repository and workflow scopes.
- Remote child `HEAD` values remain at the recorded `3.13.0` preparation commits: OsLib `5b26149`, RaiUtils `8e8b730`, RaiImage `1667f53`, JsonPit `6c172c1`, ImgSeeder `a730699`, and PitSeeder `1ba1cf4`.
- `v3.13.1` is absent from all six child remotes, so no repository has started this release line.
- No push, tag creation, workflow dispatch, or NuGet publication was performed during this preparation.

## Next Maintenance Step

- Keep the separate JsonPit concurrency CR open until it is explicitly selected for implementation.
- After explicit approval, commit the remaining child changes in dependency order, then commit the updated parent submodule pointers and centralized `doc/` refinements.
- Do not publish to NuGet or trigger the sequential release chain unless explicitly requested.
