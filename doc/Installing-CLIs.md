# Installing RAIkeep CLIs across the fleet

Engenho now owns fleet provisioning after a coordinated release. The shell and
PowerShell installers below remain reference implementations; do not run them
as part of release preparation or the release chain.

The reference fleet installer runs from a RAIkeep checkout on macOS or Linux/WSL. It installs
`amafu`, `raid`, `iorg`, `pits`, `rail`, and the Python commands `jpit` and `jsonpit`.
Both the default destination list and SSH logins come from `Observers` in the
executing machine's `~/.config/RAIkeep.json5`. There is no embedded fleet list.
The default version comes from `scripts/release-manifest.json`; an explicit
`X.Y.Z` argument can select another published release.

For example, a general-purpose configuration can contain:

```json5
Observers: [
  { Name: "ServerNode", SshTarget: "operator@server-node" },
  { Name: "WorkstationNode", SshTarget: "operator@workstation-node" }
]
```

`all`, or omitting targets, selects these Observers in configuration order. Use
`local` explicitly to install on the controller. An empty Observer list fails
with an explanation rather than contacting a predefined set of machines.

Select a different configuration with `--config <file>` (or `RAIKEEP_CONFIG`).
SSH keys, ports, jump hosts, and host aliases can stay in the executing account's
normal SSH configuration; `SshTarget` identifies the destination login.

```sh
bash scripts/install-clis.sh --help
bash scripts/install-clis.sh all --dry-run
bash scripts/install-clis.sh ServerNode:windows --skip-python --dry-run
bash scripts/install-clis.sh --config /path/to/RAIkeep.json5 all --dry-run
```

`--dry-run` previews the selected tools/version and checks prerequisites without
installing tools, changing PATH, or setting up cloud storage. A missing requested
prerequisite produces a nonzero exit status. `--check` remains an alias; help and
examples use `--dry-run` consistently.

## Windows and WSL are separate installation environments

Keep one Observer per SSH endpoint. Add an environment suffix when needed:

| Target | Execution environment |
| --- | --- |
| `Themba` | Ubuntu/WSL, as exposed by its configured SSH login |
| `Themba:wsl` | The same Ubuntu/WSL environment |
| `Themba:windows` | Native Windows, through PowerShell interoperability |
| `Ixhiba` or `Ixhiba:windows` | Native Windows, as exposed by its SSH login |
| `Ixhiba:wsl` | An existing default WSL distribution, if one is operational |

The fleet is determined by your configuration. A default/all run follows
the environment exposed by each SSH endpoint; it does not also install Windows
tools on hosts whose SSH endpoint is WSL. Select both targets explicitly to
install in both environments. Windows binaries cannot serve as Linux binaries,
and their Python environments and configuration files are separate.

After the selected version has been published and prerequisites are ready:

```sh
bash scripts/install-clis.sh Themba Themba:windows Ixhiba
```

Use `--no-cloud-setup` for a tools-only installation. The script never installs
WSL, creates a distribution, or opens a cloud-client application. If a WSL target
is unavailable, that target fails rather than falling back to another environment.

## Native Windows prerequisites

Install the .NET 10 SDK and Python 3.12 or newer on Windows before installing the
complete CLI suite, or select `--skip-python` to install the five .NET tools only.
Python inside WSL does not satisfy the Windows prerequisite;
the Microsoft Store placeholder commands alone do not provide Python either.

`--skip-python` leaves any existing `jpit`/`jsonpit` installation unchanged and
does not require, invoke, install, update, or verify Python on the destination.
The Bash controller itself still uses local Python for JSON5 parsing and command
encoding. This controller dependency is separate from destination prerequisites;
the planned Engenho TypeScript port can perform both operations without Python.

The Windows installer uses .NET global tools and one private Python virtual
environment under `%LOCALAPPDATA%\RAIkeep\jsonpit-venv`. It adds their directories
to the user's PATH. Open a new Windows terminal after installation.

From PowerShell in a RAIkeep checkout, the native installer can also run directly:

```powershell
$version = (Get-Content .\scripts\release-manifest.json -Raw | ConvertFrom-Json).current_version
.\scripts\install-clis-windows.ps1 -Version $version -DryRun
.\scripts\install-clis-windows.ps1 -Version $version -DryRun -SkipPython
.\scripts\install-clis-windows.ps1 -Version $version
```

Amafu currently detects cloud roots on macOS and Linux/WSL. Native Windows cloud
configuration must use Windows paths; the installer preserves any existing file
and does not create an empty configuration or copy Linux paths into it. WSL uses
its own Linux configuration and `~/.CloudStorage/` shortcuts.

## Verified prerequisites on 2026-10-26

- Themba: Ubuntu/WSL has .NET SDK 10.0.401 and Python 3.12.3.
- Themba native Windows: .NET SDK 10.0.401 is present; usable Python is missing.
- Ixhiba native Windows: Windows Server 2022, .NET SDK 10.0.103; Python is missing.
  `wsl.exe` exists but fails to enumerate distributions, so WSL operation is not
  established. Merely finding `wsl.exe` is insufficient.

These checks did not install or update any tools on those machines. The .NET-only
dry run with `--skip-python` can proceed without native Windows Python. Full
native Windows installation still needs verification; requesting Python tools
also requires their Python prerequisites.

## Installer regression tests

```sh
python3 scripts/test-installer-routing.py
python3 scripts/test-python-installer.py
```

These use isolated fixtures and fake package/SSH commands. They verify login
resolution, separate environment routing, prerequisite failure reporting, and
isolated Python installation behavior without provisioning real machines.
