# RAIkeep

## Terminal font for RAIkeep CLIs

ImgSeeder (`iorg`) and PitSeeder (`pits`) use embedded Nerd Font provider and numbered-option glyphs in their help output. Installation instructions for Blink on iPadOS, macOS, and Ubuntu—including the Blink CSS font-family stylesheet URL—are in [TERMINAL_FONTS.md](https://github.com/Burkhardt/RAIkeep/blob/main/doc/TERMINAL_FONTS.md).

`RAIkeep` is the umbrella workspace for five related .NET libraries and two command-line packages:

| Order | Repository | Package / command | Current or upcoming role |
|---:|---|---|---|
| 1 | `OsLib` | `OsLibCore` | 4.2.4: coordinated path/file and tool boundary |
| 2 | `RaiUtils` | `RaiUtils` | 4.2.4: coordinated shared exception foundation |
| 3 | `RaiImage` | `RaiImage` | 4.2.4: Unicode-safe ImageTree bucketing and legacy lookup |
| 4 | `RaiDiagram` | `RaiDiagram` | 4.2.4: Unicode-safe diagram artifact dependency line |
| 5 | `JsonPit` | `JsonPit` | 4.2.4 coordinated dependency line |
| 6 | `ImgSeeder` | `ImgSeeder` / `iorg` | 4.2.4: Unicode-safe organized image destinations |
| 7 | `PitSeeder` | `PitSeeder` / `pits` | 4.2.4 coordinated dependency line |

Each child remains its own Git repository, package, solution, and release
workflow. The umbrella workspace supplies local project wiring, coordinated
validation, dependency-order documentation, and sequential release automation.

## Current release line

The prepared coordinated release is `4.2.4`. RAI starts the release chain
manually after reviewing the prepared commits and verification results.

RAIkeep 4.2.4 implements accepted CR016. RaiImage normalizes ImageTree-owned
logical names to NFC before deriving buckets or filenames, slices prefixes by
Unicode text elements, and resolves legacy NFC, NFD, or mixed-normalization
trees segment by segment.

The principal functional changes are:

- `RaiImage`: canonicalizes subscriber names, item identifiers, templates, image filenames, and typed ImageTree text artifacts to Unicode NFC.
- `RaiImage`: derives 3x3, 8x2, and canonical-name buckets by Unicode text elements so surrogate pairs and combining sequences are never split.
- `RaiImage`: resolves legacy directory levels and source filenames by canonical equivalence while preserving the caller-provided ImageTree root.
- `RaiImage`: fails with `RaiImageIOException` when a normalization-sensitive filesystem contains ambiguous canonically equivalent matches.
- `RaiImage`: includes SVG in its default source-image lookup extensions.
- Directory and file discovery stays behind OsLib's `RaiPath`/`RaiFile` boundary.
- The accepted CR015 nested tombstone, delete-command, and typed CLI contracts carry forward unchanged.

RaiUtils, RaiImage, and ImgSeeder participate in the same major line so fallback package dependencies remain aligned throughout the release order.

## Documentation

All change requests and release notes are centralized in [`doc/`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/README.md). Child repositories should not contain independent `CR_*.md` or `RELEASE_NOTES*.md` files.

Current coordinated 4.2.4 release notes:

- [OsLibCore 4.2.4](https://github.com/Burkhardt/RAIkeep/blob/main/doc/OsLib_RELEASE_NOTES_4.2.4.md)
- [RaiUtils 4.2.4](https://github.com/Burkhardt/RAIkeep/blob/main/doc/RaiUtils_RELEASE_NOTES_4.2.4.md)
- [RaiImage 4.2.4](https://github.com/Burkhardt/RAIkeep/blob/main/doc/RaiImage_RELEASE_NOTES_4.2.4.md)
- [RaiDiagram 4.2.4](https://github.com/Burkhardt/RAIkeep/blob/main/doc/RaiDiagram_RELEASE_NOTES_4.2.4.md)
- [JsonPit 4.2.4](https://github.com/Burkhardt/RAIkeep/blob/main/doc/JsonPit_RELEASE_NOTES_4.2.4.md)
- [ImgSeeder 4.2.4](https://github.com/Burkhardt/RAIkeep/blob/main/doc/ImgSeeder_RELEASE_NOTES_4.2.4.md)
- [PitSeeder 4.2.4](https://github.com/Burkhardt/RAIkeep/blob/main/doc/PitSeeder_RELEASE_NOTES_4.2.4.md)
- [RAIkeep 4.2.4](https://github.com/Burkhardt/RAIkeep/blob/main/doc/RAIkeep_RELEASE_NOTES_4.2.4.md)

The prior coordinated line remains documented in [RAIkeep 4.1.0 release notes](https://github.com/Burkhardt/RAIkeep/blob/main/doc/RAIkeep_RELEASE_NOTES_4.1.0.md).

Flag and coordination behavior is documented in [JsonPit flag files and concurrency](https://github.com/Burkhardt/RAIkeep/blob/main/doc/JsonPit-FlagFiles-And-Concurrency.md). It explains the distinction between per-process activity windows and the stable master-writer lease without replacing the separate open concurrency CR.

## Local validation

From the workspace root:

```bash
dotnet build RAIkeep.slnx
dotnet test OsLib/OsLib.Tests/OsLib.Tests.csproj
dotnet test RaiUtils/RaiUtils.slnx
dotnet test RaiImage/RaiImage.slnx
dotnet test RaiDiagram/RaiDiagram.slnx
dotnet test ImgSeeder/ImgSeeder.slnx
dotnet test PitSeeder/PitSeeder.slnx
```

The JsonPit suite includes real cloud/remote scenarios and a separately documented open concurrency regression. Use the validation scope stated in the JsonPit release notes rather than hiding those distinctions behind incidental test-runner parallelism or local configuration substitution.

## Strict release gate

Publication requires explicit approval. Preparing versions, documentation, commits, or packages does not authorize a push, tag, workflow dispatch, or NuGet publication.

After approval, use one release mechanism for the chain. The established local orchestrator is:

```bash
cd /Users/RSB/Projects/GitHub/RAIkeep
scripts/release-chain.sh 4.2.4
```

Before publication begins, all seven child release commits and their exact submodule pointers must already be committed on the umbrella `main`. The script preflights that state, pushes the prepared umbrella `main`, and applies the passed version as its tag first. The umbrella tag does not publish a package; its workflow is manual-only.

It then processes packages in this exact order:

```text
OsLibCore → RaiUtils → RaiImage → RaiDiagram → JsonPit → ImgSeeder → PitSeeder
```

For every package before the next repository is pushed/tagged:

1. Push the prepared repository `main` only if it is ahead.
2. Push that repository's requested version tag, such as `v4.2.4`, to trigger its publish workflow.
3. Wait for the matching GitHub workflow to finish successfully.
4. Verify the exact `.nupkg` and exact-version registration document are both visible from NuGet with HTTP `200`.
5. Only then continue to the next repository.

The chain waits on observed NuGet availability rather than a fixed delay. Do not run multiple release mechanisms for the same version. The local script refuses to move an existing conflicting version tag and verifies at the end that the umbrella still records the exact released child commits.

Detailed operational guidance is in [RunReleaseChain.md](https://github.com/Burkhardt/RAIkeep/blob/main/RunReleaseChain.md).

## Working conventions

- Preserve the real machine configuration file as the source of truth; do not substitute environment variables or rewrite configuration for test isolation.
- Keep the shared configured cloud-root contract aligned on `Dropbox`, `OneDrive`, `GoogleDrive`, and `ICloudDrive`.
- Use OsLib path/file abstractions in JsonPit and the CLIs instead of introducing direct filesystem operations where an OsLib API applies.
- Do not use temporary-file rename replacement for canonical pits or cloud-backed coordination flags.
- Keep one in-memory `Pit` instance per distinct pit path in a long-running process and share it through the application container/singleton mechanism.
