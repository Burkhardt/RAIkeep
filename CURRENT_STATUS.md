# CURRENT_STATUS

Last updated: 2026-08-05

Current coordinated package line: `3.13.1` released; `3.13.2` (CR003) implemented locally, publication pending release authorization

## CR003 implementation state (coordinated 3.13.2)

[`CR003_RAI_to_RAIkeep_JsonPit-concurrency-contract-and-persistence-races.md`](doc/CR003_RAI_to_RAIkeep_JsonPit-concurrency-contract-and-persistence-races.md) and the
[live split-master recovery concept](doc/JsonPit-CONCEPT-Live-Split-Master-Recovery.md) are implemented across OsLib, JsonPit, and PitSeeder/`pits`:

- OsLib 3.13.2: no-delete/no-rename `TextFile.Save` (copy-based backup), `CanonicalJson`, `EventFile`/`EventDirectory`; `AwaitMaterializing` freshness tolerance widened for coarse-granularity cloud mounts (Mzansi `/srv` stores whole-second mtimes).
- JsonPit 3.13.2: state/snapshot gate for concurrent `Add`/`Save` (fixes the confirmed `SaveInterleavedWithAdds` race), exact-PID master ownership, one live public `Pit` per canonical path, validated candidate loads with `JsonPitPersistenceException`, hashed collision-safe change files, two-stage post-save cleanup grace, live split-master recovery (write set, watcher, loser/orphan protocols), durable audit events, disposal durability boundary.
- PitSeeder 3.13.2: read-only `pits --events` audit mode (`--event-machine`, `--event-level`); finite CLI runs dispose pits through the CR003 durability boundary.
- Release notes: `doc/OsLib_RELEASE_NOTES_3.13.2.md`, `doc/JsonPit_RELEASE_NOTES_3.13.2.md`, `doc/PitSeeder_RELEASE_NOTES_3.13.2.md`.
- Evidence: recorded full-umbrella acceptance run (all suites incl. both SSH scenarios): 361 passed / 1 failed / 0 skipped — the single failure was `RemoteSyncTests` exhausting its 600 s OneDrive propagation window for the Mzansi-bound merged pit while the rest of the suite churned the same cloud root; the scenario passed in isolation immediately before (1 m 26 s) and immediately after (2 m). The two-server split-master scenario passed both inside the combined run and standalone (19.3 s scenario time, artifacts recorded in the JsonPit release notes). pits v3.13.2 deployed to Mzansi (`/usr/local/bin/pits`, v3.8.10 kept as `.bak`).
- Not performed (per instruction): no NuGet publication, no release tag, no NuGet workflow trigger.

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
- An immediate isolated rerun failed again in `ConcurrentDictionary.ICollection.CopyTo(...)`, confirming the open race documented in [`doc/CR003_RAI_to_RAIkeep_JsonPit-concurrency-contract-and-persistence-races.md`](doc/CR003_RAI_to_RAIkeep_JsonPit-concurrency-contract-and-persistence-races.md).

The PitSeeder lifecycle request is resolved in [`doc/PitSeeder_CR_release_for_cli-resolved-in-v3.13.1.md`](doc/PitSeeder_CR_release_for_cli-resolved-in-v3.13.1.md). [`CR003`](doc/CR003_RAI_to_RAIkeep_JsonPit-concurrency-contract-and-persistence-races.md) and its [live split-master recovery concept](doc/JsonPit-CONCEPT-Live-Split-Master-Recovery.md) were accepted and finalized on 2026-08-05 for coordinated `3.13.2` implementation; implementation has not begun in this documentation step.

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

- Implement accepted CR003 across OsLib, JsonPit, PitSeeder/`pits`, and the umbrella documentation, then execute its required configured-cloud and remote acceptance suite before coordinated `3.13.2` release work.
- Assign a new package version before publishing the post-3.13.1 cloud-provider and ImgSeeder-icon changes; NuGet packages are immutable.
- Commit the post-release child changes and then the updated umbrella pointers only after review.
