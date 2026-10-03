# Release Notes: RAIkeep v4.5.0

RAIkeep v4.5.0 coordinates live object reference semantics, sparse mutation tracking, selectable tracking modes in JsonPit, and an automated release validation gate across all nine packages at version 4.5.0.

## JsonPit live references and mutation tracking

JsonPit now adopts caller-supplied live objects and existing nested objects when adding an entity (`Pit.Add(item)`). Current indexers return those exact live references rather than projecting cloned copies on every lookup.

- **Sparse Tracked Mutations:** Supported in-place edits and property indexer mutations immediately append sparse delta fragments internally without rewriting unrelated attributes or earlier history.
- **Per-Instance Tracking Modes:** `Pit.DefaultMutationTrackingMode` configures process-local behavior for new Pits:
  - `TrackedChangesWithFallback` (default): Immediately tracks supported operations and reconciles live values against the last accepted baseline at persistence boundaries. Unreported edits receive their timestamp when detected.
  - `TrackedChangesOnly`: Optimized for server workloads, strictly recording API-tracked mutations without boundary comparisons.
- **Reference Identity Contract:** Verified by `ReferenceTests.ArrayOperator_ReturnsAddedItem`, guaranteeing instance identity (`Assert.Same`) across lookups and mutations.
- **Historical Snapshot Isolation:** Historical reads (`GetAt`, time-travel) remain independent, immutable snapshots.

## Coordinated Package Alignments

- **PitSeeder (`pits`):** Property deletion (`del-prop`) uses live item mutation (`DeletePropertyPath`) directly, appending sparse tombstones without read-modify-write. Reports version 4.5.0.
- **ImgSeeder (`iorg`), RaidSeeder (`raid`), Amafu:** Aligned to 4.5.0 with updated CLI version reporting and install documentation.
- **OsLibCore, RaiUtils, RaiImage, RaiDiagram:** Coordinated foundation and utility dependencies aligned at 4.5.0.
- **Automated Consistency Gate:** Integrated `scripts/validate-release.py` verifying all 9 package project files, code constants, test assertions, docs, and release notes before any tags or releases occur.

## Validation and release coordination

Verification covers all 226 non-remote JsonPit tests, all 84 PitSeeder tests, and remote SSH/cloud drive synchronization scenarios with Mzansi. All package and internal dependency versions align at 4.5.0.

This document does not itself assert that publication has completed. Rainer executes `scripts/release-chain.sh 4.5.0`. Adele maintains Python implementation and parity.
