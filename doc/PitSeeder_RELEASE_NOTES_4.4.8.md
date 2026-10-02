# Release Notes: PitSeeder v4.4.8

4.4.8 uses live JsonPit property deletion and aligned dependencies; pits reports version 4.4.8.

Property deletion now calls the live item's `DeletePropertyPath` directly. JsonPit appends the sparse tombstone internally; CLI syntax and Save boundaries stay the same.

All package and internal dependency versions are aligned to 4.4.8. The version intentionally skips C# 4.4.7 to align the next coordinated release with jsonpit-python; Python implementation and publication remain with its maintainer.

Validation and release handoff: [RAIkeep 4.4.8](https://github.com/Burkhardt/RAIkeep/blob/main/doc/RAIkeep_RELEASE_NOTES_4.4.8.md). Preparation does not publish this package.
