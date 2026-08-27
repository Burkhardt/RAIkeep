# JsonPit 4.2.3

Implements the JsonPit portion of accepted CR015.

- Treats JSON null as a property tombstone at arbitrary nested object depth.
- Recursively merges historical fragments so sibling properties survive nested
  deletions.
- Omits tombstoned properties and newly empty parent objects from projected
  reads and JSON exports.
- Adds `PitItem.Merge(JObject)` with tombstone-aware partial merge semantics.
- Adds `PitItem.DeletePropertyPath(...)` for explicit dot-delimited traversal.
- Preserves `DeleteProperty(...)` as a literal top-level property operation.
- Preserves append-only historical fragments, time travel, deletion barriers,
  and later property reintroduction.

RAI retains the manual coordinated release gate; no tag or publication is
authorized by these notes.

Release verification: 23 focused merge/property-deletion tests passed,
including ten added or tightened CR015 cases. The complete JsonPit Release suite
passed all 156 tests, including configured persistence and remote scenarios.
