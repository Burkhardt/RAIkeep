# RAIkeep 4.4.2 Release Notes

RAIkeep 4.4.2 is the synchronized eight-package delivery of accepted
[`CR040_AIA_to_RAIkeep_and_jsonpit_Prohibit-Read-Modify-Write.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR040_AIA_to_RAIkeep_and_jsonpit_Prohibit-Read-Modify-Write.md)
and
[`CR041_jsonpit_to_RAIkeep_Restore-Clean-Change-Filenames.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR041_jsonpit_to_RAIkeep_Restore-Clean-Change-Filenames.md).

## Sparse mutation protection

- JsonPit rejects client mutation or tombstoning of engine-managed `Id`,
  `Modified`, and `Deleted` attributes atomically.
- Live storage rejects projected read-modify-write payloads while explicit
  trusted historical replay continues through `AddHistorical(...)`.
- `pits seed` validates before opening the destination; `delete-property`
  creates sparse fragments and protects lifecycle attributes.

## Clean change artifacts

- New changes and receipts use readable
  `{Modified.UtcTicks}_{ExactProcessIdentity}.{json|receipt}` names.
- Dual-format discovery retains existing SHA-suffixed change files during
  rolling upgrades; legacy files keep hash validation.
- Process-monotonic live timestamps close the practical clock-resolution
  collision gap without lengthening filenames.
- Existing canonical accounting, immutable receipts, and the ten-minute cleanup
  grace apply equally to both formats.

## Release coordination

The already-published `v4.4.1` tags and packages remain immutable. CR040 and
CR041 therefore ship in the next coordinated patch, 4.4.2. All eight packages
align in this order: OsLibCore, RaiUtils, RaiImage, RaiDiagram, RaidSeeder,
JsonPit, ImgSeeder, and PitSeeder. No TempDir-to-cloud move, directory swap, or
finalizer filesystem I/O is introduced.

Publication remains behind RAI's manual `scripts/release-chain.sh 4.4.2` gate.
