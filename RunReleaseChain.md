# Prep work

As preprocessing, first commit all changes in all subprojects with meaningful messages.
Then derive the next release number from the latest remote `vX.Y.Z` tag common to all 6 child repositories. Do not use unreleased local project-file drift as the source of truth.
Then change the csproj version numbers accordingly with one shared number, and check all md and puml files that need updates so both forms of documentation reflect the current package line.

# How to run next time:

<code>cd /Users/rsb/Project2026/GitHub/RAIkeep
scripts/release-chain.sh</code>

Passing an explicit version is still supported when needed:

<code>scripts/release-chain.sh 3.13.1</code>

The enforced package order is:

- `OsLibCore`
- `RaiUtils`
- `RaiImage`
- `JsonPit`
- `ImgSeeder`
- `PitSeeder`

The chain keeps the 330-second wait between published packages and verifies package visibility through the NuGet flat-container `.nupkg` URL. Each package must finish its own publish workflow, NuGet visibility check, and hold window before the next package starts.

Do not run this as part of version-prep work unless publication is explicitly requested.

## About running inside the LLM:

```
Yes, this can be run within this chat workflow by asking me to execute it.
I am using GPT-5.3-Codex.
The exact model tier selection such as Medium is controlled by your Copilot/session configuration, not by the shell script itself.
```
