# PitSeeder 4.4.1 Release Notes

PitSeeder and `pits` 4.4.1 participate in the synchronized eight-package
delivery of accepted
[`CR037_AIA_to_RAIkeep_RaidSeeder_Diagram_Artifact_Management.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR037_AIA_to_RAIkeep_RaidSeeder_Diagram_Artifact_Management.md).
They implement accepted
[`CR037.1_AIA_to_RAIkeep_CLI_Global_Flag_and_Verb_Dispatch_Resilience.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR037.1_AIA_to_RAIkeep_CLI_Global_Flag_and_Verb_Dispatch_Resilience.md).

Seed, export, audit, delete, maintenance, JSON5-comment, and clean-exit
process-flag behavior remain intact. Fallback dependencies and CLI version
output align to 4.4.1. A misplaced reserved verb now exits `2` with an
actionable command-first correction before pit/filesystem access, and version
flags take immediate precedence.
