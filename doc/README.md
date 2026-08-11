# RAIkeep centralized documents

This directory is the umbrella workspace location for release notes and change requests from all RAIkeep child projects.

Files are flattened into this directory and prefixed with their source project to prevent collisions:

- `<Project>_RELEASE_NOTES_<version>.md`
- `<Project>_CR_<request>.md`

Do not add `RELEASE_NOTES*.md` or `CR_*.md` files to child-project directories. Move them here and retain the project prefix.

## Technical guides

- [`CLI-PARSER-TRANSITION-4.x-TO-5.x.md`](CLI-PARSER-TRANSITION-4.x-TO-5.x.md) records the dual-syntax compatibility contract for `pits` and `iorg` in `4.x` and the planned removal of their legacy parsers in `5.x.x`.
- [`JsonPit-FlagFiles-And-Concurrency.md`](JsonPit-FlagFiles-And-Concurrency.md) explains the separate per-process activity flags, stable `Master.flag` lease, canonical-write decision, CLI cleanup, and current coordination boundary.
- [`JsonPit-CONCEPT-Live-Split-Master-Recovery.md`](JsonPit-CONCEPT-Live-Split-Master-Recovery.md) is the accepted v3.13.2 live-process recovery design after a cloud provider exposes a conflicting `Master*.flag` copy.
- [`Details of CR003.md`](<Details of CR003.md>) is the implementation companion for CR003, including current code seams, sequencing guidance, rejected shortcuts, and a test approach for every substantial agreement.

## Change requests

Open:

- [`CR006_AfricaStage_to_RAIkeep_CliSubcommands.md`](https://github.com/Burkhardt/AIA/blob/main/doc/CR006_AfricaStage_to_RAIkeep_CliSubcommands.md) — approved for the coordinated v4.0.1 CLI transition implementation
- [`CR003_RAI_to_RAIkeep_JsonPit-concurrency-contract-and-persistence-races.md`](CR003_RAI_to_RAIkeep_JsonPit-concurrency-contract-and-persistence-races.md) — accepted and finalized for coordinated v3.13.2 implementation

Resolved:

- [`PitSeeder_CR_release_for_cli-resolved-in-v3.13.1.md`](PitSeeder_CR_release_for_cli-resolved-in-v3.13.1.md)
- [`RaiImage_CR_ImageTreeFile_NamingAwareCtor-resolved-in-v3.9.0.md`](RaiImage_CR_ImageTreeFile_NamingAwareCtor-resolved-in-v3.9.0.md)
