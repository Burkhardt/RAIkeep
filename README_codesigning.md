# Code signing policy

RAIkeep is preparing an application to SignPath Foundation for free Windows code
signing. Activation depends on Foundation acceptance and integration with the
component build workflows. The 4.6.6 documentation release does not activate
signing; earlier releases also predate this integration. A release's notes will
identify its signed Windows artifacts when signing becomes available.

Upon acceptance and activation, the attribution for eligible signed artifacts
will be “Free code signing provided by [SignPath.io](https://signpath.io/),
certificate by [SignPath Foundation](https://signpath.org/).”

## Scope and release approval

RAIkeep is an umbrella repository that brings together separately maintained
component Git repositories as submodules. The active suite has 13 component
repositories, publishing 11 NuGet packages and three PyPI distributions under
the Burkhardt account. RaiGuard publishes two NuGet packages, which is why the
repository and package counts differ. Its packages declare Apache-2.0 licensing.

This application requests signing coverage for all RAIkeep-owned Windows
executables and DLLs across the entire active suite, not just OsLibCore, which
is the representative download link in the form. The tables below enumerate
the component repositories, distributions and proposed Windows signing targets.
The frozen legacy Python implementation is listed for migration context only.

The initial Windows signing targets are the project's .NET libraries, analyzer
assemblies, and published CLI executables. Inqaba, Umgodi JSON, and Vikela are
included in the suite inventory as Python distributions. Any Windows executable
packaging for them will need an agreed signing configuration.

[Field-by-field application instructions](https://github.com/Burkhardt/RAIkeep/blob/main/doc/SIGNPATH_APPLICATION.md)
include the text to paste into the form; there is no attachment requirement.

The proposed committer, reviewer, and signing approver is Dr. Rainer Burkhardt.
Additional maintainers and role changes will be recorded here before they receive
signing access. [Maintainer profile](https://github.com/Burkhardt)

Following acceptance, component GitHub Actions builds will submit artifacts for
signing, with human approval of each release. Signing participants must use MFA
for GitHub and SignPath. Signing configuration will bind artifacts to their
source repository, build, product, and version. Upstream dependencies retain their
upstream provenance. [SignPath Foundation conditions](https://signpath.org/terms)

Engenho coordinates releases and provisions published packages. This application
covers the RAIkeep artifacts that it distributes. Engenho's own software and
licensing are managed separately.

## Proposed Windows artifact inventory

This inventory covers the suite in one application. The Foundation must approve
its scope and artifact configurations before signing is enabled.

| Component | RAIkeep-owned Windows artifacts |
| --- | --- |
| OsLibCore | `OsLib.dll` |
| RaiUtils | `RaiUtils.dll` |
| JsonPit | `JsonPit.dll` |
| RaiImage | `RaiImage.dll` |
| RaiDiagram | `RaiDiagram.dll` |
| Amafu | `amafu.dll`, published `amafu.exe` |
| PitSeeder | `pits.dll`, published `pits.exe` |
| ImgSeeder | `ImgSeeder.dll`, published `ImgSeeder.exe`; installed command launcher `iorg.exe` |
| RaidSeeder | `raid.dll`, published `raid.exe` |
| RaiGuard / RaiGuard.Analyzer | `rail.dll`, `RaiGuard.Core.dll`, `RaiGuard.CodeFixes.dll`; installed command launcher `rail.exe` |

Sign each shipped build variant, including the applicable analyzer assemblies and
copies embedded in tool packages. Native AOT or single-file distributions can
have different layouts; their actual build outputs determine the signing list.
Installed tool launchers are a separate integration target, as described below;
their names do not imply that prebuilt signed copies are currently published.
Keep upstream binaries' original signatures and provenance. Python source/wheel
distributions are part of the suite but are not themselves Windows PE binaries.
Generated Python installation launchers are not claimed to be signed by RAIkeep.

### NuGet installation and launchers

Authenticode signing of `.exe` and `.dll` files is separate from signing a NuGet
package. A signed `.nupkg` does not automatically Authenticode-sign its contents.
`dotnet tool install` does not sign files with the RAIkeep publisher certificate.
For the current framework-dependent global tools, the SDK generates a launcher
in the user's tools directory; a signed DLL does not confer its signature on that
new launcher. [Microsoft installation documentation](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-tool-install)

The signing integration must verify both the shipped assemblies and the actual
installed launcher on Windows. Investigate prebuilt shims or .NET 10 RID-specific
tool packaging, and prove that installation preserves the signed executable.
[Microsoft tool packaging documentation](https://learn.microsoft.com/en-us/dotnet/core/tools/rid-specific-tools)
No claim of complete Windows signing coverage will be made before that test.

## Downloads

The package pages below provide current versions and installation instructions.
The umbrella release records the coordinated version and links its component
release notes. [RAIkeep releases](https://github.com/Burkhardt/RAIkeep/releases)

| Component source | Published packages | Purpose |
| --- | --- | --- |
| [Amafu](https://github.com/Burkhardt/Amafu) | [Amafu](https://www.nuget.org/packages/Amafu) | Cloud configuration and `amafu` CLI |
| [OsLib](https://github.com/Burkhardt/OsLib) | [OsLibCore](https://www.nuget.org/packages/OsLibCore) | Filesystem, configuration, and command abstractions |
| [RaiUtils](https://github.com/Burkhardt/RaiUtils) | [RaiUtils](https://www.nuget.org/packages/RaiUtils) | Shared .NET utilities |
| [JsonPit](https://github.com/Burkhardt/JsonPit) | [JsonPit](https://www.nuget.org/packages/JsonPit) | Historical JSON persistence |
| [RaiImage](https://github.com/Burkhardt/RaiImage) | [RaiImage](https://www.nuget.org/packages/RaiImage) | Image naming, paths, and processing |
| [RaiDiagram](https://github.com/Burkhardt/RaiDiagram) | [RaiDiagram](https://www.nuget.org/packages/RaiDiagram) | Diagram models and rendering |
| [PitSeeder](https://github.com/Burkhardt/PitSeeder) | [PitSeeder](https://www.nuget.org/packages/PitSeeder) | `pits` CLI |
| [ImgSeeder](https://github.com/Burkhardt/ImgSeeder) | [ImgSeeder](https://www.nuget.org/packages/ImgSeeder) | `iorg` CLI |
| [RaidSeeder](https://github.com/Burkhardt/RaidSeeder) | [RaidSeeder](https://www.nuget.org/packages/RaidSeeder) | `raid` CLI |
| [RaiGuard](https://github.com/Burkhardt/RaiGuard) | [RaiGuard](https://www.nuget.org/packages/RaiGuard), [RaiGuard.Analyzer](https://www.nuget.org/packages/RaiGuard.Analyzer) | `rail` CLI and Roslyn analyzer/code fixes |
| [Inqaba](https://github.com/Burkhardt/inqaba) | [inqaba](https://pypi.org/project/inqaba/) | Python path, file, and configuration APIs |
| [Umgodi JSON](https://github.com/Burkhardt/umgodi-json) | [umgodi-json](https://pypi.org/project/umgodi-json/) | Python JSON persistence and `umgodi`/`jpit` CLIs |
| [Vikela](https://github.com/Burkhardt/vikela) | [vikela](https://pypi.org/project/vikela/) | Python mutation guardrails |

The frozen Python implementation remains available for existing installations.
Its successor is Umgodi JSON. [Legacy jsonpit distribution](https://pypi.org/project/jsonpit/)

### Installation and removal

Use the installation command on the selected package page. Global .NET tools
can be removed with `dotnet tool uninstall --global <PackageId>`, using `Amafu`,
`PitSeeder`, `ImgSeeder`, `RaidSeeder`, or `RaiGuard` as appropriate. Remove a
library reference with `dotnet remove package <PackageId>` in the consuming
project. Python packages installed with pip can be removed in that environment
with `python -m pip uninstall <distribution>`.

Users select the data and cloud locations used by the tools. Package removal
retains those user data directories and their history. Configuration and cloud
integration commands describe their options in the component documentation.
[Amafu documentation](https://github.com/Burkhardt/Amafu#readme)

## Privacy policy

RAIkeep processes files, JSON histories, images, diagrams, and source code at
locations selected by the user or application. Its policy is to transfer data
only to destinations requested or configured by the user or operator.

Cloud clients synchronize files placed in configured cloud directories according
to the user's cloud account and sharing settings. Pit coordination and recovery
files can contain machine names, process identities, timestamps, diagnostics, and
historical application data. The same sharing settings apply to these files.
Network imports and externally invoked tools use the sources and services chosen
for the requested operation.

Installing packages and fetching releases contacts the selected package registry
or hosting provider. A user who posts logs or data in a public GitHub issue makes
that submitted content available to other readers. Applications embedding these
libraries establish their own privacy policies for the data they collect.

Applicable service policies depend on the services selected by the user.
[GitHub privacy](https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement),
[Microsoft privacy](https://privacy.microsoft.com/en-us/privacystatement),
[Dropbox privacy](https://www.dropbox.com/privacy),
[Google privacy](https://policies.google.com/privacy),
[Apple privacy](https://www.apple.com/legal/privacy/), and
[PyPI privacy](https://policies.python.org/pypi.org/Privacy-Notice/).
