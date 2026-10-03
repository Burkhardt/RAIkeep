# Release Notes: JsonPit v4.5.0

4.5.0 adds original live object references, sparse tracked mutations, and per-instance in-memory tracking modes.

`Pit.Add(item)` adopts the original item and nested objects for a new identity. Current accessors return those live references. Tracked edits append sparse fragments; history owns independent snapshots. Projection happens at acceptance/load/merge boundaries.

`Pit.DefaultMutationTrackingMode` defaults to `TrackedChangesWithFallback`. Each Pit captures this process-local policy for its in-memory lifetime; it is never persisted. Servers can choose `TrackedChangesOnly` at startup to disable boundary comparisons. **Unreported edits will receive their history timestamp when detected.** Multiple unreported edits may coalesce, and detection timestamps may affect conflict precedence.

GettingStarted documents live mutation and `people.ItemProperty = new { Id = "Max", ... }`. The mutation guide and agent guidance define supported operations, sparse-history isolation, and concurrency limits. Legacy filename regression tests now match the released naming formats and explicitly test real checksum collisions without overwriting.

All package and internal dependency versions are aligned to 4.5.0. Coordinates platform-wide with automated release consistency validation.

Validation and release handoff: [RAIkeep 4.5.0](https://github.com/Burkhardt/RAIkeep/blob/main/doc/RAIkeep_RELEASE_NOTES_4.5.0.md). Preparation does not publish this package.
