# Release Notes: PitSeeder v4.5.0

4.5.0 uses live JsonPit property deletion and aligned dependencies; pits reports version 4.5.0.

Property deletion now calls the live item's `DeletePropertyPath` directly. JsonPit appends the sparse tombstone internally; CLI syntax and Save boundaries stay the same.

All package and internal dependency versions are aligned to 4.5.0, coordinating live object reference semantics, sparse mutation tracking, and automated release validation gating across the entire RAIkeep platform.

Validation and release handoff: [RAIkeep 4.5.0](https://github.com/Burkhardt/RAIkeep/blob/main/doc/RAIkeep_RELEASE_NOTES_4.5.0.md). Preparation does not publish this package.
