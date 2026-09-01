# JsonPit 4.2.5

Historical projection alignment for accepted CR017.

- Keeps `Pit.GetAt(...)`, timestamped `Pit.ExportJson(...)`, and
  `PitItems.ProjectState(...)` as the authoritative point-in-time engine.
- Carries event ordering, nested tombstones, deletion walls, resurrection, and
  late/backdated-fragment semantics forward unchanged.
- Aligns fallback dependencies on OsLibCore and RaiUtils 4.2.5.

Release verification: all 156 JsonPit tests passed—154 local/configured cases
plus both isolated live Nkosikazi/Mzansi synchronization scenarios.

RAI retains the manual coordinated release gate; no tag or publication is
authorized by these notes.
