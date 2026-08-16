# RAIkeep 4.2.0 Release Notes

**Status:** Prepared source and verification candidate; not published
**Change request:** `CR009_AIA_to_RAIkeep_RaiDiagram_Package.md`

RAIkeep 4.2.0 introduces RaiDiagram and expands the coordinated chain from six
to seven package repositories while preserving the CR008 and JsonPit lifecycle
contracts released in 4.1.0.

## RaiDiagram

- Adds the public, domain-neutral RaiDiagram package and repository.
- Uses JSON5 `.raid` manifests to separate semantic model references,
  projection/filter intent, and visual presentation.
- Provides `IDiagramModelProvider`, model snapshots, structured reconciliation,
  and semantic/presentation hashes for agent-supported stale-diagram evaluation.
- Compiles role-first UML26 diagrams to PlantUML and renders through RaiImage.
- Embeds authoritative `.raid` identity, schema, and semantic hash provenance in
  generated SVG.
- Does not depend on AIA, WWWA, or JsonPit; AIA owns its provider implementation.

## Existing packages

- OsLibCore, RaiUtils, RaiImage, and JsonPit carry their 4.1.0 behavior forward
  on the coordinated 4.2.0 line.
- RaiImage and JsonPit now honor `UseLocalRAIkeepSources=false`, closing a release
  validation gap that could otherwise substitute sibling project sources.
- ImgSeeder and PitSeeder align fallback dependencies and CLI version output on
  4.2.0 without other CLI behavior changes.

## Release process

- The chain order is `OsLibCore → RaiUtils → RaiImage → RaiDiagram → JsonPit →
  ImgSeeder → PitSeeder`.
- Every package must pass a package-only restore before its tag is created.
- The orchestrator waits for both exact-package and exact-version NuGet
  visibility instead of sleeping for a fixed interval.
- RaiDiagram trusted publishing must be configured on NuGet.org before the chain
  reaches its first publication.

These notes do not authorize tagging or publication. RAI starts
`scripts/release-chain.sh 4.2.0` only after the prepared commits and validation
results are handed back.

## Verification result

- Focused JsonPit finalizer regression: 1 passed.
- Complete Release suites: OsLibCore 81, RaiUtils 22, RaiImage 97, RaiDiagram 20,
  JsonPit 146, ImgSeeder 15, and PitSeeder 20 tests passed.
- A disposable local NuGet feed restored and packed all seven 4.2.0 packages in
  release order with `UseLocalRAIkeepSources=false`; generated dependency
  metadata resolves the coordinated 4.2.0 package graph.
