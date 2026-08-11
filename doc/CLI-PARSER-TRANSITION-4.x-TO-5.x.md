# CLI parser transition from 4.x to 5.x

**Recorded:** 2026-08-10
**Applies to:** `pits` (PitSeeder) and `iorg` (ImgSeeder)

RAIkeep's `4.x` release line will provide a non-breaking transition from the
existing flat, flag-driven CLI syntax to the subcommand syntax requested by
`CR006_AfricaStage_to_RAIkeep_CliSubcommands.md`.

## 4.x transition contract

- A recognized command in the first argument position selects the new parser:
  `seed`, `export`, or `audit` for `pits`; `organize` or `clean` for `iorg`.
- An invocation without a recognized leading command continues through the
  legacy parser.
- Both parsers normalize their input into the same operation model and invoke
  the same handlers. Compatibility must not create a second implementation of
  seeding, exporting, auditing, organizing, or cleaning.
- Established legacy seed/export and image-organizer invocations remain
  supported throughout `4.x`.
- Configuration aliases are not deprecated by this parser transition. In
  particular, `iorg -r <dir>` and `iorg --root <dir>` are both supported by the
  new `organize` and `clean` command parser as well as the `4.x` legacy parser.
- The recently introduced `pits` audit flag family is intentionally excluded
  from the legacy compatibility promise. `--events`, `--event-machine`, and
  `--event-level` move directly to `pits audit`, `--machine`, and `--level`,
  respectively. Legacy use receives an actionable error directing the caller
  to the new command instead of being silently reinterpreted.
- Audit JSON output remains supported under the new `pits audit` command so
  existing machine-readable event workflows retain an equivalent command path.
- Help and release notes lead with the subcommand syntax and identify the flat
  syntax as transitional. Deprecation messaging must not contaminate JSON or
  other pipe-oriented standard output.

The executable therefore does not require a subcommand for every `4.x`
invocation. A subcommand is required only when using the new syntax.

## 5.x removal boundary

The `5.x.x` line will use the subcommand parser exclusively. The legacy parser
and its flat operation-selecting flags are scheduled for removal in that major
line; there is no promise that legacy invocations will run under `5.x.x`.

Before removal, RAIkeep must:

1. provide a subcommand equivalent for every legacy capability that remains
   supported product behavior;
2. cover both the `4.x` compatibility paths and the `5.x`-ready subcommand paths
   with provider-owned tests;
3. document the final command mapping and breaking removal in the relevant
   PitSeeder and ImgSeeder release notes; and
4. give consuming projects a receiver-led validation opportunity under the
   cross-boundary Change Request process.

This transition note records provider policy. It does not rename or modify the
requester-owned CR and does not itself authorize package publication.
