# OsLibCore 3.13.1 Release Notes

## Summary

`OsLibCore 3.13.1` adds the file primitives required by JsonPit coordination files while preserving the existing path and cloud-configuration model.

## Changes

- Added `TextFile.SaveInPlace()` for small coordination files that must be updated without a preceding delete or rename.
- Retained `AwaitMaterializing(...)` after an in-place write so cloud-backed callers keep the existing materialization check.
- Added the read-only `RaiFile.LastWriteTimeUtc` property for consumers that need physical file modification time without direct `System.IO.FileInfo` access.
- Did not add a last-write-time setter. Physical modification time remains the real filesystem/cloud write time; callers should keep logical timestamps in their own data model.
- Updated API documentation, README entries, package metadata, and the RaiFile hierarchy diagram for `3.13.1`.

## Compatibility

- The new APIs are additive.
- No configuration-loading or environment-variable behavior changed.
- Existing `TextFile.Save(...)`, backup, and cloud-path behavior remain available unchanged.

## Validation

- Umbrella `RAIkeep.slnx` build succeeds.
- `OsLib.Tests`: `66` passed, `0` failed.

## Release sequencing

`OsLibCore` is first in the coordinated release chain. Do not begin the `RaiUtils` release until the OsLibCore publish workflow succeeds, the `3.13.1` flat-container package returns HTTP `200`, and the required `330`-second hold has completed.
