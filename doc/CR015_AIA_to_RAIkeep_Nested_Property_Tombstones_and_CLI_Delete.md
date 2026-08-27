# CR015 — Nested Property Tombstones and First-Class CLI Delete Commands

**Requesting product:** AIA  
**Requesters:** Adele (PM, AIA) and Zébio (Dev, AIA)  
**Receiving product:** RAIkeep (`JsonPit`, `PitSeeder`, and `OsLibCore`)  
**Acceptance owner:** RAI  
**Target release:** Coordinated RAIkeep v4.2.3  
**Date submitted:** 2026-08-26  
**Status:** Implemented and verified — prepared for RAI's manual v4.2.3 release gate  
**AIA Step 3 confirmation:** [CR015 Accepted: Nested Property Tombstone Semantics and First-Class CLI Delete Commands](https://github.com/Burkhardt/AIA/blob/260dbe73e3a0603485b8839416c46c58853493cb/doc/CR015_Accepted_Nested_Property_Tombstones_and_CLI_Delete.md)

## 1. Objective and context

AIA and WWWA/AOM entity instances store structured metadata in pits. Properties
occur both at the top level and within nested relational containers such as
`What.Chat`, `Who.Participant`, and `Action.Conversation`.

JsonPit already supports item tombstones and top-level property tombstones, but
a nested null patch currently survives as a literal JSON null instead of
removing the nested property from projected state. PitSeeder also lacks explicit
commands for deleting an item or property without constructing a temporary seed
file.

CR015 closes both gaps while preserving JsonPit's append-only history.

## 2. Accepted provider clarifications

1. The change is assigned to the coordinated v4.2.3 patch line. Its additive,
   backward-compatible scope does not require a v4.3 minor release.
2. `property` is the canonical term, consistent with JSON and the existing
   `PitItem.SetProperty(...)` and `PitItem.DeleteProperty(...)` APIs.
3. `PitItem.DeleteProperty(string propertyName)` retains literal top-level
   semantics. Nested dot traversal is exposed separately as
   `PitItem.DeletePropertyPath(string propertyPath)` so an existing top-level
   property whose name contains a dot does not silently change meaning.
4. OsLibCore's typed `PitsCommand` boundary is extended for both new commands;
   callers do not construct raw process arguments.
5. `-n` retains its established `--nologo` meaning. Delete commands always
   persist accepted mutations; CR015 introduces no no-save or no-flush mode.
6. No new package, identity abstraction, or test harness is introduced.

## 3. Accepted behavior

### 3.1 Nested property tombstones (`JsonPit`)

- A JSON null at any nesting depth is a property tombstone during JsonPit merge
  and projection.
- Projected reads and exports omit the tombstoned property rather than exposing
  a literal null token.
- A parent object made empty solely by tombstones is omitted recursively.
- Sibling properties remain intact.
- Later non-null values can reintroduce a tombstoned property.
- Historical fragments and tombstones remain append-only in the `.pit` format.

### 3.2 Delete commands (`PitSeeder` / `pits`)

```text
pits delete-property <PitName> <ItemId> <PropertyPath> [-c <Config>] [-r <TenantRoot>] [-n]
pits delete-item <PitName> <ItemId> [-c <Config>] [-r <TenantRoot>] [-n]
```

`delete-property` accepts dot notation such as `What.Chat`, appends the nested
property tombstone, saves the pit, and releases the normal process activity
window. `delete-item` appends an item tombstone, saves the pit, and removes the
item from projected reads and exports.

Both commands use the existing configured-cloud and pit-root resolution rules.

### 3.3 Typed command boundary (`OsLibCore`)

Public typed request and build/run APIs cover `delete-property` and
`delete-item`, including synchronous and asynchronous execution. Mandatory
values and property-path structure are validated before process start, and
arguments remain discrete tokens.

## 4. Acceptance scenarios

1. Merging `{ "What": { "Chat": null } }` into an item containing
   `What.Instrument` and `What.Chat` preserves `Instrument` and omits `Chat`.
2. Tombstoning the only active nested child recursively omits the newly empty
   parent container.
3. Nested deletion survives save/reload, is absent from JSON export, and retains
   structurally valid historical fragments.
4. `pits delete-property Activity <Id> What.Chat ...` exits zero and a subsequent
   export omits `What.Chat`.
5. `pits delete-item Object <Id> ...` exits zero and a subsequent export omits
   the item.
6. Typed OsLibCore requests produce the exact command tokens and reject missing
   or malformed mandatory values before execution.

## 5. Release gate

Implementation, focused regression tests, public API documentation, package
release notes, and coordinated v4.2.3 preparation are authorized. RAI retains
the manual decision to start the release chain. CR015 does not authorize tags or
publication by the implementing agent.

## 6. Implementation verification

- Coordinated Release build: passed.
- JsonPit focused tombstone/property suite: 23 tests passed.
- JsonPit complete Release suite: 156 tests passed, including configured
  persistence and remote scenarios.
- PitSeeder Release suite: 23 tests passed.
- OsLibCore Release suite: 110 tests passed.
- All other coordinated package suites passed and all seven 4.2.3 packages were
  packed locally for metadata inspection.
