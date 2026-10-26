# Prompt for Rita: Engenho fleet CLI installation in TypeScript

Rita, please implement the RAIkeep fleet CLI installer as a TypeScript capability
in Engenho. Use the current shell implementation as the behavioral reference,
while using your existing Engenho runner, authentication, job, and result
contracts. Inspect those contracts before choosing integration points; this
handover does not prescribe a new HTTP endpoint.

## Reference implementation

- [Fleet orchestration](https://github.com/Burkhardt/RAIkeep/blob/main/scripts/install-clis.sh)
- [Native Windows payload](https://github.com/Burkhardt/RAIkeep/blob/main/scripts/install-clis-windows.ps1)
- [Observer resolution](https://github.com/Burkhardt/RAIkeep/blob/main/scripts/resolve-install-observer.py)
- [Installer guide](https://github.com/Burkhardt/RAIkeep/blob/main/doc/Installing-CLIs.md)
- [Routing regression tests](https://github.com/Burkhardt/RAIkeep/blob/main/scripts/test-installer-routing.py)
- [Python installation regression tests](https://github.com/Burkhardt/RAIkeep/blob/main/scripts/test-python-installer.py)

The latest changes may still be local in the RAIkeep working tree when you receive
this prompt. Confirm their commit before using GitHub as the source reference.

## Configurable destinations

Read `~/.config/RAIkeep.json5` on the machine executing the Engenho installation
job. "Local configuration" means that executing host's file, not automatically
the browser user's or another development machine's configuration. Allow an
operator-configured alternative file path without introducing a fixed fleet.

Use a proper JSON5 parser in TypeScript. Do not depend on Python to read this file
and do not parse JSON5 with regex replacements. Preserve unrelated configuration.

Use the existing Observer contract:

```json5
Observers: [
  { Name: "ServerNode", SshTarget: "operator@server-node" },
  { Name: "WorkstationNode", SshTarget: "operator@workstation-node" }
]
```

- The default/all destination list comes from `Observers`, in its configured order.
- A selected Observer name resolves to its `SshTarget`; names are case-insensitive.
- An empty/missing fleet, duplicate names, malformed entries, or unknown selected
  Observer names must produce clear diagnostics. Do not guess replacement hosts.
- Select local execution explicitly; a matching hostname alone must not bypass a
  configured SSH login that might use a different account.
- Use the executing account's SSH agent, keys, known hosts, aliases, and SSH config.
  `SshTarget` is a login address/alias, not a password or private-key container.
  Do not disable host-key checking or log credentials.

## Independent execution environments

A physical Windows host and its WSL distribution are separate installation
environments. One Observer login is sufficient; each requested environment is a
separate execution target:

- Default/SSH: use the environment exposed by that SSH endpoint.
- Windows: run a native PowerShell payload, including through WSL interoperability
  when the endpoint is Linux/WSL on Windows.
- WSL: use an already operational WSL environment. From native Windows, invoke the
  installed distribution through `wsl.exe --exec`. Fail clearly if unavailable.

Do not install WSL, create a distribution, change its default user, reboot a host,
open cloud apps, or silently substitute another environment. Do not assume that
finding `wsl.exe` proves a usable WSL distribution exists. Preserve the distinction
between Windows profile paths and Linux home paths/configuration.

On current fleet checks, Themba exposes Ubuntu/WSL through SSH and also supports
native Windows PowerShell interoperability. Ixhiba exposes native Windows through
SSH, but its WSL command cannot currently enumerate or launch distributions.
Keep these observations out of hardcoded routing rules.

## Package selection and Python optionality

Install these .NET global tools at the exact requested synchronized version:
`Amafu`, `RaidSeeder`, `ImgSeeder`, `PitSeeder`, `RaiGuard`.
They provide `amafu`, `raid`, `iorg`, `pits`, and `rail` respectively.

Python tools are optional. Provide `skipPython` in the typed request and
`--skip-python` in a CLI adapter:

- With `skipPython=true`, install/check only the .NET tools. Do not require,
  invoke, install, update, remove, or verify Python, `jpit`, or `jsonpit` on the
  destination. Leave existing Python installations untouched.
- Otherwise require usable Python 3.12+ on the destination. Store placeholder
  aliases alone are insufficient. Missing prerequisites are reported, not
  automatically installed.
- Install the distribution `jsonpit==<version>` into one isolated environment
  owning both `jpit` and `jsonpit`. Avoid competing environments installed from
  both distribution names. Do not bypass PEP 668 or change system Python.
- Use pipx/private venv/uv as appropriate on Unix; the current Windows reference
  uses a private venv under `%LOCALAPPDATA%\RAIkeep\jsonpit-venv`.

The TypeScript controller itself must not require Python, including for JSON5,
base64 encoding, SSH orchestration, or .NET-only installations.

Require an explicit released version, or read the approved local RAIkeep release
manifest when available. Do not silently install whatever happens to be latest.
Do not execute the release chain, publish packages, or alter release tags.

## Consistent dry-run behavior

Use `dryRun` / `--dry-run`, consistent with Amafu. The shell's old `--check` name
is only a compatibility alias, not the preferred terminology.

A dry run may read local configuration, probe SSH/OS/runtime availability, and
query tool versions. It must return the resolved target/environment, exact
version, requested/skipped packages, proposed commands/actions, prerequisite
results, and any blocker. It must not install/update tools, create venvs, edit
PATH/startup files/cloud configuration, create symlinks, or repair mounts.

Run checks for the selected packages only. Missing Python must not make a
.NET-only dry run fail. Require dry-run intent explicitly in the Engenho request;
do not invent a separate approval workflow inside the installer.

## Execution and results

Keep this in an authorized trusted Engenho runner. Sandboxed user scripts must
not gain arbitrary filesystem access or an unrestricted SSH execution endpoint.
Remote destinations must resolve through the configured, authorized Observers.

Use argument arrays with Deno's process APIs (or the established Engenho process
adapter), bounded timeouts, cancellation, and separate stdout/stderr capture.
Quote remote shell arguments correctly. Windows OpenSSH can impose cmd.exe's
command-line length limit: stream large payloads over stdin with a short
PowerShell bootstrap instead of embedding the whole script in `-EncodedCommand`.

Reuse proven platform placement and execution capabilities where relevant; do
not port OsLib filesystem/cloud algorithms into a second TypeScript library.
The source installer and payloads define operational behavior, not a requirement
to reproduce their implementation language verbatim.

Make updates repeatable and verify exact resulting CLI versions. Apply persistent
PATH changes for the destination user, never the controller or another account.
Report selected Python tools as skipped rather than failed when omitted.
Return per-target results, paths, exit codes, diagnostics, and a deterministic
fleet summary; one failed target must not be reported as overall success.

Cloud setup remains optional. Preserve existing configuration and provider data.
Native Windows Amafu cloud discovery is not implemented in the current RAIkeep
release: report this limitation instead of generating an empty config or copying
Linux cloud paths to Windows. Never open OneDrive/Google Drive apps or perform
account login as part of installation.

WSL can have distinct mount namespaces for SSH and existing interactive shells.
An SSH-only success does not prove interactive usability. If you expose cloud
health results, identify the tested context and Linux user; metadata checks as
root alone are insufficient. Mount repair is a separate explicitly authorized
operation, not an installer side effect.

## Acceptance and handover

Add automated tests for configuration-driven fleet selection without embedded
hosts, case-insensitive lookup, empty/duplicate/unknown selections, Windows/WSL
routing, unavailable WSL, dry-run immutability, .NET-only success without Python,
isolated Python ownership of both commands, exact versions, payload transport,
timeouts/cancellation, and partial failures. Use neutral fixture names.

Deliver the typed request/result contracts, Engenho integration, a CLI adapter if
appropriate, runnable tests, and short operator examples showing `--dry-run` and
`--skip-python`. Report what was verified with mocks versus live hosts. Coordinate
any real installation separately; do not deploy or provision machines merely to
prove the adapter works.
