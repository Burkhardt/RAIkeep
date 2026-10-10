# RAIkeep

## Terminal font for RAIkeep CLIs

Amafu (`amafu`), RaidSeeder (`raid`), ImgSeeder (`iorg`), and PitSeeder (`pits`) use embedded Nerd Font provider and numbered-option glyphs in their help output. Installation instructions for Blink on iPadOS, macOS, and Ubuntu—including the Blink CSS font-family stylesheet URL—are in [TERMINAL_FONTS.md](https://github.com/Burkhardt/RAIkeep/blob/main/doc/TERMINAL_FONTS.md).

`RAIkeep` is the umbrella workspace for five related .NET libraries and four command-line packages:

| Order | Repository | Package / command | Current or upcoming role |
|---:|---|---|---|
| 1 | `Amafu` | `Amafu` / `amafu` | 4.5.5 synchronized cloud configuration tool |
| 2 | `OsLib` | `OsLibCore` | 4.5.5 synchronized immutable configuration consumer |
| 3 | `RaiUtils` | `RaiUtils` | 4.5.5 synchronized dependency line |
| 4 | `RaiImage` | `RaiImage` | 4.5.5 synchronized dependency line |
| 5 | `RaiDiagram` | `RaiDiagram` | 4.5.5 synchronized diagram line |
| 6 | `RaidSeeder` | `RaidSeeder` / `raid` | 4.5.5 synchronized diagram artifact manager |
| 7 | `JsonPit` | `JsonPit` | 4.5.5 synchronized persistence line |
| 8 | `ImgSeeder` | `ImgSeeder` / `iorg` | 4.5.5 synchronized image-management line |
| 9 | `PitSeeder` | `PitSeeder` / `pits` | 4.5.5 live-ID preflight and stdin ingestion |

Each child remains its own Git repository, package, solution, and release
workflow. The umbrella workspace supplies local project wiring, coordinated
validation, dependency-order documentation, and sequential release automation.

## Current release line

The prepared coordinated release is `4.5.7`. RAI starts the release chain
manually after reviewing the prepared commits and verification results.

RAIkeep 4.5.8 implements CR060: SSH fleet provisioning and parity sync
wrappers, sandboxed Deno execution requests, and typed Amafu, raid, and jpit
command composition. RaiImage exposes the same fluent SSH path for ImageMagick
workloads.

All four C# CLI tools and the Python `jpit` CLI are coordinated through this
umbrella. The release chain validates the `jsonpit` Python test suite, checks
`pits list` / `jpit list` parity, and publishes the matching PyPI distribution
beside the NuGet packages.

All ten packages participate in the coordinated line so fallback package dependencies remain aligned throughout the release order.

## Documentation

New to `pits`? Follow [First steps with pits](https://github.com/Burkhardt/RAIkeep/blob/main/doc/FirstSteps_pits.md) to create a pit in iCloud Drive and fill it with weather data from a `curl` call.

All change requests and release notes are centralized in [`doc/`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/README.md). Child repositories should not contain independent `CR_*.md` or `RELEASE_NOTES*.md` files.

The [RAIkeep Manifesto](https://github.com/Burkhardt/RAIkeep/blob/main/MANIFESTO.md)
explains why transparent, historical JSON matters for agentic engineering and
defines JsonPit's asynchronous persistence and eventual-durability model.

Current coordinated 4.5.7 release notes:

- [Amafu 4.5.7](https://github.com/Burkhardt/RAIkeep/blob/main/doc/Amafu_RELEASE_NOTES_4.5.7.md)
- [OsLibCore 4.5.7](https://github.com/Burkhardt/RAIkeep/blob/main/doc/OsLib_RELEASE_NOTES_4.5.7.md)
- [RaiUtils 4.5.7](https://github.com/Burkhardt/RAIkeep/blob/main/doc/RaiUtils_RELEASE_NOTES_4.5.7.md)
- [RaiImage 4.5.7](https://github.com/Burkhardt/RAIkeep/blob/main/doc/RaiImage_RELEASE_NOTES_4.5.7.md)
- [RaiDiagram 4.5.7](https://github.com/Burkhardt/RAIkeep/blob/main/doc/RaiDiagram_RELEASE_NOTES_4.5.7.md)
- [RaidSeeder 4.5.7](https://github.com/Burkhardt/RAIkeep/blob/main/doc/RaidSeeder_RELEASE_NOTES_4.5.7.md)
- [JsonPit 4.5.7](https://github.com/Burkhardt/RAIkeep/blob/main/doc/JsonPit_RELEASE_NOTES_4.5.7.md)
- [ImgSeeder 4.5.7](https://github.com/Burkhardt/RAIkeep/blob/main/doc/ImgSeeder_RELEASE_NOTES_4.5.7.md)
- [PitSeeder 4.5.7](https://github.com/Burkhardt/RAIkeep/blob/main/doc/PitSeeder_RELEASE_NOTES_4.5.7.md)
- [RAIkeep 4.5.8](https://github.com/Burkhardt/RAIkeep/blob/main/doc/RAIkeep_RELEASE_NOTES_4.5.8.md)

The prior coordinated line remains documented in [RAIkeep 4.1.0 release notes](https://github.com/Burkhardt/RAIkeep/blob/main/doc/RAIkeep_RELEASE_NOTES_4.1.0.md).

Flag and coordination behavior is documented in [JsonPit flag files and concurrency](https://github.com/Burkhardt/RAIkeep/blob/main/doc/JsonPit-FlagFiles-And-Concurrency.md). It explains the distinction between per-process activity windows and the stable master-writer lease without replacing the separate open concurrency CR.

## Local validation

From the workspace root:

```bash
dotnet build RAIkeep.slnx
dotnet test Amafu/Amafu.slnx
dotnet test OsLib/OsLib.Tests/OsLib.Tests.csproj
dotnet test RaiUtils/RaiUtils.slnx
dotnet test RaiImage/RaiImage.slnx
dotnet test RaiDiagram/RaiDiagram.slnx
dotnet test RaidSeeder/RaidSeeder.slnx
dotnet test JsonPit/JsonPit.slnx
dotnet test ImgSeeder/ImgSeeder.slnx
dotnet test PitSeeder/PitSeeder.slnx
```

The JsonPit suite includes real cloud/remote scenarios and a separately documented open concurrency regression. Use the validation scope stated in the JsonPit release notes rather than hiding those distinctions behind incidental test-runner parallelism or local configuration substitution.

## Strict release gate

Publication requires explicit approval. Preparing versions, documentation, commits, or packages does not authorize a push, tag, workflow dispatch, or NuGet publication.

After approval, use one release mechanism for the chain. The established local orchestrator is:

```bash
cd /Users/RSB/Projects/GitHub/RAIkeep
scripts/release-chain.sh 4.5.7
```

Before publication begins, all ten child release commits and their exact submodule pointers must already be committed on the umbrella `main`. The script preflights that state, pushes the prepared umbrella `main`, and applies the passed version as its tag first. The umbrella tag publishes no NuGet package; it creates and verifies the synchronized GitHub Release before package tagging begins.

It then processes packages in this exact order:

```text
Amafu → OsLibCore → RaiUtils → RaiImage → RaiDiagram → RaidSeeder → JsonPit → JsonPit.Python → ImgSeeder → PitSeeder
```

The Python `jsonpit` distribution follows C# `JsonPit` and is published to
PyPI before ImgSeeder and PitSeeder. Set `PYPI_TOKEN` in the release
environment; the chain supplies it to Twine without placing it on the command
line.

For every package before the next repository is pushed/tagged:

1. Push the prepared repository `main` only if it is ahead.
2. Push that repository's requested version tag, such as `v4.5.2`, to trigger its publish workflow.
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
