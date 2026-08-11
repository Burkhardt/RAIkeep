# Release Notes: OsLibCore v4.0.1

**Date:** 2026-08-10
**Author / Delivering Agent:** RAIkeep Dev Agent
**Delivered Version:** v4.0.1
**Target Consumers:** RAIkeep package family, AfricaStage, AIA
**Status:** Prepared — publication approval pending

## 1. Summary

OsLibCore v4.0.1 is the synchronized foundation package for the coordinated
CR006 CLI patch line. It contains no OsLibCore API or behavior change from
v4.0.0.

## 2. Resolved Change Requests (CRs)

- [`CR006_AfricaStage_to_RAIkeep_CliSubcommands.md`](https://github.com/Burkhardt/AIA/blob/main/doc/CR006_AfricaStage_to_RAIkeep_CliSubcommands.md) — synchronized package participation only; implementation is owned by ImgSeeder and PitSeeder.

## 3. Root Cause Analysis & Technical Resolution

RAIkeep packages are released as one coordinated version line. OsLibCore moves
to v4.0.1 so downstream fallback dependencies remain exact and deterministic;
no source-level resolution was required in this component.

## 4. Public Contract & API / Package Changes

- Package version: `4.0.1`.
- Public API and runtime behavior: unchanged from `4.0.0`.

## 5. Validation & Acceptance Evidence

- OsLib.Tests: **80 passed, 0 failed, 0 skipped** in the coordinated run.

## 6. Upgrade & Consumption Instructions

Consume OsLibCore v4.0.1 with the other five coordinated RAIkeep v4.0.1 packages.
