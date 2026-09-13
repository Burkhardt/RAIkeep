# RAIkeep centralized documents

This directory is the umbrella workspace location for release notes and change requests from all RAIkeep child projects.

Files are flattened into this directory and prefixed with their source project to prevent collisions:

- `<Project>_RELEASE_NOTES_<version>.md`
- `<Project>_CR_<request>.md`

Do not add `RELEASE_NOTES*.md` or `CR_*.md` files to child-project directories. Move them here and retain the project prefix.

## Current coordinated release notes

- [RAIkeep 4.3.2](https://github.com/Burkhardt/RAIkeep/blob/main/doc/RAIkeep_RELEASE_NOTES_4.3.2.md)
- [OsLibCore 4.3.2](https://github.com/Burkhardt/RAIkeep/blob/main/doc/OsLib_RELEASE_NOTES_4.3.2.md)
- [RaiUtils 4.3.2](https://github.com/Burkhardt/RAIkeep/blob/main/doc/RaiUtils_RELEASE_NOTES_4.3.2.md)
- [RaiImage 4.3.2](https://github.com/Burkhardt/RAIkeep/blob/main/doc/RaiImage_RELEASE_NOTES_4.3.2.md)
- [RaiDiagram 4.3.2](https://github.com/Burkhardt/RAIkeep/blob/main/doc/RaiDiagram_RELEASE_NOTES_4.3.2.md)
- [JsonPit 4.3.2](https://github.com/Burkhardt/RAIkeep/blob/main/doc/JsonPit_RELEASE_NOTES_4.3.2.md)
- [ImgSeeder 4.3.2](https://github.com/Burkhardt/RAIkeep/blob/main/doc/ImgSeeder_RELEASE_NOTES_4.3.2.md)
- [PitSeeder 4.3.2](https://github.com/Burkhardt/RAIkeep/blob/main/doc/PitSeeder_RELEASE_NOTES_4.3.2.md)

## Technical guides

- [`RAIkeep_BACKLOG.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/RAIkeep_BACKLOG.md) records product-backlog designs and their implementation status, including the event archive delivered in 4.2.10.
- [`PITS-AUDIT.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/PITS-AUDIT.md) is the operational manual for interpreting and safely querying JsonPit's durable recovery log with `pits audit`.
- [`IORG-OPERATIONS.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/IORG-OPERATIONS.md) documents iorg organization, read-only discovery, exact-family inspection, moves, cleanup, conventions, and CloudDrive safety; iorg has no event-audit facility.
- [`Cloud-Storage-In-Place-Invariant.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/Cloud-Storage-In-Place-Invariant.md) defines the mandatory no-TempDir-to-cloud and continuous-cloud-pathname rules formalized after the CR022 incident investigation.
- [`CLI-PARSER-TRANSITION-4.x-TO-5.x.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CLI-PARSER-TRANSITION-4.x-TO-5.x.md) records the dual-syntax compatibility contract for `pits` and `iorg` in `4.x` and the planned removal of their legacy parsers in `5.x.x`.
- [`JsonPit-FlagFiles-And-Concurrency.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/JsonPit-FlagFiles-And-Concurrency.md) explains the separate per-process activity flags, stable `Master.flag` lease, canonical-write decision, CLI cleanup, and current coordination boundary.
- [`JsonPit-CONCEPT-Live-Split-Master-Recovery.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/JsonPit-CONCEPT-Live-Split-Master-Recovery.md) is the accepted v3.13.2 live-process recovery design after a cloud provider exposes a conflicting `Master*.flag` copy.
- [`RaiDiagram-CONCEPT-UML26.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/RaiDiagram-CONCEPT-UML26.md) proposes the RAIkeep UML26 semantic diagram dialect, separate RaiDiagram package, role-first use-case model, tenant themes, and PlantUML-first rendering architecture.
- [`ADR-0001-RaiDiagram-Package-Boundary.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/ADR-0001-RaiDiagram-Package-Boundary.md) records the accepted boundary between RaiDiagram's public diagram capabilities and AIA's WWWA modeling responsibilities.
- [`ADR-0002-RaiDiagram-Subscriber-Scoped-Artifacts-and-Styles.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/ADR-0002-RaiDiagram-Subscriber-Scoped-Artifacts-and-Styles.md) records that subscriber values remain ImageTree storage-routing segments rather than identities and that style fallbacks are explicit and local.
- [`Details of CR003.md`](<https://github.com/Burkhardt/RAIkeep/blob/main/doc/Details%20of%20CR003.md>) is the implementation companion for CR003, including current code seams, sequencing guidance, rejected shortcuts, and a test approach for every substantial agreement.

## Change requests

Open:

- [`CR016_AIA_to_RAIkeep_RaiImage_Unicode_Normalization_Bucketing.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR016_AIA_to_RAIkeep_RaiImage_Unicode_Normalization_Bucketing.md) — accepted AIA request for NFC ImageTree names, grapheme-safe bucketing, and normalization-resilient legacy reads, targeted at RAIkeep v4.2.4
- [`CR010_AfricaStage_to_RAIkeep_RaiDiagram_Subscriber_Scoped_Artifacts_and_Styles.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR010_AfricaStage_to_RAIkeep_RaiDiagram_Subscriber_Scoped_Artifacts_and_Styles.md) — accepted AfricaStage request for subscriber-scoped ImageTree diagram artifacts and explicit local PlantUML style fallbacks, targeted at RAIkeep v4.2.2
- [`CR009_AIA_to_RAIkeep_RaiDiagram_Package.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR009_AIA_to_RAIkeep_RaiDiagram_Package.md) — approved domain-neutral RaiDiagram package targeted at RAIkeep v4.2.0
- [`CR008_AIA_to_RAIkeep_OsLib_RaiImage_Boundary_Enhancements.md`](https://github.com/Burkhardt/AIA/blob/main/doc/CR008_AIA_to_RAIkeep_OsLib_RaiImage_Boundary_Enhancements.md) — approved AIA boundary request targeted at RAIkeep v4.1.0
- [`CR006_AfricaStage_to_RAIkeep_CliSubcommands.md`](https://github.com/Burkhardt/AIA/blob/main/doc/CR006_AfricaStage_to_RAIkeep_CliSubcommands.md) — approved for the coordinated v4.0.1 CLI transition implementation
- [`CR003_RAI_to_RAIkeep_JsonPit-concurrency-contract-and-persistence-races.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR003_RAI_to_RAIkeep_JsonPit-concurrency-contract-and-persistence-races.md) — accepted and finalized for coordinated v3.13.2 implementation

Resolved:

- [`CR027_AIA_to_RAIkeep_ClassDiagram_Generalization_and_SetSuperClass.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR027_AIA_to_RAIkeep_ClassDiagram_Generalization_and_SetSuperClass.md) — accepted and implemented for coordinated RAIkeep v4.3.2; publication remains behind RAI's manual gate
- [`CR026_AIA_to_RAIkeep_Diagram_Builder_Revision_Fidelity_and_Reference_Stereotypes.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR026_AIA_to_RAIkeep_Diagram_Builder_Revision_Fidelity_and_Reference_Stereotypes.md) — released, formally accepted, and verified in coordinated RAIkeep v4.3.1
- [`CR025_AIA_to_RAIkeep_Typed_Raid_Builders_and_Deterministic_ItemTree_Emission.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR025_AIA_to_RAIkeep_Typed_Raid_Builders_and_Deterministic_ItemTree_Emission.md) — accepted and implemented for coordinated RAIkeep v4.3.0; publication remains behind RAI's manual gate
- [`CR024_AIA_to_RAIkeep_Ephemeral_Flag_Self_Cleanup.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR024_AIA_to_RAIkeep_Ephemeral_Flag_Self_Cleanup.md) — accepted and implemented for coordinated RAIkeep v4.3.0 after the unpublished v4.2.11 preparation
- [`CR023_AIA_to_RAIkeep_PlantUml_Relationship_Rendering.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR023_AIA_to_RAIkeep_PlantUml_Relationship_Rendering.md) — accepted and implemented for coordinated RAIkeep v4.3.0 after the unpublished v4.2.11 preparation
- [`CR022_RAI_to_RAIkeep_Cloud_Safe_In_Place_Filesystem_Invariant.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR022_RAI_to_RAIkeep_Cloud_Safe_In_Place_Filesystem_Invariant.md) — accepted incident corrective action implemented for coordinated RAIkeep v4.2.9; publication remains behind RAI's manual gate
- [`CR021_RAI_to_RAIkeep_JsonPit_Durable_Cleanup_Receipts_and_Pits_Coordination.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR021_RAI_to_RAIkeep_JsonPit_Durable_Cleanup_Receipts_and_Pits_Coordination.md) — accepted and implemented for coordinated RAIkeep v4.2.8; publication remains behind RAI's manual gate

- [`CR020_RAI_to_RAIkeep_Iorg_Read_Only_Wildcard_Listing.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR020_RAI_to_RAIkeep_Iorg_Read_Only_Wildcard_Listing.md) — accepted and implemented for coordinated RAIkeep v4.2.7; publication remains behind RAI's manual gate
- [`CR019_AIA_to_RAIkeep_WordCase_Seams_and_Placement.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR019_AIA_to_RAIkeep_WordCase_Seams_and_Placement.md) — formally accepted for coordinated RAIkeep v4.2.6; relocates word-case helpers to RaiUtils and adds lossless Unicode-safe seam positions
- [`CR017_AIA_to_RAIkeep_Pits_Point_in_Time_Export.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR017_AIA_to_RAIkeep_Pits_Point_in_Time_Export.md) — formally accepted, implemented, and verified for RAIkeep v4.2.5; publication remained behind RAI's manual gate
- [`CR015_AIA_to_RAIkeep_Nested_Property_Tombstones_and_CLI_Delete.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR015_AIA_to_RAIkeep_Nested_Property_Tombstones_and_CLI_Delete.md) — accepted, implemented, verified, and released in RAIkeep v4.2.3
- [`CR014_RAI_to_RAIkeep_Typed_CLI_Command_Wrappers.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR014_RAI_to_RAIkeep_Typed_CLI_Command_Wrappers.md) — accepted, implemented, verified, and released in RAIkeep v4.2.2
- [`CR014.1_test-concept.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR014.1_test-concept.md) — accepted verification guidance applied to the released CR014 wrappers
- [`PitSeeder_CR_release_for_cli-resolved-in-v3.13.1.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/PitSeeder_CR_release_for_cli-resolved-in-v3.13.1.md)
- [`RaiImage_CR_ImageTreeFile_NamingAwareCtor-resolved-in-v3.9.0.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/RaiImage_CR_ImageTreeFile_NamingAwareCtor-resolved-in-v3.9.0.md)
