# RaiImage 4.2.7 Release Notes

Implements the shared item-file architecture adopted with accepted
[CR020](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR020_RAI_to_RAIkeep_Iorg_Read_Only_Wildcard_Listing.md).

- Makes `ItemTreePath` the tree home of one subscriber-local ItemId and all of its files.
- Adds `ItemTreePath.SelectFiles()` for exact-ItemId selection across images, SVG, PUML, config PUML, and RAID files while excluding bucket siblings.
- Adds destination-oriented `ItemTreePath.mv(source)` for complete-family relocation, ItemId rename, subscriber move, and path-convention migration.
- Preflights collisions, attempts rollback on partial failure, and prunes empty vacated buckets.
- Adds `PathConventionType.Flat` support alongside canonical, 3x3, and 8x2 placement.
- Renames the non-image tree text type to `ItemTreeTextFile`.
- Replaces procedural `ImageTreeFile.From...` construction with constructors accepting `ItemTreePath` and fluent `SelectFirstExistingFile(...)` image resolution.
- Covers the complete `AfricanBrisket` mixed-file example, sibling exclusion, subscriber relocation, rename, and 8x2/3x3/Flat migrations.

Tagging and NuGet publication remain behind RAI's manual release gate.
