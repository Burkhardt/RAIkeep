param(
	[Parameter(Mandatory = $true)][ValidatePattern('^\d+\.\d+\.\d+$')][string]$Version,
	[Alias('CheckOnly')][switch]$DryRun,
	[switch]$SkipPython,
	[switch]$NoCloudSetup
)

$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'

function Find-RaiKeepPython {
	foreach ($name in @('py', 'python', 'python3')) {
		$command = Get-Command $name -ErrorAction SilentlyContinue
		# Store execution aliases are not Python installations.
		if (!$command -or $command.Source -match '\\Microsoft\\WindowsApps\\') { continue }
		$prefix = @()
		if ($name -eq 'py') { $prefix = @('-3') }
		try {
			$null = & $command.Source @prefix -c 'import sys; sys.exit(0 if sys.version_info >= (3,12) else 1)' 2>$null
			if ($LASTEXITCODE -eq 0) {
				return @{ Executable = $command.Source; Prefix = $prefix }
			}
		} catch { continue }
	}
	return $null
}

function Invoke-RaiKeepChecked {
	param([string]$Executable, [string[]]$Arguments)
	& $Executable @Arguments
	if ($LASTEXITCODE -ne 0) {
		throw "$Executable failed (exit $LASTEXITCODE). Installation stopped."
	}
}

$dotnet = Get-Command dotnet -ErrorAction SilentlyContinue
$sdk = $null
if ($dotnet) {
	try {
		$sdkOutput = & $dotnet.Source --version 2>$null
		if ($LASTEXITCODE -eq 0 -and "$sdkOutput" -match '^\d+\.') { $sdk = "$sdkOutput".Trim() }
	} catch { $sdk = $null }
}
$python = $null
if (!$SkipPython) { $python = Find-RaiKeepPython }
$ready = $null -ne $sdk -and [int]($sdk.Split('.')[0]) -ge 10 -and ($SkipPython -or $null -ne $python)
if ($DryRun) {
	[pscustomobject]@{
		Environment = 'Windows'; User = [Environment]::UserName
		DotnetSdk = $sdk; Python = $(if ($python) { $python.Executable } else { $null })
		PythonRequested = !$SkipPython; Version = $Version
		PythonPackage = $(if (!$SkipPython) { "jsonpit==$Version" } else { $null })
		Packages = @('Amafu', 'RaidSeeder', 'ImgSeeder', 'PitSeeder', 'RaiGuard')
		Ready = $ready
	} | ConvertTo-Json
	if (!$ready) { exit 2 }
	exit 0
}
if (!$ready) {
	throw 'Native Windows installation requires the .NET 10 SDK, and Python 3.12+ unless -SkipPython is selected. Install the missing prerequisites or skip the Python tools, then rerun. No tools were changed.'
}

foreach ($package in @('Amafu', 'RaidSeeder', 'ImgSeeder', 'PitSeeder', 'RaiGuard')) {
	Write-Output "Installing $package $Version on Windows..."
	& $dotnet.Source tool update --global $package --version $Version --no-cache
	if ($LASTEXITCODE -ne 0) {
		Invoke-RaiKeepChecked $dotnet.Source @('tool', 'install', '--global', $package, '--version', $Version, '--no-cache')
	}
}

# A private virtual environment avoids modifying system Python and owns both names.
$venv = Join-Path $env:LOCALAPPDATA 'RAIkeep\jsonpit-venv'
if (!$SkipPython) {
	Invoke-RaiKeepChecked $python.Executable ($python.Prefix + @('-m', 'venv', $venv))
	$venvPython = Join-Path $venv 'Scripts\python.exe'
	Invoke-RaiKeepChecked $venvPython @('-m', 'pip', 'install', '--upgrade', '--no-cache-dir', "jsonpit==$Version")
}

$dotnetTools = Join-Path $env:USERPROFILE '.dotnet\tools'
$pythonTools = Join-Path $venv 'Scripts'
$existingPath = [Environment]::GetEnvironmentVariable('Path', 'User')
$managedPaths = @($dotnetTools)
if (!$SkipPython) { $managedPaths += $pythonTools }
$remainingPaths = @($existingPath -split ';' | Where-Object { $_ -and $_ -notin $managedPaths })
$userPath = (@($managedPaths) + @($remainingPaths)) -join ';'
if ($userPath -ne $existingPath) { [Environment]::SetEnvironmentVariable('Path', $userPath, 'User') }
$env:PATH = ($managedPaths -join ';') + ';' + $env:PATH

if ($NoCloudSetup) {
	Write-Output 'Cloud setup skipped for this tools-only installation.'
} else {
	# Native Windows discovery is not implemented in this Amafu release. Do not
	# overwrite a Windows profile with an empty config or copy Linux-only paths.
	Write-Output 'Native Windows cloud configuration is separate from WSL. Existing configuration is preserved; automatic cloud detection is currently supported on macOS and Linux/WSL.'
}

$names = @('amafu', 'raid', 'iorg', 'pits', 'rail')
if (!$SkipPython) { $names += @('jpit', 'jsonpit') }
foreach ($name in $names) {
	$directory = $dotnetTools
	if ($name -in @('jpit', 'jsonpit')) { $directory = $pythonTools }
	$executable = Join-Path $directory ($name + '.exe')
	$actual = (& $executable --version | Select-Object -First 1)
	if ($LASTEXITCODE -ne 0 -or "$actual".Trim() -ne "$name v$Version") {
		throw "$name reports '$actual'; expected '$name v$Version'."
	}
	Write-Output $actual
}
Write-Output 'Installation complete. Open a new Windows terminal to pick up the user PATH.'
