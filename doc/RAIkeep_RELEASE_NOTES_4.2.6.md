# RAIkeep 4.2.6 Release Notes

**Status:** Implemented, verified, and prepared; not published

**Accepted request:** [CR019 — `WordCase` seam positions and placement in RaiUtils](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR019_AIA_to_RAIkeep_WordCase_Seams_and_Placement.md)

**AIA proposal:** [CR019 at the reviewed AIA commit](https://github.com/Burkhardt/AIA/blob/9b4e98e810409067a477c4c798980ad27f163975/doc/CR019_AIA_to_RAIkeep_WordCase_Seams_and_Placement.md)

RAIkeep 4.2.6 is a coordinated patch across all seven packages.

## CR019 changes

- `WordCase`, `StringHelper`, `WordSplit`, `CamelSplit`, and `ToTitle` now live
  canonically in the dependency-light RaiUtils package.
- RaiUtils adds `WordSeams()`, returning lossless UTF-16 soft-wrap positions
  without altering, normalizing, or validating the supplied text.
- The normative rules cover Pascal/camel joins, acronym endings, digit runs,
  compound separators, structured labels, repeated delimiters, and apostrophe
  preservation.
- Unicode-aware text-element traversal protects surrogate pairs and combining
  sequences and recognizes uppercase German and Portuguese characters at seam
  boundaries.
- RaiImage consumes the RaiUtils implementation and retains only CLR-safe
  compatibility facades for its former public binary names. Legacy facade
  methods are deliberately not extensions, preventing ambiguous extension
  resolution when both namespaces are imported.
- HTML remains a consumer concern: web clients slice the original at the
  returned offsets and insert real `<wbr />` elements.

## Compatibility

- Existing compiled `RaiImage.WordCase` and static
  `RaiImage.StringHelper` calls continue to resolve through compatibility
  facades.
- Recompiled extension-method callers add `using RaiUtils;`, as accepted in
  CR019.
- The operation is a character-preserving display projection. It does not
  define an identifier grammar or convert structured labels into identifiers.

## Verification

- Focused RaiUtils CR019 coverage: 29 passed, 0 failed, 0 skipped.
- Focused RaiImage compatibility coverage: 3 passed, 0 failed, 0 skipped.
- Seven complete package suites: 517 passed, 0 failed, 0 skipped:
  OsLibCore 111, RaiUtils 51, RaiImage 112, RaiDiagram 34, JsonPit 156,
  ImgSeeder 16, and PitSeeder 37.
- The RaiDiagram suite ran with the real PlantUML CLI required and available;
  none of its integration tests were skipped.
- JsonPit's full release suite included its two isolated live Mzansi tests.
- The final coordinated Release build completed with zero errors and zero
  warnings.
- An unchanged consumer assembly compiled against the published 4.2.5
  `RaiImage.WordCase` and `RaiImage.StringHelper` signatures ran successfully
  against the prepared 4.2.6 binaries, proving the intended binary bridge.
- All seven 4.2.6 NuGet packages were packed locally. Package identities,
  embedded READMEs, binaries, and exact 4.2.6 dependency metadata were
  inspected without publishing.
- Markdown document-link and whitespace validation passed.

RAI retains the manual tag and publication gate. These notes do not authorize
the implementing agent to start the release chain.
