# RAIkeep 4.2.2 Release Notes

**Status:** Prepared source and verification candidate; not published
**Accepted requests:**
`CR008_AIA_to_RAIkeep_OsLib_RaiImage_Boundary_Enhancements.md`,
`CR009_AIA_to_RAIkeep_RaiDiagram_Package.md`, and
`CR010_AfricaStage_to_RAIkeep_RaiDiagram_Subscriber_Scoped_Artifacts_and_Styles.md`,
and `CR014_RAI_to_RAIkeep_Typed_CLI_Command_Wrappers.md`, including the
accepted `CR014.1_test-concept.md` guidance

RAIkeep 4.2.2 realigns all seven packages after the two CLI-only 4.2.1 releases,
implements CR010, and completes the AIA-reported CR008/CR009 patch gaps.
It also implements CR014 without adding an eighth package or duplicating the
package-owned PitSeeder and ImgSeeder test responsibilities.

## Boundary changes

- OsLibCore exposes `RaiFileIOException` and wraps OS file I/O failures from
  `RaiFile.ReadAllBytesAsync(...)` without wrapping cancellation.
- RaiDiagram publicly exposes `DiagramModel.FromManifest(...)` and
  `DiagramDestination.CreateSubscriberRoot()` for AIA consumers.
- RaiImage and RaiDiagram store typed text and rendered image artifacts in one
  subscriber-local `ItemTreePath` bucket.
- RaiDiagram resolves deterministic local PlantUML themes/styles from explicit
  subscriber locations and injects the exact `_config.puml` through `-config`.
- SVG provenance identifies the authoritative `.raid`, semantic/config/render
  hashes, and exact ordered style layers.
- Subscriber remains a storage-routing segment; no RAIkeep identity-management
  or authorization subsystem is introduced.
- OsLibCore exposes typed `PitsCommand` and `IorgCommand` request/option APIs
  for preferred 4.x commands, installed executables, and managed CLI assemblies.
- Tokenized execution preserves exact argument values for server calls and
  validates mandatory/mutually exclusive parameters before process start.
- Process results expose the exact argument vector and distinguish successful
  CLI completion, nonzero CLI exit, timeout, cancellation, and start failure.
- RaiImage owns typed ImageMagick, PlantUML, OptiPNG, and JPEGTran wrappers;
  production image/diagram operations no longer hand-build those tool calls.

## Compatibility and carried behavior

- JsonPit retains the no-finalizer-I/O recovery contract and weak registry
  cleanup that makes abandoned canonical paths reopenable.
- ImgSeeder and PitSeeder retain their 4.2.1 Nerd Font help improvements.
- ImgSeeder and PitSeeder continue testing their own CLI behavior and provide
  minimal real-CLI wrapper smoke checks; OsLib tests wrapper validation,
  forwarding, result capture, timeout, cancellation, and launch failures.
- Package-only restore validation remains mandatory before every release tag.

## Release process

RAI manually starts `scripts/release-chain.sh 4.2.2` after all seven prepared
child commits and their exact umbrella submodule pointers are committed. The
script publishes in dependency order and waits for exact NuGet visibility.

These notes do not authorize tagging or publication.

## Verification result

- Focused CR008 `RaiFileIOException` tests: 3 passed.
- Focused CR014/CR014.1 wrapper-contract tests: 21 passed.
- Focused JsonPit finalizer regression: 1 passed.
- Complete Release suites: OsLibCore 104, RaiUtils 22, RaiImage 104,
  RaiDiagram 34, JsonPit 146, ImgSeeder 16, and PitSeeder 20 tests passed.
- Seven freshly packed 4.2.2 artifacts passed downstream package-only restore
  and pack validation with local project substitution disabled.
- All four real RaiDiagram renderer tests passed locally. They are categorized
  as `PlantUMLIntegration` and skip with an explicit diagnostic in environments
  without a complete PlantUML/Graphviz installation; the other 30 RaiDiagram
  tests remain mandatory. `RAIDIAGRAM_REQUIRE_REAL_PLANTUML=1` restores a hard
  external-tool gate where desired.
