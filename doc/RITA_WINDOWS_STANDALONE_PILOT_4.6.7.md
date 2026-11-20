# Rita: Windows standalone CLI pilot — RAIkeep 4.6.7

> Historical brief. The pilot is complete. The [November 19 decision](DECISION_WINDOWS_DISTRIBUTION_4.6.7.md)
> supersedes the proposed next steps below. WinGet remediation, signing and
> automatic installation-format switching remain paused.

Test the standalone Windows releases of **pits** and **raid** on **Themba-win**, accessible through `ssh Themba-win`, after the 4.6.7 release chain finishes.

## Objective

Determine whether the published standalone executables work where the existing .NET global-tool installations encountered Windows Application Control blocks. Compare startup and actual functionality. This is the first stage of evaluating WinGet; do not create or publish WinGet manifests yet.

The two tools cover these dependency branches:

- `pits` → JsonPit → OsLib / RaiUtils
- `raid` → RaiDiagram → RaiImage / OsLib / RaiUtils

A successful help command alone is insufficient: dependencies may load only when specific functionality is exercised. Functional success also does not prove exhaustive coverage of every library method.

## Scope and isolation

- Use **4.6.7 for both standalone tools**. Confirm both release assets exist before starting; wait for release completion if necessary.
- Keep existing tool installations and PATH unchanged. Invoke every tested executable by its resolved absolute path.
- Use a new local test directory outside OneDrive, Dropbox, and other cloud-synchronized folders. Never use production pits or AfricaStage data.
- Preserve Windows security settings and file blocking metadata. Do not disable Smart App Control, add exclusions, or run `Unblock-File`.
- Do not launch a release, provision the fleet, or change repository files as part of this pilot.
- Preserve logs and test outputs for review. Stop after reporting results.

## 1. Record the baseline

Record:

- Windows edition, build, and architecture; confirm x64 compatibility.
- Smart App Control state and any relevant managed application-control policy visible to the current account. Report unavailable information rather than changing permissions or policy.
- Existing `pits` and `raid` command resolutions, executable paths, and installed package versions. `Get-Command pits,raid -All` and `dotnet tool list --global` can help.
- Test start time and time zone.

Run `-h` and `--version` against each existing installation by absolute path. Capture stdout, stderr, exit codes, and launch exceptions. Record version differences from 4.6.7; an older baseline is not a controlled same-version comparison.

## 2. Download and extract standalone releases

Release pages:

- https://github.com/Burkhardt/PitSeeder/releases/tag/v4.6.7
- https://github.com/Burkhardt/RaidSeeder/releases/tag/v4.6.7

Windows x64 ZIPs:

- https://github.com/Burkhardt/PitSeeder/releases/download/v4.6.7/pits-v4.6.7-win-x64.zip
- https://github.com/Burkhardt/RaidSeeder/releases/download/v4.6.7/raid-v4.6.7-win-x64.zip

Create a fresh run directory, for example:

```powershell
$testRoot = Join-Path $env:LOCALAPPDATA ("RAIkeepTests\standalone-4.6.7-" + (Get-Date -Format 'yyyyMMdd-HHmmss'))
New-Item -ItemType Directory -Path $testRoot -ErrorAction Stop | Out-Null
```

Download both ZIPs and extract each to a separate directory beneath this root. Record the download/extraction method and SHA-256 hashes (`Get-FileHash`). Compare hashes against GitHub release asset digests when available; a hash match confirms artifact identity, not publisher trust.

Record any `Zone.Identifier` streams on the downloaded ZIPs and extracted executables. Absence is a result to record, not an instruction to add or remove metadata.

The release workflows package a `win-x64` directory inside each ZIP. Locate the extracted `pits.exe` and `raid.exe`, confirm they are from the new extraction directories, and assign their absolute paths to `$pitsExe` and `$raidExe`. Do not resolve these variables through PATH.

Run both executables with `-h` and `--version`. Capture output and failures and verify that successful version output reports 4.6.7.

## 3. Exercise JsonPit through pits

Create an isolated pit root and a UTF-8 seed file:

```powershell
New-Item -ItemType Directory -Path "$testRoot\pits" -ErrorAction Stop | Out-Null
[System.IO.File]::WriteAllText(
    "$testRoot\Person.json",
    '[{"Id":"Alice","Kind":"Person","Name":"Windows packaging test"}]',
    [System.Text.UTF8Encoding]::new($false)
)

& $pitsExe seed Person --source "$testRoot\Person.json" -r "$testRoot\pits" -n
# Capture the exit code and output immediately before continuing.

& $pitsExe export Person -r "$testRoot\pits" --json -n
# Capture the exit code and output immediately.
```

Acceptance:

- Both commands exit successfully.
- `$testRoot\pits\Person\Person.pit` exists and is nonempty.
- The export from the separate process is valid JSON and contains `Id = Alice`, `Kind = Person`, and `Name = Windows packaging test`.

If seeding fails, retain the failure as the primary result rather than interpreting a subsequent missing-pit error as a separate library failure.

## 4. Exercise diagram generation through raid

Write this content to `$testRoot\Orders.puml` as UTF-8:

```plantuml
@startuml Orders
object "Order42 : Order" as order {
  Number = 42
}
actor "Customer" as customer
customer --> order : places
@enduml
```

Run:

```powershell
& $raidExe import --puml "$testRoot\Orders.puml" --out "$testRoot\diagrams" --domain Examples --name Orders --name-ext OD
# Capture the exit code and output immediately. Continue only on success.

& $raidExe validate "$testRoot\diagrams\Orders_OD.raid"
& $raidExe validate "$testRoot\diagrams\Orders_OD.puml"
& $raidExe validate "$testRoot\diagrams\Orders_OD.svg"
# Capture each command's exit code and output separately.
```

Acceptance:

- Import and all three validation commands exit successfully.
- All three generated files exist and are nonempty.
- Inspect the SVG for the Customer actor, Order42 object with Number slot, and the connecting relationship labeled `places`.

If rendering cannot be inspected through the remote session, retain the SVG for local visual review and mark that check pending. Distinguish fixture/parser errors from Windows policy blocks.

## 5. Compare with installed .NET tools

If the existing tools pass startup checks, repeat the same functional fixtures using their explicit executable paths and fresh, separate output directories. Do not share a pit root between the two installations.

If an existing executable cannot launch, record the block and do not attempt dependent functional commands. Do not upgrade or reinstall the existing tools just to force a version match; report any comparison limitation.

## 6. Diagnose failures

For execution or assembly-load failures, capture:

- Exact command, time, executable path, stdout/stderr, and exit code or PowerShell launch exception. A launch failure may leave a stale `$LASTEXITCODE`; record the exception explicitly.
- Exact blocked EXE or DLL path, including any extraction location reported by Windows.
- Corresponding events from `Microsoft-Windows-CodeIntegrity/Operational` and relevant AppLocker logs around the test time, where accessible.
- Signature status (`Get-AuthenticodeSignature`) and SHA-256 hash of the implicated file when accessible.
- Any distinction between an application exception, missing prerequisite, and an explicit application-control denial.

Do not assume every failure is caused by OsLib. Record evidence before drawing a conclusion. If logs require additional access, report the limitation without changing security policy.

## 7. Report and stop

Provide a table with one row per tool and installation method:

| Tool | Installation | Version | Help/version | Functional operation | Blocked file or error |
| --- | --- | --- | --- | --- | --- |
| pits | Existing .NET tool | | | | |
| pits | Standalone ZIP | 4.6.7 | | | |
| raid | Existing .NET tool | | | | |
| raid | Standalone ZIP | 4.6.7 | | | |

Include artifact hashes, security state, download method, metadata observations, log locations, and generated output locations. State whether a difference could be explained by version or packaging rather than installation route.

Recommend whether a local WinGet installation trial is worthwhile based on these results. Standalone ZIP success does not establish that WinGet bypasses application control; a later comparison would use identical released bytes.

This pilot establishes behavior on Themba-win only. Do not generalize it to every Windows build, enterprise policy, or CPU architecture.

**Stop after the report. No WinGet submission, security-policy changes, fleet provisioning, or release actions are part of this instruction.**
