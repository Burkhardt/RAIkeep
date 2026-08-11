# Release Notes: RaiUtils v4.0.1

**Date:** 2026-08-10
**Author / Delivering Agent:** RAIkeep Dev Agent
**Delivered Version:** v4.0.1
**Target Consumers:** RAIkeep package family, AfricaStage, AIA
**Status:** Prepared — publication approval pending

## 1. Summary

RaiUtils v4.0.1 is the synchronized utility package for the coordinated CR006
CLI patch line. It contains no RaiUtils API or behavior change from v4.0.0.

## 2. Resolved Change Requests (CRs)

- [`CR006_AfricaStage_to_RAIkeep_CliSubcommands.md`](https://github.com/Burkhardt/AIA/blob/main/doc/CR006_AfricaStage_to_RAIkeep_CliSubcommands.md) — synchronized package participation only; implementation is owned by ImgSeeder and PitSeeder.

## 3. Root Cause Analysis & Technical Resolution

RAIkeep packages are released as one coordinated version line. RaiUtils moves
to v4.0.1 to preserve that line; no source-level resolution was required here.

## 4. Public Contract & API / Package Changes

- Package version: `4.0.1`.
- Public API and runtime behavior: unchanged from `4.0.0`.

## 5. Validation & Acceptance Evidence

- RaiUtils.Tests: **21 passed, 0 failed, 0 skipped** in the coordinated run.

## 6. Upgrade & Consumption Instructions

Consume RaiUtils v4.0.1 with the other five coordinated RAIkeep v4.0.1 packages.
