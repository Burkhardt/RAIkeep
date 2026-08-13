# RAIkeep 4.1.0 Release Notes

**Status:** Source and verification candidate; not published  
**Change request:** `CR008_AIA_to_RAIkeep_OsLib_RaiImage_Boundary_Enhancements.md`

RAIkeep 4.1.0 strengthens the operating-system and image boundaries requested
by AIA while preserving `Os.Config` as the runtime source of truth.

## OsLibCore

- `Os.TempDir` remains the configured `RaiPath`; it was not removed from 4.0.
- First initialization now creates, observes, and removes an OsLib `TmpFile` in
  the configured directory.
- Initialization fails fast when that probe cannot be written. The implementation
  does not mutate `Os.Config`, substitute an environment override, or silently
  fall back to another directory after configuration has been resolved.
- `RaiPathException` and `RaiPathNotFoundException` provide path-specific failures.
- `RaiFile.WriteFromAsync(IAsyncEnumerable<byte[]>, CancellationToken)` provides
  chunked ingestion without exposing `System.IO.Stream` to consumers.

## RaiUtils

- Added the cross-package `RaiException` base class.
- Added `ToolNotFoundException` for missing external executables.

## RaiImage

- Added `RaiImageIOException` and `RaiImageNotFoundException`.
- Missing directories/paths use `RaiPathNotFoundException`; a missing image in an
  existing location uses `RaiImageNotFoundException`.
- Missing ImageMagick and PlantUML executables use `ToolNotFoundException` rather
  than `System.IO.FileNotFoundException`.
- Image files inherit and verify the async byte-chunk ingestion boundary.

The names differ intentionally from the originally submitted
`RaiImageFileNotFoundException`: RAIkeep and AIA subsequently agreed to separate
missing paths from missing images.

## JsonPit internal regression included with the work

- Abandoned `Pit` instances are no longer retained by `FileSystemWatcher` event
  handlers or debounce tasks.
- Watcher dispatch uses weak ownership, allowing forced collection to remove the
  weak registry entry and make the generated path reopenable.
- The finalizer remains free of recovery publication, watcher disposal, and
  filesystem I/O.

## Verification

Focused CR008 tests and the relevant OsLibCore, RaiUtils, RaiImage, and JsonPit
Release suites are required before release. The release gate remains explicit:
these notes do not authorize a tag, push, NuGet publication, or package-version
change.
