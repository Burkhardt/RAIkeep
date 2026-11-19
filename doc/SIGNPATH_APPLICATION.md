# RAIkeep SignPath application draft

This is the field-by-field guide for [the SignPath application](https://signpath.org/apply).
Copy the table values and the Tagline, Description and Reputation text below.
The umbrella README and signing policy are already published. Verify the new
NuGet/PyPI README notices after the manual release before submitting. The status
language describes application preparation and future signing subject to
acceptance. [Application form](https://signpath.org/apply)

## Form fields

| Field | Value |
| --- | --- |
| Project Name | RAIkeep |
| Repository URL | https://github.com/Burkhardt/RAIkeep |
| Homepage URL | https://github.com/Burkhardt/RAIkeep#readme |
| Download URL | https://www.nuget.org/packages/OsLibCore |
| Privacy Policy URL | Leave blank under the form's optional condition; a proposed privacy statement is included in README_codesigning.md for review |
| Wikipedia URL | Leave blank |
| Category | Developer Tools |
| Maintainer Type | Individual maintainer(s) |
| Build System | GitHub Actions |
| First Name | Rainer |
| Last Name | Burkhardt |
| Email | Use the application email already entered in the form |
| Company Name | Optional; enter your organization if you want it associated with the application |
| Primary Discovery Channel | Choose the available AI assistant category, or the closest matching option |
| Exact Source | OpenAI Codex discussion, with confirmation from Microsoft Learn's Windows code-signing guidance |

## Tagline

Open-source .NET and Python foundations for data, media, and developer automation.

## Description

RAIkeep is an Apache-2.0 umbrella project for .NET and Python libraries and CLIs covering historical JSON storage, cloud files, media and developer guardrails. Its 13 component repositories publish 11 NuGet packages and three PyPI distributions. This application requests signing of all project-owned Windows executables and DLLs across the suite. OsLibCore is the representative download link, not the entire scope.

If the form imposes a smaller character limit, use this shorter description and
include the inventory URL below in Reputation:

RAIkeep is an Apache-2.0 umbrella for 13 .NET/Python component repositories, published as 11 NuGet packages and three PyPI distributions. We request signing for all project-owned Windows EXE/DLL artifacts across the suite.

## Reputation

OsLib and JsonPit have public GitHub histories dating to March 2019. NuGet reports 45,793 cumulative downloads for OsLibCore and 13,860 for JsonPit as of November 18, 2026. Over the preceding 30 days, their repositories received 17 and 21 commits respectively. The suite has public source, tests, GitHub Actions builds, and coordinated releases.

Paste these supporting URLs into the same Reputation field.

```text
https://www.nuget.org/packages/OsLibCore
https://www.nuget.org/packages/JsonPit
https://github.com/Burkhardt/OsLib/commits/main/
https://github.com/Burkhardt/JsonPit/commits/main/
https://github.com/Burkhardt/RAIkeep/blob/main/README_codesigning.md#proposed-windows-artifact-inventory
```

GitHub calls the component repository OsLib; its NuGet package is OsLibCore.
Public Insights links are also available at the addresses below. Traffic
analytics require repository access, so use public commit history and package
statistics as the directly reviewable evidence in the form.

```text
https://github.com/Burkhardt/OsLib/pulse
https://github.com/Burkhardt/JsonPit/pulse
```

## URL choices

The umbrella repository is the homepage. Use the OsLibCore NuGet page as the
single Download URL. After the coordinated 4.6.6 release, its packaged README
will display the SignPath preparation notice and link the umbrella signing policy.
The other .NET packages use NuGet; Python downloads use these PyPI pages:

- https://pypi.org/project/inqaba/
- https://pypi.org/project/umgodi-json/
- https://pypi.org/project/vikela/

Include those additional URLs in Reputation if space permits. The public
[policy and inventory](../README_codesigning.md) lists all suite components and
the proposed Windows binaries. The form has no attachment field; no separate
upload is required. The application requests coverage of that suite, subject to
Foundation review. Do not represent planned signing as already active.

The form allows an empty Privacy Policy URL when the software does not collect
user data. RAIkeep processes user-selected application data and configured cloud
files; the public policy describes that behavior. Leave Wikipedia empty.

## Before submission

Wait until NuGet and PyPI serve 4.6.6 and inspect their rendered README notices.
Then resume this application. The release does not activate code signing.

Confirm that the proposed maintainer roles and privacy policy accurately describe
the project, and that the public URLs resolve after publication. Confirm MFA on
the GitHub account and accept the Foundation's signing-approval requirements.
The [Engenho signing handover](HANDOVER_TO_RITA_Engenho_SignPath.md) describes
the proposed implementation and installed-launcher verification.
The application describes a planned integration. Foundation acceptance and its
review of the project's reputation are still required.
[Code signing policy](../README_codesigning.md) · [Foundation terms](https://signpath.org/terms)
