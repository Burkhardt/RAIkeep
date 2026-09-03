# RaiImage 4.2.6 Release Notes

Adopts the accepted CR019 package-boundary correction in the coordinated
RAIkeep 4.2.6 release.

- Consumes word-case conversion and splitting from RaiUtils.
- Removes the independent word-case implementation from RaiImage.
- Retains `RaiImage.WordCase` and ordinary static `RaiImage.StringHelper`
  compatibility facades for callers compiled against earlier package lines.
- Keeps legacy facade methods out of extension-method discovery, preventing
  ambiguous calls when `RaiImage` and `RaiUtils` are both imported.
- Aligns fallback dependencies on `OsLibCore 4.2.6` and `RaiUtils 4.2.6`.
