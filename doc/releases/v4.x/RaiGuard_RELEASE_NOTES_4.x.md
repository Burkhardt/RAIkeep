# RaiGuard Release Notes 4.x

## 4.6.0

- Release version: `4.6.0`
- Coordination tag: `v4.6.0`

### Highlights
- Resolve RAI011/RAI012 receivers semantically, track chronological aliases, collections and bounded source helpers, and preserve supported same-owner live mutations. Share semantic analysis with rail and report incomplete reference resolution explicitly.

### Coordinated Dependencies
- Aligned with RAIkeep synchronized `4.6.0` line.

---

## 4.5.18

- Release version: `4.5.18`
- Coordination tag: `v4.5.18`

### Highlights
- Show the executing machine as "on <machine>" in the CLI banner. Size both decorative rules to the complete heading, including the hostname; preserve bold cyan styling and plain redirected output. Apply the same heading to the grouped rule display.

### Coordinated Dependencies
- Aligned with RAIkeep synchronized `4.5.18` line.

---

## 4.5.17

- Release version: `4.5.17`
- Coordination tag: `v4.5.17`

### Highlights
- Includes RAI002 file-size diagnostics and the semantic FileInfo.Length code fix from the interrupted 4.5.16 preparation. Prefer an existing RaiFile.Length expression when its type can be proved; otherwise offer the supported typed path wrapper.

### Coordinated Dependencies
- Aligned with RAIkeep synchronized `4.5.17` line.

---

## 4.5.16

- Release version: `4.5.16`
- Coordination tag: `v4.5.16`

### Highlights
- Extend RAI002 with explicit RaiFile.Length guidance for file-size reads during compilation and inline rail checks.
- Add a conservative semantic Roslyn code fix that reuses a verified RaiFile receiver or constructs RaiFile from a path.
- Preserve other RAI002 diagnostics and refuse fixes when the referenced OsLib lacks the required API.

### Coordinated Dependencies
- Aligned with RAIkeep synchronized `4.5.16` line.

---

## 4.5.15

- Release version: `4.5.15`
- Coordination tag: `v4.5.15`

### Highlights
- Apply the shared rail help theme and extend banner rules to the complete heading width.
- Wrap grouped descriptions and rule entries at 90 visible columns without splitting words. Align rule rows with Description, omit bullets/brackets, and keep every rule ID bold blue.
- Use quoted-code styling for group names, italic magenta description labels, yellow description text, and cyan rule titles. Analyzer rule semantics are unchanged.

### Coordinated Dependencies
- Aligned with RAIkeep synchronized `4.5.15` line.

---

## 4.5.14

- Release version: `4.5.14`
- Coordination tag: `v4.5.14`

### Highlights
- Add conservative RAI006 code fixes for immediately executed seed calls with recoverable constant tokens, plus canonical tenant-scoped factory guidance.
- Include the existing RAI011 correction for freshly generated items, with underscore-prefixed Pit-field recognition and regression coverage for proven snapshots.
- Include the current RAI017 media-URL composition diagnostic and code fix from the RaiGuard work.

### Coordinated Dependencies
- Aligned with RAIkeep synchronized `4.5.14` line.

---

## 4.5.13

- Release version: `4.5.13`
- Coordination tag: `v4.5.13`

### Highlights
- Coordinated version alignment; no package-local behavior change.

### Coordinated Dependencies
- Aligned with RAIkeep synchronized `4.5.13` line.

---

## 4.5.12

- Release version: `4.5.12`
- Coordination tag: `v4.5.12`

### Highlights
- Publish the prepared 16-rule analyzer and CLI changes with coordinated 4.5.12 package versions.

### Coordinated Dependencies
- Aligned with RAIkeep synchronized `4.5.12` line.

---

## 4.5.11

- Release version: `4.5.11`
- Coordination tag: `v4.5.11`

### Highlights
- Expand the analyzer and `rail` CLI from the earlier rule set to 16 numbered architecture rules. Add code fixes, CLI rewrites, architecture rule documentation, and updated tutorial guidance.

### Coordinated Dependencies
- Aligned with RAIkeep synchronized `4.5.11` line.

---

## 4.5.10

- Release version: `4.5.10`
- Coordination tag: `v4.5.10`

### Highlights
- Coordinated 4.5.10 version alignment; no package-local behavior change.

### Coordinated Dependencies
- Aligned with RAIkeep synchronized `4.5.10` line.

---

## 4.5.9

- Release version: `4.5.9`
- Coordination tag: `v4.5.9`

### Highlights
- Coordinated 4.5.9 version alignment; no package-local behavior change.

### Coordinated Dependencies
- Aligned with RAIkeep synchronized `4.5.9` line.

---

## 4.5.8

- Release version: `4.5.8`
- Coordination tag: `v4.5.8`

### Highlights

- RaiGuard joins the RAIkeep umbrella as the `rail` global tool and Roslyn analyzer package.
- The coordinated installer provisions `rail` with the other fleet CLIs.
- The release chain verifies both the `RaiGuard` tool and `RaiGuard.Analyzer` NuGet packages.

### Coordinated Dependencies

- Aligned with the RAIkeep synchronized `4.5.8` line.
