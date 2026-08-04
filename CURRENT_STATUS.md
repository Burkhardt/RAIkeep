# CURRENT_STATUS

Last updated: 2026-08-03

Current coordinated package line: `3.13.1`

Post-release maintenance is preparing a `380`-second future release hold, four-provider configured cloud-root support (`Dropbox`, `OneDrive`, `GoogleDrive`, `ICloudDrive`), and the missing ImgSeeder NuGet package icon. These changes are not part of the already-tagged `3.13.1` artifacts and require a later package version to reach NuGet.

## Release Truth

- The coordinated `v3.13.1` line is released across `OsLibCore`, `RaiUtils`, `RaiImage`, `JsonPit`, `ImgSeeder`/`iorg`, and `PitSeeder`/`pits`.
- The local release order is now `RAIkeep umbrella label -> OsLib -> RaiUtils -> RaiImage -> JsonPit -> ImgSeeder -> PitSeeder`.
- Future release-chain runs enforce a `380`-second wait between published packages and verify flat-container `.nupkg` visibility, including lowercase `imgseeder`; the window was raised after observed RaiUtils indexing latency.
- All seven repositories carry `v3.13.1`. All six package workflows completed successfully, and all six exact packages returned HTTP `200` from the NuGet flat container on 2026-08-03.

## Current Working Release Metadata

- All six child working trees now target `3.13.1`.
- The centralized current release notes are `doc/<Project>_RELEASE_NOTES_3.13.1.md`.
- The tagged `3.13.1` release commits are published. The post-release 380-second, iCloud-provider, ImgSeeder-icon, and handover maintenance described above is currently uncommitted.

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
- `RunReleaseChain.md`, `scripts/release-chain.sh`, and the umbrella sequential workflow now agree on the required `380`-second hold. The local script additionally applies the passed version to the prepared RAIkeep umbrella first, after verifying that it records the exact six child release commits.

## Published Release State

- `gh auth status` succeeds for the active `Burkhardt` account with repository and workflow scopes.
- The released child commits are OsLib `9be7c92`, RaiUtils `86faaa2`, RaiImage `12079cd`, JsonPit `e59f4a8`, ImgSeeder `330831c`, and PitSeeder `64a6673`.
- The released umbrella tag points to `3b7919f`.
- The successful package workflow run IDs are OsLib `30855844030`, RaiUtils `30856264199`, RaiImage `30856677476`, JsonPit `30857083981`, ImgSeeder `30857500291`, and PitSeeder `30857935094`.

## Next Maintenance Step

- Keep the separate JsonPit concurrency CR open until it is explicitly selected for implementation.
- Assign a new package version before publishing the post-3.13.1 cloud-provider and ImgSeeder-icon changes; NuGet packages are immutable.
- Commit the post-release child changes and then the updated umbrella pointers only after review.
