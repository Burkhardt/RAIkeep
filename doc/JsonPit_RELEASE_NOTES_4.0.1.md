# Release Notes: JsonPit v4.0.1

**Date:** 2026-08-10
**Author / Delivering Agent:** RAIkeep Dev Agent
**Delivered Version:** v4.0.1
**Target Consumers:** RAIkeep package family, AfricaStage, AIA
**Status:** Prepared — publication approval pending

## 1. Summary

JsonPit v4.0.1 is the synchronized persistence package for the coordinated
CR006 CLI patch line. It contains no JsonPit API, persistence, lease, recovery,
or concurrency behavior change from v4.0.0.

## 2. Resolved Change Requests (CRs)

- [`CR006_AfricaStage_to_RAIkeep_CliSubcommands.md`](https://github.com/Burkhardt/AIA/blob/main/doc/CR006_AfricaStage_to_RAIkeep_CliSubcommands.md) — synchronized package participation only; CLI implementation is owned by ImgSeeder and PitSeeder.

## 3. Root Cause Analysis & Technical Resolution

JsonPit moves to v4.0.1 and aligns fallback dependencies on OsLibCore and
RaiUtils v4.0.1. The CR006 changes remain outside JsonPit's runtime contracts.

## 4. Public Contract & API / Package Changes

- Package version: `4.0.1`.
- Fallback dependencies: OsLibCore `4.0.1`, RaiUtils `4.0.1`.
- Public API and runtime behavior: unchanged from `4.0.0`.

## 5. Validation & Acceptance Evidence

- Current Release revalidation: **145 passed, 1 failed, 0 skipped**. The existing
  finalizer/GC ownership test
  `Finalizer_PerformsNoRecoveryPublicationOrFilesystemIO_AndPathBecomesReopenable`
  also fails in isolation because the generated unique path remains registered
  after forced collection. No JsonPit source or test changed in v4.0.1; only
  synchronized version and dependency metadata changed.

## 6. Upgrade & Consumption Instructions

Consume JsonPit v4.0.1 with the other five coordinated RAIkeep v4.0.1 packages.
