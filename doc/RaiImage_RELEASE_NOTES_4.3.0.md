# RaiImage 4.3.0 Release Notes

RaiImage 4.3.0 supplies CR025's deterministic diagram-artifact storage contract.

- `ItemTreeTextFile` now exposes optional `ItemNumber`, symmetric with
  `ImageTreeFile.ImageNumber`.
- Base `ItemId`, optional `ItemNumber`, and archetype `NameExt` remain separate.
- Names compose as `ItemId[_NN][_NameExt].ext`; buckets use only `ItemId`.
- Public subscriber rendering overloads preserve those parts across `.puml`,
  `_config.puml`, and `.svg` siblings.
- The CR022 continuous-cloud-pathname invariant remains mandatory.

See [CR025](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR025_AIA_to_RAIkeep_Typed_Raid_Builders_and_Deterministic_ItemTree_Emission.md).
The unpublished 4.2.11 preparation is superseded. Publication remains behind
RAI's manual `scripts/release-chain.sh 4.3.0` gate.
