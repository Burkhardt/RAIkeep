# RAIkeep centralized documents

This directory is the umbrella workspace location for release notes and change requests from all RAIkeep child projects.

Files are flattened into this directory and prefixed with their source project to prevent collisions:

- `<Project>_RELEASE_NOTES_<version>.md`
- `<Project>_CR_<request>.md`

Do not add `RELEASE_NOTES*.md` or `CR_*.md` files to child-project directories. Move them here and retain the project prefix.

## Technical guides

- [`JsonPit-FlagFiles-And-Concurrency.md`](JsonPit-FlagFiles-And-Concurrency.md) explains the separate per-process activity flags, stable `Master.flag` lease, canonical-write decision, CLI cleanup, and current coordination boundary.

## Change requests

Open:

- [`JsonPit_CR_concurrency-for-next-release-RAI-commented.md`](JsonPit_CR_concurrency-for-next-release-RAI-commented.md)

Resolved:

- [`PitSeeder_CR_release_for_cli-resolved-in-v3.13.1.md`](PitSeeder_CR_release_for_cli-resolved-in-v3.13.1.md)
- [`RaiImage_CR_ImageTreeFile_NamingAwareCtor-resolved-in-v3.9.0.md`](RaiImage_CR_ImageTreeFile_NamingAwareCtor-resolved-in-v3.9.0.md)
