# OsLibCore 4.4.1 Release Notes

OsLibCore 4.4.1 implements the public command boundary requested by accepted
[`CR037_AIA_to_RAIkeep_RaidSeeder_Diagram_Artifact_Management.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR037_AIA_to_RAIkeep_RaidSeeder_Diagram_Artifact_Management.md).
It also implements accepted
[`CR037.1_AIA_to_RAIkeep_CLI_Global_Flag_and_Verb_Dispatch_Resilience.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR037.1_AIA_to_RAIkeep_CLI_Global_Flag_and_Verb_Dispatch_Resilience.md).
The synchronized release also carries accepted
[`CR040_AIA_to_RAIkeep_and_jsonpit_Prohibit-Read-Modify-Write.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR040_AIA_to_RAIkeep_and_jsonpit_Prohibit-Read-Modify-Write.md)
and
[`CR041_jsonpit_to_RAIkeep_Restore-Clean-Change-Filenames.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR041_jsonpit_to_RAIkeep_Restore-Clean-Change-Filenames.md);
those changes are implemented in JsonPit and PitSeeder.

It adds typed `RaidCommand` requests for `import`, `export`, `refresh`, and
`validate`; separate ItemId/Number/NameExt identity; cloud and ItemTree options;
hydratable/plain SVG selection; token-safe execution through
`CliCommand`/`RaiSystem`; and serialized process-wide invocation. Controlled
fake-executable tests verify exact argument boundaries and execution results.
The shared `CliVerbDispatch` boundary detects reserved verbs outside argument
zero and produces deterministic corrected command lines before product I/O.
