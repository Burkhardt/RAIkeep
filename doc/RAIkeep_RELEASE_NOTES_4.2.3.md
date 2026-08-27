# RAIkeep 4.2.3 Release Notes

**Status:** Prepared source and verification candidate; not published  
**Accepted request:**
[`CR015_AIA_to_RAIkeep_Nested_Property_Tombstones_and_CLI_Delete.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR015_AIA_to_RAIkeep_Nested_Property_Tombstones_and_CLI_Delete.md)  
**AIA Step 3 confirmation:**
[`CR015_Accepted_Nested_Property_Tombstones_and_CLI_Delete.md`](https://github.com/Burkhardt/AIA/blob/260dbe73e3a0603485b8839416c46c58853493cb/doc/CR015_Accepted_Nested_Property_Tombstones_and_CLI_Delete.md)

RAIkeep 4.2.3 is a coordinated, backward-compatible patch across all seven
packages.

## CR015 changes

- JsonPit recursively applies null property tombstones at arbitrary object depth.
- Projected reads and exports omit tombstoned nested properties and recursively
  prune parent objects left empty by the mutation.
- `PitItem.DeletePropertyPath(...)` provides explicit dot-path traversal while
  `DeleteProperty(...)` retains literal top-level property-name semantics.
- Historical `.pit` fragments remain append-only, including the null markers
  required for time travel and audit integrity.
- PitSeeder adds `pits delete-property` and `pits delete-item` with the existing
  pit-root, configured-cloud, no-logo, debug, and process-window options.
- OsLibCore adds typed `PitsDeletePropertyRequest` and
  `PitsDeleteItemRequest` builders plus synchronous/asynchronous execution.
- Delete arguments remain discrete process tokens; malformed mandatory values
  are rejected before process start.

## Compatibility

- `-n` continues to mean `--nologo`; delete commands always persist accepted
  mutations.
- The coordinated 4.2.2 recovery, diagram, image, exception, and tool-wrapper
  contracts carry forward unchanged.
- No package, identity subsystem, raw process boundary, or legacy CLI removal is
  introduced.

RAI retains the manual tag and publication gate. These notes do not authorize
the implementing agent to start the release chain.

Release verification: the coordinated Release build succeeded; OsLib passed
110 tests, RaiUtils 22, RaiImage 104, RaiDiagram 34, ImgSeeder 16, and
PitSeeder 23. JsonPit passed all 156 tests, including configured persistence and
remote scenarios.
