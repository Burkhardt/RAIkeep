# Release Notes: RAIkeep v4.4.4

RAIkeep v4.4.4 implements accepted [`CR044_AIA_and_jsonpit_to_RAIkeep_Auto-Detect-Cloud-Drives-and-Init-Config.md`](CR/CR044_AIA_and_jsonpit_to_RAIkeep_Auto-Detect-Cloud-Drives-and-Init-Config.md) as a coordinated nine-package release.

## New standalone bootstrap tool

- Introduces `Burkhardt/Amafu` and the native `amafu` command.
- `amafu detect` discovers mounted cloud providers without writes.
- `amafu init` (alias `init-config`) generates `~/.config/RAIkeep.json5`, with overwrite protection, `--force`, and `--dry-run`.
- Amafu is independent of OsLib and protects OsLib's immutable startup configuration boundary.
- Distribution includes the NuGet tool plus NativeAOT GitHub release binaries for macOS, Linux, and Windows.
- Automatic cloud-provider discovery is supported and tested only on macOS in 4.4.4; Linux and Windows currently use the explicit starter-template fallback.

## Suite integration

- `pits` provides actionable `amafu init` guidance when configuration is absent.
- Amafu is the first package released after the umbrella GitHub Release and before OsLibCore.
- Recovery supports `scripts/release-chain.sh 4.4.4 --resume-after-amafu`.
- All nine packages align at 4.4.4; existing library and CLI behavior is otherwise unchanged.

Tagging, GitHub Releases, and NuGet publication remain behind RAI's manual release-chain gate.
