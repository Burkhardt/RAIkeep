# Release Notes: PitSeeder v4.4.4

PitSeeder participates in accepted [`CR044_AIA_and_jsonpit_to_RAIkeep_Auto-Detect-Cloud-Drives-and-Init-Config.md`](CR/CR044_AIA_and_jsonpit_to_RAIkeep_Auto-Detect-Cloud-Drives-and-Init-Config.md).

When standard RAIkeep configuration is absent, storage commands now stop before cloud-provider resolution and direct the operator to run `amafu init`. PitSeeder does not duplicate Amafu detection or configuration-writing logic. Existing seed, export, audit, delete, and maintenance behavior remains unchanged.
