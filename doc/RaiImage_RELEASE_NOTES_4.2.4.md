# RaiImage 4.2.4

Implements accepted CR016 Unicode normalization in multi-level ImageTree
bucketing and lookup.

- Normalizes ImageTree-owned subscriber names, item ids, templates, filenames,
  route values, and typed text artifacts to Unicode NFC.
- Preserves caller-provided ImageTree root paths.
- Calculates 3x3, 8x2, and canonical-name prefixes by Unicode text elements.
- Prevents bucket slicing through combining sequences, surrogate pairs, or
  multi-code-point emoji clusters.
- Resolves legacy NFC, NFD, and mixed-normalization directories and source files
  one segment at a time through `RaiPath` and `RaiFile` enumeration.
- Preserves the resolved physical legacy source path for reading while new
  derived outputs retain canonical placement.
- Rejects ambiguous canonically equivalent matches with
  `RaiImageIOException`.
- Includes SVG in `DefaultSourceExtensions`.
- Aligns fallback dependencies on OsLibCore and RaiUtils 4.2.4.

Release verification: all 119 RaiImage Release tests passed. Fifteen dedicated
CR016 cases cover German umlauts; Portuguese `ã`, `é`, and `ç`; an African
orthography combining sequence; mixed legacy trees; every path convention; and
Unicode text-element boundaries.

RAI retains the manual coordinated release gate; no tag or publication is
authorized by these notes.
