# ImgSeeder 4.2.7 Release Notes

Implements the `iorg` media and diagram tree custodianship requested by accepted
[CR020](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR020_RAI_to_RAIkeep_Iorg_Read_Only_Wildcard_Listing.md).

- Adds read-only `iorg list <FileNamePattern>` discovery across supported image, `.puml`, and `.raid` files.
- Adds `iorg move <SourceItemId> [TargetItemId]` for exact-family relocation, optional rename, and convention migration.
- Adds Flat as path-convention option 4 while retaining 8x2 as option 3/default.
- Makes `iorg clean <ItemId> --force` remove the complete exact item family; dry run remains the default.
- Makes `iorg clean --cache` explicitly remove rendered derivatives while preserving source images and diagram artifacts.
- Removes the misleading Legacy row from root help; `-r` remains supported as the short spelling of `--root`.
- Tests the complete `AfricanBrisket` image/diagram family and proves `AfricanBrigadine` remains untouched in a shared bucket.

Tagging and NuGet publication remain behind RAI's manual release gate.
