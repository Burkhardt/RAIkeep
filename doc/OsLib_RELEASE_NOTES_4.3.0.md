# OsLibCore 4.3.0 Release Notes

OsLibCore 4.3.0 is the coordinated foundation for accepted
[CR023](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR023_AIA_to_RAIkeep_PlantUml_Relationship_Rendering.md),
[CR024](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR024_AIA_to_RAIkeep_Ephemeral_Flag_Self_Cleanup.md), and
[CR025](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR025_AIA_to_RAIkeep_Typed_Raid_Builders_and_Deterministic_ItemTree_Emission.md).

- Public behavior is unchanged from 4.2.10.
- CR024 consumes the existing cloud-aware `RaiFile.rm()` boundary.
- CR025 artifact storage continues to inherit the CR022 in-place CloudDrive invariant.
- Package and fallback dependency versions align on 4.3.0.

The unpublished 4.2.11 preparation is superseded by this release. Publication
remains behind RAI's manual `scripts/release-chain.sh 4.3.0` gate.
