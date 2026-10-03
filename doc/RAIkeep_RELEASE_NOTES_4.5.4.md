# Release Notes: RAIkeep v4.5.4

This patch fixes Amafu cloud initialization: `amafu init --create-links` now
writes the created `~/.CloudStorage/<provider>/` shortcuts into `RAIkeep.json5`.
Previously it created the shortcuts but retained the original physical paths
in the configuration. Preview and saved output now agree for both `init` and
`init-config`.

See [Amafu 4.5.4 release notes](Amafu_RELEASE_NOTES_4.5.4.md) for examples and
migration of existing configuration with `amafu reconcile --apply`.

All nine C# packages and applicable internal dependencies align to 4.5.4.
The other packages have no runtime behavior changes in this patch. JsonPit's
GettingStarted guide documents the corrected initialization behavior.

Release tooling retains the assembly-derived Amafu version output and its
matching validation checks. The C# release chain handles publication;
Python/jpit releases remain separately coordinated with Adele.

## Verification

- Complete Amafu suite: 62 passed, 0 failed, 0 skipped.
- Version-filtered Release tests with local sources: 13 passed across Amafu,
  ImgSeeder, PitSeeder, RaiDiagram, and RaidSeeder.
- Release validator: 80 checks passed; release-tool regression tests: 2 passed.
- Release-chain shell syntax check passed.
