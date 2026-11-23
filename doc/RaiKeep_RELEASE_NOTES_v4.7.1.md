# Release Notes: RAIkeep v4.7.1

## 1. Release scope

This coordinated candidate supersedes the incomplete 4.7.0 release without
changing its published tags or artifacts.

## 2. Python persistence

Umgodi Pit constructors require `InqPath` directories. The `jpit` and `umgodi`
CLI commands continue to accept supported path and `.pit` filename inputs.

## 3. Guardrails

Vikela adds RAI021, RAI022 and RAI023 for recognizable configuration
substitution, temporary Pit locations and invalid Pit path arguments. RaiGuard
adds RAI021 configuration-substitution analysis for C# tests.

## 4. Cloud test configuration

Umgodi test Pits use isolated directories in the real configured Dropbox
drive. If Dropbox has no timing file, test setup copies the original OneDrive
timing file once and warns that Dropbox-specific values should be calibrated.

## 5. Compatibility

The legacy jsonpit-python repository is archived. `jpit` remains an alias
provided by the `umgodi-json` distribution.

## 6. Release status

This is a candidate, not an instruction to publish. The
[preflight record](RELEASE_PREFLIGHT_4.7.1.md) tracks completed checks and
remaining release blockers.
