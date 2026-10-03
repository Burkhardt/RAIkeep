# Prep work

As preprocessing, prepare the release using the automated bumping engine:

<code>cd /Users/RSB/Projects/GitHub/RAIkeep
./scripts/bump-version.py 4.5.4</code>

This uses [`scripts/release-manifest.json`](scripts/release-manifest.json) to deterministically update all project files, code constants, CLI tests, and documentation, and scaffolds the 10 release note files. If any new version-tracked file is introduced, simply add its path and replacement rule to `scripts/release-manifest.json`.

After bumping, author the narrative highlights in the scaffolded release note documents (`doc/*_RELEASE_NOTES_<ver>.md`). Commit all changes in subprojects and the umbrella before starting the release chain.

# How to run next time:

<code>cd /Users/RSB/Projects/GitHub/RAIkeep
scripts/release-chain.sh 4.5.4</code>

The script first preflights all ten repositories: the umbrella and nine package repositories. It then pushes the prepared RAIkeep umbrella `main` if needed and applies the passed version as the umbrella tag (for example `v4.5.4`). The umbrella tag is applied before any child repository is pushed or tagged. It does not publish a NuGet package because the umbrella workflow creates the coordinated GitHub Release only.

The enforced package order after that umbrella label is:

- `Amafu`
- `OsLibCore`
- `RaiUtils`
- `RaiImage`
- `RaiDiagram`
- `RaidSeeder`
- `JsonPit`
- `ImgSeeder`
- `PitSeeder`

## Python coordination

The release chain publishes only the C# stack. Adele owns jsonpit-python/jpit
publication and parity checks. C# tag-based automatic version selection does
not inspect Python releases. Before using the installer for a fully aligned
4.5.4 setup, verify that Adele has published Python 4.5.4 as well.

## One-time Amafu publishing bootstrap

Before the inaugural `v4.4.4` chain, create a NuGet Trusted Publishing policy
for the new package workflow. Use package owner `Burkhardt`, repository owner
`Burkhardt`, repository `Amafu`, workflow file `publish-nuget.yaml`, no GitHub
environment, push-new-packages-and-versions scope, and the exact package pattern
`Amafu`. This is account configuration and is intentionally not performed by
the release script.

After each successful publish workflow, the chain polls NuGet until both the exact flat-container `.nupkg` and exact-version registration document return HTTP `200`. Each package must finish its workflow and both visibility checks before the next repository push/tag begins; there is no fixed delay.

The preflight refuses to start unless every child is clean, on `main`, not behind its remote, set to the requested version, and recorded at that exact commit by the umbrella. Existing version tags are accepted only when they already point to the expected commit; the script refuses to move a conflicting local or remote tag.

Use this local orchestrator as the single coordinated release mechanism. Each child repository's tag-triggered workflow still owns its package publication.

If the chain stops after RaiDiagram has already been tagged, repair and dispatch
the immutable RaiDiagram release workflow as documented for that incident, then
resume only through:

<code>scripts/release-chain.sh 4.5.4 --resume-after-raidiagram</code>

Recovery mode preserves all existing tags, pushes a clean reviewed umbrella
recovery commit when necessary, waits until the RaiDiagram package and
registration endpoints both return HTTP `200`, and only then releases RaidSeeder,
JsonPit, ImgSeeder, and PitSeeder in order. Do not manually time NuGet propagation or
start the remaining package workflows independently.

If the inaugural Amafu publication needs recovery after its immutable tag was
created, resume the remaining chain through:

<code>scripts/release-chain.sh 4.5.4 --resume-after-amafu</code>

This waits for Amafu's NuGet visibility before releasing OsLibCore and the
remaining dependency chain.

If the chain stops after OsLibCore has already been published, resume the remaining chain through:

<code>scripts/release-chain.sh 4.5.4 --resume-after-oslib</code>

This verifies that Amafu and OsLibCore are both available on NuGet before releasing RaiUtils and the remaining dependency chain.

Do not run this as part of version-prep work unless publication is explicitly requested.

## About running inside the LLM:

```
Yes, this can be run within this chat workflow by asking me to execute it.
I am using GPT-5.3-Codex.
The exact model tier selection such as Medium is controlled by your Copilot/session configuration, not by the shell script itself.
```
