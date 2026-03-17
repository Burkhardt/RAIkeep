# MANIFESTO

## Purpose

`RAIkeep` exists as the umbrella workspace for `JsonPit`, `OsLib`, `RaiUtils`, and `RaiImage`.

Its role is not to erase package boundaries. Its role is to make integration work, architectural alignment, and real-world validation possible while each library remains independently owned and independently releasable.

## Agreements

### Package independence

Each package keeps its own identity, release flow, and internal responsibility.

The umbrella workspace is for coordinated work, not for collapsing the libraries into a single indistinguishable codebase.

### Real tests must be real

If a test claims to validate cloud behavior, it must run against an actual cloud-backed location on the machine that executes the test.

Sandboxed, redirected, or synthetic setups are valid for mechanics tests, but they must be named honestly and kept separate from real-environment cloud tests.

### Deterministic test behavior

Unit-style tests should leave the file system as they found it.

Randomized file and directory names are not the default testing strategy. Deterministic reusable paths with explicit cleanup are preferred.

### Configuration over environment

Library setup should be driven by `OsConfigFile`-based configuration.

Environment variables are not the configuration model. They may exist as legacy compatibility inputs or for narrowly defined system-resolution fallbacks, but they are not the desired source of truth.

For real cloud tests in particular, explicit configuration must win and environment-variable-based discovery must be ignored.

### Stable config location

The shared configuration location is:

`~/.config/RAIkeep/osconfig.json`

Resolution of `~` is accepted. The use of environment variables to choose different config locations is not the intended direction.

### Save, not Persist

Configuration writes should use `Save()`.

Legacy `Persist()` APIs are considered obsolete compatibility wrappers and should be retired from active use.

### Honest naming

Names must describe reality.

If a test exercises configuration mechanics, probing rules, path normalization, or fallback logic, it should be named as such.

If a test is named for cloud behavior, it should validate cloud behavior on a real provider-backed path.

## Engineering direction

The direction of the codebase is toward:

- explicit configuration instead of implicit machine-state discovery
- deterministic tests instead of randomized temp layouts
- real integration tests instead of simulated claims
- small reusable libraries with clear boundaries
- documentation that reflects actual behavior rather than aspiration

## Working rule

When there is tension between convenience and truth, choose truth.

When there is tension between legacy behavior and architectural clarity, move toward clarity in small safe steps.