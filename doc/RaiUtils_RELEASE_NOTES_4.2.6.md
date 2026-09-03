# RaiUtils 4.2.6 Release Notes

Implements accepted CR019 in the coordinated RAIkeep 4.2.6 release.

- Makes `RaiUtils.WordCase` and `RaiUtils.StringHelper` the canonical home for
  general word-case conversion and splitting.
- Adds lossless `WordSeams()` UTF-16 offsets for display soft-wrapping.
- Applies the normative acronym, case-transition, digit, separator,
  apostrophe, and whitespace rules.
- Traverses Unicode text elements so surrogate pairs and combining sequences
  are never split.
- Adds German, Portuguese, structured-label, repeated-separator, and exact
  round-trip regression coverage.
