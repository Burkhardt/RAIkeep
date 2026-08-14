# Prep work

As preprocessing, first commit all changes in all subprojects with meaningful messages.
Then derive the next release number from the latest remote `vX.Y.Z` tag common to all seven child repositories. RaiDiagram's first coordinated release requires the explicit `4.2.0` argument because it has no earlier tag. Do not use unreleased local project-file drift as the source of truth.
Then change the csproj version numbers accordingly with one shared number, and check all md and puml files that need updates so both forms of documentation reflect the current package line.
Finally, commit the umbrella documentation and all seven updated submodule pointers on the RAIkeep `main` branch. The umbrella commit must already point to the exact seven child commits intended for release before the script starts.

# How to run next time:

<code>cd /Users/RSB/Projects/GitHub/RAIkeep
scripts/release-chain.sh</code>

Passing an explicit version is still supported when needed:

<code>scripts/release-chain.sh 4.2.0</code>

The script first preflights all eight repositories: the umbrella and seven package repositories. It then pushes the prepared RAIkeep umbrella `main` if needed and applies the passed version as the umbrella tag (for example `v4.2.0`). The umbrella tag is applied before any child repository is pushed or tagged. It does not publish a NuGet package because the umbrella workflow is manual-only.

The enforced package order after that umbrella label is:

- `OsLibCore`
- `RaiUtils`
- `RaiImage`
- `RaiDiagram`
- `JsonPit`
- `ImgSeeder`
- `PitSeeder`

After each successful publish workflow, the chain polls NuGet until both the exact flat-container `.nupkg` and exact-version registration document return HTTP `200`. Each package must finish its workflow and both visibility checks before the next repository push/tag begins; there is no fixed delay.

The preflight refuses to start unless every child is clean, on `main`, not behind its remote, set to the requested version, and recorded at that exact commit by the umbrella. Existing version tags are accepted only when they already point to the expected commit; the script refuses to move a conflicting local or remote tag.

Use this local orchestrator as the single coordinated release mechanism. Each child repository's tag-triggered workflow still owns its package publication.

Do not run this as part of version-prep work unless publication is explicitly requested.

## About running inside the LLM:

```
Yes, this can be run within this chat workflow by asking me to execute it.
I am using GPT-5.3-Codex.
The exact model tier selection such as Medium is controlled by your Copilot/session configuration, not by the shell script itself.
```
