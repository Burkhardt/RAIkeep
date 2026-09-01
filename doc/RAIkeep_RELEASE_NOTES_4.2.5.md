# RAIkeep 4.2.5 Release Notes

**Status:** Prepared and verified; not published
**Accepted request:**
[`CR017_AIA_to_RAIkeep_Pits_Point_in_Time_Export.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR017_AIA_to_RAIkeep_Pits_Point_in_Time_Export.md)
**AIA proposal:**
[`CR017_AIA_to_RAIkeep_Pits_Point_in_Time_Export.md`](https://github.com/Burkhardt/AIA/blob/923cbddbefd0c69730a99746bedd16f150397050/doc/CR017_AIA_to_RAIkeep_Pits_Point_in_Time_Export.md)
**AIA Step 3 confirmation:**
[`CR017_Accepted_Pits_Point_in_Time_Export.md`](https://github.com/Burkhardt/AIA/blob/1394850b5fd8fc77e74a9e9fa28903d333c87aa7/doc/CR017_Accepted_Pits_Point_in_Time_Export.md)

RAIkeep 4.2.5 is a coordinated, backward-compatible patch across all seven
packages.

## CR017 changes

- `pits export` accepts optional `--at` for single-pit and WWWA targets through
  both `--json` and `--out-dir`.
- Offset-explicit timestamps are normalized to UTC and evaluated inclusively.
- Projection delegates to JsonPit's existing historical engine over all
  history available to the invocation.
- Point-in-time output uses the strict `_export`/`data` envelope with distinct
  `at` and `exported` UTC timestamps.
- No-`--at` exports retain their established unwrapped array/object shape.
- WWWA projection builds its lookup from four independently projected pits;
  missing targets remain safely unresolved at the source reference.
- OsLibCore exposes the same capability through optional
  `PitsExportRequest.At` with exact argument tokenization.

## Temporal and compatibility boundary

- `at` is the requested event-time cutoff. `exported` is when the command built
  the document from history then available.
- `exported` is not a distributed synchronization barrier or a completeness
  guarantee. The same `at` can yield a different result after late or backdated
  history arrives.
- Items not yet created, or deleted at the cutoff, are omitted.
- Existing output filenames remain unchanged because provenance is stored in
  the point-in-time document.
- CR016 Unicode-safe ImageTree behavior and CR015 nested deletion behavior
  carry forward unchanged.

## Verification

- Coordinated Release build: passed (all 14 solution projects).
- OsLibCore: 111 tests passed.
- RaiUtils: 22 tests passed.
- RaiImage: 119 tests passed.
- RaiDiagram: 34 tests passed through the real PlantUML integration path.
- JsonPit: all 156 tests passed (154 local/configured cases plus both isolated
  live Nkosikazi/Mzansi synchronization scenarios).
- ImgSeeder: 16 tests passed.
- PitSeeder: 37 tests passed, including 14 focused CR017 cases.

RAI retains the manual tag and publication gate. These notes do not authorize
the implementing agent to start the release chain.
