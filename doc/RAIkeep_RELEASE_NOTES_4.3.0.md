# RAIkeep 4.3.0 Release Notes

RAIkeep 4.3.0 is the coordinated seven-package delivery of accepted
[CR023 PlantUML relationship rendering](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR023_AIA_to_RAIkeep_PlantUml_Relationship_Rendering.md),
[CR024 process-flag self-cleanup](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR024_AIA_to_RAIkeep_Ephemeral_Flag_Self_Cleanup.md), and
[CR025 typed RaiDiagram builders and deterministic ItemTree emission](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR025_AIA_to_RAIkeep_Typed_Raid_Builders_and_Deterministic_ItemTree_Emission.md).

## RaiDiagram 4.3

- Typed builders create UCD, RFD/OD, CD, AD, and SD manifests through managed C#.
- PlantUML source compilation remains Java-free and emits native syntax with
  conditional `allowmixing`; the optional renderer remains compatible.
- Base `ItemId`, optional `ItemNumber`, and archetype `NameExt` stay distinct.
  Filenames use `ItemId[_NN][_NameExt].ext`, while ItemTree buckets use only the
  base ItemId.
- `.raid`, `.puml`, `_config.puml`, and `.svg` are deterministic co-located
  subscriber siblings.
- Real PlantUML 1.2026.8 syntax validation and SVG diagnostic detection guard
  the generated source.

## Carried accepted lifecycle work

- CR023 relationship labels, cardinality, and accepted-vocabulary discovery are included.
- CR024 clean disposal removes only the exact owned PID flag; finalizers remain I/O-free.
- CR022's no-TempDir-to-cloud and continuous-cloud-pathname rules remain mandatory.

RAI intentionally did not publish v4.2.11; all prepared CR023/CR024 changes are
superseded and carried into v4.3.0. All seven package/fallback versions align on
4.3.0. Tagging, GitHub labeling, workflow dispatch, and NuGet publication remain
behind RAI's manual `scripts/release-chain.sh 4.3.0` gate.
