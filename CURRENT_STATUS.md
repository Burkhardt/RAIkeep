# CURRENT_STATUS

Last updated: 2026-09-11

Current released package line: `4.2.10`

Prepared coordinated package line: `4.2.11`

## Released 4.2.10 state

- The RAIkeep umbrella coordinates seven independently published package repositories.
- `OsLibCore`, `RaiUtils`, `RaiImage`, `RaiDiagram`, `JsonPit`, `ImgSeeder`, and `PitSeeder` 4.2.10 are the current coordinated baseline.
- CR010 through CR022 contracts remain active throughout the line.

## Coordinated 4.2.11 preparation

- Accepted CR023 adds PlantUML relationship rendering for AIA Activity Interaction diagrams, including the concise `Role` relationship, labels, cardinality, and public accepted-vocabulary discovery.
- Mixed, Activity, ActivityObject, and Sequence compilations opt into PlantUML `allowmixing`; unsupported constructs remain fail-closed and discoverable through `Validate(...)`.
- Accepted CR024 makes explicit read-only and writable `Pit.Dispose()` remove the exact PID-specific process flag they own through `RaiFile.rm()` after the existing durability boundary.
- Default finite `pits` invocations now leave no owned process flag after normal completion or exception unwind. Ctrl+C and process-exit cleanup use the same disposal path.
- `Master.flag`, master-lease TTL, crash recovery, and explicit maintenance pruning are unchanged. Finalizers remain strictly free of filesystem and recovery-publication I/O.
- `--retain-window` remains an explicit 4.x compatibility exception in 4.2.11 and is scheduled for removal in the next major release.
- All seven package projects and fallback dependency properties align on 4.2.11.
- No v4.2.11 tag, push, GitHub label, workflow dispatch, or NuGet publication has occurred; RAI retains the manual release gate.

## Coordinated release tooling

- `scripts/release-chain.sh` is the single coordinated release orchestrator.
- The enforced order is `OsLibCore → RaiUtils → RaiImage → RaiDiagram → JsonPit → ImgSeeder → PitSeeder`.
- Every package performs a package-only restore before its tag is created.
- The chain waits for both the exact `.nupkg` and exact-version NuGet registration document to return HTTP `200`; it does not use a fixed indexing delay.
- The umbrella label records the exact seven child commits before any package tag is created.

## Documentation state

- Every package README identifies 4.2.11 as its current prepared line and links to centralized release notes with absolute GitHub URLs.
- Foldable API references document each changed public library boundary.
- CR023 and CR024 provider records capture the accepted behavior, compatibility exception, and manual release boundary.
- `scripts/check-markdown-document-links.sh` rejects relative Markdown document links; the prepared documentation passes.

## Validation

- All seven complete package Release suites pass with zero skipped tests: OsLibCore 135, RaiUtils 51, RaiImage 119, RaiDiagram 38, JsonPit 176, ImgSeeder 33, and PitSeeder 44—596/596 total.
- RaiDiagram's suite exercises the real, unpruned PlantUML CLI and verifies an Activity/Object relationship SVG contains both endpoints, its role label, and cardinality.
- JsonPit includes the live OneDrive/Mzansi split-master regression and the original no-finalizer-I/O/path-reopenability regression.
- Focused CR024 coverage proves owned deletion, foreign-flag preservation, read-only and writable disposal, `Master.flag` preservation, exceptional CLI cleanup, twenty sequential finite CLI calls with zero residual flags, and explicit `--retain-window` retention.

## 4.2.11 release readiness

- The seven implementations, tests, versions, fallback dependency pins, READMEs, API references, CR records, and coordinated release notes are complete.
- The coordinated Release build succeeds with zero warnings and zero errors.
- All seven package-only dependency restores pass against a local 4.2.11 feed. The seven local packages have been inspected for exact identity, version, dependency pins, package README, and CLI tool payloads.
- All package work is committed on local `main`; the umbrella commit records the exact seven prepared child revisions.
- RAI may start `scripts/release-chain.sh 4.2.11` manually. The release chain remains the only action that pushes, tags, labels, dispatches publishing workflows, or waits for NuGet availability.
