# RAIkeep 4.2.4 Release Notes

**Status:** Prepared source and verification candidate; not published  
**Accepted request:**
[`CR016_AIA_to_RAIkeep_RaiImage_Unicode_Normalization_Bucketing.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR016_AIA_to_RAIkeep_RaiImage_Unicode_Normalization_Bucketing.md)  
**AIA proposal:**
[`CR016_AIA_to_RAIkeep_RaiImage_Unicode_Normalization_Bucketing.md`](https://github.com/Burkhardt/AIA/blob/55e9820f47a67ef0bd0ec8902c2b90f71ed0a430/doc/CR016_AIA_to_RAIkeep_RaiImage_Unicode_Normalization_Bucketing.md)  
**AIA Step 3 confirmation:**
[`CR016_Accepted_RaiImage_Unicode_Normalization_Bucketing.md`](https://github.com/Burkhardt/AIA/blob/0c0b22b8a038112a078974172688f7839c80ce0d/doc/CR016_Accepted_RaiImage_Unicode_Normalization_Bucketing.md)

RAIkeep 4.2.4 is a coordinated, backward-compatible patch across all seven
packages.

## CR016 changes

- RaiImage canonicalizes ImageTree-owned subscriber names, item identifiers,
  templates, filenames, route values, and typed text artifacts to Unicode NFC.
- Caller-provided ImageTree roots retain their original filesystem spelling.
- 3x3, 8x2, and canonical-name bucket widths count Unicode text elements rather
  than UTF-16 code units.
- Reads resolve legacy NFC, NFD, and mixed-normalization directories and files
  segment by segment without renaming them.
- Canonically ambiguous directories or source files fail explicitly with
  `RaiImageIOException`.
- SVG joins RaiImage's default source lookup extensions.
- Filesystem traversal uses the established OsLib `RaiPath`/`RaiFile` boundary.

## Compatibility

- Existing ASCII ImageTree placement is unchanged.
- Existing non-ASCII trees remain readable even when historical directory
  levels use different canonical Unicode representations.
- New outputs use RaiImage's canonical NFC logical spelling; APFS/HFS may expose
  a filesystem-normalized spelling while remaining canonically reopenable.
- The accepted CR015 tombstone, delete-command, and typed CLI contracts carry
  forward unchanged.
- No identity subsystem, package removal, CLI syntax change, or raw process
  boundary is introduced.

## Verification

- Coordinated Release build: passed (all 14 solution projects).
- OsLibCore: 110 tests passed.
- RaiUtils: 22 tests passed.
- RaiImage: 119 tests passed, including 15 dedicated CR016 cases.
- RaiDiagram: 34 tests passed through the real PlantUML integration path.
- JsonPit: all 156 tests passed (154 local/configured cases plus both isolated
  live Nkosikazi/Mzansi synchronization scenarios).
- ImgSeeder: 16 tests passed.
- PitSeeder: 23 tests passed.

RAI retains the manual tag and publication gate. These notes do not authorize
the implementing agent to start the release chain.
