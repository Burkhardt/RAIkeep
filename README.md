# RAIkeep

`RAIkeep` is the umbrella workspace for five related .NET libraries and two command-line packages:

| Order | Repository | Package / command | Current or upcoming role |
|---:|---|---|---|
| 1 | `OsLib` | `OsLibCore` | 4.1: validated configured TempDir, path exceptions, async chunk ingestion |
| 2 | `RaiUtils` | `RaiUtils` | 4.1: shared RaiException and ToolNotFoundException |
| 3 | `RaiImage` | `RaiImage` | 4.1: image/path/tool exception boundary and chunk ingestion |
| 4 | `RaiDiagram` | `RaiDiagram` | 4.2: agent-readable `.raid` manifests, reconciliation, and PlantUML rendering |
| 5 | `JsonPit` | `JsonPit` | 4.1: abandoned watcher ownership/finalizer regression fix |
| 6 | `ImgSeeder` | `ImgSeeder` / `iorg` | 4.1 dependency alignment; established CLI behavior retained |
| 7 | `PitSeeder` | `PitSeeder` / `pits` | 4.1 dependency alignment; established CLI behavior retained |

Each child remains its own Git repository, package, solution, and release
workflow. The umbrella workspace supplies local project wiring, coordinated
validation, dependency-order documentation, and sequential release automation.

## Current release line

The completed coordinated release is `4.1.0` across all six established child repositories. RaiDiagram joins the coordinated chain with `4.2.0`, after which all seven repositories share each release version.

RAIkeep 4.1.0 implements the approved CR008 boundary enhancements and the
JsonPit finalizer-ownership regression fix. Approved CR009 defines RaiDiagram as
the subsequent 4.2.0 package and repository; it is not part of the 4.1.0 release
chain. Source preparation alone does not publish or tag either release.

The principal functional changes are:

- `PitSeeder`: command-first `seed`, `export`, and `audit` syntax, contextual help, and early option validation.
- `ImgSeeder`: command-first `organize` and safe short-name `clean` syntax with isolated options.
- Established flat seed/export/image-organizer invocations remain supported throughout `4.x`; the legacy parsers are scheduled for removal in `5.x.x`.
- The recently added `pits` audit flags move directly to the new command syntax and are not retained as legacy aliases.
- OsLibCore, RaiUtils, RaiImage, and JsonPit carry the coordinated `4.1.0` boundary and lifecycle changes; ImgSeeder and PitSeeder align their fallback dependencies without changing CLI behavior.

RaiUtils, RaiImage, and ImgSeeder participate in the same major line so fallback package dependencies remain aligned throughout the release order.

## Documentation

All change requests and release notes are centralized in [`doc/`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/README.md). Child repositories should not contain independent `CR_*.md` or `RELEASE_NOTES*.md` files.

Current coordinated release notes:

- [OsLibCore 4.1.0](https://github.com/Burkhardt/RAIkeep/blob/main/doc/OsLib_RELEASE_NOTES_4.1.0.md)
- [RaiUtils 4.1.0](https://github.com/Burkhardt/RAIkeep/blob/main/doc/RaiUtils_RELEASE_NOTES_4.1.0.md)
- [RaiImage 4.1.0](https://github.com/Burkhardt/RAIkeep/blob/main/doc/RaiImage_RELEASE_NOTES_4.1.0.md)
- [JsonPit 4.1.0](https://github.com/Burkhardt/RAIkeep/blob/main/doc/JsonPit_RELEASE_NOTES_4.1.0.md)
- [ImgSeeder 4.1.0](https://github.com/Burkhardt/RAIkeep/blob/main/doc/ImgSeeder_RELEASE_NOTES_4.1.0.md)
- [PitSeeder 4.1.0](https://github.com/Burkhardt/RAIkeep/blob/main/doc/PitSeeder_RELEASE_NOTES_4.1.0.md)
- [RAIkeep 4.1.0](https://github.com/Burkhardt/RAIkeep/blob/main/doc/RAIkeep_RELEASE_NOTES_4.1.0.md)
- [RaiDiagram 4.2.0 candidate](https://github.com/Burkhardt/RAIkeep/blob/main/doc/RaiDiagram_RELEASE_NOTES_4.2.0.md)

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
scripts/release-chain.sh 4.2.0
```

Before publication begins, all seven child release commits and their exact submodule pointers must already be committed on the umbrella `main`. The script preflights that state, pushes the prepared umbrella `main`, and applies the passed version as its tag first. The umbrella tag does not publish a package; its workflow is manual-only.

It then processes packages in this exact order:

```text
OsLibCore → RaiUtils → RaiImage → RaiDiagram → JsonPit → ImgSeeder → PitSeeder
```

For every package before the next repository is pushed/tagged:

1. Push the prepared repository `main` only if it is ahead.
2. Push that repository's requested version tag, such as `v4.2.0`, to trigger its publish workflow.
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
