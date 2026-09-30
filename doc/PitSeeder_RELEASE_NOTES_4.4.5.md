# Release Notes: PitSeeder v4.4.5

PitSeeder v4.4.5 implements accepted [`CR047_jsonpit_and_pits_Require-Existing-Patch-Flag-and-Seed-Commit-Count.md`](CR/CR047_jsonpit_and_pits_Require-Existing-Patch-Flag-and-Seed-Commit-Count.md).

## Strict patch mode

- `pits seed <PitName> --source <file> --require-existing` rejects every missing or tombstoned entity ID.
- `--patch` is an exact alias of `--require-existing`.
- The complete payload is parsed and validated before an unflagged, read-only living-state projection is opened.
- Every ID is checked before the normal writable `Pit` is constructed, so rejection creates no process flag, master lease, target directory, or partial write.
- Without either flag, existing upsert behavior remains unchanged.

## Operator feedback and verification

- Successful seeds report `[pits] Successfully committed {N} entity(ies) to Pit '{PitName}'.`
- Strict empty batches fail with a non-zero exit and an explicit diagnostic.
- Sipho's TC-01 through TC-05 are permanent CLI integration tests, supplemented by tombstoned-ID and byte-for-byte no-mutation regressions.
