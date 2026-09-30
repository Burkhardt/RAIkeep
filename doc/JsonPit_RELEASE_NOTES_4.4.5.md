# Release Notes: JsonPit v4.4.5

JsonPit participates unchanged at the public library level in the synchronized RAIkeep v4.4.5 release for accepted [`CR047_jsonpit_and_pits_Require-Existing-Patch-Flag-and-Seed-Commit-Count.md`](CR/CR047_jsonpit_and_pits_Require-Existing-Patch-Flag-and-Seed-Commit-Count.md). PitSeeder uses JsonPit's existing unflagged read-only projection and `Contains(id, withDeleted: false)` APIs to validate strict patches without changing the persistence or coordination contracts.
