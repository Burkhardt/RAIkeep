# Release Notes: RAIkeep v4.5.2

RAIkeep 4.5.2 improves cloud-drive setup with optional Amafu shortcuts, installer
PATH fixes, and a practical weather-data walkthrough. All nine C# packages and
internal package dependencies align to 4.5.2. JsonPit persistence and live-object
mutation behavior are unchanged.

## Cloud setup

- `amafu detect --create-links` creates missing `~/.CloudStorage/<provider>`
  symbolic links for detected cloud roots. Plain detection remains read-only.
- `amafu init --create-links` creates links along with a new configuration.
  Matching links are reused; conflicting paths are preserved and reported.
  `--dry-run` writes nothing, and generated configuration retains real roots.
- Amafu remains a standalone bootstrap utility without an OsLib dependency.
- The installer puts managed CLI paths ahead of legacy installations and
  configures zsh non-interactive SSH and login sessions as well as interactive
  shells, backing up existing startup files before edits.
- JsonPit's GettingStarted recommends cloud shortcuts. FirstSteps_pits walks
  through creating an iCloud pit and importing Open-Meteo JSON with curl and jq.

## Release preparation

- Fix the manifest's literal C# interpolation braces and keep Amafu's existing
  version output format consistent with its tests and validator.
- Validate conditional fallback dependency versions; previously those checks
  were skipped because the presence check did not match attributes.
- Preserve historical feature-introduction versions when bumping current docs.
- Update the installer default and release instructions to 4.5.2.

## Verification and handoff

- Complete Release solution run: **844 passed, 0 failed, 0 skipped**, including
  JsonPit SSH/cloud synchronization scenarios.
- Release-tool regression tests: **2 passed**; release validator: **81 checks passed**.
- macOS ARM64 native Amafu publish and CLI version/dry-run smoke checks passed.
- Shell syntax checks passed for installer and release-chain scripts.
- Compiler/analyzer warnings remain; there were no build or test errors.

CR050 multi-account discovery is a separate draft for review, not implemented
in this release. Amafu still selects the first existing root per provider.
Rainer runs `scripts/release-chain.sh 4.5.2` after preparation. No publication is
performed by version preparation or tests. The script publishes the C# stack;
Adele owns jsonpit-python/jpit 4.5.2 publication and parity verification separately.
Python 4.5.2 must be published before using the installer for a fully aligned
4.5.2 setup; Python 4.5.1 is already in use.
