# CR016 — RaiImage Unicode Normalization in Multi-Level Path Bucketing

**Requesting product:** AIA  
**Requesters:** Adele (PM, AIA) and Zébio (Dev, AIA)  
**Receiving product:** RAIkeep (`RaiImage`, with the existing `OsLibCore` file/path boundary)  
**Acceptance owner:** RAI  
**Target release:** Coordinated RAIkeep v4.2.4  
**Date submitted:** 2026-08-27  
**Status:** Implemented and verified — prepared for RAI's manual v4.2.4 release gate  
**AIA proposal:** [CR016 at the reviewed AIA commit](https://github.com/Burkhardt/AIA/blob/55e9820f47a67ef0bd0ec8902c2b90f71ed0a430/doc/CR016_AIA_to_RAIkeep_RaiImage_Unicode_Normalization_Bucketing.md)  
**AIA Step 3 confirmation:** [CR016 Accepted: RaiImage Unicode Normalization in Multi-Level Path Bucketing](https://github.com/Burkhardt/AIA/blob/0c0b22b8a038112a078974172688f7839c80ce0d/doc/CR016_Accepted_RaiImage_Unicode_Normalization_Bucketing.md)

## 1. Objective and observed defect

ImageTree asset identifiers containing canonically equivalent non-ASCII text
could be represented differently at separate directory levels. A live example
stored `Schwäbis` in NFC, `Schwäbisch` in NFD, and the filename in NFD. An NFC
HTTP request could not derive one path spelling that matched every level, so the
asset remained unreachable.

The previous implementation also sliced .NET strings by UTF-16 code units. A
bucket boundary could therefore split a surrogate pair or a multi-code-point
grapheme cluster.

## 2. Accepted provider clarifications

1. The change is assigned to the coordinated v4.2.4 patch line because it is a
   backward-compatible correctness fix.
2. RaiImage-owned logical identifiers and derived segments use Unicode
   Normalization Form C. A caller-provided ImageTree root remains unchanged so
   an existing external filesystem anchor is not silently rewritten.
3. Bucket widths count Unicode text elements rather than UTF-16 code units.
4. Reads resolve canonical-equivalent directory levels and filenames one level
   at a time. Existing assets are not renamed or mutated by lookup.
5. When a normalization-sensitive filesystem contains more than one
   canonically equivalent match, lookup fails with `RaiImageIOException` rather
   than choosing nondeterministically.
6. RaiImage performs traversal through `RaiPath` and `RaiFile`; CR016 adds no
   direct `System.IO` traversal or new identity-management concept.
7. A filesystem such as APFS may expose a decomposed spelling even when an NFC
   string was supplied. The contract governs RaiImage's logical spelling and
   successful reopening, not an impossible guarantee about filesystem-returned
   bytes.

## 3. Implemented behavior

- Subscriber names, item ids, template/name extensions, route values, image
  filenames, and typed ImageTree text artifacts are canonicalized to NFC.
- `ItemTreePath` and `ImageTreeFile` derive all supported bucket conventions by
  Unicode text element.
- Root reconstruction recognizes canonical-equivalent existing bucket suffixes.
- `FromImageTree(...)` resolves subscriber, top bucket, sub-bucket, and source
  filename independently by canonical equivalence.
- Resolved legacy physical paths remain usable for reads while subsequent
  derived outputs retain canonical ImageTree placement.
- SVG participates in default source lookup.

## 4. Acceptance coverage

- German NFC/NFD umlauts at both 8x2 bucket levels and in the filename.
- Portuguese `ã`, `é`, and `ç` in subscriber names, item identifiers, buckets,
  routes, and filenames.
- An African orthography combining sequence (`ḓ`).
- A multi-code-point emoji cluster exactly at a bucket boundary.
- 3x3, 8x2, and canonical-name conventions.
- Typed ImageTree image and text artifacts.
- Deliberately mixed NFC/NFD legacy directory levels.
- Ambiguous canonical-equivalent source detection where the host filesystem
  permits both physical names.

## 5. Release gate

Implementation, regression coverage, API documentation, package release notes,
and coordinated v4.2.4 preparation are authorized. RAI retains the manual
decision to start the release chain. CR016 does not authorize tags or NuGet
publication by the implementing agent.

## 6. Implementation verification

- Coordinated Release build passed across all 14 projects.
- RaiImage focused CR016 suite: 15 cases passed.
- RaiImage complete Release suite: 119 tests passed.
- JsonPit: all 156 tests passed, including both isolated live
  Nkosikazi/Mzansi synchronization scenarios.
- All other coordinated package suites passed: OsLibCore 110, RaiUtils 22,
  RaiDiagram 34, ImgSeeder 16, and PitSeeder 23.
