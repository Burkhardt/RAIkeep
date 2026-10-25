# Prep work

As preprocessing, prepare the release using the automated bumping engine:

<code>cd /Users/RSB/Projects/GitHub/RAIkeep
./scripts/bump-version.py 4.5.13</code>

This uses [`scripts/release-manifest.json`](scripts/release-manifest.json) to deterministically update all project files, code constants, CLI tests, and documentation, and scaffolds the 11 release note files. If any new version-tracked file is introduced, simply add its path and replacement rule to `scripts/release-manifest.json`.

After bumping, author the new `## <version>` sections prepended to the consolidated package histories in `doc/releases/v<major>.x/<Package>_RELEASE_NOTES_<major>.x.md`. Commit all changes in subprojects and the umbrella before starting the release chain.

## Release commit subjects

The GitHub commit list is part of the release record. Use a short, plain-English
subject that names the delivered behavior, such as `Clean EventFile naming and
legacy hash validation` or `Add strict pits seed request`. Do not prefix a
subject with `feat:`, `chore:`, `release:`, or `Prepare`. If a commit only
synchronizes the coordinated line, use `Coordinated X.Y.Z release`.

# How to run next time:

<code>cd /Users/RSB/Projects/GitHub/RAIkeep
scripts/release-chain.sh 4.5.13</code>

The script first preflights all twelve repositories: the umbrella, ten NuGet package repositories, and `JsonPit.Python`. The umbrella commit must already record every prepared child commit, but its `main` push and version tag are the **last** publication step. Only after every NuGet and PyPI package is visible does the script tag the umbrella (for example `v4.5.13`) and verify its coordinated GitHub Release. The umbrella workflow publishes no NuGet package.

The enforced release order is:

- `Amafu`
- `OsLibCore`
- `RaiUtils`
- `RaiImage`
- `RaiDiagram`
- `RaidSeeder`
- `JsonPit`
- `JsonPit.Python`
- `ImgSeeder`
- `PitSeeder`
- `RaiGuard`
- `RAIkeep` umbrella GitHub Release

## Python coordination

Before any tag is created, Python preflight validates both distribution versions,
the exact companion dependency, current documentation, and embedded standalone
sources. It builds wheels and source archives for both `jsonpit` and `jpit`, then
installs the wheels in a temporary virtual environment and checks `-v` and
`--version` for both commands, including the `v` prefix.

After C# `JsonPit`, the chain uploads both distributions with `PYPI_TOKEN`, waits
for both exact versions on PyPI, and creates the Python GitHub Release with the
standalone download and package assets. Release notes come from the prepared
local checkout, so publishing does not depend on an umbrella tag created later.

The fleet installer uses one managed `jsonpit` environment for both commands;
it does not install a second pipx environment for the `jpit` companion or bypass
system Python protection. To repair an existing duplicate pipx installation:

```bash
pipx uninstall jpit
pipx install --force "jsonpit==4.5.13"
```

## One-time Amafu publishing bootstrap

Before the inaugural `v4.4.4` chain, create a NuGet Trusted Publishing policy
for the new package workflow. Use package owner `Burkhardt`, repository owner
`Burkhardt`, repository `Amafu`, workflow file `publish-nuget.yaml`, no GitHub
environment, push-new-packages-and-versions scope, and the exact package pattern
`Amafu`. This is account configuration and is intentionally not performed by
the release script.

After each successful publish workflow, the chain polls NuGet until both the exact flat-container `.nupkg` and exact-version registration document return HTTP `200`. Each package must finish its workflow and both visibility checks before the next repository push/tag begins; there is no fixed delay.
Polling uses a HEAD request for the package and a bounded request for the registration document. A transient network timeout is logged and retried; a package that remains unavailable for 30 minutes stops the chain with a recovery message.

The preflight refuses to start unless every child is clean, on `main`, not behind its remote, set to the requested version, and recorded at that exact commit by the prepared umbrella. It also checks the umbrella's branch and any existing version tag before publishing a child. The script refuses to move a conflicting local or remote tag.

Use this local orchestrator as the single coordinated release mechanism. Each child repository's tag-triggered workflow still owns its package publication.

If the chain stops after RaiDiagram has already been tagged, repair and dispatch
the immutable RaiDiagram release workflow as documented for that incident, then
resume only through:

<code>scripts/release-chain.sh 4.5.13 --resume-after-raidiagram</code>

Recovery mode preserves all existing child tags and leaves the umbrella untagged
until the end. It waits until the RaiDiagram package and
registration endpoints both return HTTP `200`, and only then releases RaidSeeder,
JsonPit, JsonPit.Python, ImgSeeder, PitSeeder, and RaiGuard in order. It finishes
by publishing the umbrella GitHub Release. Do not manually time NuGet propagation or
start the remaining package workflows independently.

If the inaugural Amafu publication needs recovery after its immutable tag was
created, resume the remaining chain through:

<code>scripts/release-chain.sh 4.5.13 --resume-after-amafu</code>

This waits for Amafu's NuGet visibility before releasing OsLibCore and the
remaining dependency chain.

If the chain stops after OsLibCore has already been published, resume the remaining chain through:

<code>scripts/release-chain.sh 4.5.13 --resume-after-oslib</code>

This verifies that Amafu and OsLibCore are both available on NuGet before releasing RaiUtils and the remaining dependency chain.

If the chain stops after RaiImage has already been published, first verify that
Amafu, OsLibCore, RaiUtils, and RaiImage are visible on NuGet. Then resume
without republishing them:

<code>scripts/release-chain.sh 4.5.13 --resume-after-raiimage</code>

This checks the existing packages and immutable submodule pointers before
releasing RaiDiagram and the remaining packages in order, with the umbrella last.

If all child packages have published but the final umbrella step fails, verify
the child tags and package visibility and finish only the umbrella step with:

<code>scripts/release-chain.sh 4.5.13 --resume-after-raiguard</code>

Do not run this as part of version-prep work unless publication is explicitly requested.

## About running inside the LLM:

```
Yes, this can be run within this chat workflow by asking me to execute it.
I am using GPT-5.3-Codex.
The exact model tier selection such as Medium is controlled by your Copilot/session configuration, not by the shell script itself.
```
