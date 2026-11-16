# CR087 provider review

Accepted for implementation on November 15, 2026. The local 4.6.4 release candidate and the public 0.1.0 Python distributions predate the fix. The active Python delivery target is `umgodi-json`, which supplies `jpit`. The frozen legacy package has the historical defect.

## Reproduction

On a disposable local pit, the C# CLI merged a day-old fragment and issued a receipt. After aging the receipt by eleven minutes, a second distinct historical fragment forced canonical persistence during the next maintenance pass. The CLI reported current master, canonical persisted, one eligible change, zero changes removed, zero receipts removed and a cleanup revalidation deferral. A control pass with every change already accounted for skipped Store and retired the eligible pair. Including a pending historical fragment is essential for a CLI regression that exercises the faulty Store branch.

In an independent Python fixture, a flagged Umgodi pit persisted a day-old fragment. Immediately afterwards the on-disk master named the calling process and reported an expired lease. The Python cleanup loop also needs a fresh exact-owner check and evidence that the persisted canonical snapshot accounts for the change before removing an eligible pair.

## Acceptance work

Cover active lease renewal, a foreign takeover after persistence, the ten-minute receipt grace and preservation of canonical history in JsonPit.Tests, pits.Tests and the active Umgodi tests. Preserve snapshot notification and dirty-fragment semantics when additions race with serialization. A fresh lease must not acknowledge data beyond the captured snapshot. Use temporary local roots for these regressions.

[Requested change and acceptance criteria](https://github.com/Burkhardt/AIA/blob/main/doc/CR087_AIA_to_RAIkeep_JsonPit_Store_MasterFlag_Lease_Backdating.md)
