# CURRENT_STATUS

Last updated: 2026-09-08

Current released package line: `4.2.6`

Upcoming coordinated package line: `4.2.7`

## Released 4.2.6 state

- The RAIkeep umbrella coordinates seven independently published package repositories.
- `OsLibCore`, `RaiUtils`, `RaiImage`, `RaiDiagram`, `JsonPit`, `ImgSeeder`, and `PitSeeder` 4.2.6 are visible through NuGet's exact package endpoint.
- CR019's canonical RaiUtils word-case and Unicode-safe word-seam implementation is available throughout the aligned package line.

## Coordinated 4.2.7 preparation

- Accepted CR020 establishes `ItemTreePath` as the object-oriented home of one subscriber-local ItemId and all of its image and diagram files.
- `ItemTreePath.SelectFiles()` selects an exact item family while excluding similarly named siblings in a shared bucket.
- Destination-oriented `ItemTreePath.mv(source)` moves or renames complete item families across subscriber roots and canonical, 3x3, 8x2, or Flat layouts.
- `ImageTreeFile`, `ItemTreeTextFile`, and the RaiDiagram artifact types accept `ItemTreePath`; the active static `FromImageTree` / `FromItemTree` construction path has been removed.
- `iorg list` provides read-only wildcard discovery. `iorg move` provides exact-ItemId relocation and optional rename. `iorg clean` distinguishes complete item deletion from explicit derivative-cache cleanup.
- OsLibCore exposes typed list and move requests through `IorgCommand` and keeps recursive filesystem traversal behind the `RaiPath` / `RaiFile` boundary.
- All seven package projects and fallback dependency properties are aligned on 4.2.7.
- No 4.2.7 tag or NuGet publication has been created; RAI retains the manual release gate.

## Coordinated release tooling

- `scripts/release-chain.sh` is the single coordinated release orchestrator.
- The enforced order is `OsLibCore → RaiUtils → RaiImage → RaiDiagram → JsonPit → ImgSeeder → PitSeeder`.
- Every package performs a package-only restore before its tag is created.
- The chain waits for both the exact `.nupkg` and exact-version NuGet registration document to return HTTP `200`; it does not use a fixed indexing delay.
- The umbrella label records the exact seven child commits before any package tag is created.

## Documentation state

- Package README links to Markdown documents use absolute GitHub URLs so they work from NuGet as well as GitHub.
- Foldable API references exist for OsLibCore, RaiUtils, RaiImage, JsonPit, and RaiDiagram.
- CR020 and coordinated 4.2.7 release notes are centralized under `doc/`.
- `scripts/check-markdown-document-links.sh` and its GitHub workflow reject new relative Markdown document links.

## Validation

- The full umbrella Release build succeeds.
- Current deterministic release suites pass: OsLibCore 117, RaiUtils 51, RaiImage 117, RaiDiagram 35, JsonPit 154, ImgSeeder 28, and PitSeeder 37 tests (539 total).
- RaiDiagram's passing suite includes the real local PlantUML integration path.
- The complete mixed `AfricanBrisket` image/diagram family, wildcard listing, sibling exclusion, rename, subscriber relocation, 3x3/8x2/Flat migration, indexed ItemIds, and short ItemIds with coincident physical convention homes are covered.
- The two Mzansi-backed JsonPit integration tests are not presently a code gate: read-only diagnosis found the remote OneDrive synchronizer inactive. The deterministic JsonPit suite remains green.
- The umbrella build still reports existing xUnit analyzer warnings in JsonPit concurrency tests; CR020 adds no compiler errors.

## Remaining 4.2.7 release preparation

- Pack and inspect all seven local 4.2.7 artifacts.
- Commit each child repository on `main`, then commit the exact seven updated submodule pointers and umbrella documents on `main`.
- RAI may then start `scripts/release-chain.sh 4.2.7` manually.
