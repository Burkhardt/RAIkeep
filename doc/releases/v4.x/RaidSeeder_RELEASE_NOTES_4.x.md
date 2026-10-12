# RaidSeeder Release Notes 4.x

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
CR052 adds source-located PlantUML preflight diagnostics, object/deployment import, and complete derivation before output writes. The bounded legacy import-xmi/import-otw commands support diagram listing and selection. PlantUML remains the active external authoring format.

### Coordinated Dependencies
- Aligned with RAIkeep synchronized `4.5.5` line.

---

## 4.5.4

Participates in the coordinated RAIkeep 4.5.4 patch release for the Amafu
`init --create-links` configuration-path fix. Package versions and applicable
internal dependency versions are aligned to 4.5.4. No runtime behavior changes
are introduced in RaidSeeder by this patch.

See [Amafu 4.5.4 release notes](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/Amafu_RELEASE_NOTES_4.x.md#454) for the fix and
configuration migration instructions.

---

## 4.5.3

Coordinated 4.5.3 release aligning CLI and package dependencies with RaiDiagram 4.5.3. Public commands and behavior are unchanged.

Validation and release handoff: [RAIkeep 4.5.3](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/RAIkeep_RELEASE_NOTES_4.x.md#453). Preparation does not publish this package.

---

## 4.5.2

Coordinated 4.5.2 release; runtime behavior is unchanged. Internal package dependencies, where present, align to 4.5.2.

Validation and release handoff: [RAIkeep 4.5.2](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/RAIkeep_RELEASE_NOTES_4.x.md#452). Preparation does not publish this package.

---

## 4.5.0

Coordinated 4.5.0 dependency alignment; raid reports version 4.5.0.

All package and internal dependency versions are aligned to 4.5.0, coordinating live object reference semantics, sparse mutation tracking, and automated release validation gating across the entire RAIkeep platform.

Validation and release handoff: [RAIkeep 4.5.0](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/RAIkeep_RELEASE_NOTES_4.x.md#450). Preparation does not publish this package.

---

## 4.4.8

Coordinated 4.4.8 dependency alignment; raid reports version 4.4.8.

All package and internal dependency versions are aligned to 4.4.8. The version intentionally skips C# 4.4.7 to align the next coordinated release with jsonpit-python; Python implementation and publication remain with its maintainer.

Validation and release handoff: [RAIkeep 4.4.8](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/RAIkeep_RELEASE_NOTES_4.x.md#448). Preparation does not publish this package.

---

## 4.4.6

Participates in the synchronized 4.4.6 dependency line; reports `raid v4.4.6`. Diagram artifact behavior is unchanged.

This is part of the coordinated nine-package [CR049](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR/CR049_AIA_and_jsonpit_to_RAIkeep_Live-ID-Validation_and_Zip-Image-Import.md) release. Package versions and fallback dependencies align at 4.4.6.

See [RAIkeep release notes](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/RAIkeep_RELEASE_NOTES_4.x.md#446) for shared behavior, validation, and the manual publication gate.

---

## 4.4.5

RaidSeeder participates unchanged in the synchronized RAIkeep v4.4.5 release for accepted [`CR047_jsonpit_and_pits_Require-Existing-Patch-Flag-and-Seed-Commit-Count.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR/CR047_jsonpit_and_pits_Require-Existing-Patch-Flag-and-Seed-Commit-Count.md). The `raid` artifact-management command remains unchanged.

---

## 4.4.4

RaidSeeder participates unchanged in the synchronized RAIkeep v4.4.4 release for accepted [`CR044_AIA_and_jsonpit_to_RAIkeep_Auto-Detect-Cloud-Drives-and-Init-Config.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR/CR044_AIA_and_jsonpit_to_RAIkeep_Auto-Detect-Cloud-Drives-and-Init-Config.md). The `raid` command continues to manage authoritative `.raid` manifests and their `.puml`/`.svg` derivatives.

---

## 4.4.3

RaidSeeder and `raid` 4.4.3 participate unchanged in the synchronized
eight-package delivery of accepted
[`CR043_AfricaStage_to_RAIkeep_Improve-pits-seed-array-error-message.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR043_AfricaStage_to_RAIkeep_Improve-pits-seed-array-error-message.md).

Import, export, refresh, validate, cloud addressing, and hydratable/plain SVG
behavior remain unchanged. Fallback dependencies align to RaiDiagram 4.4.3.

---

## 4.4.2

RaidSeeder and `raid` 4.4.2 participate unchanged in the synchronized
eight-package delivery of accepted
[`CR040_AIA_to_RAIkeep_and_jsonpit_Prohibit-Read-Modify-Write.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR040_AIA_to_RAIkeep_and_jsonpit_Prohibit-Read-Modify-Write.md)
and
[`CR041_jsonpit_to_RAIkeep_Restore-Clean-Change-Filenames.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR041_jsonpit_to_RAIkeep_Restore-Clean-Change-Filenames.md).

Import, export, refresh, validate, cloud addressing, and hydratable/plain SVG
behavior remain unchanged. Fallback dependencies align to RaiDiagram 4.4.2.

---

## 4.4.1

RaidSeeder 4.4.1 implements accepted
[`CR037_AIA_to_RAIkeep_RaidSeeder_Diagram_Artifact_Management.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR037_AIA_to_RAIkeep_RaidSeeder_Diagram_Artifact_Management.md).
It also implements accepted
[`CR037.1_AIA_to_RAIkeep_CLI_Global_Flag_and_Verb_Dispatch_Resilience.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR037.1_AIA_to_RAIkeep_CLI_Global_Flag_and_Verb_Dispatch_Resilience.md).

The repository and NuGet identity move from `RaidCli` to `RaidSeeder`; the
installed shell command remains `raid`. The CLI now provides `import`, `export`,
`refresh`, and `validate`, with polished Nerd Font help and iorg-aligned
`--cloud`, `--root`, `--app`, `--tenant`, and ItemTree addressing.

ItemId, Number, and NameExt remain separate. Export derives current `.raid`,
`.puml`, and/or hydratable/plain `.svg` from the authoritative manifest. Refresh
updates only stale or missing co-located derivatives. The v4.4.0 `RaidCli`
package and tag remain immutable; NuGet deprecation is a post-publication step.

Reserved verbs are now protected system keywords. Misplaced verbs fail before
artifact access with exit code `2` and an exact verb-first correction;
`-v`/`--version` takes immediate precedence at any argument position.
