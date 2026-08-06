# RAIkeep

`RAIkeep` is the umbrella workspace for four related .NET libraries and two command-line packages:

| Order | Repository | Package / command | `3.13.2` role |
|---:|---|---|---|
| 1 | `OsLib` | `OsLibCore` | Adds in-place coordination-file writes and read-only physical last-write time |
| 2 | `RaiUtils` | `RaiUtils` | Aligns with OsLibCore `3.13.2` |
| 3 | `RaiImage` | `RaiImage` | Aligns dependencies and carries forward the current image/PlantUML APIs |
| 4 | `JsonPit` | `JsonPit` | Adds per-PID activity flags and ownership-verified process-window release |
| 5 | `ImgSeeder` | `ImgSeeder` / `iorg` | Aligns the image CLI with the `3.13.2` library chain |
| 6 | `PitSeeder` | `PitSeeder` / `pits` | Releases finite CLI activity windows by default and adds `--retain-window` |

Each child remains its own Git repository, package, solution, and release workflow. The umbrella workspace supplies local project wiring, coordinated validation, dependency-order documentation, and sequential release automation.

## Current release line

The prepared coordinated release is `3.13.2` across all six repositories.

The principal functional changes are:

- `OsLibCore`: `TextFile.SaveInPlace()` updates small cloud-backed coordination files without a preceding delete or rename.
- `OsLibCore`: `RaiFile.LastWriteTimeUtc` exposes physical modification time without direct `System.IO.FileInfo` use in consumers.
- `JsonPit`: process activity flags use `{Machine}-{Subscriber}-{PID}.flag` and can be released only by their owning process.
- `JsonPit`: `Master.flag` remains a separate stable participant lease and is not released by process-window cleanup.
- `PitSeeder`: finite commands release their process activity windows after completion or exception; Ctrl+C and process exit provide best-effort cleanup.
- `PitSeeder`: `--retain-window` explicitly preserves timeout-based process activity.
- The original OneDrive-sensitive shared-filename and delete/recreate process-flag pattern is no longer used.

RaiUtils, RaiImage, and ImgSeeder participate in the same patch line so fallback package dependencies remain aligned throughout the release order.

## Documentation

All change requests and release notes are centralized in [`doc/`](doc/README.md). Child repositories should not contain independent `CR_*.md` or `RELEASE_NOTES*.md` files.

Current release notes:

- [OsLibCore 3.13.2](doc/OsLib_RELEASE_NOTES_3.13.2.md)
- [RaiUtils 3.13.2](doc/RaiUtils_RELEASE_NOTES_3.13.2.md)
- [RaiImage 3.13.2](doc/RaiImage_RELEASE_NOTES_3.13.2.md)
- [JsonPit 3.13.2](doc/JsonPit_RELEASE_NOTES_3.13.2.md)
- [ImgSeeder 3.13.2](doc/ImgSeeder_RELEASE_NOTES_3.13.2.md)
- [PitSeeder 3.13.2](doc/PitSeeder_RELEASE_NOTES_3.13.2.md)

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
scripts/release-chain.sh 3.13.2
```

Before publication begins, all six child release commits and their exact submodule pointers must already be committed on the umbrella `main`. The script preflights that state, pushes the prepared umbrella `main`, and applies the passed version as its tag first. The umbrella tag does not publish a package; its workflow is manual-only.

It then processes packages in this exact order:

```text
OsLibCore → RaiUtils → RaiImage → JsonPit → ImgSeeder → PitSeeder
```

For every package before the next repository is pushed/tagged:

1. Push the prepared repository `main` only if it is ahead.
2. Push that repository's `v3.13.2` tag to trigger its publish workflow.
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
