# OsLibCore 4.2.2

Coordinated patch release completing the accepted
`CR008_AIA_to_RAIkeep_OsLib_RaiImage_Boundary_Enhancements.md` boundary.

This release also implements the OsLibCore portion of accepted
`CR014_RAI_to_RAIkeep_Typed_CLI_Command_Wrappers.md` and its accepted
`CR014.1_test-concept.md` testing guidance.

- `RaiFile.ReadAllBytesAsync(...)` wraps operating-system `IOException` and
  `UnauthorizedAccessException` failures in `RaiFileIOException`.
- `RaiFileIOException` retains `IOException` compatibility, exposes the affected
  `FileName`, and preserves the original failure as `InnerException`.
- Cancellation remains `OperationCanceledException` and is not wrapped.
- The validated configured `Os.TempDir`, immutable `Os.Config`, `RaiPath`
  exceptions, and stream-free ingestion contracts remain unchanged.
- Adds public `PitsCommand` and `IorgCommand` wrappers for installed-binary and
  managed-DLL invocation from servers, agents, and package-owned tests.
- Adds typed request/option contracts for preferred 4.x `seed`, `export`,
  `audit`, `organize`, and `clean` command forms.
- Validates mandatory, mutually exclusive, numbered, and path-like parameters
  before process start.
- Adds tokenized `CliCommand.Run(...)` / `RunAsync(...)` overloads backed by
  `ProcessStartInfo.ArgumentList`, plus safe POSIX serialization for explicit
  SSH command boundaries.
- `RaiSystemResult` now exposes the exact original `ArgumentList` and derived
  `Succeeded` state. Timeout kills the process tree and returns `TimedOut`;
  caller cancellation kills the process tree and remains cancellation.
- CR014.1 coverage uses capture executables for edge-case argument forwarding,
  output/error/exit handling, timeout, cancellation, and startup failures;
  package-owned `--version` smoke checks invoke the real managed CLIs.
- Extends `SshSystem` with tokenized SSH options; JsonPit's remote scenarios no
  longer hand-build SSH process invocations.

Released as part of the coordinated RAIkeep v4.2.2 release.

Release verification: 104 OsLib Release tests passed, including 21 focused
CR014/CR014.1 wrapper-contract tests.
