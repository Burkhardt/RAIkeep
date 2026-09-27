# PitSeeder 4.4.1 Release Notes

PitSeeder and `pits` 4.4.1 participate in the synchronized eight-package
delivery of accepted
[`CR037_AIA_to_RAIkeep_RaidSeeder_Diagram_Artifact_Management.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR037_AIA_to_RAIkeep_RaidSeeder_Diagram_Artifact_Management.md).
They implement accepted
[`CR037.1_AIA_to_RAIkeep_CLI_Global_Flag_and_Verb_Dispatch_Resilience.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR037.1_AIA_to_RAIkeep_CLI_Global_Flag_and_Verb_Dispatch_Resilience.md).
It also implements the CLI boundaries of accepted
[`CR040_AIA_to_RAIkeep_and_jsonpit_Prohibit-Read-Modify-Write.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR040_AIA_to_RAIkeep_and_jsonpit_Prohibit-Read-Modify-Write.md)
and interoperates with accepted
[`CR041_jsonpit_to_RAIkeep_Restore-Clean-Change-Filenames.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR041_jsonpit_to_RAIkeep_Restore-Clean-Change-Filenames.md).

Seed, export, audit, delete, maintenance, JSON5-comment, and clean-exit
process-flag behavior remain intact. Fallback dependencies and CLI version
output align to 4.4.1. A misplaced reserved verb now exits `2` with an
actionable command-first correction before pit/filesystem access, and version
flags take immediate precedence.

`pits seed` validates all input objects before opening a destination pit and
rejects client-supplied `Modified` or `Deleted`. `delete-property` rejects
`Id`, `Modified`, and `Deleted`, directing callers to `delete-item` for entity
deletion. Ordinary maintenance recognizes clean CR041 change/receipt stems and
legacy SHA-suffixed artifacts during rolling upgrades.
