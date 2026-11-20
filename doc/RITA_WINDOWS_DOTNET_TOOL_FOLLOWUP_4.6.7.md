# Rita: Windows .NET tool follow-up — RAIkeep 4.6.7

> Historical brief. The pilot is complete. The [November 19 decision](DECISION_WINDOWS_DISTRIBUTION_4.6.7.md)
> supersedes the proposed next steps below. Do not rerun tests or update global
> installations on the authority of this archived brief.

## Target: Themba-win, not Themba

**Run all tests in the native Windows 11 environment reached through `ssh Themba-win`.**

- **Themba-win** is the Windows 11 environment whose Smart App Control behavior we are investigating.
- **Themba** is the WSL environment on the same physical machine. Do not use that SSH target or execute these tests inside WSL.

Use Windows PowerShell, Windows paths, the Windows .NET SDK, and Windows executables. Confirm the OS and executable paths before starting. A successful Linux/WSL run does not answer this investigation.

## Objective and current evidence

Determine whether the existing NuGet / `dotnet tool` distribution route works for both representative RAIkeep CLIs on Windows 11 with Smart App Control enforced.

Results already reported on Themba-win:

| Tool and installation | Version | Result |
| --- | --- | --- |
| Isolated PitSeeder .NET tool | 4.6.7 | Help/version and actual seed/export passed |
| Standalone pits ZIP | 4.6.7 | EXE blocked at launch |
| Standalone raid ZIP | 4.6.7 | Help/version, import, and three validations passed; visual SVG inspection pending |
| Existing global PitSeeder .NET tool | 4.6.6 | OsLib.dll blocked |
| Existing global RaidSeeder .NET tool | 4.6.6 | Launcher blocked |

Different artifacts and installation contexts received different decisions. We have not established the precise reason. Do not describe this as proof of a package-manager exemption or a guarantee for future releases.

## Authorized next step

Install **RaidSeeder 4.6.7 into a fresh isolated tool directory** and run startup plus actual diagram operations. Preserve existing global tools and PATH.

Do not change Smart App Control, application-control policy, exclusions, permissions, or blocking metadata. Do not use `Unblock-File`, substitute launch mechanisms to bypass a denial, build new binaries, add signing, or start WinGet work.

Use disposable local directories outside cloud storage. No production pits, no fleet provisioning, and no release actions.

## 1. Capture environment and install

Record timestamps/time zone, Windows edition/build/architecture, current Smart App Control state, `dotnet --info`, and the Windows paths returned by `Get-Command dotnet,raid -All`.

Run in Windows PowerShell:

```powershell
$testRoot = Join-Path $env:LOCALAPPDATA (
    "RAIkeepTests\raid-dotnet-4.6.7-" +
    (Get-Date -Format "yyyyMMdd-HHmmss")
)
New-Item -ItemType Directory -Path $testRoot -ErrorAction Stop |
    Out-Null

$toolDir = Join-Path $testRoot "dotnet-tool"

dotnet tool install RaidSeeder `
    --version 4.6.7 `
    --tool-path $toolDir `
    --source https://api.nuget.org/v3/index.json

# Capture installation output and exit code before running another command.
# Stop dependent checks if installation failed.
dotnet tool list --tool-path $toolDir

$raidExe = Join-Path $toolDir "raid.exe"
```

Confirm the installed package version is 4.6.7. Invoke `$raidExe` by absolute path; do not resolve `raid` through PATH for the isolated test.

The explicit `--tool-path` installs into a separate directory without updating the global installation. Reference: https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-tool-install

## 2. Startup checks

```powershell
& $raidExe -h
# Capture stdout, stderr, exit code, launch exception, and timestamp.

& $raidExe --version
# Capture separately; successful output must identify raid v4.6.7.
```

If Windows blocks startup, mark functional testing not run and proceed to diagnostics. A PowerShell launch exception can leave `$LASTEXITCODE` stale; record the exception rather than reporting that stale value as the process result.

## 3. Actual diagram operation

Write a UTF-8 fixture without a byte-order mark:

```powershell
$source = @'
@startuml Orders
object "Order42 : Order" as order {
  Number = 42
}
actor "Customer" as customer
customer --> order : places
@enduml
'@

$pumlPath = Join-Path $testRoot "Orders.puml"
$diagramDir = Join-Path $testRoot "diagrams"
[System.IO.File]::WriteAllText(
    $pumlPath, $source, [System.Text.UTF8Encoding]::new($false)
)

& $raidExe import --puml $pumlPath --out $diagramDir --domain Examples --name Orders --name-ext OD
# Capture output and exit code immediately. Continue only on success.

& $raidExe validate "$diagramDir\Orders_OD.raid"
# Capture output and exit code immediately.
& $raidExe validate "$diagramDir\Orders_OD.puml"
# Capture output and exit code immediately.
& $raidExe validate "$diagramDir\Orders_OD.svg"
# Capture output and exit code immediately.
```

Acceptance:

- Import and all three validation commands exit successfully.
- All three generated files exist and are nonempty.
- The SVG contains the Customer actor, Order42 object, Number slot with value 42, and relationship labeled `places`.
- Inspect the rendered SVG if possible. If only structural/text checks are available through SSH, report visual review as pending and preserve the file for inspection.

This exercises functionality beyond help/version but does not prove that every dependency method or optional code path has executed.

## 4. Diagnostics and evidence

Record the isolated launcher and relevant RAIkeep assemblies' SHA-256 hashes, Authenticode signature status, and presence/absence of `Zone.Identifier`. Include OsLib.dll, RaiUtils.dll, RaiImage.dll, and RaiDiagram.dll where present under the isolated installation.

For any failure, collect the exact command, timestamp, output, exception, and implicated file path. Correlate with accessible events from `Microsoft-Windows-CodeIntegrity/Operational` and relevant AppLocker logs. Include event messages and policy identifiers, not only event numbers.

Distinguish installation/download failures, application errors, missing prerequisites, and application-control denials. If diagnostic access is unavailable, record that limitation without changing permissions or policy.

## 5. Report and stop

Provide:

| Tool | Installation | Version | Help/version | Functional check | Exact blocked file/error |
| --- | --- | --- | --- | --- | --- |
| raid | New isolated .NET tool | 4.6.7 | | | |

Reference the earlier successful isolated pits 4.6.7 result as prior evidence, not as a new test. State the Windows environment, security state, log paths, artifact hashes, and output locations. Keep the test directory and logs for review.

If raid passes, the conclusion is: **both representative CLIs have passed isolated .NET tool tests on Themba-win at version 4.6.7**. The ordinary global installation locations still require verification.

## Subsequent step — global installation checks require approval

Do not update global tools during this isolated pilot. After reporting, request approval to update only PitSeeder and RaidSeeder on Themba-win to 4.6.7 and repeat the functional checks at their normal Windows command paths.

That later step would verify command resolution, package versions, startup, a fresh disposable pit seed/export, and fresh diagram import/validation. Preserve unrelated tools and use new output directories. Do not run fleet-wide provisioning for this test.

**Stop after the isolated test report. No global updates are authorized by this brief.**
