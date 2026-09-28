# RAIkeep 4.4.3 Release Notes

RAIkeep 4.4.3 is the synchronized eight-package delivery of accepted
[`CR043_AfricaStage_to_RAIkeep_Improve-pits-seed-array-error-message.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR043_AfricaStage_to_RAIkeep_Improve-pits-seed-array-error-message.md).

## `pits seed` payload ergonomics

- A single root JSON/JSON5 entity is accepted when it has an exact, non-empty
  string `Id`.
- Arrays and keyed maps remain supported without conversion or migration.
- Invalid roots describe all three accepted forms instead of incorrectly saying
  that a valid root object is not an object.
- Every array/map entry must be an object and every entity must have a valid
  `Id` before the destination pit is opened.
- Rejected payloads therefore create no pit directory, process flag, or partial
  persistence state.

## Release coordination

All eight packages align in this order: OsLibCore, RaiUtils, RaiImage,
RaiDiagram, RaidSeeder, JsonPit, ImgSeeder, and PitSeeder. No filesystem,
cloud-storage, persistence, finalizer, or diagram behavior changes outside the
PitSeeder seed boundary.

Publication remains behind RAI's manual `scripts/release-chain.sh 4.4.3` gate.
