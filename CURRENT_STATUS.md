# CURRENT_STATUS

Last updated: 2026-08-14

Current released package line: `4.1.0`

Upcoming coordinated package line: `4.2.0`

## Released 4.1.0 state

- The RAIkeep umbrella and all six established package repositories carry matching `v4.1.0` tags at their released commits.
- `OsLibCore`, `RaiUtils`, `RaiImage`, `JsonPit`, `ImgSeeder`, and `PitSeeder` `4.1.0` are visible through both NuGet's exact flat-container package and exact-version registration endpoints.
- CR008's TempDir validation, shared exception boundaries, and stream-free ingestion APIs are released.
- JsonPit's finalizer ownership regression is fixed while retaining the no-finalizer-I/O and no-finalizer-recovery-publication contract.
- ImgSeeder's package-only test graph no longer duplicates stale OsLibCore and RaiImage dependency versions.

## RaiDiagram 4.2.0 preparation

- `RaiDiagram` is a public standalone repository and a RAIkeep submodule: <https://github.com/Burkhardt/RaiDiagram>.
- The initial CR009 implementation provides JSON5 `.raid` manifests, semantic and presentation hashing, domain-neutral model-provider contracts, structured reconciliation, PlantUML compilation/rendering, and SVG provenance metadata.
- The repository includes the RAI logo, Apache-2.0 license, foldable `API.md`, 20 passing tests, and a tag-triggered NuGet trusted-publishing workflow.
- No RaiDiagram version tag or NuGet package has been published.

## Coordinated release tooling

- `scripts/release-chain.sh` is the single coordinated release orchestrator.
- The enforced order is `OsLibCore → RaiUtils → RaiImage → RaiDiagram → JsonPit → ImgSeeder → PitSeeder`.
- Every package performs a package-only restore before its tag is created.
- The chain waits for both the exact `.nupkg` and exact-version NuGet registration document to return HTTP `200`; it no longer uses a fixed indexing delay.
- The obsolete umbrella workflow that could publish a second chain independently has been removed.

## Documentation state

- Package README links to Markdown documents use absolute GitHub URLs so they work from NuGet as well as GitHub.
- Package READMEs use ordinary Markdown headings rather than raw `<details>` markup that NuGet displays poorly.
- Foldable API references exist for OsLibCore, RaiUtils, RaiImage, JsonPit, and RaiDiagram.
- `scripts/check-markdown-document-links.sh` and its GitHub workflow reject new relative Markdown document links.

## Validation

- The full umbrella Release build, including RaiDiagram, succeeds.
- RaiDiagram tests: 20 passed, 0 failed.
- Markdown link and whitespace validation passes across the umbrella and all seven child repositories.
- The umbrella build currently reports existing xUnit analyzer warnings in JsonPit concurrency tests; this release-tooling and documentation work adds no compiler errors.

## Remaining 4.2.0 release preparation

- Align all seven package versions and fallback dependencies on `4.2.0`.
- Configure RaiDiagram as a trusted publisher on NuGet.org before its first tag-triggered publication.
- Run the full relevant release test suites and package-only restore gates.
- Commit the exact seven child release pointers in the umbrella before RAI starts `scripts/release-chain.sh 4.2.0`.
