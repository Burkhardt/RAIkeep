# OsLibCore 4.4.1 Release Notes

OsLibCore 4.4.1 implements the public command boundary requested by accepted
[`CR037_AIA_to_RAIkeep_RaidSeeder_Diagram_Artifact_Management.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR037_AIA_to_RAIkeep_RaidSeeder_Diagram_Artifact_Management.md).
It also implements accepted
[`CR037.1_AIA_to_RAIkeep_CLI_Global_Flag_and_Verb_Dispatch_Resilience.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR037.1_AIA_to_RAIkeep_CLI_Global_Flag_and_Verb_Dispatch_Resilience.md).

It adds typed `RaidCommand` requests for `import`, `export`, `refresh`, and
`validate`; separate ItemId/Number/NameExt identity; cloud and ItemTree options;
hydratable/plain SVG selection; token-safe execution through
`CliCommand`/`RaiSystem`; and serialized process-wide invocation. Controlled
fake-executable tests verify exact argument boundaries and execution results.
The shared `CliVerbDispatch` boundary detects reserved verbs outside argument
zero and produces deterministic corrected command lines before product I/O.
