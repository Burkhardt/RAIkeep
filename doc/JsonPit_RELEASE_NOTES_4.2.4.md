# JsonPit 4.2.4

Coordinated dependency release for accepted CR016.

- Aligns fallback dependencies on OsLibCore and RaiUtils 4.2.4.
- Preserves CR015 nested tombstones and explicit nested deletion unchanged.
- Introduces no JsonPit public API behavior change.

Release verification: all 156 JsonPit tests passed—154 local/configured cases
plus both isolated live Nkosikazi/Mzansi synchronization scenarios.

RAI retains the manual coordinated release gate; no tag or publication is
authorized by these notes.
