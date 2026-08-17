# RAIkeep centralized documents

This directory is the umbrella workspace location for release notes and change requests from all RAIkeep child projects.

Files are flattened into this directory and prefixed with their source project to prevent collisions:

- `<Project>_RELEASE_NOTES_<version>.md`
- `<Project>_CR_<request>.md`

Do not add `RELEASE_NOTES*.md` or `CR_*.md` files to child-project directories. Move them here and retain the project prefix.

## Current CLI patch release notes

- [ImgSeeder 4.2.1](https://github.com/Burkhardt/RAIkeep/blob/main/doc/ImgSeeder_RELEASE_NOTES_4.2.1.md)
- [PitSeeder 4.2.1](https://github.com/Burkhardt/RAIkeep/blob/main/doc/PitSeeder_RELEASE_NOTES_4.2.1.md)

These CLI-only packages continue to use the coordinated 4.2.0 library packages.
The umbrella and library package versions are unchanged.

## Current coordinated release notes

- [RAIkeep 4.2.0](https://github.com/Burkhardt/RAIkeep/blob/main/doc/RAIkeep_RELEASE_NOTES_4.2.0.md)
- [OsLibCore 4.2.0](https://github.com/Burkhardt/RAIkeep/blob/main/doc/OsLib_RELEASE_NOTES_4.2.0.md)
- [RaiUtils 4.2.0](https://github.com/Burkhardt/RAIkeep/blob/main/doc/RaiUtils_RELEASE_NOTES_4.2.0.md)
- [RaiImage 4.2.0](https://github.com/Burkhardt/RAIkeep/blob/main/doc/RaiImage_RELEASE_NOTES_4.2.0.md)
- [RaiDiagram 4.2.0](https://github.com/Burkhardt/RAIkeep/blob/main/doc/RaiDiagram_RELEASE_NOTES_4.2.0.md)
- [JsonPit 4.2.0](https://github.com/Burkhardt/RAIkeep/blob/main/doc/JsonPit_RELEASE_NOTES_4.2.0.md)
- [ImgSeeder 4.2.0](https://github.com/Burkhardt/RAIkeep/blob/main/doc/ImgSeeder_RELEASE_NOTES_4.2.0.md)
- [PitSeeder 4.2.0](https://github.com/Burkhardt/RAIkeep/blob/main/doc/PitSeeder_RELEASE_NOTES_4.2.0.md)

## Technical guides

- [`CLI-PARSER-TRANSITION-4.x-TO-5.x.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CLI-PARSER-TRANSITION-4.x-TO-5.x.md) records the dual-syntax compatibility contract for `pits` and `iorg` in `4.x` and the planned removal of their legacy parsers in `5.x.x`.
- [`JsonPit-FlagFiles-And-Concurrency.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/JsonPit-FlagFiles-And-Concurrency.md) explains the separate per-process activity flags, stable `Master.flag` lease, canonical-write decision, CLI cleanup, and current coordination boundary.
- [`JsonPit-CONCEPT-Live-Split-Master-Recovery.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/JsonPit-CONCEPT-Live-Split-Master-Recovery.md) is the accepted v3.13.2 live-process recovery design after a cloud provider exposes a conflicting `Master*.flag` copy.
- [`RaiDiagram-CONCEPT-UML26.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/RaiDiagram-CONCEPT-UML26.md) proposes the RAIkeep UML26 semantic diagram dialect, separate RaiDiagram package, role-first use-case model, tenant themes, and PlantUML-first rendering architecture.
- [`ADR001_RaiDiagram_Package_Boundary.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/ADR001_RaiDiagram_Package_Boundary.md) records the accepted boundary between RaiDiagram's public diagram capabilities and AIA's WWWA modeling responsibilities.
- [`Details of CR003.md`](<https://github.com/Burkhardt/RAIkeep/blob/main/doc/Details%20of%20CR003.md>) is the implementation companion for CR003, including current code seams, sequencing guidance, rejected shortcuts, and a test approach for every substantial agreement.

## Change requests

Open:

- [`CR009_AIA_to_RAIkeep_RaiDiagram_Package.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR009_AIA_to_RAIkeep_RaiDiagram_Package.md) — approved domain-neutral RaiDiagram package targeted at RAIkeep v4.2.0
- [`CR008_AIA_to_RAIkeep_OsLib_RaiImage_Boundary_Enhancements.md`](https://github.com/Burkhardt/AIA/blob/main/doc/CR008_AIA_to_RAIkeep_OsLib_RaiImage_Boundary_Enhancements.md) — approved AIA boundary request targeted at RAIkeep v4.1.0
- [`CR006_AfricaStage_to_RAIkeep_CliSubcommands.md`](https://github.com/Burkhardt/AIA/blob/main/doc/CR006_AfricaStage_to_RAIkeep_CliSubcommands.md) — approved for the coordinated v4.0.1 CLI transition implementation
- [`CR003_RAI_to_RAIkeep_JsonPit-concurrency-contract-and-persistence-races.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR003_RAI_to_RAIkeep_JsonPit-concurrency-contract-and-persistence-races.md) — accepted and finalized for coordinated v3.13.2 implementation

Resolved:

- [`PitSeeder_CR_release_for_cli-resolved-in-v3.13.1.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/PitSeeder_CR_release_for_cli-resolved-in-v3.13.1.md)
- [`RaiImage_CR_ImageTreeFile_NamingAwareCtor-resolved-in-v3.9.0.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/RaiImage_CR_ImageTreeFile_NamingAwareCtor-resolved-in-v3.9.0.md)
