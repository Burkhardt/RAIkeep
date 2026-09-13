# CURRENT_STATUS

Last updated: 2026-09-12

Current released package line: `4.2.10`

Prepared coordinated package line: `4.3.0`

RAI intentionally skipped publication of the prepared v4.2.11 line. Its
accepted CR023 and CR024 work is carried into v4.3.0; no v4.2.11 package or
umbrella release was published.

## Coordinated 4.3.0 preparation

- Accepted CR023 renders PlantUML relationships with labels, cardinality, and
  discoverable fail-closed compiler vocabulary.
- Accepted CR024 removes each exact owned PID process flag on explicit
  `Pit.Dispose()` and finite `pits` exit after durability work. `Master.flag`,
  TTL, crash recovery, maintenance pruning, and I/O-free finalizers are unchanged.
- `--retain-window` remains a documented 4.x compatibility exception and is
  scheduled for removal in the next major release.
- Accepted CR025 adds typed UCD, RFD/OD, CD, AD, and SD builders in
  `RaiDiagram.Builders`, including `KlOneRoleDef`.
- `PlantUmlDiagramCompiler` remains pure managed C#, emits native syntax, and
  conditionally injects `allowmixing`. `IDiagramRenderer` remains an optional
  4.x server-side compatibility API.
- Diagram artifacts keep base `ItemId`, optional `ItemNumber`, and archetype
  `NameExt` separate. Names compose as `ItemId[_NN][_NameExt].ext`; cumulative
  ItemTree buckets derive only from base `ItemId`.
- `.raid`, `.puml`, `_config.puml`, and `.svg` siblings share one subscriber
  ItemTree home without arbitrary diagram-type directories.
- Real PlantUML 1.2026.8 syntax validation and SVG diagnostic detection cover
  every typed builder. AIA owns browser WASM/TeaVM execution tests.
- All seven package projects and fallback dependency properties align on 4.3.0.
- No v4.3.0 push, tag, GitHub label, workflow dispatch, or NuGet publication has
  occurred; RAI retains the manual release gate.

## Coordinated release tooling

- `scripts/release-chain.sh` is the single coordinated release orchestrator.
- The enforced order is `OsLibCore → RaiUtils → RaiImage → RaiDiagram → JsonPit → ImgSeeder → PitSeeder`.
- Every package performs a package-only restore before its tag is created.
- The chain waits for both the exact `.nupkg` and exact-version NuGet
  registration document to return HTTP `200`; it does not use a fixed delay.
- The umbrella label records the exact seven child commits before any package
  tag is created.

## Documentation state

- Every package README identifies 4.3.0 as its current prepared line and links
  to centralized release notes with absolute GitHub URLs.
- Foldable API references document each changed public library boundary.
- CR023 and CR024 record their move from unpublished 4.2.11 to 4.3.0; CR025
  records the corrected ItemId/ItemNumber/NameExt contract and manual gate.
- The v4.2.11 release-note records are explicitly marked superseded before publication.

## Validation

- The complete seven-package Release suite passes with zero skipped tests:
  OsLibCore 135, RaiUtils 51, RaiImage 122, RaiDiagram 48, JsonPit 176,
  ImgSeeder 33, and PitSeeder 44—609/609 total.
- RaiDiagram's 48-test suite runs the real, unpruned PlantUML 1.2026.8 CLI and
  verifies all five builders, relationship rendering, styles, artifact
  provenance, numbered naming, and error/warning diagnostics.
- JsonPit retains its live OneDrive/Mzansi split-master tests and the
  no-finalizer-I/O/path-reopenability regression.
- Seven local 4.3.0 packages restore successfully as a package-only graph.
  Package inspection confirms exact identities, dependency pins, package
  READMEs, and the `iorg`/`pits` tool entry points.

## 4.3.0 release readiness

- The implementations, tests, versions, fallback dependency pins, READMEs, API
  references, CR records, and coordinated release notes are complete.
- All package work is committed on local `main`; the umbrella commit records
  the exact seven prepared child revisions.
- RAI may start `scripts/release-chain.sh 4.3.0` manually. The release chain
  remains the only action that pushes, tags, labels, dispatches publishing
  workflows, or waits for NuGet availability.
