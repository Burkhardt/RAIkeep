# RAIkeep RELEASE NOTES 4.5.8

- Release version: `4.5.8`
- Coordination tag: `v4.5.8`

## Highlights
- Coordinated umbrella release across all 10 platform packages on NuGet.org and PyPI (`jsonpit 4.5.8`).
- Delivers CR059 fleet CLI dispatch in `OsLib` (`DenoCommand`, `AmafuCommand`, `IorgCommand`, `JpitCommand`, `PitsCommand`, `RaidCommand`) supporting typed local and `OverSsh` remote execution.
- Enables remote image processing in `RaiImage` via `ImageMagickCommand.OverSsh(target)`.
- Delivers `JsonPit` `PitItem.ExtendWith` matching-`Id` relaxation, permitting updates that declare their own identity while strictly protecting envelope metadata (`Created`, `Modified`, `Deleted`).
- Full fleet provisioning verified and operational across `Nkosikazi`, `Mzansi`, `umshadisi@Mdlaka`, and `Neo`.

## Coordinated Dependencies
- Aligned with RAIkeep synchronized `4.5.8` line.
