# Release Notes: RAIkeep v4.0.1

**Date:** 2026-08-10
**Author / Delivering Agent:** RAIkeep Dev Agent
**Delivered Version:** v4.0.1
**Target Consumers:** AfricaStage, AIA
**Status:** Prepared — publication approval pending

## 1. Summary

RAIkeep v4.0.1 delivers the coordinated CR006 command-first CLI transition.
Functional changes are confined to PitSeeder/`pits` and ImgSeeder/`iorg`;
OsLibCore, RaiUtils, RaiImage, and JsonPit participate as synchronized patch
packages without runtime changes.

## 2. Resolved Change Requests (CRs)

- [`CR006_AfricaStage_to_RAIkeep_CliSubcommands.md`](https://github.com/Burkhardt/AIA/blob/main/doc/CR006_AfricaStage_to_RAIkeep_CliSubcommands.md) — command-first `pits` and `iorg` interfaces with a documented 4.x-to-5.x transition.

## 3. Root Cause Analysis & Technical Resolution

Both CLIs inferred operations from flat option combinations, producing crowded
help and late collision handling. Command-first dispatch now isolates operation
syntax while automatically retaining the established flat parser for mature
workflows. Both paths call the same handlers.

The recent event-audit flags are excluded from legacy compatibility and move
directly to `pits audit`. The legacy parsers are scheduled for removal in
`5.x.x` after command-surface parity and consumer validation.

## 4. Public Contract & API / Package Changes

- Coordinated package line: `4.0.1` across all six packages.
- Functional CLI changes: ImgSeeder and PitSeeder only.
- Library APIs and behavior: unchanged from `4.0.0`.
- Transition policy: [`CLI-PARSER-TRANSITION-4.x-TO-5.x.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CLI-PARSER-TRANSITION-4.x-TO-5.x.md).

## 5. Validation & Acceptance Evidence

- Current coordinated Release revalidation: **375 passed, 1 failed, 0 skipped**.
- Component totals: OsLib 80, RaiUtils 21, RaiImage 94, JsonPit 146,
  ImgSeeder 15, and PitSeeder 20.
- The sole current failure is JsonPit's existing finalizer/GC ownership test,
  `Finalizer_PerformsNoRecoveryPublicationOrFilesystemIO_AndPathBecomesReopenable`;
  it reproduces in isolation. JsonPit has no source change in this release beyond
  synchronized version and dependency metadata. The six-package release-chain
  workflows build and pack rather than execute local cloud/SSH tests.

## 6. Upgrade & Consumption Instructions

1. Upgrade the six-package RAIkeep line together to v4.0.1 after publication.
2. Migrate scripts to the command syntax documented in the PitSeeder and
   ImgSeeder v4.0.1 release notes.
3. Independently validate AfricaStage/AIA integration behavior.
4. Publish `CR006_Accepted_CliSubcommands.md` or
   `CR006_Rejected_CliSubcommands.md` from the requester side.
