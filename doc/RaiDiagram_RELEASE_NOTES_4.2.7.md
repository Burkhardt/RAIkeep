# RaiDiagram 4.2.7 Release Notes

Implements RaiDiagram alignment with accepted
[CR020](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR020_RAI_to_RAIkeep_Iorg_Read_Only_Wildcard_Listing.md).

- `RaidFile`, `PumlSourceFile`, `PumlConfigFile`, `PumlStyleFile`, `PumlThemeFile`, and `DiagramArtifactSet` accept an `ItemTreePath`.
- Diagram source, resolved config, manifest, and rendered image files therefore share the same ItemId ownership and movement contract.
- Active RaiDiagram code no longer relies on `FromImageTree` or `FromSubscriber` file factories.
- PlantUML compilation, local style resolution, and SVG provenance behavior remain intact.

Tagging and NuGet publication remain behind RAI's manual release gate.
