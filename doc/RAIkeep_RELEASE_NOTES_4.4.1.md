# RAIkeep 4.4.1 Release Notes

RAIkeep 4.4.1 is the synchronized eight-package delivery of accepted
[`CR037_AIA_to_RAIkeep_RaidSeeder_Diagram_Artifact_Management.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR037_AIA_to_RAIkeep_RaidSeeder_Diagram_Artifact_Management.md).
It also delivers accepted
[`CR037.1_AIA_to_RAIkeep_CLI_Global_Flag_and_Verb_Dispatch_Resilience.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR037.1_AIA_to_RAIkeep_CLI_Global_Flag_and_Verb_Dispatch_Resilience.md).
It additionally delivers accepted
[`CR040_AIA_to_RAIkeep_and_jsonpit_Prohibit-Read-Modify-Write.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR040_AIA_to_RAIkeep_and_jsonpit_Prohibit-Read-Modify-Write.md)
and
[`CR041_jsonpit_to_RAIkeep_Restore-Clean-Change-Filenames.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR041_jsonpit_to_RAIkeep_Restore-Clean-Change-Filenames.md).

## RaidSeeder diagram artifact management

- Renames the dedicated repository and successor NuGet tool package from
  `RaidCli` to `RaidSeeder`; the installed command remains `raid`.
- Adds `raid import`, `export`, `refresh`, and `validate`, plus iorg-aligned
  cloud, application-root, exact-root, tenant, path-convention, Number, and
  NameExt options.
- Treats `.raid` as authoritative and derives `.puml` and `.svg` rather than
  trusting possibly stale siblings.
- Refresh writes only missing or stale derivatives; a current artifact is not
  rewritten, and refresh never rewrites the authoritative manifest.
- Adds hydratable and plain SVG profiles. Hydratable output includes structural
  metadata, ports, routing, and declared expressions, but never dynamic
  `aim-satisfied` evaluation state.
- Guarantees semantic round-trip fidelity for compiler-emitted PUML.
- Adds OsLibCore's typed `RaidCommand` wrapper and exact argument-forwarding
  verification.

## CLI dispatch resilience

- `pits`, `iorg`, and `raid` reserve their registered verbs and require an
  explicit subcommand at argument zero.
- A misplaced verb fails before filesystem/database access with exit code `2`,
  identifies the misplaced verb, and prints the corrected command line.
- `-v`/`--version` remains an immediate successful operation wherever it
  appears; command-first `verb --help` remains verb-specific.

## JsonPit sparse mutation and clean change files

- Client property mutation cannot set or tombstone engine-managed `Id`,
  `Modified`, or `Deleted`; protected failures are atomic.
- Live storage rejects projected read-modify-write payloads. Explicit trusted
  historical replay retains original lifecycle fields through `AddHistorical`.
- `pits seed` validates every payload before opening its destination and
  `delete-property` protects the lifecycle boundary.
- New changes and receipts use readable
  `{UtcTicks}_{ExactProcessIdentity}.{json|receipt}` names. Both C# and Python
  engines continue to discover legacy SHA-suffixed change files.
- Live C# mutations receive process-monotonic UTC ticks, preventing concurrent
  OS-clock resolution collisions without lengthening the public filename.
- Maintenance applies canonical accounting, immutable receipts, and the
  established ten-minute grace equally to clean and legacy names.

## Cloud safety and release coordination

Managed artifacts remain written directly at their final paths. No
TempDir-to-cloud move, established-directory swap, or
no-op rewrite is used. All eight packages align at 4.4.1 in this order:
OsLibCore, RaiUtils, RaiImage, RaiDiagram, RaidSeeder, JsonPit, ImgSeeder, and
PitSeeder.

Publication remains behind RAI's manual
`scripts/release-chain.sh 4.4.1` gate. The immutable `RaidCli 4.4.0` tag and
package are not rewritten; deprecation with `RaidSeeder` as replacement occurs
only after successful 4.4.1 publication and verification.
