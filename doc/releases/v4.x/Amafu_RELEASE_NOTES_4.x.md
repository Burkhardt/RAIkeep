# Amafu Release Notes 4.x

## 4.5.8

- Release version: `4.5.8`
- Coordination tag: `v4.5.8`

### Highlights
- Coordinated release aligned with the 4.5.8 synchronized platform line.
- Shortcut-first cloud storage resolution (CR057 Pillar 1).

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

Fixes `amafu init --create-links` so the generated `RAIkeep.json5` uses the
shortcuts it creates, instead of the original provider paths. For example,
`GoogleDriveRainer` now maps to `~/.CloudStorage/GoogleDriveRainer/`, and
`ICloudDrive` maps to `~/.CloudStorage/ICloudDrive/`.

```bash
amafu init --create-links --dry-run   # Preview the exact shortcut-based configuration
amafu init --create-links             # Create shortcuts and a new configuration
```

The same behavior applies to `init-config`. Dry runs create neither links nor
configuration files. Plain `amafu init` continues to use the detected physical
paths; `amafu detect --json` continues to report physical roots.

For an existing configuration, use `amafu reconcile` to preview the migration,
then `amafu reconcile --apply` to apply it with a backup. `init` still refuses
to overwrite an existing configuration unless `--force` is explicitly supplied.

### Verification

- Complete Amafu suite: 62 passed, 0 failed, 0 skipped.
- Release validation: 80 checks passed.
- Release-tool regression suite: 2 passed.

Regression coverage checks that preview and saved configuration match exactly
for both init commands, including two Google Drive accounts and iCloud Drive.
Every configured shortcut is checked against its intended target and used to
read a file from that target. Existing tests cover plain init, link conflicts,
JSON detection output, and configuration overwrite protection.

The C# packages and dependency versions are aligned to the coordinated 4.5.4
patch release. Publication is performed by the release chain.

---

## 4.5.3

CR051 adds multiple Google Drive and corporate OneDrive accounts, named
shortcuts, and optional provider/account metadata in detection JSON. Each
account independently prefers its data subfolder. Name collisions fail with
both roots reported; identical roots reached through aliases are deduplicated.
Dropbox and iCloud discovery are unchanged.

### Personal OneDrive and automation

Exactly one personal root is selected as `OneDrive`. An explicit
`--onedrive-personal <folder>` wins; otherwise a valid configured root wins;
otherwise the longest folder name wins, with highest numeric suffix and then
ordinal path order as tie breakers. Corporate roots remain configured.
Commands never prompt interactively.

`amafu reconcile` previews additional roots and a migration of configuration to
`~/.CloudStorage` paths. `--apply` creates a uniquely named backup and applies
changes, preserving unrelated JSON5 settings and default order. Existing
unavailable entries are retained. Only an explicit personal OneDrive selection
may repoint its verified configured link. No cloud data is moved or deleted.

### Compatibility

OsLib's matching CR051 change consumes every configured cloud-root label and
classifies symbolic shortcut paths, including new descendants. Deploy updated
OsLib consumers alongside Amafu before migrating configuration. PitSeeder
selection accepts account-qualified keys present in Cloud and DefaultCloudOrder.
Python/jpit parity remains Adele's verification responsibility.

### Verification

- Amafu: **60 passed, 0 failed, 0 skipped**.
- OsLib: **147 passed, 0 failed, 0 skipped**.
- PitSeeder: **87 passed, 0 failed, 0 skipped**.
- macOS ARM64 NativeAOT publish and read-only detection smoke test passed.
- Corporate OneDrive is covered by filesystem fixtures, not a live corporate account.

These notes describe prepared source changes, not a completed package publication
or a coordinated release-chain preflight. Python parity remains unverified here.

---

## 4.5.2

Adds `--create-links` to `detect` and `init` for provider shortcuts under `~/.CloudStorage`. Matching links are reused; conflicting paths are never overwritten. `--dry-run` writes nothing. Configuration and JSON detection output keep the real provider roots. No OsLib dependency or provider-data migration is introduced.

Validation and release handoff: [RAIkeep 4.5.2](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/RAIkeep_RELEASE_NOTES_4.x.md#452). Preparation does not publish this package.

---

## 4.5.0

Coordinated 4.5.0 release; cloud configuration behavior is unchanged.

All package and internal dependency versions are aligned to 4.5.0, coordinating live object reference semantics, sparse mutation tracking, and automated release validation gating across the entire RAIkeep platform.

Validation and release handoff: [RAIkeep 4.5.0](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/RAIkeep_RELEASE_NOTES_4.x.md#450). Preparation does not publish this package.

---

## 4.4.8

Coordinated 4.4.8 release; cloud configuration behavior is unchanged.

All package and internal dependency versions are aligned to 4.4.8. The version intentionally skips C# 4.4.7 to align the next coordinated release with jsonpit-python; Python implementation and publication remain with its maintainer.

Validation and release handoff: [RAIkeep 4.4.8](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/RAIkeep_RELEASE_NOTES_4.x.md#448). Preparation does not publish this package.

---

## 4.4.6

Participates in the synchronized 4.4.6 release; reports `amafu v4.4.6`. Cloud configuration behavior is unchanged.

This is part of the coordinated nine-package [CR049](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR/CR049_AIA_and_jsonpit_to_RAIkeep_Live-ID-Validation_and_Zip-Image-Import.md) release. Package versions and fallback dependencies align at 4.4.6.

See [RAIkeep release notes](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/RAIkeep_RELEASE_NOTES_4.x.md#446) for shared behavior, validation, and the manual publication gate.

---

## 4.4.5

Amafu participates unchanged in the synchronized RAIkeep v4.4.5 release for accepted [`CR047_jsonpit_and_pits_Require-Existing-Patch-Flag-and-Seed-Commit-Count.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR/CR047_jsonpit_and_pits_Require-Existing-Patch-Flag-and-Seed-Commit-Count.md). Cloud discovery and configuration initialization retain their v4.4.4 behavior.

---

## 4.4.4

Amafu is the standalone cloud-storage discovery and RAIkeep configuration bootstrap tool introduced by accepted [`CR044_AIA_and_jsonpit_to_RAIkeep_Auto-Detect-Cloud-Drives-and-Init-Config.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR/CR044_AIA_and_jsonpit_to_RAIkeep_Auto-Detect-Cloud-Drives-and-Init-Config.md).

### Highlights

- Adds `amafu detect`, `amafu init`, and the `amafu init-config` alias.
- Detects documented macOS OneDrive, Dropbox, Google Drive, and iCloud Drive locations in deterministic provider order.
- Generates standard JSON5 at `~/.config/RAIkeep.json5`, refuses overwrite unless `--force` is supplied, and supports `--dry-run` without writes.
- Runs independently of OsLib and all other RAIkeep packages. Its internal model is `AmafuConfiguration`; it does not expose or mutate `Os.Config`.
- Ships as a NuGet global tool and as zero-runtime NativeAOT binaries for macOS ARM64/x64, Linux ARM64/x64, and Windows x64.
- Automatic provider discovery is supported and tested only on macOS in 4.4.4. Linux and Windows binaries provide the command surface and documented starter-template fallback; provider detection on those systems is future work.
- Preserves the RAIkeep Nerd Font CLI visual language and rejects elevated execution to protect user-owned configuration files.

No release action occurs by preparing these notes; RAI retains the manual release gate.
