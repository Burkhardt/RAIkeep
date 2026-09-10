# RAIkeep 4.2.10 Release Notes

RAIkeep 4.2.10 is the coordinated seven-package delivery of the RAI-authorized
JsonPit recovery-event archive backlog and improved `iorg` application-root /
tenant addressing. It preserves accepted
[CR021](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR021_RAI_to_RAIkeep_JsonPit_Durable_Cleanup_Receipts_and_Pits_Coordination.md)
and the mandatory
[CR022 cloud-storage invariant](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR022_RAI_to_RAIkeep_Cloud_Safe_In_Place_Filesystem_Invariant.md).

## Recovery-event compaction

- `pits maintain ... --archive-events` previews exact event-archive work;
  `--apply` is required to write the archive and retire loose copies.
- The OsLib-backed archive is immutable, created at its final pathname inside the
  existing `Events` directory, and never staged in `Os.TempDir`.
- Source events remain until complete filename/byte validation succeeds, and are
  then removed individually. Retry, corruption, and collision paths fail safe.
- `pits audit` and `PitAudit` transparently preserve one logical history across
  loose and archived storage.

## Iorg addressing

- `-a, --app` accepts an application root and appends `Image`.
- `-t, --tenant` is the preferred explicit subscriber spelling;
  `--subscriber` remains an alias.
- `-r, --root` continues to mean an exact ImageTree root, and help output now
  presents these alternatives consistently.
- The umbrella solution explicitly includes the ImgSeeder executable so the
  coordinated build verifies every deliverable under the requested Release
  configuration.

All seven package versions and fallback dependency properties align on 4.2.10.
Tagging, GitHub labeling, and NuGet publication remain behind RAI's manual
`scripts/release-chain.sh 4.2.10` gate.
