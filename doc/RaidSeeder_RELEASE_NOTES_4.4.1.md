# RaidSeeder 4.4.1 Release Notes

RaidSeeder 4.4.1 implements accepted
[`CR037_AIA_to_RAIkeep_RaidSeeder_Diagram_Artifact_Management.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR037_AIA_to_RAIkeep_RaidSeeder_Diagram_Artifact_Management.md).
It also implements accepted
[`CR037.1_AIA_to_RAIkeep_CLI_Global_Flag_and_Verb_Dispatch_Resilience.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR037.1_AIA_to_RAIkeep_CLI_Global_Flag_and_Verb_Dispatch_Resilience.md).

The repository and NuGet identity move from `RaidCli` to `RaidSeeder`; the
installed shell command remains `raid`. The CLI now provides `import`, `export`,
`refresh`, and `validate`, with polished Nerd Font help and iorg-aligned
`--cloud`, `--root`, `--app`, `--tenant`, and ItemTree addressing.

ItemId, Number, and NameExt remain separate. Export derives current `.raid`,
`.puml`, and/or hydratable/plain `.svg` from the authoritative manifest. Refresh
updates only stale or missing co-located derivatives. The v4.4.0 `RaidCli`
package and tag remain immutable; NuGet deprecation is a post-publication step.

Reserved verbs are now protected system keywords. Misplaced verbs fail before
artifact access with exit code `2` and an exact verb-first correction;
`-v`/`--version` takes immediate precedence at any argument position.
