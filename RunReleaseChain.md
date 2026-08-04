# Prep work

As preprocessing, first commit all changes in all subprojects with meaningful messages.
Then derive the next release number from the latest remote `vX.Y.Z` tag common to all 6 child repositories. Do not use unreleased local project-file drift as the source of truth.
Then change the csproj version numbers accordingly with one shared number, and check all md and puml files that need updates so both forms of documentation reflect the current package line.
Finally, commit the umbrella documentation and all six updated submodule pointers on the RAIkeep `main` branch. The umbrella commit must already point to the exact six child commits intended for release before the script starts.

# How to run next time:

<code>cd /Users/RSB/Projects/GitHub/RAIkeep
scripts/release-chain.sh</code>

Passing an explicit version is still supported when needed:

<code>scripts/release-chain.sh 3.13.1</code>

The script first preflights all seven repositories. It then pushes the prepared RAIkeep umbrella `main` if needed and applies the passed version as the umbrella tag (for example `v3.13.1`). The umbrella tag is applied before any child repository is pushed or tagged. It does not publish a NuGet package because the umbrella workflow is manual-only.

The enforced package order after that umbrella label is:

- `OsLibCore`
- `RaiUtils`
- `RaiImage`
- `JsonPit`
- `ImgSeeder`
- `PitSeeder`

The chain enforces a 380-second hold after each successful publish workflow and verifies package visibility through the NuGet flat-container `.nupkg` URL. The longer window accommodates observed RaiUtils indexing latency. Each package must finish its own publish workflow, NuGet visibility check, and full hold window before the next repository push/tag begins.

The preflight refuses to start unless every child is clean, on `main`, not behind its remote, set to the requested version, and recorded at that exact commit by the umbrella. Existing version tags are accepted only when they already point to the expected commit; the script refuses to move a conflicting local or remote tag.

Use this local orchestrator or the umbrella sequential workflow for a release, never both for the same version.

Do not run this as part of version-prep work unless publication is explicitly requested.

## About running inside the LLM:

```
Yes, this can be run within this chat workflow by asking me to execute it.
I am using GPT-5.3-Codex.
The exact model tier selection such as Medium is controlled by your Copilot/session configuration, not by the shell script itself.
```
