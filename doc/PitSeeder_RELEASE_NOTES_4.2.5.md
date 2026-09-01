# PitSeeder 4.2.5

Implements accepted CR017 point-in-time export.

- Adds `--at <timestamp>` to single-pit and WWWA exports through both `--json`
  and `--out-dir`.
- Requires an explicit `Z` or numeric UTC offset and evaluates history
  inclusively at the requested instant.
- Uses JsonPit's established historical projection, tombstone, deletion-wall,
  resurrection, and ordering rules rather than introducing a second algorithm.
- Emits strict `{ "_export": { "at", "exported" }, "data": ... }` JSON only
  when `--at` is present; no-`--at` output retains its established root shape.
- Projects the four WWWA pits independently, then performs existing one-level
  resolution. Missing targets are omitted from the lookup while source
  references remain safely unresolved.
- Keeps established output filenames unchanged and reports `pits v4.2.5`.
- Aligns fallback dependencies on JsonPit and OsLibCore 4.2.5.

Release verification: 37 PitSeeder Release tests passed, including 14 focused
CR017 cases covering parsing, temporal boundaries, deletion, resurrection,
late history, filenames, envelopes, and WWWA resolution.

RAI retains the manual coordinated release gate; no tag or publication is
authorized by these notes.
