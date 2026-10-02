# JsonPit live references — investigation and implementation plan

Status: implemented and verified for the next coordinated release, 4.4.8. The original-object reference test passes unchanged. Rainer approved the two runtime modes described below; each instance captures the process default for its lifetime in memory only. Release-mode verification passed all 225 non-remote JsonPit tests, both remote SSH/cloud tests, and all 84 PitSeeder tests. The local builds used current project sources; the SSH sync scenario used Mzansi's installed pits v4.4.1. Changes remain in the working tree; no release has been published.

## Required behavior

JsonPit continues to store sparse fragments. Assigning or adding an attribute to a live item appends the corresponding fragment; deleting an attribute appends a null tombstone. Returning a live reference must not turn an edit into a full-object replacement in history.

For a new ID, `pit.Add(item)` must adopt that exact `PitItem` as the live item, including its existing nested objects. `pit[id]` must return `item` itself. The `PitItem` indexer must return the original nested node. Repeated lookups retain these identities while the item and nodes remain live. References held before Add and references obtained through either indexer address the same objects. Historical reads remain detached snapshots.

The agreed minimal reference test uses the following setup and assertions (see `JsonPit/JsonPit.Tests/ReferenceTests.cs` for the complete test):

```csharp
var who = new JObject { ["Owner"] = "Unknown" };
var item = new PitItem("Ego") { ["Who"] = who };
pit.Add(item);

var ego = pit["Ego"];
Assert.Same(item, ego);
Assert.Same(who, ego["Who"]);

ego["Instagram"] = "@Dr2RAI";
ego["Who"]["Owner"] = "Rainer";

Assert.Equal("@Dr2RAI", (string)item["Instagram"]);
Assert.Equal("Rainer", (string)who["Owner"]);
Assert.Same(ego, pit["Ego"]);
Assert.Same(who, pit["Ego"]["Who"]);
```

This test deliberately establishes only reference identity and mutation visibility. Additional tests must establish the sparse-history contract: the nested edit produces a fragment containing the entity identity and `Who.Owner`, plus engine metadata, without copying unrelated attributes. The earlier fragment must still contain `Owner = "Unknown"`. Existing Save and explicit Dispose durability behavior remains; assignment itself does not perform filesystem I/O.

## Baseline behavior before this implementation

1. `Pit.this[string]` in `JsonPit/JsonPit.cs:79` calls `PitItems.ProjectState()` on every lookup.
2. `ProjectState()` in `JsonPit/PitItems.cs:96` folds retained sparse history into a new `JObject`, using `ApplyProjectedProperty()` to combine objects and remove tombstoned properties. It returns `new PitItem(accumulator)`.
3. `PitItem(JObject)` in `JsonPit/PitItem.cs:298` deep-clones its input again. `PitItem` is a class derived from `JObject`: it is already a C# reference type. The returned reference points to a newly reconstructed object, not a Pit-owned live object.
4. The second indexer is inherited from `JObject`. It edits that newly reconstructed object. There is no owner connection that turns the edit into a sparse history append. Plain indexer assignment also bypasses `PitItem.Invalidate()`.

The copies isolate history during projection. The architectural gap is that the current indexer exposes that projection directly instead of exposing a persistent live item. Removing `DeepClone()` alone does not supply the missing live item or mutation protocol.

Returning `LatestFragment()` would also be incorrect: a latest fragment may contain only one changed attribute and cannot represent the complete current item.

There is a separate storage ownership issue: `AddCore()` → `PitItems.Push()` currently retains the supplied mutable `PitItem` as a historical fragment. An immutable list does not make its elements immutable. The supplied object must instead become the live item, with an independent snapshot stored in history. Copy at the history boundary; preserve the original objects at the live-access boundary.

## Verified result and what it establishes

Before implementation, the simplified test compiled and failed at `ReferenceTests.cs:25`, `Assert.Same(item, ego)`, with “Values are not the same instance.” After implementation it passes unchanged, including the nested-reference and subsequent-lookup assertions. Separate tests cover tracking, persistence, and history rather than expanding the minimal identity test.

The test now uses a mutable `PitItem` and a mutable `JObject`, with no anonymous-object import or unrelated entity. Its requirements are:

- Preserve the identity of the object supplied to Add, not just identity between two later lookups.
- Preserve the identity of the nested object supplied before Add.
- Make edits through the retrieved references visible through the original references.
- Continue returning those original objects after the edits.

Keep this test small and unchanged while implementing. Add separate tests for history and lifecycle behavior. Replacing its original-object assertions with equality checks or assertions against newly created proxies would weaken the agreed contract.

A C# indexer assignment invokes its setter. It does not require a C# `ref` return. Retrieving a nested object should return that same live node, but replacing a property value does not retarget a previously captured reference to the old value. This is ordinary reference behavior.

## Architecture to implement

### Where the current value is established

The ordered history fold belongs at the accepted state-change boundary: initial loading, accepted live fragment insertion, historical replay/merge, and reload. It updates the already registered live object in place. Neither `Pit.this[string]` nor `PitItem`'s indexer should reconstruct current state during ordinary access. For persisted data, construct the live graph as part of loading; current lookups then only resolve the registered reference.

Use the existing deterministic fragment ordering, including equal-timestamp tie-breaks. A LINQ pipeline can select the applicable history interval, stop at the entity-deletion boundary, reverse the descending history into application order, and fold its properties using `Aggregate`. The recursive property application still implements tombstones, nested object merging, and array replacement. Do not replace this with grouping only by top-level property name: an older fragment may contribute a nested sibling that a newer fragment omits. LINQ improves the expression of the fold; measure allocations and execution cost rather than assuming it is faster than a loop. Avoid sorting already ordered history again or refolding on reads.

Maintain two distinct structures inside the Pit:

- A registry of live items keyed using the Pit's existing ID comparison rules. For new items, it holds the original supplied object, not a substitute projection or wrapper. Each live item and nested mutable node has an owner/path association without replacing the node. Current access returns the registered object.
- The existing history of owned sparse fragments. These retain accepted values independently of the live graph. Historical projection continues to read this history.

A supported edit follows this sequence: identify owner and path → validate the operation → construct the minimal fragment → accept it through the existing history/concurrency boundary → reflect the accepted result in the live graph. A rejected edit must not leave the graph changed. Internal graph refreshes must not generate new fragments.

`Add` of a new entity adopts the caller-supplied item and its nested graph, and stores an independent historical snapshot. This is now a requirement, not an open design choice. `Add` of another sparse fragment for an existing ID must preserve the established live identity and apply the accepted changes to it. The later fragment is mutation input, not a replacement live root. Data first loaded from disk has no caller-supplied identity; materialize it once, then preserve that live identity.

Tracking must also work through original aliases such as `item["Instagram"] = ...` and `who["Owner"] = ...` after attachment. Intercepting only access through `pit[id]` is insufficient. Resolve attachment ownership before implementation for an object already attached to another Pit, re-adding the live object itself, and concurrent first Add calls for the same ID; these cases must not silently replace an established identity or create multiple owners.

Retained references must survive ordinary updates and merges. Preserve nested node identity for in-place edits and changes to siblings. Explicit subtree replacement, deletion, entity deletion/recreation, rename, and disposal need documented invalidation rules. Recommended rule: detached or obsolete nodes cannot silently write into a different/new entity lifetime.

## Newtonsoft constraint and compatibility decision

JsonPit currently inherits a large mutable API from `JObject`. Supporting only `PitItem.SetProperty()` does not cover the requested nested indexers, `Add`, `Remove`, arrays, or edits through a `JObject`-typed reference.

Newtonsoft.Json 13.0.4's string indexer is non-virtual; its object indexer is virtual. Hiding the string indexer alone leaves paths through base types and interfaces. Container mutation hooks such as `InsertItem` and `SetItem` are internal. Property/collection notifications can observe many operations, but direct `JValue.Value` assignment provides no such notification. These facts are visible in the upstream [JObject source](https://github.com/JamesNK/Newtonsoft.Json/blob/13.0.4/Src/Newtonsoft.Json/Linq/JObject.cs), [JContainer source](https://github.com/JamesNK/Newtonsoft.Json/blob/13.0.4/Src/Newtonsoft.Json/Linq/JContainer.cs), and [JValue source](https://github.com/JamesNK/Newtonsoft.Json/blob/13.0.4/Src/Newtonsoft.Json/Linq/JValue.cs).

First implement a small compatibility prototype, outside production code, using the exact existing `PitItem` and plain nested `JObject` from the test. Attach tracking without replacing either instance. Cover edits through the original variables and retrieved references, nested indexer assignment, inherited `Add`/`Remove`, cast-to-JObject access, notification reentrancy, and failed-operation rollback. A cache alone supplies shared memory but does not ensure that every edit creates a fragment.

Replacing supplied nodes with library-controlled wrappers would violate the new `Assert.Same` contract, so it is not an interchangeable implementation option. Prove the requested indexer operations with the original objects first. If notification limitations prevent some additional inherited operations from being tracked reliably, report the exact unsupported operations and discuss the API tradeoff before proceeding. Do not claim unrestricted tracking from a single event subscription or hidden indexer. Post-change notifications also require an explicit strategy for validation, rollback, and serialization with concurrent mutation; they do not automatically implement the acceptance sequence above.

### Prototype result and ratified runtime modes

A temporary console prototype ran against the installed Newtonsoft.Json 13.0.4 assembly. Indexer insertion, indexer replacement, property removal, and null assignment each raised a collection notification. Updating existing metadata, restoring a removed property, and pruning a null property from the notification handler succeeded in these single-observer cases. This demonstrates useful interception points; it does not yet establish correctness with additional subscribers, concurrent writers, or the full JsonPit persistence path.

Direct `((JValue)root["Name"]).Value = "after"` changed the value but raised **zero** notifications. Rainer selected a configurable policy:

- `MutationTrackingMode.TrackedChangesOnly`: track supported operations immediately, with no fallback comparison passes. Server applications select it before constructing Pits and must use the tracked APIs.
- `MutationTrackingMode.TrackedChangesWithFallback`: the default. Also compare live values with their last accepted baseline at Save and other relevant boundaries. Unreported edits will receive their history timestamp when detected. Intermediate states may be coalesced and detection order may differ from actual edit order.

`Pit.DefaultMutationTrackingMode` sets the default for new instances. `pit.TrackingMode` is fixed for that instance's in-memory lifetime. The mode is never persisted; server and CLI processes may open the same data with different modes. Both modes retain the original objects and the existing sparse-fragment format. Normal application and agent-generated code uses the tracked path even when fallback is enabled.

Implementation documentation is in `JsonPit/MUTATION_TRACKING.md`, linked from README, GettingStarted, and AGENTS.md, with the same detection-time limitation in the enum XML comments. Root notification processing runs after external collection subscribers have returned; nested property notifications handle indexer edits before collection reentrancy restrictions apply.

## Method-by-method work inventory

“Change” identifies required work for the shared-live-object design. “Review” identifies methods that must retain their contract and may need implementation edits depending on the chosen JSON node representation. Methods on the same row share the stated work.

### JsonPit/JsonPit.cs

| Methods / members | Work |
| --- | --- |
| `this[string]` | Change: return the exact adopted item for caller-created entities; materialize loaded entities once. No projection or clone on ordinary lookup. Preserve missing/deleted lookup behavior. |
| `Get(string, bool)`, `AllUndeleted()` | Change: use the same live identity for current living items. Keep returned tombstones detached. Review the existing `JObject` return types. |
| `GetAt()` | Review: always return a detached historical snapshot; never enroll it in live tracking. |
| `Add(PitItem)`, `AddCore()` | Change: adopt the exact supplied item and existing child nodes for a new ID; snapshot its values independently for history. For later sparse additions, update the existing live graph without replacing it. Coordinate attachment, append, and live updates; preserve CAS ordering and live ID checks. |
| `Add(string)`, both `AddItems(...)`, `PitItem` setter, `ItemProperty` setter, `NormalizeIdentityPayload()` | Review/change integration: converge on the same insertion/refresh path, preserve batch preflight, and distinguish importing values from attaching live objects. |
| New internal mutation dispatcher and live-item registry helpers | Add: validate owner/path, build sparse fragment, commit once per logical operation, suppress feedback during refresh, handle no-ops and failed edits. Names to be chosen during implementation. |
| `Delete()`, `RenameId()` | Change: update/invalidate live identities and nested handles consistently with item lifecycle; preserve legacy-ID deletion support. |
| `AddHistorical()`, `MergeIntoHistory()` | Change: replay fragments without restamping, then reconcile any materialized live item; refresh must not create another write. |
| `Load()`, `Reload()` | Change: reconcile the accepted history snapshot with live identities rather than leave held references stale when replacing `HistoricItems`. |
| `ParseHistoricItems()`, both `initValues(...)`, all `Pit(...)` constructors | Review/change ownership: loaded fragments are detached; initialize registry and identity/lifetime state; preserve timestamp and clean/dirty semantics. |
| `ConsiderCase()`, `IgnoreCase()` | Change: keep live registry comparison and history lookup rules consistent. |
| `HistoricItems` public field; generic and non-generic `GetEnumerator()` | Compatibility decision in this implementation: retain the dictionary type; explicitly document direct writes as engine-level, unsupported application mutations. Historical payload access returns detached snapshots. A future breaking API revision can remove the mutable dictionary surface; do not silently turn existing dictionary assignments into discarded writes. |
| `ValuesOverTime()`, `ValueListsOverTime()` | Change: do not expose mutable tokens owned by historical fragments. Return detached values. |
| `AllUndeletedDynamic()` | Review: currently constructs independent Expandos. Define it as explicit exported values or provide live dynamic access; do not imply reference semantics for its current result. |
| Both `ExportJson(...)` | Review: export detached values, avoiding adoption/reparenting of live tokens and serialization of owner state. |
| `Contains()`, `ContainsKey()`, `Keys` | Review: preserve existing historical-presence vs living-presence distinctions. |
| `Invalid()`, `GetLatestItemChanged()`, `GetMemChanged()` | Review: accepted live edits must be represented by dirty, timestamped fragments; reading/materializing live items must not mark the Pit changed. |
| `EqualsIgnoringModified()`, `NextLiveMutationTimestamp()` | Review: keep deterministic timestamps and replay behavior; compare live edit effects against current state for no-op detection, rather than accidentally comparing a whole item with one sparse fragment. |
| `Store()`, `Save()`, `ReadCanonicalSnapshot()`, `CreateChangeFiles()`, `CreateChangeFile()`, `CompareToOtherHistory()` | Review/change integration: preserve snapshot isolation, serialization of fragments, and validation of exactly the stored fragments. No persistence of live owner links. |
| `RecordInRecoveryWriteSet()`, `RecoveryWriteSetKey()`, `SnapshotRecoveryUnion()`, `PublishFragmentsAsChangeFiles()` | Review/change ownership: recovery must retain stable accepted fragments, never mutable live views. |
| `ApplyMaintenanceUnderGate()` | Review: route history reconciliation through the same live refresh boundary. Inspection-only maintenance remains read-only. |
| `Dispose()`, `Dispose(bool)` | Change: terminate live mutation access consistently with shutdown and preserve existing durability handling. Avoid owner/handler lifetime leaks. |

### JsonPit/PitItem.cs

| Methods / members | Work |
| --- | --- |
| Class/base type and inherited indexers | Change/design: distinguish detached fragment construction from an attached live item; implement the approved tracked mutation surface, including nested access. |
| New owner/path/attachment and internal refresh helpers | Add: attach tracking to the original nodes, including edits through pre-existing aliases; dispatch sparse edits, suppress dispatch for engine updates, detach invalid handles. Do not replace nodes or serialize tracking state. |
| `SetProperty(string)`, `SetProperty(object)`, `Extend(string)`, both `ExtendWith(...)`, `Merge(JObject)` | Change: live mode submits one logical sparse mutation; detached mode remains usable for fragment construction. Avoid recursive/double dispatch. |
| `DeleteProperty()`, `DeletePropertyPath()` | Change: live mode submits a tombstone immediately and updates the live view; retain literal-name vs explicit dot-path distinction. |
| `Delete()` | Change: attached mode delegates item deletion to its owner; detached mode builds the existing engine tombstone. |
| `Id`, `Modified`, `Deleted`, `Note` | Change/review: prevent direct live identity/lifecycle bypasses, permit engine-managed updates, and track ordinary Note edits. |
| `ValidateClientPayload()`, `EnsureValidForLiveAdd()`, `ValidateLiveId()`, `ValidatePropertyMutationPayload()`, `ThrowIfProtectedTombstone()`, `ParsePropertyPath()` | Review/refactor for reuse: all new live paths use existing validation; enforce protected attributes before committing. |
| `Valid()`, `Validate()`, both `Invalidate(...)` | Change/review: fragment dirty state belongs to accepted history; internal timestamp/refresh changes must not recursively emit edits. |
| All constructors, especially `PitItem(PitItem, ...)`, `PitItem(JObject)`, private JSON constructor; `CreateEngineMutationCopy()` | Change/review: separate live attachment from detached copy/import; copy operations must not inherit ownership. Provide an internal fragment-snapshot operation preserving timestamp, dirty state, and provenance. |
| `ToString()`, `Equals(PitItem)`, `Equals(object)`, `GetHashCode()` | Review: serialize data only; preserve/document content equality separately from reference identity. Do not key owner/handler registries by mutable content hashes. |
| Inherited `Add`, `Remove`, `RemoveAll`, `Replace`, merge overloads, dictionary access, dynamic access, `JProperty.Value`, nested `JObject`/`JArray` operations, `JValue.Value` | Explicit compatibility inventory: each path must be tracked, deliberately detached, or documented as unsupported under the agreed public model. These are not all overridable in Newtonsoft. |

### JsonPit/PitItems.cs and adjacent callers

| Methods / members | Work |
| --- | --- |
| `Push()`, both `PitItems(...)` constructors | Change: protect historical payload ownership. Use an internal trusted path to avoid cloning every existing fragment on every append. Preserve clean/dirty metadata and deterministic ordering. |
| `History`, `Items`, `GetEnumerator()`, `ItemsBase.Key` | Change/review public exposure: external callers must not mutate internal historical payloads or bypass item identity bookkeeping. |
| `ProjectState()`, `ApplyProjectedProperty()` | Retain detached historical projection semantics. Remove their per-lookup use from current access. Extract/reuse folding logic for live reconciliation without replacing adopted roots or nested objects during in-place updates. |
| `Peek()`, `Get()` | Review/document as historical container projections; current live identity should be supplied by the owning Pit. |
| `LatestFragment()`, `CompareFragments()`, `FindProjectionStartIndex()` | Retain internal history behavior; no returning a latest fragment as the live entity. |
| `ChangeFile.CanonicalPayloadFor()` and change-file parsing/serialization | Regression verification: persisted format, canonical hashes, and sparse payloads remain compatible. |
| `PitSeeder/pits/Program.cs`: `RunDeleteMutation()`, `RunDeletePropertyCommand()`, `RunDeleteItemCommand()` | Once core works, simplify the property-deletion branch to call the live API or an optional Pit-level convenience API. Preserve CLI behavior and validation. |
| `JsonPit/GettingStarted.md`, public API documentation and examples | Explain live objects, explicit detached snapshots, sparse appends, and Save. Make live deletion the primary example; keep explicit fragment construction as the lower-level option. |

Unrelated archive/image processing, event filenames, and release publication are outside this plan. Other persistence helpers need changes only if the internal historical-store type changes; review every `HistoricItems`/`History` access when implementing that encapsulation.

## Implementation sequence and tests

1. Keep the agreed minimal test as the failing reference specification. Original item and nested-node identity are settled requirements. Resolve only the additional attachment/lifecycle cases that it does not cover.
2. Prototype tracking on the exact supplied objects. Prove the requested indexer operations and edits through original aliases; assess additional inherited operations and report concrete limitations. No replacement proxies to make the identity requirement disappear.
3. Implement fragment ownership and a single sparse-mutation acceptance path together with live attachment. Preserve existing timestamp, validation, tombstone, concurrency, and recovery contracts. Do not ship a partial change that returns raw stored-history objects just to make the test pass.
4. Make the minimal test pass through adoption of the original live graph. Add separate history assertions: the initial fragment retains `Owner = "Unknown"`, each edit produces only its intended delta, and all original/retrieved aliases remain coherent. No extra writes on reads or internal refreshes.
5. Reconcile Add/load/merge/reload/delete/rename with held references. Document subtree replacement and stale-handle behavior. Ensure rejected changes leave both live state and history untouched.
6. Integrate persistence and update documentation/CLI examples only after the new behavior is verified.

Required regression coverage: direct assignment through both original and retrieved references; `Add` for new and existing IDs; top-level and nested deletion; nested object and array edits; two aliases observing the same update; no-op edits; no unrelated properties or empty Note leaking into fragments; detached imports/copies/time-travel results; earlier history unchanged; save/reopen; foreign-fragment merge; concurrent independent edits and first-add races; Save during edits; callback reentrancy; ID comparison; protected attributes; attachment to multiple Pits; disposal; and obsolete node references.

`ReadOnly` currently blocks Save/Store but does not universally forbid in-memory Add. Preserve or explicitly revise that contract; do not infer it from Python's binding condition. Test mutable read-only in-memory use separately from durable writable use.

Python 4.4.7 already projects and then calls `bind()` in `jsonpit/store.py:get()`. Its `item.py` indexer/set/delete helpers append deltas. It does not establish a shared identity per lookup, and returning an ordinary nested dictionary does not automatically dispatch nested edits. Use its sparse-delta tests as parity evidence for fragment contents, not as proof of the stronger live-reference contract requested here. Coordinate the final public behavior with the Python maintainer for 4.4.8.

## Follow-up: four baseline test failures

Rainer explicitly authorized investigating and repairing these tests during implementation. All four failures were reproduced against the unchanged JsonPit HEAD in a temporary baseline checkout. Released commit `b4ddfc6` introduced four-character change-file checksums; OsLib commit `a6a144d` introduced clean event names. These tests retained older assumptions. No production filename or persistence format was changed to satisfy them.

| Original test | Assessment and correction |
| --- | --- |
| `CreateChangeFile_WritesCanonicalPitUnderChangesDirectory` | Still valuable; its name and unhashed filename assertion were stale. Renamed to describe the existing placement beside the canonical pit. Now checks location, four-character checksum, exact canonical bytes, successful validation, and fragment values. |
| `LiveLoser_WatcherDetectsConflict_PublishesWriteSet_RetiresOnlyItsLongerFlag` | Still essential recovery coverage. Kept recovery and authority assertions; changed event filename checks to the released hash-free names and checked their JSON stages too. |
| `LegacyDottedRecoveryEvent_IsInventoriedThenRepairedOnlyWhenAuthorized` | Still valuable migration coverage. Construct the actual old hashed, extensionless fixture explicitly; using today's EventFile cannot manufacture that historical format. Kept report-only and authorized repair assertions. |
| `DistinctEqualTimestampFragments_WithSameIdentity_FailFastInsteadOfOverwriting` | The no-overwrite guarantee remains essential, but equal timestamps alone no longer imply a filename collision. Replaced with coexistence/idempotence coverage for different checksums, plus a deterministic test generating a real four-character checksum collision and verifying rejection with byte-for-byte preservation of the existing file. |

## Remote verification — 2026-10-02

At Rainer's request, both separate remote integration tests were run through SSH to Mzansi and real OneDrive propagation. Both passed, with no skips, in 3.06 minutes:

- `TwoServerSplitMaster_LiveLocalLoser_RecoversThroughProviderSyncedConflictSignal`: the local claimant recovered its saved and dirty fragments, retired its conflict flag, preserved the remote winner's authority, and emitted the required audit events. Its event assertions received the same hash-free filename correction as the local recovery test, with JSON-stage checks retained.
- `RemoteSync_MasterClient_FullScenario`: all six phases passed, covering creation, remote client writes, local merge, master transfer, return synchronization, receipt-based cleanup, and preservation of all three entries.

The local library was built from this working tree. Mzansi's installed `/usr/local/bin/pits` reported v4.4.1; it was not replaced. This demonstrates interoperability with that deployed peer, not a current-build-on-both-machines test. Run evidence: `/tmp/raikeep-live-remote.log` and `/tmp/raikeep-live-remote-results/remote.trx`.
