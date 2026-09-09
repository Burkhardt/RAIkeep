# RAIkeep 4.2.7 Release Notes

RAIkeep 4.2.7 is the coordinated seven-package implementation of accepted
[CR020 — `iorg` Media & Diagram Tree Custodianship](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR020_RAI_to_RAIkeep_Iorg_Read_Only_Wildcard_Listing.md).

## ItemTree architecture

- `ItemTreePath` is the object-oriented home of one subscriber-local ItemId and every physical file belonging to it.
- `SelectFiles()` returns images, derivatives, SVG, PUML, config PUML, and RAID files for the exact ItemId without selecting similar bucket siblings.
- `destination.mv(source)` moves or renames the whole family and supports canonical, 3x3, 8x2, and Flat placement.
- Image and diagram artifact constructors share `ItemTreePath`; the active `FromImageTree`/`FromItemTree` factory path has been removed.

## `iorg`

- `iorg list <FileNamePattern>` recursively discovers managed image and diagram files without mutation.
- `iorg move <SourceItemId> [TargetItemId]` performs exact-family relocation, optional rename, and path-convention migration.
- `iorg clean --cache` removes rendered derivatives while preserving source and diagram files.
- `iorg clean <ItemId> --force` removes the complete item family; without `--force` it remains a dry run.
- Root help no longer calls supported syntax Legacy; `-r` remains the supported short spelling of `--root`.

## Compatibility and release boundary

- Existing `PathConventionType` values retain their positions; `Flat` is appended and exposed as CLI option 4.
- All seven package versions and fallback dependencies align on 4.2.7.
- No tag or NuGet publication is created during preparation. RAI retains the manual release-chain gate.
