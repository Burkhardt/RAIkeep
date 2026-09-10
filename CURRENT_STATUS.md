# CURRENT_STATUS

Last updated: 2026-09-09

Current released package line: `4.2.7`

Upcoming coordinated package line: `4.2.8`

## Released 4.2.7 state

- The RAIkeep umbrella coordinates seven independently published package repositories.
- `OsLibCore`, `RaiUtils`, `RaiImage`, `RaiDiagram`, `JsonPit`, `ImgSeeder`, and `PitSeeder` 4.2.7 are the current coordinated baseline.
- CR020 ItemTree selection, movement, and `iorg` custodianship are aligned throughout that package line.

## Coordinated 4.2.8 preparation

- Accepted CR021 replaces JsonPit's process-local change-cleanup timer with immutable same-stem `.receipt` evidence whose first canonical-accounting time survives restart and master transfer.
- `Pit.Maintain(...)` provides report-only and explicit apply behavior; eligible cleanup revalidates authority and canonical accounting, then removes change first and receipt second.
- PID-window pruning requires explicit apply plus an age; recognizable extensionless flags/events require separate repair authorization.
- `pits maintain` supports one pit or WWWA with human/JSON results and avoids disposal republishing retired changes.
- OsLibCore preserves dotted explicit `TextFile` stems and serializes same-target typed `PitsCommand` calls across wrapper instances.
- All seven package projects and fallback dependency properties are aligned on 4.2.8.
- No 4.2.8 tag or NuGet publication has been created; RAI retains the manual release gate.

## Coordinated release tooling

- `scripts/release-chain.sh` is the single coordinated release orchestrator.
- The enforced order is `OsLibCore → RaiUtils → RaiImage → RaiDiagram → JsonPit → ImgSeeder → PitSeeder`.
- Every package performs a package-only restore before its tag is created.
- The chain waits for both the exact `.nupkg` and exact-version NuGet registration document to return HTTP `200`; it does not use a fixed indexing delay.
- The umbrella label records the exact seven child commits before any package tag is created.

## Documentation state

- Package README links to Markdown documents use absolute GitHub URLs so they work from NuGet as well as GitHub.
- Foldable API references exist for OsLibCore, RaiUtils, RaiImage, JsonPit, and RaiDiagram.
- CR021 and coordinated 4.2.8 release notes are centralized under `doc/`.
- `scripts/check-markdown-document-links.sh` and its GitHub workflow reject new relative Markdown document links.

## Validation

- The full umbrella Release build succeeds.
- Current package tests pass 558 of 559 cases: OsLibCore 124, RaiUtils 51, RaiImage 117, RaiDiagram 35, JsonPit 164 of 165, ImgSeeder 28, and PitSeeder 39 (zero skipped).
- The CR021 receipt lifecycle passes against a real configured CloudDrive root, including materialization, restart, preservation of the original receipt time, elapsed-grace change-first cleanup, and receipt removal.
- RaiDiagram's passing suite includes the real local PlantUML integration path.
- The complete mixed `AfricanBrisket` image/diagram family, wildcard listing, sibling exclusion, rename, subscriber relocation, 3x3/8x2/Flat migration, indexed ItemIds, and short ItemIds with coincident physical convention homes are covered.
- Of the two Mzansi scenarios, the broader remote-sync flow passed and the split-master propagation scenario reached its established ten-minute timeout because Mzansi's OneDrive synchronizer was inactive. This is an external operational prerequisite rather than a CR021 code failure. CR021's required configured-CloudDrive storage boundary is green locally without a skip.
- The umbrella build still reports existing xUnit analyzer warnings in JsonPit concurrency tests; CR020 adds no compiler errors.

## Remaining 4.2.8 release preparation

- Commit each child repository on `main`, then commit the exact seven updated submodule pointers and umbrella documents on `main`.
- Confirm the resulting worktrees are clean and the seven inspected local package artifacts remain aligned on 4.2.8.
- RAI may then start `scripts/release-chain.sh 4.2.8` manually.
