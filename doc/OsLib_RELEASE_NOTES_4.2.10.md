# OsLibCore 4.2.10 Release Notes

OsLibCore 4.2.10 supplies the reusable storage and typed-command boundaries for
RAIkeep's RAI-authorized recovery-event archive and `iorg` addressing work.

- Adds `RaiZipFile`, `RaiZipEntry`, `RaiZipWriteResult`, and
  `RaiZipWriteStatus` for immutable collection archives.
- Archives are created directly at their final pathname in an existing parent;
  there is no TempDir staging, directory creation, extraction, overwrite, or
  delete/recreate of an established archive.
- Same-name retries reuse only a fully filename-and-byte-identical archive.
  Different or invalid existing content is preserved and reported.
- `EventDirectory.Inspect(...)` combines valid loose `.event` files and
  `Events_*.zip` entries without extraction and reports retained invalid or
  conflicting evidence.
- `PitsMaintainRequest.ArchiveEvents` emits `--archive-events` through the
  process-coordinated `PitsCommand` boundary.
- `IorgCommandOptions.RootIsApplicationRoot` emits `--app`;
  `IorgCommandOptions.Tenant` emits `--tenant`, while `Subscriber` remains a
  source-compatible alias.

Regression coverage verifies create-once behavior, identical retry, collision
and corruption retention, missing-parent non-creation, exact typed tokens, and
the absence of temporary archive files.
