# CURRENT_STATUS

Last updated: 2026-09-10

Current released package line: `4.2.9`

Prepared coordinated package line: `4.2.10`

## Released 4.2.9 state

- The RAIkeep umbrella coordinates seven independently published package repositories.
- `OsLibCore`, `RaiUtils`, `RaiImage`, `RaiDiagram`, `JsonPit`, `ImgSeeder`, and `PitSeeder` 4.2.9 are the current coordinated baseline.
- CR022 cloud-safe in-place filesystem enforcement and CR021 durable cleanup receipts remain active throughout the line.

## Coordinated 4.2.10 preparation

- RAI explicitly authorized implementation of the recovery-event archive backlog.
- `RaiZipFile` creates immutable collection archives directly at the final pathname inside an existing directory; same-name content is validated and never overwritten.
- `PitMaintenanceOptions.ArchiveEvents` and `pits maintain --archive-events` support non-mutating preview and explicit apply for one pit or WWWA.
- Loose event sources remain until complete filename/byte validation succeeds, then retire individually. Retry, corruption, collision, and post-snapshot publication paths retain evidence safely.
- `PitAudit` and `pits audit` combine loose and archived events without extraction and deduplicate by event identity.
- `iorg` adds `-a, --app` application-root addressing and preferred `-t, --tenant`; `-r, --root` remains the exact ImageTree-root alternative and `--subscriber` remains an alias.
- OsLib typed wrappers expose the new `pits` and `iorg` option forms.
- All seven package projects and fallback dependency properties align on 4.2.10.
- No v4.2.10 tag, push, GitHub label, workflow dispatch, or NuGet publication has occurred; RAI retains the manual release gate.

## Coordinated release tooling

- `scripts/release-chain.sh` is the single coordinated release orchestrator.
- The enforced order is `OsLibCore → RaiUtils → RaiImage → RaiDiagram → JsonPit → ImgSeeder → PitSeeder`.
- Every package performs a package-only restore before its tag is created.
- The chain waits for both the exact `.nupkg` and exact-version NuGet registration document to return HTTP `200`; it does not use a fixed indexing delay.
- The umbrella label records the exact seven child commits before any package tag is created.

## Documentation state

- Every package README identifies 4.2.10 as its current prepared line and links to centralized release notes with absolute GitHub URLs.
- Foldable API references document each changed public library boundary.
- The `pits audit` and `iorg` operational manuals document event archives and application-root/tenant addressing respectively.
- `scripts/check-markdown-document-links.sh` and its GitHub workflow reject new relative Markdown document links.

## Validation

- All seven complete package Release suites pass: OsLibCore 135, RaiUtils 51, RaiImage 119, RaiDiagram 35, JsonPit 174, ImgSeeder 33, and PitSeeder 43—590/590 total with zero skipped.
- The RaiDiagram suite exercised the real local PlantUML integration path.
- Focused archive coverage includes preview, apply, single-pit/WWWA CLI paths, immutable retry, corruption/collision retention, identity deduplication, and post-snapshot event publication.
- Focused iorg coverage proves app-root/tenant resolution, exact-root equivalence, aliases, mutual exclusion, required tenant validation, and help alignment.
- The coordinated Release build succeeds with zero warnings and zero errors; the umbrella solution now includes the ImgSeeder executable explicitly, so every deliverable builds under `Release`.
- All seven local `4.2.10` NuGet artifacts have been packed and inspected for exact package identity, version, coordinated dependency pins, package README, and CLI tool payloads.

## 4.2.10 release readiness

- The seven package implementations, tests, versions, dependency pins, READMEs, API references, coordinated release notes, and local package inspections are complete.
- All package work is committed on `main`; the umbrella commit records the exact seven prepared child revisions.
- RAI may start `scripts/release-chain.sh 4.2.10` manually. The release chain remains the only action that pushes, tags, labels, dispatches publishing workflows, or waits for NuGet availability.
