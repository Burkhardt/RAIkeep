# RAIkeep RELEASE NOTES 4.5.5

- Release version: `4.5.5`
- Coordination tag: `v4.5.5`

## Highlights
CR054 delivers compact image receipts and Structured D3 normalization. CR052 delivers object-slot import, deployment PlantUML support, and preflight diagnostics. The accepted bounded XMI deployment importer is retained. All packages align to 4.5.5; no publication is implied by this preparation.

## Coordinated Dependencies
- Aligned with RAIkeep synchronized `4.5.5` line.

## Verification

`dotnet test RAIkeep.slnx -p:UseLocalRAIkeepSources=true` completed across all nine
assemblies. Eight passed immediately; three RaiImage failures were corrected
(numbered-rendering overload and D3 expectations), then all 161 RaiImage tests
passed on the affected-assembly rerun. Aggregate: **909 passed, 0 remaining
failures, 0 skipped**. No second full-suite run was needed for that localized fix.

| Assembly | Passed |
| --- | ---: |
| Amafu | 62 |
| ImgSeeder | 66 |
| JsonPit | 227 |
| OsLib | 147 |
| PitSeeder | 87 |
| RaiDiagram | 92 |
| RaidSeeder | 16 |
| RaiImage | 161 |
| RaiUtils | 51 |

The existing analyzer warnings remain; this is not a warning-free build claim.
`validate-release.py 4.5.5` verifies coordinated version and documentation metadata.
Private reference corpora and the local path inventory are excluded from commits.
Broad cleanup of pre-existing domain examples remains outside this delivery.

## Compatibility

Structured images and numbered diagram siblings now generate minimum-width D3.
Readers accept earlier numeric widths, but recomposed paths change. No automatic
migration runs; migrate stored files and references together before replaying old
imports. Receipt consumers should use Summary/Exceptions/Error and CLI exit codes,
not a top-level activity Status. Default receipts omit Files; explicit --exif adds it.
