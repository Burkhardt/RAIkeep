# Release Notes: RAIkeep v4.4.5

RAIkeep v4.4.5 implements accepted [`CR047_jsonpit_and_pits_Require-Existing-Patch-Flag-and-Seed-Commit-Count.md`](CR/CR047_jsonpit_and_pits_Require-Existing-Patch-Flag-and-Seed-Commit-Count.md) as a coordinated nine-package release.

## `pits seed` strict patch safety

- Adds `--require-existing` and its `--patch` alias for single-pit seed operations.
- Validates every ID against current living state before opening a writable Pit.
- Missing and tombstoned IDs abort the entire batch with exit code `1`; no valid sibling patch is partially committed.
- Empty strict batches fail explicitly, while default no-flag seed/upsert behavior remains backward compatible.
- Successful seeds report the exact committed payload count.
- `OsLibCore.PitsSeedRequest.RequireExisting` exposes the canonical strict-patch token to services and agents without hand-built process arguments.

## Coordination and validation

- Preflight uses an unflagged, read-only projection, preserving JsonPit's process-window, master-lease, eventual-durability, and cloud-safe in-place contracts.
- Sipho's five acceptance vectors and additional tombstone/no-side-effect cases run through the real managed `pits` command wrapper.
- All nine packages align at 4.4.5 so fallback dependencies remain synchronized throughout the release order.

Tagging, GitHub Releases, and NuGet publication remain behind RAI's manual release-chain gate.
