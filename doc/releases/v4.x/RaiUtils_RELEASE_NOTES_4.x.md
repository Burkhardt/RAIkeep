# RaiUtils Release Notes 4.x

## 4.5.9

- Release version: `4.5.9`
- Coordination tag: `v4.5.9`

### Highlights
- Coordinated 4.5.9 version alignment; no package-local behavior change.

### Coordinated Dependencies
- Aligned with RAIkeep synchronized `4.5.9` line.

---

## 4.5.8

- Release version: `4.5.8`
- Coordination tag: `v4.5.8`

### Highlights
- Coordinated release aligned with the 4.5.8 synchronized platform line.

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
Coordinated package/dependency alignment to 4.5.5. No independent runtime behavior change in this component.

### Coordinated Dependencies
- Aligned with RAIkeep synchronized `4.5.5` line.

---

## 4.5.4

Participates in the coordinated RAIkeep 4.5.4 patch release for the Amafu
`init --create-links` configuration-path fix. Package versions and applicable
internal dependency versions are aligned to 4.5.4. No runtime behavior changes
are introduced in RaiUtils by this patch.

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

Coordinated 4.5.0 utility dependency; public behavior is unchanged.

All package and internal dependency versions are aligned to 4.5.0, coordinating live object reference semantics, sparse mutation tracking, and automated release validation gating across the entire RAIkeep platform.

Validation and release handoff: [RAIkeep 4.5.0](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/RAIkeep_RELEASE_NOTES_4.x.md#450). Preparation does not publish this package.

---

## 4.4.8

Coordinated 4.4.8 utility dependency; public behavior is unchanged.

All package and internal dependency versions are aligned to 4.4.8. The version intentionally skips C# 4.4.7 to align the next coordinated release with jsonpit-python; Python implementation and publication remain with its maintainer.

Validation and release handoff: [RAIkeep 4.4.8](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/RAIkeep_RELEASE_NOTES_4.x.md#448). Preparation does not publish this package.

---

## 4.4.6

Participates in the synchronized 4.4.6 dependency line. Existing word-case normalization remains authoritative for image names.

This is part of the coordinated nine-package [CR049](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR/CR049_AIA_and_jsonpit_to_RAIkeep_Live-ID-Validation_and_Zip-Image-Import.md) release. Package versions and fallback dependencies align at 4.4.6.

See [RAIkeep release notes](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/RAIkeep_RELEASE_NOTES_4.x.md#446) for shared behavior, validation, and the manual publication gate.

---

## 4.4.5

RaiUtils participates unchanged in the synchronized RAIkeep v4.4.5 release for accepted [`CR047_jsonpit_and_pits_Require-Existing-Patch-Flag-and-Seed-Commit-Count.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR/CR047_jsonpit_and_pits_Require-Existing-Patch-Flag-and-Seed-Commit-Count.md).

---

## 4.4.4

RaiUtils participates unchanged in the synchronized RAIkeep v4.4.4 release for accepted [`CR044_AIA_and_jsonpit_to_RAIkeep_Auto-Detect-Cloud-Drives-and-Init-Config.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR/CR044_AIA_and_jsonpit_to_RAIkeep_Auto-Detect-Cloud-Drives-and-Init-Config.md). Its public utility and exception APIs remain unchanged.

---

## 4.4.3

RaiUtils 4.4.3 participates unchanged in the synchronized eight-package
delivery of accepted
[`CR043_AfricaStage_to_RAIkeep_Improve-pits-seed-array-error-message.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR043_AfricaStage_to_RAIkeep_Improve-pits-seed-array-error-message.md).

Its exception, JSON, and Unicode-safe text APIs remain unchanged. This package
aligns the coordinated dependency line at 4.4.3.

---

## 4.4.2

RaiUtils 4.4.2 participates unchanged in the synchronized eight-package
delivery of accepted
[`CR040_AIA_to_RAIkeep_and_jsonpit_Prohibit-Read-Modify-Write.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR040_AIA_to_RAIkeep_and_jsonpit_Prohibit-Read-Modify-Write.md)
and
[`CR041_jsonpit_to_RAIkeep_Restore-Clean-Change-Filenames.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR041_jsonpit_to_RAIkeep_Restore-Clean-Change-Filenames.md).

Its exception, JSON, and Unicode-safe text APIs remain unchanged. This package
aligns the coordinated dependency line at 4.4.2.

---

## 4.4.1

RaiUtils 4.4.1 participates unchanged in the synchronized eight-package
delivery of accepted
[`CR037_AIA_to_RAIkeep_RaidSeeder_Diagram_Artifact_Management.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR037_AIA_to_RAIkeep_RaidSeeder_Diagram_Artifact_Management.md).
The coordinated release also carries accepted
[`CR037.1_AIA_to_RAIkeep_CLI_Global_Flag_and_Verb_Dispatch_Resilience.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR037.1_AIA_to_RAIkeep_CLI_Global_Flag_and_Verb_Dispatch_Resilience.md).

Its existing exception and Unicode-safe text boundaries remain available on the
coordinated 4.4.1 dependency line.

---

## 4.4.0

RaiUtils 4.4.0 participates unchanged in the synchronized eight-package
delivery of accepted
[`CR036_AIA_to_RAIkeep_Raid_CLI.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR036_AIA_to_RAIkeep_Raid_CLI.md).

---

## 4.3.2

RaiUtils 4.3.2 participates unchanged in the coordinated seven-package RAIkeep
v4.3.2 delivery of accepted
[CR027](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR027_AIA_to_RAIkeep_ClassDiagram_Generalization_and_SetSuperClass.md).
Its public API is unchanged from 4.3.1. Publication remains behind RAI's manual
release-chain gate.

---

## 4.3.1

RaiUtils 4.3.1 participates unchanged in the coordinated seven-package
RAIkeep v4.3.1 delivery of accepted
[CR026](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR026_AIA_to_RAIkeep_Diagram_Builder_Revision_Fidelity_and_Reference_Stereotypes.md).
Its public API is unchanged from 4.3.0. Publication remains behind RAI's manual
release-chain gate.

---

## 4.3.0

RaiUtils 4.3.0 participates in the coordinated CR023, CR024, and
[CR025](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR025_AIA_to_RAIkeep_Typed_Raid_Builders_and_Deterministic_ItemTree_Emission.md)
release line. Its CR019 word-case/seam helpers and domain-exception foundation
are unchanged. Package versions align on 4.3.0; the unpublished 4.2.11
preparation is superseded. Publication remains behind RAI's manual gate.

---

## 4.2.11

> **Superseded before publication.** This prepared package line was not released;
> its changes are carried into v4.3.0.

RaiUtils participates unchanged in the coordinated RAIkeep 4.2.11 release. Its
word-seam, conversion, and shared exception APIs remain unchanged from 4.2.10.

---

## 4.2.10

RaiUtils participates unchanged in the coordinated RAIkeep 4.2.10 release. Its
accepted CR019 helpers and exception boundaries remain unchanged from 4.2.9.

---

## 4.2.9

RaiUtils participates unchanged in the coordinated RAIkeep 4.2.9 incident-
correction release for accepted
[CR022](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR022_RAI_to_RAIkeep_Cloud_Safe_In_Place_Filesystem_Invariant.md).
Its public API and runtime behavior remain unchanged from 4.2.8.

---

## 4.2.8

RaiUtils participates unchanged in the coordinated RAIkeep 4.2.8 release for
accepted [CR021](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR021_RAI_to_RAIkeep_JsonPit_Durable_Cleanup_Receipts_and_Pits_Coordination.md).
Its public API and runtime behavior remain unchanged from 4.2.7.

---

## 4.2.7

RaiUtils participates in the coordinated RAIkeep 4.2.7 release implementing
accepted [CR020](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR020_RAI_to_RAIkeep_Iorg_Read_Only_Wildcard_Listing.md).

- Public RaiUtils behavior is unchanged from 4.2.6.
- The package remains the canonical home for RAIkeep exceptions, word-case conversion, and Unicode-safe word seams.

Tagging and NuGet publication remain behind RAI's manual release gate.

---

## 4.2.6

Implements accepted CR019 in the coordinated RAIkeep 4.2.6 release.

- Makes `RaiUtils.WordCase` and `RaiUtils.StringHelper` the canonical home for
  general word-case conversion and splitting.
- Adds lossless `WordSeams()` UTF-16 offsets for display soft-wrapping.
- Applies the normative acronym, case-transition, digit, separator,
  apostrophe, and whitespace rules.
- Traverses Unicode text elements so surrogate pairs and combining sequences
  are never split.
- Adds German, Portuguese, structured-label, repeated-separator, and exact
  round-trip regression coverage.

---

## 4.2.5

Coordinated dependency release for accepted CR017.

- Keeps the existing shared exception surface unchanged.
- Provides the aligned 4.2.5 dependency line for downstream packages.

Release verification: 22 RaiUtils Release tests passed.

RAI retains the manual coordinated release gate; no tag or publication is
authorized by these notes.

---

## 4.2.4

Coordinated dependency release for accepted CR016.

- Retains the shared `RaiException` and `ToolNotFoundException` contracts.
- Introduces no RaiUtils public API behavior change.

Release verification: 22 RaiUtils Release tests passed.

RAI retains the manual coordinated release gate; no tag or publication is
authorized by these notes.

---

## 4.2.3

Coordinated dependency release for accepted CR015.

- Carries `RaiException` and `ToolNotFoundException` forward unchanged.
- Remains dependency-light and contains no CLI process wrapper.
- Aligns the shared package version used by the coordinated RAIkeep package
  graph.

RAI retains the manual coordinated release gate; no tag or publication is
authorized by these notes.

Release verification: 22 RaiUtils Release tests passed.

---

## 4.2.2

Coordinated dependency release for the accepted CR008, CR009, and CR010 RAIkeep
boundaries.

- Carries `RaiException` and `ToolNotFoundException` forward unchanged.
- Remains dependency-light and independent of OsLib, RaiImage, and RaiDiagram.
- Aligns the shared package line used by RaiImage, RaiDiagram, JsonPit, and
  ImgSeeder on 4.2.2.
- CR014 introduces no process wrapper in RaiUtils and preserves its
  dependency-light boundary; tool execution remains in OsLib and RaiImage.

Released as part of the coordinated RAIkeep v4.2.2 release.

Release verification: 22 RaiUtils Release tests passed.

---

## 4.2.0

Coordinated release for the seven-package RAIkeep 4.2 line.

- Carries the dependency-light `RaiException` base and `ToolNotFoundException`
  boundary introduced for CR008 forward unchanged.
- Provides the shared exception foundation used by RaiImage and the new
  RaiDiagram package.
- Updates package metadata and documentation for the coordinated 4.2.0 line.

No intentional RaiUtils runtime behavior change is introduced after 4.1.0.

Release verification: 22 RaiUtils Release tests passed.

---

## 4.1.0

Implements the shared exception portion of
`CR008_AIA_to_RAIkeep_OsLib_RaiImage_Boundary_Enhancements.md`.

- Adds `RaiException` as the dependency-light base for public RAIkeep domain
  exceptions.
- Adds `ToolNotFoundException`, carrying stable tool-name and executable-path
  diagnostics for missing command-line dependencies.
- Establishes the shared exception boundary consumed by RaiImage and the
  upcoming RaiDiagram package.

Release verification: 22 RaiUtils Release tests passed.

---

## 4.0.1

**Date:** 2026-08-10
**Author / Delivering Agent:** RAIkeep Dev Agent
**Delivered Version:** v4.0.1
**Target Consumers:** RAIkeep package family, AfricaStage, AIA
**Status:** Prepared — publication approval pending

### 1. Summary

RaiUtils v4.0.1 is the synchronized utility package for the coordinated CR006
CLI patch line. It contains no RaiUtils API or behavior change from v4.0.0.

### 2. Resolved Change Requests (CRs)

- [`CR006_AfricaStage_to_RAIkeep_CliSubcommands.md`](https://github.com/Burkhardt/AIA/blob/main/doc/CR006_AfricaStage_to_RAIkeep_CliSubcommands.md) — synchronized package participation only; implementation is owned by ImgSeeder and PitSeeder.

### 3. Root Cause Analysis & Technical Resolution

RAIkeep packages are released as one coordinated version line. RaiUtils moves
to v4.0.1 to preserve that line; no source-level resolution was required here.

### 4. Public Contract & API / Package Changes

- Package version: `4.0.1`.
- Public API and runtime behavior: unchanged from `4.0.0`.

### 5. Validation & Acceptance Evidence

- RaiUtils.Tests: **21 passed, 0 failed, 0 skipped** in the coordinated run.

### 6. Upgrade & Consumption Instructions

Consume RaiUtils v4.0.1 with the other five coordinated RAIkeep v4.0.1 packages.

---

## 4.0.0

### Summary

`RaiUtils 4.0.0` is the coordinated dependency-alignment release for `OsLibCore 4.0.0`.

### Changes

- Updated package version and release metadata to `4.0.0`.
- Aligned the OsLibCore package baseline with `4.0.0`.
- Refreshed README, API documentation, centralized release-note links, and the class-diagram release marker.

### Compatibility

- No RaiUtils production API or behavior changed from `3.13.0`.
- Configuration behavior remains unchanged.

### Validation

- `RaiUtils.Tests`: `21` passed, `0` failed in the coordinated validation run.
- The umbrella `RAIkeep.slnx` build succeeds with the local `4.0.0` sources.

### Release sequencing

`RaiUtils` is second in the coordinated release chain. Its GitHub push/tag must wait for OsLibCore workflow success, flat-container visibility, and the full `330`-second hold. `RaiImage` must wait for the same checks after RaiUtils publishes.
