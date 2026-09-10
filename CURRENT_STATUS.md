# CURRENT_STATUS

Last updated: 2026-09-09

Current released package line: `4.2.8`

Prepared coordinated package line: `4.2.9`

## Released 4.2.8 state

- The RAIkeep umbrella coordinates seven independently published package repositories.
- `OsLibCore`, `RaiUtils`, `RaiImage`, `RaiDiagram`, `JsonPit`, `ImgSeeder`, and `PitSeeder` 4.2.8 are the current coordinated baseline.
- CR021 durable cleanup receipts, explicit maintenance, process-artifact pruning, and legacy-extension repair are available throughout that line.

## Coordinated 4.2.9 preparation

- Accepted CR022 records the 2026-09-09 OneDrive incident investigation and establishes the universal cloud-storage in-place invariant.
- The investigation found no deletion or replacement of the four established live AIA pit directories. OneDrive's mass-deletion prompt was consistent with the explicitly requested retirement of expired process flags and repaired extensionless artifacts.
- A separate report-only defect could create empty missing pit directories through JsonPit's lazy `PitDir`; maintenance now checks the non-creating canonical parent.
- `pits maintain` validates the resolved root and canonical pit files before constructing any `Pit`. Wrong and partial WWWA roots are never filled in implicitly.
- OsLibCore rejects TempDir-to-cloud file and directory moves before mutation, preserves existing cloud file pathnames during replacement, rejects cloud-directory replacement, and copies cloud backups.
- ImgSeeder writes directly to final ItemTree destinations; its retained `tempRoot` parameter is behaviorally inert.
- RaiImage `JpegTran` uses isolated temporary tool files and writes successful result bytes into the continuously present destination pathname.
- All seven package projects and fallback dependency properties align on 4.2.9.
- No v4.2.9 tag, push, GitHub label, workflow dispatch, or NuGet publication has occurred; RAI retains the manual release gate.

## Coordinated release tooling

- `scripts/release-chain.sh` is the single coordinated release orchestrator.
- The enforced order is `OsLibCore → RaiUtils → RaiImage → RaiDiagram → JsonPit → ImgSeeder → PitSeeder`.
- Every package performs a package-only restore before its tag is created.
- The chain waits for both the exact `.nupkg` and exact-version NuGet registration document to return HTTP `200`; it does not use a fixed indexing delay.
- The umbrella label records the exact seven child commits before any package tag is created.

## Documentation state

- Package README links to Markdown documents use absolute GitHub URLs so they work from NuGet as well as GitHub.
- Foldable API references describe every changed public boundary.
- CR022, the cloud-storage invariant, and coordinated 4.2.9 release notes are centralized under `doc/`.
- `scripts/check-markdown-document-links.sh` and its GitHub workflow reject new relative Markdown document links.

## Validation

- All seven complete package Release suites pass: OsLibCore 131, RaiUtils 51, RaiImage 119, RaiDiagram 35, JsonPit 167, ImgSeeder 29, and PitSeeder 41—573/573 total with zero skipped.
- The CR022 focused suites pass on isolated configured-cloud roots: OsLibCore 7, RaiImage 5, JsonPit 2, ImgSeeder 7, and PitSeeder 4.
- Configured-cloud coverage observes established pathnames throughout copy/move replacement and JPEG success/failure; TempDir-to-cloud moves fail before mutation.
- Missing, wrong, and partial maintenance roots remain entry-for-entry unchanged, including directory timestamps.
- CR021 receipt, grace, legacy repair, explicit pruning, finalizer-no-I/O, and abandoned-path-reopenability coverage remains green.
- RaiDiagram's passing suite includes the real local PlantUML integration path.
- The full umbrella Release build succeeds with zero warnings and zero errors.
- The Markdown absolute-link check passes.

## 4.2.9 release readiness

- The seven package implementations, tests, versions, dependency pins, READMEs, API references, and coordinated release notes are complete.
- Every child repository is committed on `main`; the umbrella records those exact seven prepared child commits.
- All eight worktrees are clean, package artifacts have been inspected, and no v4.2.9 tag exists.
- The post-commit branch, pointer, version, workflow-name, and ahead/behind checks pass.
- RAI may start `scripts/release-chain.sh 4.2.9` manually.
