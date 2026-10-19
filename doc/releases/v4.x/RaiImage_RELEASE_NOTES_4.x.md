# RaiImage Release Notes 4.x

## 4.5.11

- Release version: `4.5.11`
- Coordination tag: `v4.5.11`

### Highlights
- Coordinated 4.5.11 version alignment; no RaiImage behavior change.

### Coordinated Dependencies
- Aligned with RAIkeep synchronized `4.5.11` line.

---

## 4.5.10

- Release version: `4.5.10`
- Coordination tag: `v4.5.10`

### Highlights
- CR061 adds `ItemTreePath.SelectRenderedDerivatives` to locate exact derivative files (`*_{ImageNumber}_*.*`) for a given item and image number while preventing prefix overlap into multidigit sequences.

### Coordinated Dependencies
- Aligned with RAIkeep synchronized `4.5.10` line.

---

## 4.5.9

- Release version: `4.5.9`
- Coordination tag: `v4.5.9`

### Highlights
- CR060 keeps preceding numeric tokens in the PascalCase image stem and uses only the final separated number as ImageNumber.

### Coordinated Dependencies
- Aligned with RAIkeep synchronized `4.5.9` line.

---

## 4.5.8

- Release version: `4.5.8`
- Coordination tag: `v4.5.8`

### Highlights
- Adds `ImageMagickCommand.OverSsh(remoteTarget)` to route image conversion and processing commands to remote hosts over SSH while preserving the typed fluent surface.

### Coordinated Dependencies
- Aligned with RAIkeep synchronized `4.5.8` line.

---

## 4.5.7

- Release version: `4.5.7`
- Coordination tag: `v4.5.7`

### Highlights
- `ImageMagickCommand.OverSsh(target)` retains the ImageMagick-specific fluent type while dispatching through OsLib's SSH path.

### Coordinated Dependencies
- Aligned with RAIkeep synchronized `4.5.7` line.

---

## 4.5.6

- Release version: `4.5.6`
- Coordination tag: `v4.5.6`

### Highlights
<!-- LLM / Author: summarize key architectural highlights and changes here -->

### Coordinated Dependencies
- Aligned with RAIkeep synchronized `4.5.6` line.

---

## 4.5.5

- Release version: `4.5.5`
- Coordination tag: `v4.5.5`

### Highlights
CR054 separates terminal numeric/date tokens from PascalCase stems and uses D3 for Structured image numbers. Legacy retains D2. Existing paths are not automatically migrated; recompose and migrate references together. Diagram artifacts and ItemTreeTextFile also adopt D3 across every sibling; include numbered diagrams in migration.

### Coordinated Dependencies
- Aligned with RAIkeep synchronized `4.5.5` line.

---

## 4.5.4

Participates in the coordinated RAIkeep 4.5.4 patch release for the Amafu
`init --create-links` configuration-path fix. Package versions and applicable
internal dependency versions are aligned to 4.5.4. No runtime behavior changes
are introduced in RaiImage by this patch.

See [Amafu 4.5.4 release notes](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/Amafu_RELEASE_NOTES_4.x.md#454) for the fix and
configuration migration instructions.

---

## 4.5.3

Coordinated 4.5.3 release; runtime behavior is unchanged. Internal package dependencies, where present, align to 4.5.3.

Validation and release handoff: [RAIkeep 4.5.3](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/RAIkeep_RELEASE_NOTES_4.x.md#453). Preparation does not publish this package.

---

## 4.5.2

Coordinated 4.5.2 release; runtime behavior is unchanged. Internal package dependencies, where present, align to 4.5.2.

Validation and release handoff: [RAIkeep 4.5.2](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/RAIkeep_RELEASE_NOTES_4.x.md#452). Preparation does not publish this package.

---

## 4.5.0

Coordinated 4.5.0 dependency alignment; image behavior is unchanged.

All package and internal dependency versions are aligned to 4.5.0, coordinating live object reference semantics, sparse mutation tracking, and automated release validation gating across the entire RAIkeep platform.

Validation and release handoff: [RAIkeep 4.5.0](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/RAIkeep_RELEASE_NOTES_4.x.md#450). Preparation does not publish this package.

---

## 4.4.8

Coordinated 4.4.8 dependency alignment; image behavior is unchanged.

All package and internal dependency versions are aligned to 4.4.8. The version intentionally skips C# 4.4.7 to align the next coordinated release with jsonpit-python; Python implementation and publication remain with its maintainer.

Validation and release handoff: [RAIkeep 4.4.8](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/RAIkeep_RELEASE_NOTES_4.x.md#448). Preparation does not publish this package.

---

## 4.4.6

Adds selectable EXIF reads through ImageMagick and structured `ExifMetadata`: date/offset pairs become `DateTimeOffset`, related fields are grouped, and exact rational values are retained. ImageTree naming conventions remain unchanged.

This is part of the coordinated nine-package [CR049](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR/CR049_AIA_and_jsonpit_to_RAIkeep_Live-ID-Validation_and_Zip-Image-Import.md) release. Package versions and fallback dependencies align at 4.4.6.

See [RAIkeep release notes](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/RAIkeep_RELEASE_NOTES_4.x.md#446) for shared behavior, validation, and the manual publication gate.

---

## 4.4.5

RaiImage participates unchanged in the synchronized RAIkeep v4.4.5 release for accepted [`CR047_jsonpit_and_pits_Require-Existing-Patch-Flag-and-Seed-Commit-Count.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR/CR047_jsonpit_and_pits_Require-Existing-Patch-Flag-and-Seed-Commit-Count.md). Fallback dependencies align to OsLibCore and RaiUtils 4.4.5.

---

## 4.4.4

RaiImage participates unchanged in the synchronized RAIkeep v4.4.4 release for accepted [`CR044_AIA_and_jsonpit_to_RAIkeep_Auto-Detect-Cloud-Drives-and-Init-Config.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR/CR044_AIA_and_jsonpit_to_RAIkeep_Auto-Detect-Cloud-Drives-and-Init-Config.md). Fallback dependencies align to OsLibCore and RaiUtils 4.4.4.

---

## 4.4.3

RaiImage 4.4.3 participates unchanged in the synchronized eight-package
delivery of accepted
[`CR043_AfricaStage_to_RAIkeep_Improve-pits-seed-array-error-message.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR043_AfricaStage_to_RAIkeep_Improve-pits-seed-array-error-message.md).

ImageTree and ItemTree behavior remains unchanged. Fallback package references
align to OsLibCore 4.4.3 and RaiUtils 4.4.3.

---

## 4.4.2

RaiImage 4.4.2 participates unchanged in the synchronized eight-package
delivery of accepted
[`CR040_AIA_to_RAIkeep_and_jsonpit_Prohibit-Read-Modify-Write.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR040_AIA_to_RAIkeep_and_jsonpit_Prohibit-Read-Modify-Write.md)
and
[`CR041_jsonpit_to_RAIkeep_Restore-Clean-Change-Filenames.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR041_jsonpit_to_RAIkeep_Restore-Clean-Change-Filenames.md).

ImageTree and ItemTree behavior remains unchanged. Fallback package references
align to OsLibCore 4.4.2 and RaiUtils 4.4.2.

---

## 4.4.1

RaiImage 4.4.1 participates unchanged in the synchronized eight-package
delivery of accepted
[`CR037_AIA_to_RAIkeep_RaidSeeder_Diagram_Artifact_Management.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR037_AIA_to_RAIkeep_RaidSeeder_Diagram_Artifact_Management.md).
The coordinated release also carries accepted
[`CR037.1_AIA_to_RAIkeep_CLI_Global_Flag_and_Verb_Dispatch_Resilience.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR037.1_AIA_to_RAIkeep_CLI_Global_Flag_and_Verb_Dispatch_Resilience.md).

The established `ItemTreePath`, `ItemTreeTextFile`, `ImageTreeFile`, and
structured `ItemId[_NN][_NameExt]` conventions remain the storage foundation
used by RaiDiagram and RaidSeeder. Fallback dependencies align to 4.4.1.

---

## 4.4.0

RaiImage 4.4.0 participates unchanged in the synchronized eight-package
delivery of accepted
[`CR036_AIA_to_RAIkeep_Raid_CLI.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR036_AIA_to_RAIkeep_Raid_CLI.md).

Fallback dependencies align to OsLibCore and RaiUtils 4.4.0.

---

## 4.3.2

RaiImage 4.3.2 participates unchanged in the coordinated seven-package RAIkeep
v4.3.2 delivery of accepted
[CR027](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR027_AIA_to_RAIkeep_ClassDiagram_Generalization_and_SetSuperClass.md).
Its public API is unchanged from 4.3.1, and fallback dependencies align to
OsLibCore and RaiUtils 4.3.2. Publication remains behind RAI's manual
release-chain gate.

---

## 4.3.1

RaiImage 4.3.1 participates unchanged in the coordinated seven-package
RAIkeep v4.3.1 delivery of accepted
[CR026](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR026_AIA_to_RAIkeep_Diagram_Builder_Revision_Fidelity_and_Reference_Stereotypes.md).
Its public API is unchanged from 4.3.0, and fallback dependencies align to
OsLibCore and RaiUtils 4.3.1. Publication remains behind RAI's manual
release-chain gate.

---

## 4.3.0

RaiImage 4.3.0 supplies CR025's deterministic diagram-artifact storage contract.

- `ItemTreeTextFile` now exposes optional `ItemNumber`, symmetric with
  `ImageTreeFile.ImageNumber`.
- Base `ItemId`, optional `ItemNumber`, and archetype `NameExt` remain separate.
- Names compose as `ItemId[_NN][_NameExt].ext`; buckets use only `ItemId`.
- Public subscriber rendering overloads preserve those parts across `.puml`,
  `_config.puml`, and `.svg` siblings.
- The CR022 continuous-cloud-pathname invariant remains mandatory.

See [CR025](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR025_AIA_to_RAIkeep_Typed_Raid_Builders_and_Deterministic_ItemTree_Emission.md).
The unpublished 4.2.11 preparation is superseded. Publication remains behind
RAI's manual `scripts/release-chain.sh 4.3.0` gate.

---

## 4.2.11

> **Superseded before publication.** This prepared package line was not released;
> its changes are carried into v4.3.0.

RaiImage participates unchanged in the coordinated RAIkeep 4.2.11 release. Its
image, ItemTree, Unicode, rendering-command, and cloud-safe mutation behavior
remain unchanged while fallback dependencies align to 4.2.11.

---

## 4.2.10

RaiImage participates unchanged in the coordinated RAIkeep 4.2.10 release. Its
image, ItemTree, Unicode, and cloud-safe mutation behavior remains unchanged
while fallback dependencies align to `OsLibCore 4.2.10` and `RaiUtils 4.2.10`.

---

## 4.2.9

RaiImage 4.2.9 implements its part of accepted
[CR022](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR022_RAI_to_RAIkeep_Cloud_Safe_In_Place_Filesystem_Invariant.md).

- `ImageMagick.JpegTran` no longer moves an established image into `Os.TempDir`.
- The external tool receives isolated temporary input and output paths.
- A successful result is copied into the continuously present destination path;
  a failed invocation leaves the original bytes and pathname unchanged.
- Regression tests exercise success and failure against a real configured
  CloudDrive and verify that no delete or rename event occurs at the image path.

Fallback dependencies align to `OsLibCore 4.2.9` and `RaiUtils 4.2.9`.

---

## 4.2.8

RaiImage participates unchanged in the coordinated RAIkeep 4.2.8 release for
accepted [CR021](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR021_RAI_to_RAIkeep_JsonPit_Durable_Cleanup_Receipts_and_Pits_Coordination.md).
Fallback dependencies align to `OsLibCore 4.2.8` and `RaiUtils 4.2.8`; image and
ItemTree behavior remains unchanged from 4.2.7.

---

## 4.2.7

Implements the shared item-file architecture adopted with accepted
[CR020](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR020_RAI_to_RAIkeep_Iorg_Read_Only_Wildcard_Listing.md).

- Makes `ItemTreePath` the tree home of one subscriber-local ItemId and all of its files.
- Adds `ItemTreePath.SelectFiles()` for exact-ItemId selection across images, SVG, PUML, config PUML, and RAID files while excluding bucket siblings.
- Adds destination-oriented `ItemTreePath.mv(source)` for complete-family relocation, ItemId rename, subscriber move, and path-convention migration.
- Preflights collisions, attempts rollback on partial failure, and prunes empty vacated buckets.
- Adds `PathConventionType.Flat` support alongside canonical, 3x3, and 8x2 placement.
- Renames the non-image tree text type to `ItemTreeTextFile`.
- Replaces procedural `ImageTreeFile.From...` construction with constructors accepting `ItemTreePath` and fluent `SelectFirstExistingFile(...)` image resolution.
- Covers the complete `AfricanBrisket` mixed-file example, sibling exclusion, subscriber relocation, rename, and 8x2/3x3/Flat migrations.

Tagging and NuGet publication remain behind RAI's manual release gate.

---

## 4.2.6

Adopts the accepted CR019 package-boundary correction in the coordinated
RAIkeep 4.2.6 release.

- Consumes word-case conversion and splitting from RaiUtils.
- Removes the independent word-case implementation from RaiImage.
- Retains `RaiImage.WordCase` and ordinary static `RaiImage.StringHelper`
  compatibility facades for callers compiled against earlier package lines.
- Keeps legacy facade methods out of extension-method discovery, preventing
  ambiguous calls when `RaiImage` and `RaiUtils` are both imported.
- Aligns fallback dependencies on `OsLibCore 4.2.6` and `RaiUtils 4.2.6`.

---

## 4.2.5

Coordinated dependency release for accepted CR017.

- Aligns fallback dependencies on OsLibCore and RaiUtils 4.2.5.
- Carries CR016 Unicode normalization, grapheme-safe bucketing, and resilient
  legacy lookup forward unchanged.

Release verification: 119 RaiImage Release tests passed.

RAI retains the manual coordinated release gate; no tag or publication is
authorized by these notes.

---

## 4.2.4

Implements accepted CR016 Unicode normalization in multi-level ImageTree
bucketing and lookup.

- Normalizes ImageTree-owned subscriber names, item ids, templates, filenames,
  route values, and typed text artifacts to Unicode NFC.
- Preserves caller-provided ImageTree root paths.
- Calculates 3x3, 8x2, and canonical-name prefixes by Unicode text elements.
- Prevents bucket slicing through combining sequences, surrogate pairs, or
  multi-code-point emoji clusters.
- Resolves legacy NFC, NFD, and mixed-normalization directories and source files
  one segment at a time through `RaiPath` and `RaiFile` enumeration.
- Preserves the resolved physical legacy source path for reading while new
  derived outputs retain canonical placement.
- Rejects ambiguous canonically equivalent matches with
  `RaiImageIOException`.
- Includes SVG in `DefaultSourceExtensions`.
- Aligns fallback dependencies on OsLibCore and RaiUtils 4.2.4.

Release verification: all 119 RaiImage Release tests passed. Fifteen dedicated
CR016 cases cover German umlauts; Portuguese `ã`, `é`, and `ç`; an African
orthography combining sequence; mixed legacy trees; every path convention; and
Unicode text-element boundaries.

RAI retains the manual coordinated release gate; no tag or publication is
authorized by these notes.

---

## 4.2.3

Coordinated dependency release for accepted CR015.

- Aligns fallback dependencies on OsLibCore and RaiUtils 4.2.3.
- Carries the CR010 subscriber-scoped artifact boundary and CR014 typed image
  tool wrappers forward unchanged.
- Introduces no image behavior or identity-management change.

RAI retains the manual coordinated release gate; no tag or publication is
authorized by these notes.

Release verification: 104 RaiImage Release tests passed.

---

## 4.2.2

Coordinated patch release implementing the RaiImage portion of accepted
`CR010_AfricaStage_to_RAIkeep_RaiDiagram_Subscriber_Scoped_Artifacts_and_Styles.md`
and carrying accepted CR008 forward.

It also implements the RaiImage tool-boundary portion of accepted
`CR014_RAI_to_RAIkeep_Typed_CLI_Command_Wrappers.md`.

- Adds `ImageTreeTextFile`, a truthful OsLib `TextFile` placed with the existing
  subscriber root, item id, `ItemTreePath`, and `PathConventionType` contract.
- Keeps `.raid`, `.puml`, and `_config.puml` text artifacts in the same item
  bucket as SVG, PNG, WebP, and JPEG images without treating text as an image.
- Represents resolved configuration with `NameExt = "config"` and
  `Ext = "puml"`, producing names such as `ScheduleRehearsal_config.puml`.
- Extends the PlantUML boundary with local `-config` injection and typed
  source/config result handles while retaining the 4.2.0 compatibility handles.
- Aligns fallback dependencies on OsLibCore and RaiUtils 4.2.2.
- Routes all ImageMagick facade calls through `ImageMagickCommand` and adds
  public `OptiPngCommand` and `JpegTranCommand` wrappers.
- Passes optimizer paths/options as discrete process tokens and retains
  synchronous/asynchronous `RaiSystemResult` output and exit-code behavior.
- Confirms PlantUML remains behind `PlantUmlCommand`, including the deliberate
  headless `java -jar` launch owned inside that wrapper.

No identity-management abstraction or direct theme download was introduced.

Released as part of the coordinated RAIkeep v4.2.2 release.

Release verification: 104 RaiImage Release tests passed in one run, including
the real ImageMagick transparency integration.

---

## 4.2.0

Coordinated release supporting approved
`CR009_AIA_to_RAIkeep_RaiDiagram_Package.md`.

- Supplies RaiDiagram's supported PlantUML rendering and image-artifact boundary.
- Keeps `RaiImageIOException`, `RaiImageNotFoundException`,
  `RaiPathNotFoundException`, and `ToolNotFoundException` distinctions intact.
- Keeps asynchronous byte-chunk ingestion available without exposing a stream
  boundary to consumers.
- Aligns fallback dependencies on OsLibCore and RaiUtils 4.2.0.
- Makes `UseLocalRAIkeepSources=false` force package references, so the release
  gate cannot silently substitute sibling project sources.

The public RaiImage behavior introduced in 4.1.0 remains compatible.

Release verification: 97 RaiImage Release tests passed.

---

## 4.1.0

Implements the RaiImage portion of
`CR008_AIA_to_RAIkeep_OsLib_RaiImage_Boundary_Enhancements.md`.

- Adds `RaiImageIOException` and `RaiImageNotFoundException`.
- Missing lookup directories throw `RaiPathNotFoundException`; missing images in
  an existing lookup location throw `RaiImageNotFoundException`.
- Missing ImageMagick and PlantUML executables throw `ToolNotFoundException`
  instead of `System.IO.FileNotFoundException`.
- Image files accept asynchronous byte chunks through inherited
  `WriteFromAsync(IAsyncEnumerable<byte[]>, CancellationToken)`.
- The originally requested `RaiImageFileNotFoundException` name was deliberately
  refined during acceptance to distinguish missing paths from missing images.

Release verification: 97 RaiImage Release tests passed.

---

## 4.0.1

**Date:** 2026-08-10
**Author / Delivering Agent:** RAIkeep Dev Agent
**Delivered Version:** v4.0.1
**Target Consumers:** RAIkeep package family, AfricaStage, AIA
**Status:** Prepared — publication approval pending

### 1. Summary

RaiImage v4.0.1 is the synchronized image-library package for the coordinated
CR006 CLI patch line. It contains no RaiImage API or behavior change from
v4.0.0.

### 2. Resolved Change Requests (CRs)

- [`CR006_AfricaStage_to_RAIkeep_CliSubcommands.md`](https://github.com/Burkhardt/AIA/blob/main/doc/CR006_AfricaStage_to_RAIkeep_CliSubcommands.md) — synchronized package participation only; CLI implementation is owned by ImgSeeder and PitSeeder.

### 3. Root Cause Analysis & Technical Resolution

RaiImage moves to v4.0.1 and aligns fallback dependencies on OsLibCore and
RaiUtils v4.0.1. No RaiImage source behavior changed.

### 4. Public Contract & API / Package Changes

- Package version: `4.0.1`.
- Fallback dependencies: OsLibCore `4.0.1`, RaiUtils `4.0.1`.
- Public API and runtime behavior: unchanged from `4.0.0`.

### 5. Validation & Acceptance Evidence

- RaiImage.Tests: **94 passed, 0 failed, 0 skipped** in the coordinated run.

### 6. Upgrade & Consumption Instructions

Consume RaiImage v4.0.1 with the other five coordinated RAIkeep v4.0.1 packages.

---

## 4.0.0

### Summary

`RaiImage 4.0.0` aligns RaiImage with `OsLibCore 4.0.0` and `RaiUtils 4.0.0` while carrying forward the current image-tree and PlantUML feature set.

### Changes

- Updated package version, release metadata, and fallback dependency pins to the coordinated `4.0.0` line.
- Updated the `ImageTreeFile.FromName(...)` acceptance-test reference to the centralized resolved CR in the RAIkeep `doc/` directory.
- Refreshed README/API documentation and the maintained PlantUML diagrams for the current release line.
- Carries forward `ImageTreeFile.RenderPlantUml(...)`, `PlantUmlCommand`, `PlantUml`, and `PlantUmlRenderResult`.
- Carries forward `WordCase` as the supported replacement for the retired `CamelCase` helper.

### Compatibility

- No RaiImage production API or runtime behavior changed from `3.13.0`.
- Existing image-tree naming and PlantUML rendering behavior remain unchanged.

### Validation

- `RaiImage.Tests`: `94` passed, `0` failed in the coordinated validation run.
- The umbrella `RAIkeep.slnx` build succeeds with the local `4.0.0` dependencies.

### Release sequencing

`RaiImage` is third in the coordinated release chain. Its GitHub push/tag must wait for RaiUtils workflow success, flat-container visibility, and the full `330`-second hold. `JsonPit` must wait for the same checks after RaiImage publishes.
