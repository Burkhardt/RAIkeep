# RAIkeep

## Terminal font for RAIkeep CLIs

ImgSeeder (`iorg`) and PitSeeder (`pits`) use embedded Nerd Font provider and numbered-option glyphs in their help output. Installation instructions for Blink on iPadOS, macOS, and Ubuntu—including the Blink CSS font-family stylesheet URL—are in [TERMINAL_FONTS.md](https://github.com/Burkhardt/RAIkeep/blob/main/doc/TERMINAL_FONTS.md).

`RAIkeep` is the umbrella workspace for five related .NET libraries and three command-line packages:

| Order | Repository | Package / command | Current or upcoming role |
|---:|---|---|---|
| 1 | `OsLib` | `OsLibCore` | 4.4.0 synchronized foundation |
| 2 | `RaiUtils` | `RaiUtils` | 4.4.0 synchronized dependency line |
| 3 | `RaiImage` | `RaiImage` | 4.4.0 synchronized dependency line |
| 4 | `RaiDiagram` | `RaiDiagram` | 4.4.0 CR036 import and aim-SVG APIs |
| 5 | `RaidCli` | `RaidCli` / `raid` | 4.4.0 CR036 diagram interchange CLI |
| 6 | `JsonPit` | `JsonPit` | 4.4.0 synchronized dependency line |
| 7 | `ImgSeeder` | `ImgSeeder` / `iorg` | 4.4.0 synchronized dependency line |
| 8 | `PitSeeder` | `PitSeeder` / `pits` | 4.4.0 comment-tolerant seed ingestion |

Each child remains its own Git repository, package, solution, and release
workflow. The umbrella workspace supplies local project wiring, coordinated
validation, dependency-order documentation, and sequential release automation.

## Current release line

The prepared coordinated release is `4.4.0`. RAI starts the release chain
manually after reviewing the prepared commits and verification results.

RAIkeep 4.4.0 implements accepted CR036. `RaiDiagram` adds an extensible
`IModelImporter` boundary, modern PlantUML activity/class ingestion, typed
deterministic canvas geometry, and public `aim-*` SVG emission/validation.
The separate `RaidCli` repository contributes the new `raid` command.

The principal functional changes are:

- `raid import --puml ...` writes canonical `.raid` and RaidCanvas-hydratable SVG.
- `raid validate ...` validates `.raid` or `aim-*` SVG input without Java or Graphviz.
- `raid --version`, `pits --version`, and `iorg --version` report `4.4.0`.
- `pits seed` accepts JSON5 line/block comments before the root array or map while still rejecting malformed payloads.
- The umbrella `v4.4.0` tag automatically creates GitHub Release `RAIkeep v4.4.0` from the matching release-notes document.

All eight packages participate in the coordinated line so fallback package dependencies remain aligned throughout the release order.

## Documentation

All change requests and release notes are centralized in [`doc/`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/README.md). Child repositories should not contain independent `CR_*.md` or `RELEASE_NOTES*.md` files.

Current coordinated 4.4.0 release notes:

- [OsLibCore 4.4.0](https://github.com/Burkhardt/RAIkeep/blob/main/doc/OsLib_RELEASE_NOTES_4.4.0.md)
- [RaiUtils 4.4.0](https://github.com/Burkhardt/RAIkeep/blob/main/doc/RaiUtils_RELEASE_NOTES_4.4.0.md)
- [RaiImage 4.4.0](https://github.com/Burkhardt/RAIkeep/blob/main/doc/RaiImage_RELEASE_NOTES_4.4.0.md)
- [RaiDiagram 4.4.0](https://github.com/Burkhardt/RAIkeep/blob/main/doc/RaiDiagram_RELEASE_NOTES_4.4.0.md)
- [RaidCli 4.4.0](https://github.com/Burkhardt/RAIkeep/blob/main/doc/RaidCli_RELEASE_NOTES_4.4.0.md)
- [JsonPit 4.4.0](https://github.com/Burkhardt/RAIkeep/blob/main/doc/JsonPit_RELEASE_NOTES_4.4.0.md)
- [ImgSeeder 4.4.0](https://github.com/Burkhardt/RAIkeep/blob/main/doc/ImgSeeder_RELEASE_NOTES_4.4.0.md)
- [PitSeeder 4.4.0](https://github.com/Burkhardt/RAIkeep/blob/main/doc/PitSeeder_RELEASE_NOTES_4.4.0.md)
- [RAIkeep 4.4.0](https://github.com/Burkhardt/RAIkeep/blob/main/doc/RAIkeep_RELEASE_NOTES_4.4.0.md)

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
scripts/release-chain.sh 4.4.0
```

Before publication begins, all eight child release commits and their exact submodule pointers must already be committed on the umbrella `main`. The script preflights that state, pushes the prepared umbrella `main`, and applies the passed version as its tag first. The umbrella tag publishes no NuGet package; it creates and verifies the synchronized GitHub Release before package tagging begins.

It then processes packages in this exact order:

```text
OsLibCore → RaiUtils → RaiImage → RaiDiagram → RaidCli → JsonPit → ImgSeeder → PitSeeder
```

For every package before the next repository is pushed/tagged:

1. Push the prepared repository `main` only if it is ahead.
2. Push that repository's requested version tag, such as `v4.4.0`, to trigger its publish workflow.
3. Wait for the matching GitHub workflow to finish successfully.
4. Verify the exact `.nupkg` and exact-version registration document are both visible from NuGet with HTTP `200`.
5. Only then continue to the next repository.

The chain waits on observed NuGet availability rather than a fixed delay. Do not run multiple release mechanisms for the same version. The local script refuses to move an existing conflicting version tag and verifies at the end that the umbrella still records the exact released child commits.

Detailed operational guidance is in [RunReleaseChain.md](https://github.com/Burkhardt/RAIkeep/blob/main/RunReleaseChain.md).

## Working conventions

- Preserve the real machine configuration file as the source of truth; do not substitute environment variables or rewrite configuration for test isolation.
- Keep the shared configured cloud-root contract aligned on `Dropbox`, `OneDrive`, `GoogleDrive`, and `ICloudDrive`.
- Use OsLib path/file abstractions in JsonPit and the CLIs instead of introducing direct filesystem operations where an OsLib API applies.
- Follow the mandatory [cloud-storage in-place invariant](https://github.com/Burkhardt/RAIkeep/blob/main/doc/Cloud-Storage-In-Place-Invariant.md): never move a TempDir-created file or directory into a configured cloud tree, and never replace an established cloud pathname as an implementation detail.
- Keep one in-memory `Pit` instance per distinct pit path in a long-running process and share it through the application container/singleton mechanism.
