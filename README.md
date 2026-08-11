# RAIkeep

`RAIkeep` is the umbrella workspace for four related .NET libraries and two command-line packages:

| Order | Repository | Package / command | `4.0.1` role |
|---:|---|---|---|
| 1 | `OsLib` | `OsLibCore` | Coordinated patch alignment; no API or behavior change |
| 2 | `RaiUtils` | `RaiUtils` | Coordinated patch alignment; no API or behavior change |
| 3 | `RaiImage` | `RaiImage` | Coordinated patch alignment; no API or behavior change |
| 4 | `JsonPit` | `JsonPit` | Coordinated patch alignment; no persistence or concurrency change |
| 5 | `ImgSeeder` | `ImgSeeder` / `iorg` | Adds `organize`/`clean` commands with a 4.x legacy transition |
| 6 | `PitSeeder` | `PitSeeder` / `pits` | Adds `seed`/`export`/`audit` commands with a 4.x legacy transition |

Each child remains its own Git repository, package, solution, and release workflow. The umbrella workspace supplies local project wiring, coordinated validation, dependency-order documentation, and sequential release automation.

## Current release line

The prepared coordinated release is `4.0.1` across all six repositories.

The principal functional changes are:

- `PitSeeder`: command-first `seed`, `export`, and `audit` syntax, contextual help, and early option validation.
- `ImgSeeder`: command-first `organize` and safe short-name `clean` syntax with isolated options.
- Established flat seed/export/image-organizer invocations remain supported throughout `4.x`; the legacy parsers are scheduled for removal in `5.x.x`.
- The recently added `pits` audit flags move directly to the new command syntax and are not retained as legacy aliases.
- OsLibCore, RaiUtils, RaiImage, and JsonPit carry synchronized `4.0.1` metadata without functional changes from `4.0.0`.

RaiUtils, RaiImage, and ImgSeeder participate in the same major line so fallback package dependencies remain aligned throughout the release order.

## Documentation

All change requests and release notes are centralized in [`doc/`](doc/README.md). Child repositories should not contain independent `CR_*.md` or `RELEASE_NOTES*.md` files.

Current release notes:

- [OsLibCore 4.0.1](doc/OsLib_RELEASE_NOTES_4.0.1.md)
- [RaiUtils 4.0.1](doc/RaiUtils_RELEASE_NOTES_4.0.1.md)
- [RaiImage 4.0.1](doc/RaiImage_RELEASE_NOTES_4.0.1.md)
- [JsonPit 4.0.1](doc/JsonPit_RELEASE_NOTES_4.0.1.md)
- [ImgSeeder 4.0.1](doc/ImgSeeder_RELEASE_NOTES_4.0.1.md)
- [PitSeeder 4.0.1](doc/PitSeeder_RELEASE_NOTES_4.0.1.md)

Flag and coordination behavior is documented in [JsonPit flag files and concurrency](doc/JsonPit-FlagFiles-And-Concurrency.md). It explains the distinction between per-process activity windows and the stable master-writer lease without replacing the separate open concurrency CR.

## Local validation

From the workspace root:

```bash
dotnet build RAIkeep.slnx
dotnet test OsLib/OsLib.Tests/OsLib.Tests.csproj
dotnet test RaiUtils/RaiUtils.slnx
dotnet test RaiImage/RaiImage.slnx
dotnet test ImgSeeder/ImgSeeder.slnx
dotnet test PitSeeder/PitSeeder.slnx
```

The JsonPit suite includes real cloud/remote scenarios and a separately documented open concurrency regression. Use the validation scope stated in the JsonPit release notes rather than hiding those distinctions behind incidental test-runner parallelism or local configuration substitution.

## Strict release gate

Publication requires explicit approval. Preparing versions, documentation, commits, or packages does not authorize a push, tag, workflow dispatch, or NuGet publication.

After approval, use one release mechanism for the chain. The established local orchestrator is:

```bash
cd /Users/RSB/Projects/GitHub/RAIkeep
scripts/release-chain.sh 4.0.1
```

Before publication begins, all six child release commits and their exact submodule pointers must already be committed on the umbrella `main`. The script preflights that state, pushes the prepared umbrella `main`, and applies the passed version as its tag first. The umbrella tag does not publish a package; its workflow is manual-only.

It then processes packages in this exact order:

```text
OsLibCore → RaiUtils → RaiImage → JsonPit → ImgSeeder → PitSeeder
```

For every package before the next repository is pushed/tagged:

1. Push the prepared repository `main` only if it is ahead.
2. Push that repository's `v4.0.1` tag to trigger its publish workflow.
3. Wait for the matching GitHub workflow to finish successfully.
4. Verify the exact `.nupkg` is visible through the NuGet flat-container URL with HTTP `200`.
5. Enforce the full `380`-second hold.
6. Only then continue to the next repository.

The local script and the umbrella sequential workflow both enforce `380` seconds. This longer window reflects observed RaiUtils indexing latency. Do not run both release mechanisms for the same version. The local script refuses to move an existing conflicting version tag and verifies at the end that the umbrella still records the exact released child commits.

Detailed operational guidance is in [RunReleaseChain.md](RunReleaseChain.md).

## Working conventions

- Preserve the real machine configuration file as the source of truth; do not substitute environment variables or rewrite configuration for test isolation.
- Keep the shared configured cloud-root contract aligned on `Dropbox`, `OneDrive`, `GoogleDrive`, and `ICloudDrive`.
- Use OsLib path/file abstractions in JsonPit and the CLIs instead of introducing direct filesystem operations where an OsLib API applies.
- Do not use temporary-file rename replacement for canonical pits or cloud-backed coordination flags.
- Keep one in-memory `Pit` instance per distinct pit path in a long-running process and share it through the application container/singleton mechanism.
