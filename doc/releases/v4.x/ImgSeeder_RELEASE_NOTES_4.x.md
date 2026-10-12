# ImgSeeder Release Notes 4.x

## 4.5.10

- Release version: `4.5.10`
- Coordination tag: `v4.5.10`

### Highlights
- CR061 implements idempotent image import semantics for `iorg organize`: unchanged destination files are skipped without rewrite, existing images with differing content are replaced in-place, exact derivative cache entries are invalidated, and `ReceiptVersion: 3` tracks `Updated` counts and compact ranges. Collision errors are preserved for intra-archive stem/number collisions.

### Coordinated Dependencies
- Aligned with RAIkeep synchronized `4.5.10` line.

---

## 4.5.9

- Release version: `4.5.9`
- Coordination tag: `v4.5.9`

### Highlights
- CR060 adds optional import IDs, `-s` for source, `-o`/`--out`/`--receipt` for receipt files, and `-i`/`--image` filtering for list and clean.
- GettingStarted.md documents the image import workflow independently of pits and jpit.

### Coordinated Dependencies
- Aligned with RAIkeep synchronized `4.5.9` line.

---

## 4.5.8

- Release version: `4.5.8`
- Coordination tag: `v4.5.8`

### Highlights
- Coordinated release aligned with the 4.5.8 synchronized platform line.
- Tab indentation formatting alignment conforming to RAI010.

### Coordinated Dependencies
- Aligned with RAIkeep synchronized `4.5.8` line.

---

## 4.5.7

- Release version: `4.5.7`
- Coordination tag: `v4.5.7`

### Highlights
- Coordinated with the 4.5.7 platform line; no package-local behavior changes.

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
CR054 adds ReceiptVersion 2: contiguous ranges, mixed Ranges, sparse Exceptions, and detailed Files only when --exif is explicitly requested. Receipts no longer serialize top-level lifecycle Status. ZIP preflight, direct final writes, live-ID validation, and cleanup remain in place.

### Coordinated Dependencies
- Aligned with RAIkeep synchronized `4.5.5` line.

---

## 4.5.4

Participates in the coordinated RAIkeep 4.5.4 patch release for the Amafu
`init --create-links` configuration-path fix. Package versions and applicable
internal dependency versions are aligned to 4.5.4. No runtime behavior changes
are introduced in ImgSeeder by this patch.

See [Amafu 4.5.4 release notes](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/Amafu_RELEASE_NOTES_4.x.md#454) for the fix and
configuration migration instructions.

---

## 4.5.3

Coordinated 4.5.3 release aligning CLI and package dependencies with OsLibCore, RaiUtils, RaiImage, and JsonPit 4.5.3. Public commands and image-organization behavior are unchanged.

Validation and release handoff: [RAIkeep 4.5.3](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/RAIkeep_RELEASE_NOTES_4.x.md#453). Preparation does not publish this package.

---

## 4.5.2

Coordinated 4.5.2 release; runtime behavior is unchanged. Internal package dependencies, where present, align to 4.5.2.

Validation and release handoff: [RAIkeep 4.5.2](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/RAIkeep_RELEASE_NOTES_4.x.md#452). Preparation does not publish this package.

---

## 4.5.0

Coordinated 4.5.0 dependencies including JsonPit live references; iorg reports version 4.5.0.

ZIP ingestion, structured EXIF output, ImageImport receipts, and image naming retain their existing behavior.

All package and internal dependency versions are aligned to 4.5.0, coordinating live object reference semantics, sparse mutation tracking, and automated release validation gating across the entire RAIkeep platform.

Validation and release handoff: [RAIkeep 4.5.0](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/RAIkeep_RELEASE_NOTES_4.x.md#450). Preparation does not publish this package.

---

## 4.4.8

Coordinated 4.4.8 dependencies including JsonPit live references; iorg reports version 4.4.8.

ZIP ingestion, structured EXIF output, ImageImport receipts, and image naming retain their existing behavior.

All package and internal dependency versions are aligned to 4.4.8. The version intentionally skips C# 4.4.7 to align the next coordinated release with jsonpit-python; Python implementation and publication remain with its maintainer.

Validation and release handoff: [RAIkeep 4.4.8](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/RAIkeep_RELEASE_NOTES_4.x.md#448). Preparation does not publish this package.

---

## 4.4.6

ImgSeeder (`iorg`) v4.4.6 fulfills **Deliverable B** of [CR049](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR/CR049_AIA_and_jsonpit_to_RAIkeep_Live-ID-Validation_and_Zip-Image-Import.md) (*ZIP Image Ingestion and JSON Receipts*), implementing automated media ingestion, machine-readable receipt emission, asynchronous native decompression, and structured EXIF inspection.

### 1. Fulfillment of CR049 Deliverable B: ZIP Archive Ingestion (`iorg organize`)

- **Local & HTTPS Ingestion (B01, B05):** Ingests photo collections directly from local `.zip` files (`--source`) or HTTPS URLs (`--source-url`) into designated tenants and ImageTree structures.
- **Path-Traversal Defense (B02):** Rejects any archive containing path traversal sequences (`..`), absolute paths, or symbolic links during archive preflight before extracting any files.
- **Non-Silent Collision Defense (B03):** Compares candidate targets against existing files. Identical bytes are marked `Unchanged`; differing content generates a collision error. Files are never silently overwritten.
- **Asynchronous Native Extraction:** On macOS and Linux/Ubuntu, decompression is dispatched to the native `unzip` tool asynchronously through `OsLib` (`RaiSystem`), executing into OS temporary storage without blocking caller threads.
- **Preserved Archives:** The source ZIP archive remains untouched after ingestion.

### 2. Authoritative `Class: "ImageImport"` Receipts (B04, B06)

- **Machine-Readable JSON Output:** When `--json` is specified, `iorg organize` outputs strictly valid JSON on `stdout` (with logging and diagnostics sent to `stderr`).
- **Complete Ingestion Manifest:** The receipt documents overall status (`Completed`, `Partial`, `Failed`), summary counts (`Copied`, `Unchanged`, `Skipped`, `Failed`), source metadata, and per-file mappings:
  - Source entry path in the archive
  - Derived entity identity (`ItemId`)
  - Target relative path within `ItemIdTree8x2`
  - Extracted EXIF metadata and final copy status
- **Piped JsonPit Ingestion (CR049 Deliverable C):** Receipts can be piped directly into `pits seed` or `jpit` via standard input (`--source -`).

### 3. Structured EXIF Metadata Extraction

- **Selective & Comprehensive Selectors:** Supports `--exif '*'` or specific tag/group selectors across both `iorg list` and `iorg organize`.
- **Typed DateTimeOffset:** Embedded date and offset pairs are normalized to ISO-8601 `DateTimeOffset`.
- **Field Grouping & Exact Rationals:** Exposure, lens, focal plane, and camera settings are grouped into structured properties while retaining exact rational values.

### 4. Cloud-Safe CR022 Placement

- All final image writes occur in-place on the destination drive, strictly observing CR022 rules against moving temporary files across volume boundaries into cloud folders.

---

**Traceability:** This release formally closes Deliverable B of [CR049](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR/CR049_AIA_and_jsonpit_to_RAIkeep_Live-ID-Validation_and_Zip-Image-Import.md). See [PitSeeder release notes](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/PitSeeder_RELEASE_NOTES_4.x.md#446) and [RAIkeep release notes](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/RAIkeep_RELEASE_NOTES_4.x.md#446) for platform coordination.

---

## 4.4.5

ImgSeeder participates unchanged in the synchronized RAIkeep v4.4.5 release for accepted [`CR047_jsonpit_and_pits_Require-Existing-Patch-Flag-and-Seed-Commit-Count.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR/CR047_jsonpit_and_pits_Require-Existing-Patch-Flag-and-Seed-Commit-Count.md). The `iorg` command and its cloud-safe ImageTree operations remain unchanged.

---

## 4.4.4

ImgSeeder participates unchanged in the synchronized RAIkeep v4.4.4 release for accepted [`CR044_AIA_and_jsonpit_to_RAIkeep_Auto-Detect-Cloud-Drives-and-Init-Config.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR/CR044_AIA_and_jsonpit_to_RAIkeep_Auto-Detect-Cloud-Drives-and-Init-Config.md). The `iorg` command and its cloud-safe ImageTree operations remain unchanged.

---

## 4.4.3

ImgSeeder and `iorg` 4.4.3 participate unchanged in the synchronized
eight-package delivery of accepted
[`CR043_AfricaStage_to_RAIkeep_Improve-pits-seed-array-error-message.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR043_AfricaStage_to_RAIkeep_Improve-pits-seed-array-error-message.md).

Image organization and ItemTree operations remain unchanged. Fallback package
dependencies and CLI version output align to 4.4.3.

---

## 4.4.2

ImgSeeder and `iorg` 4.4.2 participate unchanged in the synchronized
eight-package delivery of accepted
[`CR040_AIA_to_RAIkeep_and_jsonpit_Prohibit-Read-Modify-Write.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR040_AIA_to_RAIkeep_and_jsonpit_Prohibit-Read-Modify-Write.md)
and
[`CR041_jsonpit_to_RAIkeep_Restore-Clean-Change-Filenames.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR041_jsonpit_to_RAIkeep_Restore-Clean-Change-Filenames.md).

Image organization and ItemTree operations remain unchanged. Fallback package
dependencies and CLI version output align to 4.4.2.

---

## 4.4.1

ImgSeeder and `iorg` 4.4.1 participate in the synchronized eight-package
delivery of accepted
[`CR037_AIA_to_RAIkeep_RaidSeeder_Diagram_Artifact_Management.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR037_AIA_to_RAIkeep_RaidSeeder_Diagram_Artifact_Management.md).
They implement accepted
[`CR037.1_AIA_to_RAIkeep_CLI_Global_Flag_and_Verb_Dispatch_Resilience.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR037.1_AIA_to_RAIkeep_CLI_Global_Flag_and_Verb_Dispatch_Resilience.md).

Existing image discovery, movement, organization, cleanup, and ItemTree
addressing remain intact. Fallback dependencies and CLI version output align to
4.4.1. A misplaced reserved verb now exits `2` with an actionable command-first
correction before ImageTree access, and version flags take immediate precedence.

---

## 4.4.0

ImgSeeder and `iorg` 4.4.0 participate unchanged in the synchronized
eight-package delivery of accepted
[`CR036_AIA_to_RAIkeep_Raid_CLI.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR036_AIA_to_RAIkeep_Raid_CLI.md).

Fallback dependencies and CLI version output align to 4.4.0.

---

## 4.3.2

ImgSeeder and `iorg` 4.3.2 participate unchanged in the coordinated
seven-package RAIkeep v4.3.2 delivery of accepted
[CR027](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR027_AIA_to_RAIkeep_ClassDiagram_Generalization_and_SetSuperClass.md).
Fallback dependency and CLI versions align on 4.3.2. Publication remains behind
RAI's manual release-chain gate.

---

## 4.3.1

ImgSeeder and `iorg` 4.3.1 participate unchanged in the coordinated
seven-package RAIkeep v4.3.1 delivery of accepted
[CR026](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR026_AIA_to_RAIkeep_Diagram_Builder_Revision_Fidelity_and_Reference_Stereotypes.md).
Fallback dependency and CLI versions align on 4.3.1. Publication remains behind
RAI's manual release-chain gate.

---

## 4.3.0

ImgSeeder and `iorg` 4.3.0 participate in the coordinated CR023, CR024, and
CR025 package line. CLI behavior is unchanged from 4.2.10; dependency and tool
versions align on 4.3.0. The unpublished 4.2.11 preparation is superseded.
Publication remains behind RAI's manual release gate.

---

## 4.2.11

> **Superseded before publication.** This prepared package line was not released;
> its changes are carried into v4.3.0.

ImgSeeder participates unchanged in the coordinated RAIkeep 4.2.11 release.
Its `iorg` behavior remains unchanged from 4.2.10 while fallback dependencies
align to the 4.2.11 package line.

---

## 4.2.10

ImgSeeder 4.2.10 improves `iorg` root and tenant addressing.

- Adds `-a, --app` for an application root; iorg appends the conventional
  `Image` segment.
- Adds preferred `-t, --tenant`; `--subscriber` remains a compatibility alias.
- Retains `-r, --root` for an exact ImageTree root. Root and app are mutually
  exclusive, and app-root addressing requires an explicit tenant.
- Corrects the tenant help-row alignment and shows the unnamed-subscriber
  compatibility explanation only when that legacy form was actually used.
- Command synopses consistently show `[(-t|--tenant) <name>]` and
  `[(-p|--pathconv) <1|2|3|4>]` where applicable.

Regression coverage proves that `--app AIA --tenant nomsa` resolves the same
tree as the corresponding exact `--root AIA/Image/nomsa` form.

---

## 4.2.9

ImgSeeder 4.2.9 implements its part of accepted
[CR022](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR022_RAI_to_RAIkeep_Cloud_Safe_In_Place_Filesystem_Invariant.md).

- `iorg organize` no longer creates a subscriber staging tree in `Os.TempDir`.
- Each source image is copied directly to its final ItemTree path through the
  `RaiFile` boundary.
- The retained `tempRoot` API parameter is inert for binary and source
  compatibility; tests prove that it is never materialized.
- Configured-cloud regression coverage verifies direct final-path creation and
  preservation of the source file.

Fallback dependencies align to 4.2.9 and the CLI reports `iorg v4.2.9`.

---

## 4.2.8

ImgSeeder participates unchanged in the coordinated RAIkeep 4.2.8 release for
accepted [CR021](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR021_RAI_to_RAIkeep_JsonPit_Durable_Cleanup_Receipts_and_Pits_Coordination.md).
Fallback dependencies align to 4.2.8; existing `iorg` organize, list, move, and
clean behavior remains unchanged. The CLI reports `iorg v4.2.8`.

---

## 4.2.7

Implements the `iorg` media and diagram tree custodianship requested by accepted
[CR020](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR020_RAI_to_RAIkeep_Iorg_Read_Only_Wildcard_Listing.md).

- Adds read-only `iorg list <FileNamePattern>` discovery across supported image, `.puml`, and `.raid` files.
- Adds `iorg move <SourceItemId> [TargetItemId]` for exact-family relocation, optional rename, and convention migration.
- Adds Flat as path-convention option 4 while retaining 8x2 as option 3/default.
- Makes `iorg clean <ItemId> --force` remove the complete exact item family; dry run remains the default.
- Makes `iorg clean --cache` explicitly remove rendered derivatives while preserving source images and diagram artifacts.
- Removes the misleading Legacy row from root help; `-r` remains supported as the short spelling of `--root`.
- Tests the complete `AfricanBrisket` image/diagram family and proves `AfricanBrigadine` remains untouched in a shared bucket.

Tagging and NuGet publication remain behind RAI's manual release gate.

---

## 4.2.6

Coordinated dependency release for accepted CR019. `iorg` adopts the complete
4.2.6 package line; CLI behavior is unchanged from 4.2.5.

---

## 4.2.5

Coordinated dependency release for accepted CR017.

- Aligns fallback dependencies on JsonPit, OsLibCore, RaiUtils, and RaiImage
  4.2.5.
- Keeps `iorg` behavior and Nerd Font help output unchanged.
- Reports `iorg v4.2.5` through the CLI version boundary.

Release verification: 16 ImgSeeder Release tests passed.

RAI retains the manual coordinated release gate; no tag or publication is
authorized by these notes.

---

## 4.2.4

Coordinated dependency release for accepted CR016.

- Aligns fallback dependencies on JsonPit, OsLibCore, RaiUtils, and RaiImage
  4.2.4.
- `iorg` ImageTree destinations inherit RaiImage's NFC logical names, Unicode
  text-element bucketing, and legacy normalization compatibility.
- CLI syntax and Nerd Font help behavior remain unchanged.
- Reports `iorg v4.2.4` through the CLI version boundary.

Release verification: 16 ImgSeeder Release tests passed.

RAI retains the manual coordinated release gate; no tag or publication is
authorized by these notes.

---

## 4.2.3

Coordinated dependency release for accepted CR015.

- Aligns fallback dependencies on JsonPit, OsLibCore, RaiUtils, and RaiImage
  4.2.3.
- Retains the `iorg` command surface, Nerd Font guidance, and CR014 typed wrapper
  smoke boundary unchanged.
- Reports `iorg v4.2.3` through the CLI version boundary.

RAI retains the manual coordinated release gate; no tag or publication is
authorized by these notes.

Release verification: 16 ImgSeeder Release tests passed.

---

## 4.2.2

Coordinated dependency release for the seven-package RAIkeep 4.2.2 line.

- Aligns fallback dependencies on JsonPit, OsLibCore, RaiUtils, and RaiImage
  4.2.2.
- Retains the 4.2.1 Nerd Font provider and numbered-option glyphs, corrected
  help alignment, Blink stylesheet guidance, and clipping tolerance.
- Retains the command-first and compatible 4.x legacy `iorg` behavior.
- Reports `iorg v4.2.2` through the CLI version boundary.
- Its package-owned entry-point tests invoke the managed CLI through
  `OsLib.IorgCommand.ForManagedAssembly(...)`; its `--version` case is the
  CR014.1 real-CLI smoke check. OsLib tests the transport contract and does not
  duplicate image-organization behavior.

Released as part of the coordinated RAIkeep v4.2.2 release.

Release verification: 16 ImgSeeder Release tests passed.

---

## 4.2.1

CLI-only maintenance release based on the published RAIkeep 4.2.0 libraries.

- Uses cloud-provider initials and numbered-option glyphs that are embedded in
  `JetBrainsMonoNLNerdFontPropo-Regular`, avoiding fallback-font width
  differences in help output.
- Corrects contextual option-description alignment.
- Reserves two terminal cells at the end of help lines to tolerate proportional
  Nerd Font metrics and renderers such as Blink.
- Reports `iorg v4.2.1` through the CLI version boundary.

Package dependencies remain `JsonPit 4.2.0`, `OsLibCore 4.2.0`,
`RaiUtils 4.2.0`, and `RaiImage 4.2.0`. No library package or umbrella version is
changed by this release.

Release verification: 16 ImgSeeder Release tests passed, and the package-only
build and package metadata were verified against the published 4.2.0
dependencies.

---

## 4.2.0

Coordinated dependency release for the seven-package RAIkeep 4.2 line.

- Aligns fallback package dependencies on JsonPit, OsLibCore, RaiUtils, and
  RaiImage 4.2.0.
- Retains the command-first and compatible 4.x legacy `iorg` behavior.
- Reports `iorg v4.2.0` through the CLI version boundary.

No other ImgSeeder CLI behavior change is introduced after 4.1.0.

Release verification: 15 ImgSeeder Release tests passed.

---

## 4.1.0

Coordinated dependency release for the CR008 RAIkeep 4.1 line.

- Aligns fallback package dependencies on JsonPit, OsLibCore, RaiUtils, and
  RaiImage 4.1.0.
- Retains the command-first and compatible 4.x legacy `iorg` behavior introduced
  in 4.0.1.
- No ImgSeeder CLI behavior changes are introduced by this release.

---

## 4.0.1

**Date:** 2026-08-10
**Author / Delivering Agent:** RAIkeep Dev Agent
**Delivered Version:** v4.0.1
**Target Consumers:** AfricaStage, AIA
**Status:** Prepared — publication approval pending

### 1. Summary

ImgSeeder v4.0.1 adds command-first `organize` and `clean` interfaces to `iorg`
with operation-scoped options and contextual help. Established flat invocations
remain functional during the `4.x` transition.

### 2. Resolved Change Requests (CRs)

- [`CR006_AfricaStage_to_RAIkeep_CliSubcommands.md`](https://github.com/Burkhardt/AIA/blob/main/doc/CR006_AfricaStage_to_RAIkeep_CliSubcommands.md) — implements contextual subcommands and isolated operation options for `iorg`.

### 3. Root Cause Analysis & Technical Resolution

The flat parser exposed organization conventions and deletion switches in one
option set, then inferred delete versus organize behavior after parsing. The
v4.0.1 entry point selects the command parser only when the leading token is
`organize` or `clean`; all other input continues through the existing parser.

Both parsers normalize into the same organizer and short-name deletion handlers.
The command parser validates option scope before execution and maps human-facing
convention numbers `1`, `2`, and `3` to the three declared enum choices.

The CR's abbreviated clean example omitted the existing required deletion target.
RAIkeep retained `ShortName` as a required argument so `clean --force` can never
be interpreted as an unbounded delete. When `--subscriber` is omitted, the final
segment of the complete `--root` destination supplies the subscriber identity;
callers may instead provide an explicit parent root plus `--subscriber`.

### 4. Public Contract & API / Package Changes

Preferred syntax:

```text
iorg organize [<Subscriber> | --subscriber <name>] --source <dir> (-r|--root) <dir>
              (-p|--pathconv) <1|2|3> (-n|--nameconv) <1|2|3>
iorg clean <ShortName> [--subscriber <name>] (-r|--root) <dir> [--cache] [--force]
```

- `organize` owns source and convention options.
- `clean` owns `--cache` and `--force`; it is a dry run by default.
- `-r` remains a supported short alias for `--root` in both command parsers; it
  is a configuration option and is not deprecated by the subcommand transition.
- Help explicitly marks the `-p`/`--pathconv`, `-n`/`--nameconv`, and
  `-c`/`--cloud` defaults. Cloud choices preserve the configured
  `Os.Config.DefaultCloudOrder`, omit providers without configured paths, and
  reject providers outside that filtered list. When cloud is omitted, the first
  available configured default is selected; an explicit absolute root or `.`
  remains local unless the caller explicitly supplies a cloud option.
- Existing flat organization and short-name deletion syntax remains supported
  throughout `4.x`.
- The legacy parser is scheduled for removal in `5.x.x`; see
  [`CLI-PARSER-TRANSITION-4.x-TO-5.x.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CLI-PARSER-TRANSITION-4.x-TO-5.x.md).
- Startup banner rules no longer use repeated equals characters.

### 5. Validation & Acceptance Evidence

- `ImgSeeder.Tests`: **15 passed, 0 failed, 0 skipped**.
- Executable-process coverage proves command organization, inferred subscriber
  resolution, safe clean dry-run/force behavior, exact-target deletion, legacy
  organization compatibility, option isolation, contextual help, and banner
  formatting.
- Process-level version coverage proves `iorg --version` emits `iorg v4.0.1`.
- Debug builds complete with zero warnings and zero errors.

### 6. Upgrade & Consumption Instructions

1. Update the coordinated RAIkeep tool line to v4.0.1 after publication approval.
2. Prefer `iorg organize` and `iorg clean` for new scripts.
3. Existing flat scripts may migrate during `4.x`; they are scheduled to stop
   working in `5.x.x`.
4. Keep `ShortName` explicit for every clean operation and add `--force` only
   after reviewing the default dry-run output.
5. Independently validate AfricaStage image workflows and record the
   requester-led CR006 Accepted/Rejected evaluation.

---

## 4.0.0

### Summary

`ImgSeeder 4.0.0` is the coordinated `iorg` CLI release aligned with the four `4.0.0` RAIkeep libraries.

### Changes

- Updated assembly, file, informational, and package versions to `4.0.0`.
- Updated fallback package defaults to `JsonPit 4.0.0`, `OsLibCore 4.0.0`, `RaiUtils 4.0.0`, and `RaiImage 4.0.0`.
- Updated test-project package defaults to the same release line.
- Carries forward `-rmc` as the short alias for cache deletion while retaining `--rm-cache`.
- Refreshed the README and centralized release-note link.

### Compatibility

- No `iorg` CLI behavior changed from `3.13.0`.
- Existing command names and options remain unchanged.

### Validation

- `ImgSeeder.Tests`: `8` passed, `0` failed in the coordinated validation run.
- The umbrella `RAIkeep.slnx` build succeeds with the local `4.0.0` dependency chain.

### Release sequencing

`ImgSeeder` is fifth in the coordinated release chain. Its GitHub push/tag must wait for JsonPit workflow success, flat-container visibility, and the full `330`-second hold. `PitSeeder` must wait for the same checks after ImgSeeder publishes.
