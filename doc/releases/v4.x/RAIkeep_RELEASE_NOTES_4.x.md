# RAIkeep Release Notes 4.x

## 4.5.13

- Release version: `4.5.13`
- Coordination tag: `v4.5.13`

### Highlights
- CR067 adds video-container ingestion and single-file, verified ephemeral imports to the media toolchain. Other packages are version-aligned for the synchronized release.

### Coordinated Dependencies
- Aligned with RAIkeep synchronized `4.5.13` line.

---

## 4.5.12

- Release version: `4.5.12`
- Coordination tag: `v4.5.12`

### Highlights
- Complete the coordinated release after the 4.5.11 chain stopped at RaidSeeder publication. This version includes the corrected RaidSeeder SVG verification command and aligns all NuGet and PyPI packages.

### Coordinated Dependencies
- Aligned with RAIkeep synchronized `4.5.12` line.

---

## 4.5.11

- Release version: `4.5.11`
- Coordination tag: `v4.5.11`
- Publication was partial: the release chain stopped in RaidSeeder before its NuGet package was published. Version 4.5.12 supersedes this line.

### Highlights
- CR064 adds first-class edge stereotypes to the authoritative .raid manifest, preserves their source spelling on PlantUML import, and renders them in PlantUML and hydratable SVG. Unmanaged imports require an explicit Domain; managed imports use their tenant.
- RaiGuard expands to 16 architecture rules with updated code fixes, CLI rewrites, and documentation.
- JsonPit's remote cloud test now checks the current change-file naming contract, removing a stale release-gate failure.
- Amafu discovers Linux cloud roots from clean shortcuts, configured paths, and
  `/srv/ServerData/*Data` mounts; its JSON dry run now reports Mzansi's four
  configured providers.

### Coordinated Dependencies
- Aligned with RAIkeep synchronized `4.5.11` line.

---

## 4.5.10

- Release version: `4.5.10`
- Coordination tag: `v4.5.10`

### Highlights
- CR061 establishes idempotent image upsert semantics in `iorg organize` and `RaiImage`: existing images with matching content are unchanged, existing images with differing content are replaced in-place adhering to the CR022 cloud-storage invariant, matching derivative files are invalidated, and `ReceiptVersion: 3` reports `Updated` counts and ranges.

### Coordinated Dependencies
- Aligned with RAIkeep synchronized `4.5.10` line.

---

## 4.5.9

- Release version: `4.5.9`
- Coordination tag: `v4.5.9`

### Highlights
- CR060 preserves intermediate numeric image-stem tokens and adds iorg receipt output, source alias, and image-number filters.
- The coordinated package line and Option B release-history links are prepared for 4.5.9; publication remains a separate manual step.

### Coordinated Dependencies
- Aligned with RAIkeep synchronized `4.5.9` line.

---

## 4.5.8

- Release version: `4.5.8`
- Coordination tag: `v4.5.8`

### Highlights
- Coordinated umbrella release across all 10 platform packages on NuGet.org and PyPI (`jsonpit 4.5.8`).
- Delivers CR059 fleet CLI dispatch in `OsLib` (`DenoCommand`, `AmafuCommand`, `IorgCommand`, `JpitCommand`, `PitsCommand`, `RaidCommand`) supporting typed local and `OverSsh` remote execution.
- Enables remote image processing in `RaiImage` via `ImageMagickCommand.OverSsh(target)`.
- Delivers `JsonPit` `PitItem.ExtendWith` matching-`Id` relaxation, permitting updates that declare their own identity while strictly protecting envelope metadata (`Created`, `Modified`, `Deleted`).
- Full fleet provisioning verified and operational across `Nkosikazi`, `Mzansi`, `umshadisi@Mdlaka`, and `Neo`.

### Coordinated Dependencies
- Aligned with RAIkeep synchronized `4.5.8` line.

---

## 4.5.7

- Release version: `4.5.7`
- Coordination tag: `v4.5.7`

### Highlights
- CR059 adds fleet-ready, typed CLI dispatch: remote SSH execution, Deno run requests, and command wrappers for Amafu, raid, and jpit.
- RaiImage can route ImageMagick work to an SSH target while preserving the existing local path.

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
CR054 delivers compact image receipts and Structured D3 normalization. CR052 delivers object-slot import, deployment PlantUML support, and preflight diagnostics. The accepted bounded XMI deployment importer is retained. All packages align to 4.5.5; no publication is implied by this preparation.

### Coordinated Dependencies
- Aligned with RAIkeep synchronized `4.5.5` line.

### Verification

`dotnet test RAIkeep.slnx -p:UseLocalRAIkeepSources=true` completed across all nine
assemblies. Eight passed immediately; three RaiImage failures were corrected
(numbered-rendering overload and D3 expectations), then all 161 RaiImage tests
passed on the affected-assembly rerun. Aggregate: **909 passed, 0 remaining
failures, 0 skipped**. No second full-suite run was needed for that localized fix.

| Assembly | Passed |
| --- | ---: |
| Amafu | 62 |
| ImgSeeder | 66 |
| JsonPit | 227 |
| OsLib | 147 |
| PitSeeder | 87 |
| RaiDiagram | 92 |
| RaidSeeder | 16 |
| RaiImage | 161 |
| RaiUtils | 51 |

The existing analyzer warnings remain; this is not a warning-free build claim.
`validate-release.py 4.5.5` verifies coordinated version and documentation metadata.
Private reference corpora and the local path inventory are excluded from commits.
Broad cleanup of pre-existing domain examples remains outside this delivery.

### Compatibility

Structured images and numbered diagram siblings now generate minimum-width D3.
Readers accept earlier numeric widths, but recomposed paths change. No automatic
migration runs; migrate stored files and references together before replaying old
imports. Receipt consumers should use Summary/Exceptions/Error and CLI exit codes,
not a top-level activity Status. Default receipts omit Files; explicit --exif adds it.

---

## 4.5.4

This patch fixes Amafu cloud initialization: `amafu init --create-links` now
writes the created `~/.CloudStorage/<provider>/` shortcuts into `RAIkeep.json5`.
Previously it created the shortcuts but retained the original physical paths
in the configuration. Preview and saved output now agree for both `init` and
`init-config`.

See [Amafu 4.5.4 release notes](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/Amafu_RELEASE_NOTES_4.x.md#454) for examples and
migration of existing configuration with `amafu reconcile --apply`.

All nine C# packages and applicable internal dependencies align to 4.5.4.
The other packages have no runtime behavior changes in this patch. JsonPit's
GettingStarted guide documents the corrected initialization behavior.

Release tooling retains the assembly-derived Amafu version output and its
matching validation checks. The C# release chain handles publication;
Python/jpit releases remain separately coordinated with Adele.

### Verification

- Complete Amafu suite: 62 passed, 0 failed, 0 skipped.
- Version-filtered Release tests with local sources: 13 passed across Amafu,
  ImgSeeder, PitSeeder, RaiDiagram, and RaidSeeder.
- Release validator: 80 checks passed; release-tool regression tests: 2 passed.
- Release-chain shell syntax check passed.

---

## 4.5.3

RAIkeep 4.5.3 delivers CR051: multi-account cloud storage discovery, named shortcuts, deterministic personal OneDrive selection, noninteractive configuration reconciliation, and OsLib recognition of arbitrary named cloud roots. All nine C# packages and internal package dependencies align to 4.5.3. JsonPit distributed persistence and live-object mutation behavior remain unchanged.

### Multi-account discovery and reconciliation (CR051)

- **Multiple Google Drive accounts**: Discovers all Google Drive accounts (e.g. `GoogleDrive-rainer.burkhardt@gmail.com` -> `GoogleDriveRainer`, `GoogleDrive-yebo@umshadisi.com` -> `GoogleDriveYebo`). Each account independently selects its `GDriveData` subfolder, or `My Drive` when absent.
- **Multiple OneDrive accounts**: Discovers personal and corporate OneDrive roots. Exactly one personal OneDrive root is selected under the compatible `OneDrive` key; corporate roots (e.g. `OneDriveAfricaStage`, `OneDriveContoso`) retain independent qualified keys.
- **Deterministic personal OneDrive selection**: Explicit `--onedrive-personal <folder>` takes precedence; otherwise an existing valid configured root is retained; otherwise the longest folder name wins (with highest numeric suffix and ordinal path order as tie-breakers). Commands never prompt interactively.
- **Noninteractive reconciliation**: `amafu reconcile` previews newly discovered accounts and migration to `~/.CloudStorage` shortcuts without writes. `amafu reconcile --apply` creates shortcuts, backs up existing configuration with a unique timestamped suffix, and safely updates `Cloud` and `DefaultCloudOrder` while preserving all unrelated JSON5 settings, comments, and order.
- **Collision safety**: Case-insensitive account name collisions report both conflicting roots and fail before filesystem writes. Duplicate aliases of the same physical root are deduplicated.
- **Symbolic shortcut classification**: OsLib's `ConfiguredCloudPaths` reads all configured string roots in `Cloud` without provider enum restrictions, and resolves symbolic links and existing ancestors so `~/.CloudStorage` shortcuts receive cloud-safe in-place atomic writes.
- **CLI account key resolution**: PitSeeder (`pits -c <name>`) accepts any configured account key in `Cloud` and `DefaultCloudOrder`.

### Coordinated Package Alignment

All nine C# packages align to the 4.5.3 line:
- `Amafu` 4.5.3: multi-account discovery, reconciliation, personal OneDrive selection.
- `OsLibCore` 4.5.3: unrestricted string cloud roots, symbolic link classification.
- `RaiUtils` 4.5.3: synchronized dependency alignment.
- `RaiImage` 4.5.3: synchronized dependency alignment.
- `RaiDiagram` 4.5.3: synchronized diagram line alignment.
- `RaidSeeder` 4.5.3: synchronized CLI and dependency alignment.
- `JsonPit` 4.5.3: synchronized persistence line alignment.
- `ImgSeeder` 4.5.3: synchronized CLI and dependency alignment.
- `PitSeeder` 4.5.3: multi-account CLI resolution and synchronized alignment.

### Python Parity & Coordination

Adele coordinates `jsonpit-python`/`jpit` 4.5.3 separately. Python `jsonpit` is updated to 4.5.3 with link-resolving cloud path classification matching OsLib, and published to PyPI prior to deployment. The C# release chain publishes only the .NET stack.

### Verification

- **Amafu**: 60 passed, 0 failed, 0 skipped.
- **OsLib**: 147 passed, 0 failed, 0 skipped.
- **PitSeeder**: 87 passed, 0 failed, 0 skipped.
- Release validator: all checks passed.
- Preflight clean across all nine component repositories.

---

## 4.5.2

RAIkeep 4.5.2 improves cloud-drive setup with optional Amafu shortcuts, installer
PATH fixes, and a practical weather-data walkthrough. All nine C# packages and
internal package dependencies align to 4.5.2. JsonPit persistence and live-object
mutation behavior are unchanged.

### Cloud setup

- `amafu detect --create-links` creates missing `~/.CloudStorage/<provider>`
  symbolic links for detected cloud roots. Plain detection remains read-only.
- `amafu init --create-links` creates links along with a new configuration.
  Matching links are reused; conflicting paths are preserved and reported.
  `--dry-run` writes nothing, and generated configuration retains real roots.
- Amafu remains a standalone bootstrap utility without an OsLib dependency.
- The installer puts managed CLI paths ahead of legacy installations and
  configures zsh non-interactive SSH and login sessions as well as interactive
  shells, backing up existing startup files before edits.
- JsonPit's GettingStarted recommends cloud shortcuts. FirstSteps_pits walks
  through creating an iCloud pit and importing Open-Meteo JSON with curl and jq.

### Release preparation

- Fix the manifest's literal C# interpolation braces and keep Amafu's existing
  version output format consistent with its tests and validator.
- Validate conditional fallback dependency versions; previously those checks
  were skipped because the presence check did not match attributes.
- Preserve historical feature-introduction versions when bumping current docs.
- Update the installer default and release instructions to 4.5.2.

### Verification and handoff

- Complete Release solution run: **844 passed, 0 failed, 0 skipped**, including
  JsonPit SSH/cloud synchronization scenarios.
- Release-tool regression tests: **2 passed**; release validator: **81 checks passed**.
- macOS ARM64 native Amafu publish and CLI version/dry-run smoke checks passed.
- Shell syntax checks passed for installer and release-chain scripts.
- Compiler/analyzer warnings remain; there were no build or test errors.

CR050 multi-account discovery is a separate draft for review, not implemented
in this release. Amafu still selects the first existing root per provider.
Rainer runs `scripts/release-chain.sh 4.5.2` after preparation. No publication is
performed by version preparation or tests. The script publishes the C# stack;
Adele owns jsonpit-python/jpit 4.5.2 publication and parity verification separately.
Python 4.5.2 must be published before using the installer for a fully aligned
4.5.2 setup; Python 4.5.1 is already in use.

---

## 4.5.0

RAIkeep v4.5.0 coordinates live object reference semantics, sparse mutation tracking, selectable tracking modes in JsonPit, and an automated release validation gate across all nine packages at version 4.5.0.

### JsonPit live references and mutation tracking

JsonPit now adopts caller-supplied live objects and existing nested objects when adding an entity (`Pit.Add(item)`). Current indexers return those exact live references rather than projecting cloned copies on every lookup.

- **Sparse Tracked Mutations:** Supported in-place edits and property indexer mutations immediately append sparse delta fragments internally without rewriting unrelated attributes or earlier history.
- **Per-Instance Tracking Modes:** `Pit.DefaultMutationTrackingMode` configures process-local behavior for new Pits:
  - `TrackedChangesWithFallback` (default): Immediately tracks supported operations and reconciles live values against the last accepted baseline at persistence boundaries. Unreported edits receive their timestamp when detected.
  - `TrackedChangesOnly`: Optimized for server workloads, strictly recording API-tracked mutations without boundary comparisons.
- **Reference Identity Contract:** Verified by `ReferenceTests.ArrayOperator_ReturnsAddedItem`, guaranteeing instance identity (`Assert.Same`) across lookups and mutations.
- **Historical Snapshot Isolation:** Historical reads (`GetAt`, time-travel) remain independent, immutable snapshots.

### Coordinated Package Alignments

- **PitSeeder (`pits`):** Property deletion (`del-prop`) uses live item mutation (`DeletePropertyPath`) directly, appending sparse tombstones without read-modify-write. Reports version 4.5.0.
- **ImgSeeder (`iorg`), RaidSeeder (`raid`), Amafu:** Aligned to 4.5.0 with updated CLI version reporting and install documentation.
- **OsLibCore, RaiUtils, RaiImage, RaiDiagram:** Coordinated foundation and utility dependencies aligned at 4.5.0.
- **Automated Consistency Gate:** Integrated `scripts/validate-release.py` verifying all 9 package project files, code constants, test assertions, docs, and release notes before any tags or releases occur.

### Validation and release coordination

Verification covers all 226 non-remote JsonPit tests, all 84 PitSeeder tests, and remote SSH/cloud drive synchronization scenarios with Mzansi. All package and internal dependency versions align at 4.5.0.

This document does not itself assert that publication has completed. Rainer executes `scripts/release-chain.sh 4.5.0`. Adele maintains Python implementation and parity.

---

## 4.4.8

RAIkeep v4.4.8 introduces live object reference semantics, sparse mutation tracking, and per-instance tracking modes in JsonPit, coordinating dependency alignment across all nine packages at version 4.4.8.

### JsonPit live references and mutation tracking

JsonPit now adopts caller-supplied live objects and existing nested objects when adding an entity (`Pit.Add(item)`). Current indexers return those exact live references rather than projecting cloned copies on every lookup.

- **Sparse Tracked Mutations:** Supported in-place edits and property indexer mutations immediately append sparse delta fragments internally without rewriting unrelated attributes or earlier history.
- **Per-Instance Tracking Modes:** `Pit.DefaultMutationTrackingMode` configures process-local behavior for new Pits:
  - `TrackedChangesWithFallback` (default): Immediately tracks supported operations and reconciles live values against the last accepted baseline at persistence boundaries. Unreported edits receive their timestamp when detected.
  - `TrackedChangesOnly`: Optimized for server workloads, strictly recording API-tracked mutations without boundary comparisons.
- **Reference Identity Contract:** Verified by `ReferenceTests.ArrayOperator_ReturnsAddedItem`, guaranteeing instance identity (`Assert.Same`) across lookups and mutations.
- **Historical Snapshot Isolation:** Historical reads (`GetAt`, time-travel) remain independent, immutable snapshots.

### Coordinated Package Alignments

- **PitSeeder (`pits`):** Property deletion (`del-prop`) uses live item mutation (`DeletePropertyPath`) directly, appending sparse tombstones without read-modify-write. Reports version 4.4.8.
- **ImgSeeder (`iorg`), RaidSeeder (`raid`), Amafu:** Aligned to 4.4.8 with updated CLI version reporting.
- **OsLibCore, RaiUtils, RaiImage, RaiDiagram:** Coordinated foundation and utility dependencies aligned at 4.4.8.

### Validation and release coordination

Verification covers all 225 non-remote JsonPit tests, all 84 PitSeeder tests, and remote SSH/cloud drive synchronization scenarios with Mzansi. All package and internal dependency versions align at 4.4.8, skipping 4.4.7 to coordinate with `jsonpit-python`.

This document does not itself assert that publication has completed. Rainer executes `scripts/release-chain.sh 4.4.8`. Adele maintains Python implementation and parity.

---

## 4.4.6

RAIkeep v4.4.6 implements [CR049](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR/CR049_AIA_and_jsonpit_to_RAIkeep_Live-ID-Validation_and_Zip-Image-Import.md), incorporating Rainer's live-ID validation, ZIP ingestion, EXIF inspection, and storage filename optimization decisions.

### Live IDs and stdin receipts

JsonPit rejects `{` and `<` inside IDs at live write boundaries, including direct library calls and complete batches. Ordinary field values remain unrestricted by this rule. Historical records remain readable/exportable and can be explicitly deleted, while live re-insertion fails. PitSeeder validates the whole input before writable Pit creation, including strict patch mode. `pits seed <PitName> --source -` accepts explicit standard input.

### Storage Filename Refinements & Cloud Sync Optimization

- **ChangeFiles (4-Character Checksum):** Restored a concise 4-character hex checksum suffix (`{UtcTicks}_{ExactProcessIdentity}_{4charHex}.json`). This provides reliable cloud-sync integrity against partial writes without inflating path lengths or causing synchronization bottlenecks on cloud providers like OneDrive.
- **EventFiles (Clean Logical Naming):** Removed the 64-character SHA-256 hash suffix from compaction event filenames, standardizing on clean `{LogicalStem}.event` files.
- **Automated Event Migration:** `pits maintain --apply` automatically discovers legacy `{stem}_{sha256}.event` archives, verifies payload digests, and migrates them in-place to clean names.
- **Engine Hygiene:** Removed the obsolete `Item` class from `JsonPit` in favor of polymorphic `PitItem`.

### ZIP image imports

`iorg organize` accepts local ZIP files or direct HTTPS URLs and returns an authoritative `Class: "ImageImport"` receipt. Complete preflight protects final destinations from invalid paths/IDs and naming collisions. Existing identical bytes are `Unchanged`; different content is never silently overwritten. Partial copy failures report their actual outcomes.

On macOS/Ubuntu, native Info-ZIP extraction runs through asynchronous `RaiSystem` execution into temporary storage. The .NET import API dispatches the entire operation off the calling thread. Missing tools, insufficient temporary disk space, corrupt archives, and cancellation fail explicitly. Final images are written directly into their ImageTree paths, never moved from temp into a CloudDrive. Size/count/download-time limits are optional and have no application-imposed defaults.

### EXIF and downstream processing

Both `iorg list` and `organize` support `--exif '*'` and comma-separated selectors. Matching embedded date/offset pairs become `DateTimeOffset` values under the original date names. Thumbnail, lens, focal-plane, and exposure fields are grouped; rationals retain exact numerator/denominator and numeric value. Missing/invalid conversion inputs remain in `Unconverted` with diagnostics. No `Captured` alias or file/local-timezone fallback is introduced.

The [ImgSeeder README](https://github.com/Burkhardt/ImgSeeder/blob/main/README.md) documents ZIP ingestion, actual filename normalization, jq inspection, and buffering/checking the receipt before `pits` or `jpit` ingestion.

### Validation and release coordination

Native extraction has been exercised on macOS and Ubuntu/Mzansi. Automated coverage includes core/CLI marker validation, historical compatibility, empty/malformed stdin, receipt persistence, ZIP traversal and collisions, repeated imports, partial failures, HTTPS error handling, strict JSON stdout, native cancellation, and EXIF conversion/selection.

Final full-stack test results are recorded in the release handoff. This document does not itself assert that validation or publication has completed. All nine package versions and fallback dependencies align at 4.4.6. Rainer runs `scripts/release-chain.sh 4.4.6`; no tags, pushes, or publication are performed during preparation. Adele owns Python implementation/parity and its release.

---

## 4.4.5

RAIkeep v4.4.5 implements accepted [`CR047_jsonpit_and_pits_Require-Existing-Patch-Flag-and-Seed-Commit-Count.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR/CR047_jsonpit_and_pits_Require-Existing-Patch-Flag-and-Seed-Commit-Count.md) as a coordinated nine-package release.

### `pits seed` strict patch safety

- Adds `--require-existing` and its `--patch` alias for single-pit seed operations.
- Validates every ID against current living state before opening a writable Pit.
- Missing and tombstoned IDs abort the entire batch with exit code `1`; no valid sibling patch is partially committed.
- Empty strict batches fail explicitly, while default no-flag seed/upsert behavior remains backward compatible.
- Successful seeds report the exact committed payload count.
- `OsLibCore.PitsSeedRequest.RequireExisting` exposes the canonical strict-patch token to services and agents without hand-built process arguments.

### Coordination and validation

- Preflight uses an unflagged, read-only projection, preserving JsonPit's process-window, master-lease, eventual-durability, and cloud-safe in-place contracts.
- Sipho's five acceptance vectors and additional tombstone/no-side-effect cases run through the real managed `pits` command wrapper.
- All nine packages align at 4.4.5 so fallback dependencies remain synchronized throughout the release order.

Tagging, GitHub Releases, and NuGet publication remain behind RAI's manual release-chain gate.

---

## 4.4.4

RAIkeep v4.4.4 implements accepted [`CR044_AIA_and_jsonpit_to_RAIkeep_Auto-Detect-Cloud-Drives-and-Init-Config.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR/CR044_AIA_and_jsonpit_to_RAIkeep_Auto-Detect-Cloud-Drives-and-Init-Config.md) as a coordinated nine-package release.

### New standalone bootstrap tool

- Introduces `Burkhardt/Amafu` and the native `amafu` command.
- `amafu detect` discovers mounted cloud providers without writes.
- `amafu init` (alias `init-config`) generates `~/.config/RAIkeep.json5`, with overwrite protection, `--force`, and `--dry-run`.
- Amafu is independent of OsLib and protects OsLib's immutable startup configuration boundary.
- Distribution includes the NuGet tool plus NativeAOT GitHub release binaries for macOS, Linux, and Windows.
- Automatic cloud-provider discovery is supported and tested only on macOS in 4.4.4; Linux and Windows currently use the explicit starter-template fallback.

### Suite integration

- `pits` provides actionable `amafu init` guidance when configuration is absent.
- Amafu is the first package released after the umbrella GitHub Release and before OsLibCore.
- Recovery supports `scripts/release-chain.sh 4.4.4 --resume-after-amafu`.
- All nine packages align at 4.4.4; existing library and CLI behavior is otherwise unchanged.

Tagging, GitHub Releases, and NuGet publication remain behind RAI's manual release-chain gate.

---

## 4.4.3

RAIkeep 4.4.3 is the synchronized eight-package delivery of accepted
[`CR043_AfricaStage_to_RAIkeep_Improve-pits-seed-array-error-message.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR043_AfricaStage_to_RAIkeep_Improve-pits-seed-array-error-message.md).

### `pits seed` payload ergonomics

- A single root JSON/JSON5 entity is accepted when it has an exact, non-empty
  string `Id`.
- Arrays and keyed maps remain supported without conversion or migration.
- Invalid roots describe all three accepted forms instead of incorrectly saying
  that a valid root object is not an object.
- Every array/map entry must be an object and every entity must have a valid
  `Id` before the destination pit is opened.
- Rejected payloads therefore create no pit directory, process flag, or partial
  persistence state.

### Release coordination

All eight packages align in this order: OsLibCore, RaiUtils, RaiImage,
RaiDiagram, RaidSeeder, JsonPit, ImgSeeder, and PitSeeder. No filesystem,
cloud-storage, persistence, finalizer, or diagram behavior changes outside the
PitSeeder seed boundary.

Publication remains behind RAI's manual `scripts/release-chain.sh 4.4.3` gate.

---

## 4.4.2

RAIkeep 4.4.2 is the synchronized eight-package delivery of accepted
[`CR040_AIA_to_RAIkeep_and_jsonpit_Prohibit-Read-Modify-Write.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR040_AIA_to_RAIkeep_and_jsonpit_Prohibit-Read-Modify-Write.md)
and
[`CR041_jsonpit_to_RAIkeep_Restore-Clean-Change-Filenames.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR041_jsonpit_to_RAIkeep_Restore-Clean-Change-Filenames.md).

### Sparse mutation protection

- JsonPit rejects client mutation or tombstoning of engine-managed `Id`,
  `Modified`, and `Deleted` attributes atomically.
- Live storage rejects projected read-modify-write payloads while explicit
  trusted historical replay continues through `AddHistorical(...)`.
- `pits seed` validates before opening the destination; `delete-property`
  creates sparse fragments and protects lifecycle attributes.

### Clean change artifacts

- New changes and receipts use readable
  `{Modified.UtcTicks}_{ExactProcessIdentity}.{json|receipt}` names.
- Dual-format discovery retains existing SHA-suffixed change files during
  rolling upgrades; legacy files keep hash validation.
- Process-monotonic live timestamps close the practical clock-resolution
  collision gap without lengthening filenames.
- Existing canonical accounting, immutable receipts, and the ten-minute cleanup
  grace apply equally to both formats.

### Release coordination

The already-published `v4.4.1` tags and packages remain immutable. CR040 and
CR041 therefore ship in the next coordinated patch, 4.4.2. All eight packages
align in this order: OsLibCore, RaiUtils, RaiImage, RaiDiagram, RaidSeeder,
JsonPit, ImgSeeder, and PitSeeder. No TempDir-to-cloud move, directory swap, or
finalizer filesystem I/O is introduced.

Publication remains behind RAI's manual `scripts/release-chain.sh 4.4.2` gate.

---

## 4.4.1

RAIkeep 4.4.1 is the synchronized eight-package delivery of accepted
[`CR037_AIA_to_RAIkeep_RaidSeeder_Diagram_Artifact_Management.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR037_AIA_to_RAIkeep_RaidSeeder_Diagram_Artifact_Management.md).
It also delivers accepted
[`CR037.1_AIA_to_RAIkeep_CLI_Global_Flag_and_Verb_Dispatch_Resilience.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR037.1_AIA_to_RAIkeep_CLI_Global_Flag_and_Verb_Dispatch_Resilience.md).

### RaidSeeder diagram artifact management

- Renames the dedicated repository and successor NuGet tool package from
  `RaidCli` to `RaidSeeder`; the installed command remains `raid`.
- Adds `raid import`, `export`, `refresh`, and `validate`, plus iorg-aligned
  cloud, application-root, exact-root, tenant, path-convention, Number, and
  NameExt options.
- Treats `.raid` as authoritative and derives `.puml` and `.svg` rather than
  trusting possibly stale siblings.
- Refresh writes only missing or stale derivatives; a current artifact is not
  rewritten, and refresh never rewrites the authoritative manifest.
- Adds hydratable and plain SVG profiles. Hydratable output includes structural
  metadata, ports, routing, and declared expressions, but never dynamic
  `aim-satisfied` evaluation state.
- Guarantees semantic round-trip fidelity for compiler-emitted PUML.
- Adds OsLibCore's typed `RaidCommand` wrapper and exact argument-forwarding
  verification.

### CLI dispatch resilience

- `pits`, `iorg`, and `raid` reserve their registered verbs and require an
  explicit subcommand at argument zero.
- A misplaced verb fails before filesystem/database access with exit code `2`,
  identifies the misplaced verb, and prints the corrected command line.
- `-v`/`--version` remains an immediate successful operation wherever it
  appears; command-first `verb --help` remains verb-specific.

### Cloud safety and release coordination

All managed files are written through the OsLib/RaiFile boundary directly at
their final paths. No TempDir-to-cloud move, established-directory swap, or
no-op rewrite is used. All eight packages align at 4.4.1 in this order:
OsLibCore, RaiUtils, RaiImage, RaiDiagram, RaidSeeder, JsonPit, ImgSeeder, and
PitSeeder.

Publication remains behind RAI's manual
`scripts/release-chain.sh 4.4.1` gate. The immutable `RaidCli 4.4.0` tag and
package are not rewritten; deprecation with `RaidSeeder` as replacement occurs
only after successful 4.4.1 publication and verification.

---

## 4.4.0

RAIkeep 4.4.0 is the synchronized eight-package delivery of accepted
[`CR036_AIA_to_RAIkeep_Raid_CLI.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR036_AIA_to_RAIkeep_Raid_CLI.md).

### Raid model interchange

- Adds the independent `RaidCli` repository and NuGet tool package. Installing
  `RaidCli 4.4.0` provides the `raid` command.
- `raid import --puml <diagram.puml> [--out <dir>] [--name <id>]` imports modern
  PlantUML activity and class diagrams into canonical `.raid` plus hydratable
  `aim-*` SVG.
- `raid validate <file.raid|file.svg>` validates the manifest or public
  RaidCanvas hydration contract.
- RaiDiagram adds `IModelImporter`, `PlantUmlModelImporter`,
  `RaidDiagramModel`, typed deterministic canvas geometry, and `AimSvg`.
- The real `doc/ChangeRequestWorkflow.puml` fixture is covered end to end.

### Comment-tolerant seed files

`pits seed` accepts JSON5 line and block comments before the root array or
keyed object map. Parsing is deliberate and single-pass; malformed content is
still rejected rather than retried after broadly stripping text.

### Tag and GitHub Release synchronization

Beginning with v4.4.0, pushing the umbrella tag runs
`.github/workflows/publish-release.yml`. The workflow requires this exact notes
file and creates GitHub Release `RAIkeep v4.4.0`. The release chain waits for
and verifies that release before package tagging begins.

All filesystem reads and writes in `raid` remain on the OsLib boundary.
`TextReader`/`StringReader` are used only for in-memory parser interchange.
Publication remains behind RAI's manual `scripts/release-chain.sh 4.4.0` gate.

---

## 4.3.2

RAIkeep 4.3.2 is the coordinated seven-package delivery of accepted
[CR027 Class-Diagram Generalization and `SetSuperClass`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR027_AIA_to_RAIkeep_ClassDiagram_Generalization_and_SetSuperClass.md).

### RaiDiagram class generalization

- `ClassDiagramBuilder.SetSuperClass(...)` adds a typed superclass to a class
  diagram and a typed generalization relationship to the derived class.
- `PlantUmlDiagramCompiler` renders that semantic direction as UML `<|--`.
- An optional stereotype labels the generalization; omission produces the
  standard unlabeled UML relationship.
- Generalization and existing instance-of edges can be rendered together.
- The singular builder API rejects a second superclass definition explicitly.
- Existing class builders without a superclass preserve their prior output.

OsLibCore, RaiUtils, RaiImage, JsonPit, ImgSeeder, and PitSeeder have no
behavioral changes in this patch; they participate so all seven package and
fallback dependency versions remain aligned on 4.3.2.

Tagging, GitHub labeling, workflow dispatch, and NuGet publication remain behind
RAI's manual `scripts/release-chain.sh 4.3.2` gate.

---

## 4.3.1

RAIkeep 4.3.1 is the coordinated seven-package delivery of accepted
[CR026 Captured-Revision Fidelity and Object-Reference Stereotypes](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR026_AIA_to_RAIkeep_Diagram_Builder_Revision_Fidelity_and_Reference_Stereotypes.md).

### RaiDiagram repair and enhancement

- `DiagramModelIdentity.CapturedRevision` is treated as an opaque string across
  typed builders, model snapshots, JSON5 serialization, and `.raid` parsing.
- ISO 8601 values retain their exact characters, precision, and offset instead
  of becoming culture- or machine-time-zone-dependent strings.
- `OneUseCaseDiagramBuilder.AddObjectReference(...)` accepts an optional
  semantic stereotype; explicit verbs render directly while the existing
  bucket-derived label remains the default.
- Existing `.raid` JSON5 syntax and validation behavior remain compatible.

OsLibCore, RaiUtils, RaiImage, JsonPit, ImgSeeder, and PitSeeder have no
behavioral changes in this patch; they participate so all seven package and
fallback dependency versions remain aligned on 4.3.1.

CR027 class generalization is accepted separately for v4.3.2 and is not part of
v4.3.1. Tagging, GitHub labeling, workflow dispatch, and NuGet publication
remain behind RAI's manual `scripts/release-chain.sh 4.3.1` gate.

---

## 4.3.0

RAIkeep 4.3.0 is the coordinated seven-package delivery of accepted
[CR023 PlantUML relationship rendering](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR023_AIA_to_RAIkeep_PlantUml_Relationship_Rendering.md),
[CR024 process-flag self-cleanup](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR024_AIA_to_RAIkeep_Ephemeral_Flag_Self_Cleanup.md), and
[CR025 typed RaiDiagram builders and deterministic ItemTree emission](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR025_AIA_to_RAIkeep_Typed_Raid_Builders_and_Deterministic_ItemTree_Emission.md).

### RaiDiagram 4.3

- Typed builders create UCD, RFD/OD, CD, AD, and SD manifests through managed C#.
- PlantUML source compilation remains Java-free and emits native syntax with
  conditional `allowmixing`; the optional renderer remains compatible.
- Base `ItemId`, optional `ItemNumber`, and archetype `NameExt` stay distinct.
  Filenames use `ItemId[_NN][_NameExt].ext`, while ItemTree buckets use only the
  base ItemId.
- `.raid`, `.puml`, `_config.puml`, and `.svg` are deterministic co-located
  subscriber siblings.
- Real PlantUML 1.2026.8 syntax validation and SVG diagnostic detection guard
  the generated source.

### Carried accepted lifecycle work

- CR023 relationship labels, cardinality, and accepted-vocabulary discovery are included.
- CR024 clean disposal removes only the exact owned PID flag; finalizers remain I/O-free.
- CR022's no-TempDir-to-cloud and continuous-cloud-pathname rules remain mandatory.

RAI intentionally did not publish v4.2.11; all prepared CR023/CR024 changes are
superseded and carried into v4.3.0. All seven package/fallback versions align on
4.3.0. Tagging, GitHub labeling, workflow dispatch, and NuGet publication remain
behind RAI's manual `scripts/release-chain.sh 4.3.0` gate.

---

## 4.2.11

> **Superseded before publication.** RAI intentionally skipped v4.2.11. These
> prepared changes are delivered in the coordinated v4.3.0 release.

RAIkeep 4.2.11 is the coordinated seven-package delivery of accepted
[CR023 PlantUML relationship rendering](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR023_AIA_to_RAIkeep_PlantUml_Relationship_Rendering.md)
and
[CR024 process-flag self-cleanup](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR024_AIA_to_RAIkeep_Ephemeral_Flag_Self_Cleanup.md).

### RaiDiagram relationship rendering

- Activity Interaction manifests now render their relationships, including
  direction, role labels, and cardinality, rather than requiring an edgeless
  fallback.
- The compiler publishes its accepted element and relationship vocabularies.
- PlantUML `allowmixing` preserves truthful mixed element declarations while
  permitting their relationships to render.
- Unknown constructs remain explicit failures instead of being silently omitted.

### JsonPit and `pits` clean exit

- Graceful `Pit.Dispose()` removes the exact owned PID-specific process flag
  through OsLib's cloud-aware `RaiFile.rm()` boundary.
- Default finite CLI calls leave zero owned process flags after normal or
  exceptional completion; Ctrl+C and process-exit cleanup use the same path.
- `Master.flag`, lease TTL, crash recovery, and explicit maintenance pruning are
  unchanged.
- `--retain-window` remains only as a documented 4.2.11 compatibility exception
  and is scheduled for removal in the next major release.
- Finalizers remain strictly free of filesystem and recovery-publication I/O.

All seven versions and fallback dependency properties align on 4.2.11. Tagging,
GitHub labeling, workflow dispatch, and NuGet publication remain behind RAI's
manual `scripts/release-chain.sh 4.2.11` gate.

---

## 4.2.10

RAIkeep 4.2.10 is the coordinated seven-package delivery of the RAI-authorized
JsonPit recovery-event archive backlog and improved `iorg` application-root /
tenant addressing. It preserves accepted
[CR021](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR021_RAI_to_RAIkeep_JsonPit_Durable_Cleanup_Receipts_and_Pits_Coordination.md)
and the mandatory
[CR022 cloud-storage invariant](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR022_RAI_to_RAIkeep_Cloud_Safe_In_Place_Filesystem_Invariant.md).

### Recovery-event compaction

- `pits maintain ... --archive-events` previews exact event-archive work;
  `--apply` is required to write the archive and retire loose copies.
- The OsLib-backed archive is immutable, created at its final pathname inside the
  existing `Events` directory, and never staged in `Os.TempDir`.
- Source events remain until complete filename/byte validation succeeds, and are
  then removed individually. Retry, corruption, and collision paths fail safe.
- `pits audit` and `PitAudit` transparently preserve one logical history across
  loose and archived storage.

### Iorg addressing

- `-a, --app` accepts an application root and appends `Image`.
- `-t, --tenant` is the preferred explicit subscriber spelling;
  `--subscriber` remains an alias.
- `-r, --root` continues to mean an exact ImageTree root, and help output now
  presents these alternatives consistently.
- The umbrella solution explicitly includes the ImgSeeder executable so the
  coordinated build verifies every deliverable under the requested Release
  configuration.

All seven package versions and fallback dependency properties align on 4.2.10.
Tagging, GitHub labeling, and NuGet publication remain behind RAI's manual
`scripts/release-chain.sh 4.2.10` gate.

---

## 4.2.9

RAIkeep 4.2.9 is the coordinated seven-package incident-correction delivery of
accepted [CR022 — Cloud-Safe In-Place Filesystem Invariant](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR022_RAI_to_RAIkeep_Cloud_Safe_In_Place_Filesystem_Invariant.md).
It carries forward accepted [CR021 — JsonPit Durable Cleanup Receipts and `pits` Coordination](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR021_RAI_to_RAIkeep_JsonPit_Durable_Cleanup_Receipts_and_Pits_Coordination.md).

### Incident finding

The investigation found no evidence that JsonPit replaced the four established
AIA pit directories. The mass-deletion prompt was consistent with the explicitly
requested removal of expired process flags and repaired legacy files. It did,
however, expose one report-only path-construction defect and independent
TempDir-staging patterns elsewhere in the product line. This release corrects
those defects and turns the cloud rule into a tested, reusable boundary.

### Delivered

- `RaiFile` rejects TempDir-to-cloud moves before mutation and overwrites an
  existing cloud file without deleting or renaming its established pathname.
- `RaiPath` rejects TempDir-to-cloud directory moves and replacement of existing
  cloud directories.
- Cloud backups copy established files instead of moving them away.
- JsonPit report-only maintenance no longer materializes a missing pit directory.
- `pits maintain` validates its configured root and canonical pit files before
  constructing any `Pit`; partial WWWA trees are reported without being created.
- ImgSeeder writes directly to the final ItemTree pathname instead of staging a
  subscriber tree in `Os.TempDir`.
- `ImageMagick.JpegTran` uses isolated temporary input/output files and copies
  successful bytes into the continuously present destination pathname.
- The cloud-storage invariant is documented and covered by configured-cloud
  success, failure, and no-mutation regressions.

All seven package versions and fallback dependency properties align on 4.2.9.
Tagging, GitHub labeling, and NuGet publication remain behind RAI's manual
`scripts/release-chain.sh 4.2.9` gate.

---

## 4.2.8

RAIkeep 4.2.8 is the coordinated seven-package delivery of accepted
[CR021 — JsonPit Durable Cleanup Receipts and `pits` Coordination](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR021_RAI_to_RAIkeep_JsonPit_Durable_Cleanup_Receipts_and_Pits_Coordination.md).

### Delivered

- JsonPit cleanup eligibility is durable across restart and master transfer through immutable `.receipt` files.
- Cleanup remains crash-safe and conservative: canonical accounting and current exact-master authority are revalidated, then the change file is removed before its receipt.
- `Pit.Maintain(...)` and `pits maintain` expose report-only and explicit-apply administration without timers, finalizer work, or `Os.Config` mutation.
- Expired PID-window pruning and legacy extension repair each require separate explicit authorization.
- Dotted logical process names retain their requested `.flag` / `.event` extensions.
- Typed `PitsCommand` calls serialize same-target child invocations within one host process while preserving exact child PID authority and the distributed JsonPit protocol.

### Compatibility and release boundary

- CR021 changes no AIA source and introduces no identity-management subsystem.
- CR003 remains authoritative except for its superseded in-memory-only cleanup-eligibility rule.
- All seven package versions and fallback dependency properties align on 4.2.8.
- Tagging, GitHub labels, and NuGet publication remain behind RAI's manual `scripts/release-chain.sh 4.2.8` gate.

---

## 4.2.7

RAIkeep 4.2.7 is the coordinated seven-package implementation of accepted
[CR020 — `iorg` Media & Diagram Tree Custodianship](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR020_RAI_to_RAIkeep_Iorg_Read_Only_Wildcard_Listing.md).

### ItemTree architecture

- `ItemTreePath` is the object-oriented home of one subscriber-local ItemId and every physical file belonging to it.
- `SelectFiles()` returns images, derivatives, SVG, PUML, config PUML, and RAID files for the exact ItemId without selecting similar bucket siblings.
- `destination.mv(source)` moves or renames the whole family and supports canonical, 3x3, 8x2, and Flat placement.
- Image and diagram artifact constructors share `ItemTreePath`; the active `FromImageTree`/`FromItemTree` factory path has been removed.

### `iorg`

- `iorg list <FileNamePattern>` recursively discovers managed image and diagram files without mutation.
- `iorg move <SourceItemId> [TargetItemId]` performs exact-family relocation, optional rename, and path-convention migration.
- `iorg clean --cache` removes rendered derivatives while preserving source and diagram files.
- `iorg clean <ItemId> --force` removes the complete item family; without `--force` it remains a dry run.
- Root help no longer calls supported syntax Legacy; `-r` remains the supported short spelling of `--root`.

### Compatibility and release boundary

- Existing `PathConventionType` values retain their positions; `Flat` is appended and exposed as CLI option 4.
- All seven package versions and fallback dependencies align on 4.2.7.
- No tag or NuGet publication is created during preparation. RAI retains the manual release-chain gate.

---

## 4.2.6

**Status:** Implemented, verified, and prepared; not published

**Accepted request:** [CR019 — `WordCase` seam positions and placement in RaiUtils](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR019_AIA_to_RAIkeep_WordCase_Seams_and_Placement.md)

**AIA proposal:** [CR019 at the reviewed AIA commit](https://github.com/Burkhardt/AIA/blob/9b4e98e810409067a477c4c798980ad27f163975/doc/CR019_AIA_to_RAIkeep_WordCase_Seams_and_Placement.md)

RAIkeep 4.2.6 is a coordinated patch across all seven packages.

### CR019 changes

- `WordCase`, `StringHelper`, `WordSplit`, `CamelSplit`, and `ToTitle` now live
  canonically in the dependency-light RaiUtils package.
- RaiUtils adds `WordSeams()`, returning lossless UTF-16 soft-wrap positions
  without altering, normalizing, or validating the supplied text.
- The normative rules cover Pascal/camel joins, acronym endings, digit runs,
  compound separators, structured labels, repeated delimiters, and apostrophe
  preservation.
- Unicode-aware text-element traversal protects surrogate pairs and combining
  sequences and recognizes uppercase German and Portuguese characters at seam
  boundaries.
- RaiImage consumes the RaiUtils implementation and retains only CLR-safe
  compatibility facades for its former public binary names. Legacy facade
  methods are deliberately not extensions, preventing ambiguous extension
  resolution when both namespaces are imported.
- HTML remains a consumer concern: web clients slice the original at the
  returned offsets and insert real `<wbr />` elements.

### Compatibility

- Existing compiled `RaiImage.WordCase` and static
  `RaiImage.StringHelper` calls continue to resolve through compatibility
  facades.
- Recompiled extension-method callers add `using RaiUtils;`, as accepted in
  CR019.
- The operation is a character-preserving display projection. It does not
  define an identifier grammar or convert structured labels into identifiers.

### Verification

- Focused RaiUtils CR019 coverage: 29 passed, 0 failed, 0 skipped.
- Focused RaiImage compatibility coverage: 3 passed, 0 failed, 0 skipped.
- Seven complete package suites: 517 passed, 0 failed, 0 skipped:
  OsLibCore 111, RaiUtils 51, RaiImage 112, RaiDiagram 34, JsonPit 156,
  ImgSeeder 16, and PitSeeder 37.
- The RaiDiagram suite ran with the real PlantUML CLI required and available;
  none of its integration tests were skipped.
- JsonPit's full release suite included its two isolated live Mzansi tests.
- The final coordinated Release build completed with zero errors and zero
  warnings.
- An unchanged consumer assembly compiled against the published 4.2.5
  `RaiImage.WordCase` and `RaiImage.StringHelper` signatures ran successfully
  against the prepared 4.2.6 binaries, proving the intended binary bridge.
- All seven 4.2.6 NuGet packages were packed locally. Package identities,
  embedded READMEs, binaries, and exact 4.2.6 dependency metadata were
  inspected without publishing.
- Markdown document-link and whitespace validation passed.

RAI retains the manual tag and publication gate. These notes do not authorize
the implementing agent to start the release chain.

---

## 4.2.5

**Status:** Prepared and verified; not published
**Accepted request:**
[`CR017_AIA_to_RAIkeep_Pits_Point_in_Time_Export.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR017_AIA_to_RAIkeep_Pits_Point_in_Time_Export.md)
**AIA proposal:**
[`CR017_AIA_to_RAIkeep_Pits_Point_in_Time_Export.md`](https://github.com/Burkhardt/AIA/blob/923cbddbefd0c69730a99746bedd16f150397050/doc/CR017_AIA_to_RAIkeep_Pits_Point_in_Time_Export.md)
**AIA Step 3 confirmation:**
[`CR017_Accepted_Pits_Point_in_Time_Export.md`](https://github.com/Burkhardt/AIA/blob/1394850b5fd8fc77e74a9e9fa28903d333c87aa7/doc/CR017_Accepted_Pits_Point_in_Time_Export.md)

RAIkeep 4.2.5 is a coordinated, backward-compatible patch across all seven
packages.

### CR017 changes

- `pits export` accepts optional `--at` for single-pit and WWWA targets through
  both `--json` and `--out-dir`.
- Offset-explicit timestamps are normalized to UTC and evaluated inclusively.
- Projection delegates to JsonPit's existing historical engine over all
  history available to the invocation.
- Point-in-time output uses the strict `_export`/`data` envelope with distinct
  `at` and `exported` UTC timestamps.
- No-`--at` exports retain their established unwrapped array/object shape.
- WWWA projection builds its lookup from four independently projected pits;
  missing targets remain safely unresolved at the source reference.
- OsLibCore exposes the same capability through optional
  `PitsExportRequest.At` with exact argument tokenization.

### Temporal and compatibility boundary

- `at` is the requested event-time cutoff. `exported` is when the command built
  the document from history then available.
- `exported` is not a distributed synchronization barrier or a completeness
  guarantee. The same `at` can yield a different result after late or backdated
  history arrives.
- Items not yet created, or deleted at the cutoff, are omitted.
- Existing output filenames remain unchanged because provenance is stored in
  the point-in-time document.
- CR016 Unicode-safe ImageTree behavior and CR015 nested deletion behavior
  carry forward unchanged.

### Verification

- Coordinated Release build: passed (all 14 solution projects).
- OsLibCore: 111 tests passed.
- RaiUtils: 22 tests passed.
- RaiImage: 119 tests passed.
- RaiDiagram: 34 tests passed through the real PlantUML integration path.
- JsonPit: all 156 tests passed (154 local/configured cases plus both isolated
  live Nkosikazi/Mzansi synchronization scenarios).
- ImgSeeder: 16 tests passed.
- PitSeeder: 37 tests passed, including 14 focused CR017 cases.

RAI retains the manual tag and publication gate. These notes do not authorize
the implementing agent to start the release chain.

---

## 4.2.4

**Status:** Prepared source and verification candidate; not published  
**Accepted request:**
[`CR016_AIA_to_RAIkeep_RaiImage_Unicode_Normalization_Bucketing.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR016_AIA_to_RAIkeep_RaiImage_Unicode_Normalization_Bucketing.md)  
**AIA proposal:**
[`CR016_AIA_to_RAIkeep_RaiImage_Unicode_Normalization_Bucketing.md`](https://github.com/Burkhardt/AIA/blob/55e9820f47a67ef0bd0ec8902c2b90f71ed0a430/doc/CR016_AIA_to_RAIkeep_RaiImage_Unicode_Normalization_Bucketing.md)  
**AIA Step 3 confirmation:**
[`CR016_Accepted_RaiImage_Unicode_Normalization_Bucketing.md`](https://github.com/Burkhardt/AIA/blob/0c0b22b8a038112a078974172688f7839c80ce0d/doc/CR016_Accepted_RaiImage_Unicode_Normalization_Bucketing.md)

RAIkeep 4.2.4 is a coordinated, backward-compatible patch across all seven
packages.

### CR016 changes

- RaiImage canonicalizes ImageTree-owned subscriber names, item identifiers,
  templates, filenames, route values, and typed text artifacts to Unicode NFC.
- Caller-provided ImageTree roots retain their original filesystem spelling.
- 3x3, 8x2, and canonical-name bucket widths count Unicode text elements rather
  than UTF-16 code units.
- Reads resolve legacy NFC, NFD, and mixed-normalization directories and files
  segment by segment without renaming them.
- Canonically ambiguous directories or source files fail explicitly with
  `RaiImageIOException`.
- SVG joins RaiImage's default source lookup extensions.
- Filesystem traversal uses the established OsLib `RaiPath`/`RaiFile` boundary.

### Compatibility

- Existing ASCII ImageTree placement is unchanged.
- Existing non-ASCII trees remain readable even when historical directory
  levels use different canonical Unicode representations.
- New outputs use RaiImage's canonical NFC logical spelling; APFS/HFS may expose
  a filesystem-normalized spelling while remaining canonically reopenable.
- The accepted CR015 tombstone, delete-command, and typed CLI contracts carry
  forward unchanged.
- No identity subsystem, package removal, CLI syntax change, or raw process
  boundary is introduced.

### Verification

- Coordinated Release build: passed (all 14 solution projects).
- OsLibCore: 110 tests passed.
- RaiUtils: 22 tests passed.
- RaiImage: 119 tests passed, including 15 dedicated CR016 cases.
- RaiDiagram: 34 tests passed through the real PlantUML integration path.
- JsonPit: all 156 tests passed (154 local/configured cases plus both isolated
  live Nkosikazi/Mzansi synchronization scenarios).
- ImgSeeder: 16 tests passed.
- PitSeeder: 23 tests passed.

RAI retains the manual tag and publication gate. These notes do not authorize
the implementing agent to start the release chain.

---

## 4.2.3

**Status:** Prepared source and verification candidate; not published  
**Accepted request:**
[`CR015_AIA_to_RAIkeep_Nested_Property_Tombstones_and_CLI_Delete.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR015_AIA_to_RAIkeep_Nested_Property_Tombstones_and_CLI_Delete.md)  
**AIA Step 3 confirmation:**
[`CR015_Accepted_Nested_Property_Tombstones_and_CLI_Delete.md`](https://github.com/Burkhardt/AIA/blob/260dbe73e3a0603485b8839416c46c58853493cb/doc/CR015_Accepted_Nested_Property_Tombstones_and_CLI_Delete.md)

RAIkeep 4.2.3 is a coordinated, backward-compatible patch across all seven
packages.

### CR015 changes

- JsonPit recursively applies null property tombstones at arbitrary object depth.
- Projected reads and exports omit tombstoned nested properties and recursively
  prune parent objects left empty by the mutation.
- `PitItem.DeletePropertyPath(...)` provides explicit dot-path traversal while
  `DeleteProperty(...)` retains literal top-level property-name semantics.
- Historical `.pit` fragments remain append-only, including the null markers
  required for time travel and audit integrity.
- PitSeeder adds `pits delete-property` and `pits delete-item` with the existing
  pit-root, configured-cloud, no-logo, debug, and process-window options.
- OsLibCore adds typed `PitsDeletePropertyRequest` and
  `PitsDeleteItemRequest` builders plus synchronous/asynchronous execution.
- Delete arguments remain discrete process tokens; malformed mandatory values
  are rejected before process start.

### Compatibility

- `-n` continues to mean `--nologo`; delete commands always persist accepted
  mutations.
- The coordinated 4.2.2 recovery, diagram, image, exception, and tool-wrapper
  contracts carry forward unchanged.
- No package, identity subsystem, raw process boundary, or legacy CLI removal is
  introduced.

RAI retains the manual tag and publication gate. These notes do not authorize
the implementing agent to start the release chain.

Release verification: the coordinated Release build succeeded; OsLib passed
110 tests, RaiUtils 22, RaiImage 104, RaiDiagram 34, ImgSeeder 16, and
PitSeeder 23. JsonPit passed all 156 tests, including configured persistence and
remote scenarios.

---

## 4.2.2

**Status:** Released
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

### Boundary changes

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

### Compatibility and carried behavior

- JsonPit retains the no-finalizer-I/O recovery contract and weak registry
  cleanup that makes abandoned canonical paths reopenable.
- ImgSeeder and PitSeeder retain their 4.2.1 Nerd Font help improvements.
- ImgSeeder and PitSeeder continue testing their own CLI behavior and provide
  minimal real-CLI wrapper smoke checks; OsLib tests wrapper validation,
  forwarding, result capture, timeout, cancellation, and launch failures.
- Package-only restore validation remains mandatory before every release tag.

### Release process

RAI manually starts `scripts/release-chain.sh 4.2.2` after all seven prepared
child commits and their exact umbrella submodule pointers are committed. The
script publishes in dependency order and waits for exact NuGet visibility.

These notes do not authorize tagging or publication.

### Verification result

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

---

## 4.2.0

**Status:** Prepared source and verification candidate; not published
**Change request:** `CR009_AIA_to_RAIkeep_RaiDiagram_Package.md`

RAIkeep 4.2.0 introduces RaiDiagram and expands the coordinated chain from six
to seven package repositories while preserving the CR008 and JsonPit lifecycle
contracts released in 4.1.0.

### RaiDiagram

- Adds the public, domain-neutral RaiDiagram package and repository.
- Uses JSON5 `.raid` manifests to separate semantic model references,
  projection/filter intent, and visual presentation.
- Provides `IDiagramModelProvider`, model snapshots, structured reconciliation,
  and semantic/presentation hashes for agent-supported stale-diagram evaluation.
- Compiles role-first UML26 diagrams to PlantUML and renders through RaiImage.
- Embeds authoritative `.raid` identity, schema, and semantic hash provenance in
  generated SVG.
- Does not depend on AIA, WWWA, or JsonPit; AIA owns its provider implementation.

### Existing packages

- OsLibCore, RaiUtils, RaiImage, and JsonPit carry their 4.1.0 behavior forward
  on the coordinated 4.2.0 line.
- RaiImage and JsonPit now honor `UseLocalRAIkeepSources=false`, closing a release
  validation gap that could otherwise substitute sibling project sources.
- ImgSeeder and PitSeeder align fallback dependencies and CLI version output on
  4.2.0 without other CLI behavior changes.

### Release process

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

### Verification result

- Focused JsonPit finalizer regression: 1 passed.
- Complete Release suites: OsLibCore 81, RaiUtils 22, RaiImage 97, RaiDiagram 20,
  JsonPit 146, ImgSeeder 15, and PitSeeder 20 tests passed.
- A disposable local NuGet feed restored and packed all seven 4.2.0 packages in
  release order with `UseLocalRAIkeepSources=false`; generated dependency
  metadata resolves the coordinated 4.2.0 package graph.

---

## 4.1.0

**Status:** Source and verification candidate; not published  
**Change request:** `CR008_AIA_to_RAIkeep_OsLib_RaiImage_Boundary_Enhancements.md`

RAIkeep 4.1.0 strengthens the operating-system and image boundaries requested
by AIA while preserving `Os.Config` as the runtime source of truth.

### OsLibCore

- `Os.TempDir` remains the configured `RaiPath`; it was not removed from 4.0.
- First initialization now creates, observes, and removes an OsLib `TmpFile` in
  the configured directory.
- Initialization fails fast when that probe cannot be written. The implementation
  does not mutate `Os.Config`, substitute an environment override, or silently
  fall back to another directory after configuration has been resolved.
- `RaiPathException` and `RaiPathNotFoundException` provide path-specific failures.
- `RaiFile.WriteFromAsync(IAsyncEnumerable<byte[]>, CancellationToken)` provides
  chunked ingestion without exposing `System.IO.Stream` to consumers.

### RaiUtils

- Added the cross-package `RaiException` base class.
- Added `ToolNotFoundException` for missing external executables.

### RaiImage

- Added `RaiImageIOException` and `RaiImageNotFoundException`.
- Missing directories/paths use `RaiPathNotFoundException`; a missing image in an
  existing location uses `RaiImageNotFoundException`.
- Missing ImageMagick and PlantUML executables use `ToolNotFoundException` rather
  than `System.IO.FileNotFoundException`.
- Image files inherit and verify the async byte-chunk ingestion boundary.

The names differ intentionally from the originally submitted
`RaiImageFileNotFoundException`: RAIkeep and AIA subsequently agreed to separate
missing paths from missing images.

### JsonPit internal regression included with the work

- Abandoned `Pit` instances are no longer retained by `FileSystemWatcher` event
  handlers or debounce tasks.
- Watcher dispatch uses weak ownership, allowing forced collection to remove the
  weak registry entry and make the generated path reopenable.
- The finalizer remains free of recovery publication, watcher disposal, and
  filesystem I/O.

### Verification

Focused CR008 tests and the relevant OsLibCore, RaiUtils, RaiImage, and JsonPit
Release suites are required before release. The release gate remains explicit:
these notes do not authorize a tag, push, NuGet publication, or package-version
change.

---

## 4.0.1

**Date:** 2026-08-10
**Author / Delivering Agent:** RAIkeep Dev Agent
**Delivered Version:** v4.0.1
**Target Consumers:** AfricaStage, AIA
**Status:** Prepared — publication approval pending

### 1. Summary

RAIkeep v4.0.1 delivers the coordinated CR006 command-first CLI transition.
Functional changes are confined to PitSeeder/`pits` and ImgSeeder/`iorg`;
OsLibCore, RaiUtils, RaiImage, and JsonPit participate as synchronized patch
packages without runtime changes.

### 2. Resolved Change Requests (CRs)

- [`CR006_AfricaStage_to_RAIkeep_CliSubcommands.md`](https://github.com/Burkhardt/AIA/blob/main/doc/CR006_AfricaStage_to_RAIkeep_CliSubcommands.md) — command-first `pits` and `iorg` interfaces with a documented 4.x-to-5.x transition.

### 3. Root Cause Analysis & Technical Resolution

Both CLIs inferred operations from flat option combinations, producing crowded
help and late collision handling. Command-first dispatch now isolates operation
syntax while automatically retaining the established flat parser for mature
workflows. Both paths call the same handlers.

The recent event-audit flags are excluded from legacy compatibility and move
directly to `pits audit`. The legacy parsers are scheduled for removal in
`5.x.x` after command-surface parity and consumer validation.

### 4. Public Contract & API / Package Changes

- Coordinated package line: `4.0.1` across all six packages.
- Functional CLI changes: ImgSeeder and PitSeeder only.
- Library APIs and behavior: unchanged from `4.0.0`.
- Transition policy: [`CLI-PARSER-TRANSITION-4.x-TO-5.x.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CLI-PARSER-TRANSITION-4.x-TO-5.x.md).

### 5. Validation & Acceptance Evidence

- Current coordinated Release revalidation: **375 passed, 1 failed, 0 skipped**.
- Component totals: OsLib 80, RaiUtils 21, RaiImage 94, JsonPit 146,
  ImgSeeder 15, and PitSeeder 20.
- The sole current failure is JsonPit's existing finalizer/GC ownership test,
  `Finalizer_PerformsNoRecoveryPublicationOrFilesystemIO_AndPathBecomesReopenable`;
  it reproduces in isolation. JsonPit has no source change in this release beyond
  synchronized version and dependency metadata. The six-package release-chain
  workflows build and pack rather than execute local cloud/SSH tests.

### 6. Upgrade & Consumption Instructions

1. Upgrade the six-package RAIkeep line together to v4.0.1 after publication.
2. Migrate scripts to the command syntax documented in the PitSeeder and
   ImgSeeder v4.0.1 release notes.
3. Independently validate AfricaStage/AIA integration behavior.
4. Publish `CR006_Accepted_CliSubcommands.md` or
   `CR006_Rejected_CliSubcommands.md` from the requester side.

---

## 4.0.0

**Date:** 2026-08-06  
**Author / Delivering Agent:** RAIkeep Dev Agent  
**Delivered Version:** v4.0.0  
**Target Consumers:** AIA (Bob, Adele), AfricaStage  
**Status:** Publishing in progress (NuGet)

---

### 1. Summary

RAIkeep v4.0.0 delivers the coordinated CR003 concurrency and persistence contract
across the core package line (`OsLibCore`, `RaiUtils`, `RaiImage`, `JsonPit`,
`ImgSeeder`, `PitSeeder`).

Primary outcome:
- The confirmed concurrent save/add persistence race is fixed.
- Multi-thread, multi-process, and multi-machine cloud-synced behavior is now
  explicitly defined and tested.
- Exact-process master ownership, deterministic merge ordering, and durable
  recovery/audit paths are implemented.

---

### 2. Resolved Change Requests (CRs)

- [`CR003_RAI_to_RAIkeep_JsonPit-concurrency-contract-and-persistence-races.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR003_RAI_to_RAIkeep_JsonPit-concurrency-contract-and-persistence-races.md) — fully addressed in coordinated v4.0.0 implementation and release line.

---

### 3. Root Cause Analysis & Technical Resolution

#### Root cause confirmed

Concurrent `Save` and `Add` operations could race during persistence snapshot
materialization, producing unstable read/serialization behavior and a silent-loss
window when newer live fragments were validated against older persisted snapshots.

#### Resolution implemented

- Introduced a brief state/snapshot gate for safe point-in-time persistence capture.
- Released the gate before cloud I/O so concurrent writers are not serialized behind
  file operations.
- Validated only fragments actually included in the successfully persisted snapshot.
- Enforced exact-PID master ownership semantics for lease renewal and handoff.
- Added deterministic equal-timestamp ordering and idempotent replay handling.
- Added collision-safe hashed change-file naming and two-stage cleanup grace.
- Added live split-master recovery with durable, structured event evidence.
- Standardized OsLib in-place save contract to avoid delete/rename path gaps during
  rewrite cycles.

Detailed technical implementation is documented in component release notes:
- [`OsLib_RELEASE_NOTES_4.0.0.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/OsLib_RELEASE_NOTES_4.x.md#400)
- [`RaiUtils_RELEASE_NOTES_4.0.0.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/RaiUtils_RELEASE_NOTES_4.x.md#400)
- [`RaiImage_RELEASE_NOTES_4.0.0.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/RaiImage_RELEASE_NOTES_4.x.md#400)
- [`JsonPit_RELEASE_NOTES_4.0.0.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/JsonPit_RELEASE_NOTES_4.x.md#400)
- [`ImgSeeder_RELEASE_NOTES_4.0.0.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/ImgSeeder_RELEASE_NOTES_4.x.md#400)
- [`PitSeeder_RELEASE_NOTES_4.0.0.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/PitSeeder_RELEASE_NOTES_4.x.md#400)

---

### 4. Public Contract & API / Package Changes

#### Package line delivered

- `OsLibCore` v4.0.0
- `RaiUtils` v4.0.0
- `RaiImage` v4.0.0
- `JsonPit` v4.0.0
- `ImgSeeder` v4.0.0
- `PitSeeder` v4.0.0

#### Contract-level changes of note

- JsonPit persistence boundary and validation semantics are now explicit and
  enforced under concurrency.
- One live public `Pit` instance per canonical path per process is enforced.
- Exact-process master lease behavior is enforced across process windows.
- `pits --events` audit mode exposes durable recovery events in a read-only path.

#### Breaking/operational compatibility note

- Shared-pit participants must be upgraded together to v4.0.0 package/tool line.
  Pre-4.0.0 participants can fail on v4.0.0 hashed change-file artifacts.

---

### 5. Validation & Acceptance Evidence

- Umbrella acceptance run (non-SSH scope): **359 passed, 0 failed, 0 skipped**.
- Release build completed with **0 warnings**.
- Two-server split-master cloud scenario (OneDrive; Nkosikazi <-> Mzansi): passed,
  including loser recovery via validated hashed change files and durable event trail.
- Dynamic master/non-master remote scenario: passed standalone repeatedly.
- New explicit concurrency suites added and passing, including:
  `InProcessConcurrencyTests`, `MultiPitInstanceConcurrencyTests`,
  `MultiProcessConcurrencyTests`, `ReadDuringWriteTests`,
  `SplitMasterRecoveryTests`, `RemoteCloudConcurrencyTests`,
  `EventsAuditModeTests`, `TextFileSaveContractTests`, `EventFileTests`.

---

### 6. Upgrade & Consumption Instructions

1. Update AIA package references in `Directory.Packages.props` to the coordinated
   v4.0.0 line.
2. Restore and execute:
   - `dotnet test AIA.slnx`
   - `pnpm --dir aia-workbench build`
3. Validate CR003 acceptance criteria against live behavior, contract semantics,
   and operational notes above.
4. If accepted, create the formal consumer signoff artifact using the agreed
   evaluation template (`CR003_Accepted_<Topic>.md`).

---

### Publication Notice

RAIkeep will notify AIA immediately when all six v4.0.0 NuGet packages are
visible and the sequential publication chain has completed.
