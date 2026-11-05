# CR070: AIA to RAIkeep — `RAI007` Has No Spelling for a Test-Run Opt-In, and Three Rules Fire on Their Own Subject

> **Document Path:** `doc/CR070_AIA_to_RAIkeep_RAI007-Test-Run-Switches-and-RAI011-RAI015-Subject-Sites.md`
> **Status:** **Submitted / Awaiting Review**
> **Date:** 2026-10-28
> **Origin:** Zébio (`7011`, Lead Systems Engineer), for Dr. Rainer Burkhardt (`RAI`, CPO) & Adele (`7010`, PM AIA Platform)
> **Target Provider / Repo:** `RAIkeep` (`RaiGuard.Analyzer`)
> **Consuming Tenants:** `AIA.Core.Test`, `AIA.Api.Test`
> **Parent Records:** [`CR069`](CR069_AIA_to_RAIkeep_PitsCommand-Tenant-Scoping-and-Public-Contracts.md)

---

## 1. Executive Summary

The solution-wide sweep took RaiGuard from **149 flagged sites to 9**, with **production code at zero**.
CR069 is delivered: `4.5.14` ships `PitsCommandOptions.Tenant` and XML documentation across the
`Pits*` family, so `RAI006` is cleared in `TenantProvisioningService` and in four test tools, and the
`RAI011` false positive on freshly minted items is gone.

The nine that remain are **not** a backlog. They fall into two kinds, and neither is suppressed — per
platform policy the warning stays audible and comes here instead.

| Rule | Sites | Kind |
|---|---|---|
| `RAI007` | 7 | **Rule gap.** No sanctioned spelling exists for the thing the code is doing. |
| `RAI015` | 1 | **Rule fires on its own subject.** The flagged call *is* the hazard under test. |
| `RAI011` | 1 | **Rule fires on its own subject.** The flagged write *is* the regression being pinned. |

Requirement 1 is the substantive ask. Requirements 2–3 ask only for an exemption shape, so that an
audit of these rules is a list of real findings rather than a list that has to be re-triaged by hand
every time.

---

## 2. Requirement 1 — `RAI007` Cannot Express a Test-Run Opt-In

### 2.1 The diagnostic
```text
warning RAI007: 'Environment.GetEnvironmentVariable' bypasses immutable 'Os.Config' runtime
configuration; use 'Os.Config', 'Os.TempDir', 'Os.LocalBackupDir', 'Os.UserHomeDir', or
'WebApplicationFactory.UseSetting' instead
```

### 2.2 Why none of the five alternatives fit
The seven sites all read a switch that **a developer or CI passes to one test run**:

| Site | Switch | What it decides |
|---|---|---|
| `AIA.Core.Test/LiveTenantFactAttribute.cs(49)` | `AIA_LIVE_TENANT_SCAN` | Whether live-tenant tests run at all |
| `AIA.Core.Test/CredentialMintingTool.cs(55,62,64)` | `AIA_MINT_*` | Whether the tool runs, and for which subject/tenant |
| `AIA.Core.Test/LiveWorkbenchBoardTests.cs(60)` | `AIA_BOARD_SUBJECT` | Whose board to read |
| `AIA.Api.Test/ContractSnapshotTests.cs(65)` | `AIA_UPDATE_CONTRACT` | Whether to rewrite the committed OpenAPI snapshot |
| `AIA.Api.Test/StageSpecializationTests.cs(133)` | `AIA_OPENAPI_OUTPUT` | Where to export the contract, if anywhere |

- **`Os.Config` is machine configuration.** It is the right home for a cloud root or a provider
  order — facts about the workstation that outlive any run. A test-run toggle is the opposite:
  per-invocation and disposable. Writing one into `Os.Config` would mean a test mutating machine
  configuration to tell itself what to do, which is worse than reading the environment, not better.
- **`Os.TempDir` / `Os.LocalBackupDir` / `Os.UserHomeDir`** are locations. They answer a different
  question.
- **`WebApplicationFactory.UseSetting` configures a host.** It is exactly right where a host is
  involved — AIA adopted it in this sweep and it cleared **seven** `RAI007` sites in
  `AiaApiFactory`, replacing process-global environment variables with settings scoped to the host
  under construction. But `LiveTenantFactAttribute` runs at xUnit **discovery** time, before any
  host exists, and `CredentialMintingTool` builds no host at all.

So the rule is correct in substance — AIA has no business reading runtime configuration out of the
environment — and simply has no spelling for the one legitimate case: *this run was opted in*.

### 2.3 Requested specification
Either of the following would resolve all seven; the first is preferred because it gives the pattern
a name instead of an exception.

**Option A (preferred) — a sanctioned accessor.** Add to `OsLib`:
```csharp
/// <summary>A switch passed to THIS process by a developer or CI — not runtime configuration.
/// Returns null when unset. Deliberately does not consult Os.Config: a run-scoped toggle must not
/// be able to come from, or leak into, machine configuration.</summary>
public static string? Os.RunSwitch(string name);
```
`RAI007` then recommends `Os.RunSwitch` for a read and keeps recommending `Os.Config` for a write,
which is the distinction the rule is really about.

**Option B — an attribute.** Honour `[RaiGuardRunSwitch]` (or the existing suppression attribute) on
a member, so the exemption is declared in code and greppable, rather than inferred.

**Either way, please keep the diagnostic pointing at the remedy.** `RAI006`'s message in `4.5.14`
now carries the CR069 URL, which is a genuine improvement — a rule that recommends an API should be
able to show a caller how to use it, and that one now does.

---

## 3. Requirements 2 and 3 — Rules That Fire on Their Own Subject

Two sites are tests **of the hazard the rule names**. Obeying the rule at either one would delete the
guard, so both carry a `NOTE` and stay audible.

### 3.1 `RAI015` — `AIA.Core.Test/AiaJsonTests.cs(32)`
```csharp
Assert.Equal(JTokenType.Date, JObject.Parse(Document)["AtUtc"]!.Type);
```
The test's name is `TheDefaultParserTurnsAnIsoStringIntoADate`. The default coercion **is** the
subject; `AiaJson` is the remedy and is asserted in the very next test. Parsing this through
`AiaJson` would assert `AiaJson` against itself and prove nothing.

### 3.2 `RAI011` — `AIA.Core.Test/JsonPitWriteContractTests.cs(95)`
```csharp
var live = _pit["A1"]!;        // 4.5.8: a handle, not a copy
_pit.Add(Delta("A1", new JObject { ["Name"] = "Renamed by someone else" }));
live.ExtendWith(new JObject { ["Status"] = "Doing" });
_pit.Add(live);                // ← RAI011
```
This pins that `pit[id]` returns a **live handle** on `4.5.8+`, so the full-state write no longer
reverts the concurrent rename. It is deliberately written as the flagged pattern, because a future
release that reintroduced snapshot semantics would otherwise bring the data loss back silently.

### 3.3 Requested specification
`RAI011` and `RAI015` are both well-targeted rules and AIA wants them loud. The ask is only an
exemption shape — the attribute from Option B above is sufficient for all three requirements, so a
single mechanism closes this CR.

**A note on `RAI011`'s scope, for the description rather than the detector.** The sweep narrowed two
real engine sites (`ObjectInstantiator.BindFiller` / `UnbindFiller`) to sparse deltas. Worth
recording why the tripwire tests for them assert what they do: with `pit[id]` returning a handle, the
stomp is **not reproducible in-process**, because the read and the write both sit inside the method
and there is no second writer. The defect `RAI011` prevents is about what gets **published** to a
cloud replica. The rule's current wording ("stomps concurrent cloud replica fields") is already
right; a sentence making explicit that this is a *publication* hazard and not an in-process one would
save the next reader the experiment.

---

## 4. Acceptance Criteria

1. `dotnet build AIA.slnx --no-incremental` reports **0 warnings** across all five projects, with no
   `#pragma warning disable` anywhere in the solution.
2. The seven `RAI007` sites express their intent through a named accessor or a declared exemption,
   not through an unexplained `NOTE`.
3. `RAI011` and `RAI015` keep firing everywhere else in the solution — this CR must not widen into a
   blanket exemption for test assemblies.

---

## 5. Current State in AIA (for the reviewer)

| | Before sweep | After |
|---|---|---|
| Flagged sites (unique) | 149 | **9** |
| …in production (`AIA.Core`, `AIA.Api`) | 8 | **0** |
| `#pragma warning disable` for a RAI rule | 0 | **0** |
| Suite | 1,599 green | 1,607 green (+2 WIP ordering, +3 delta tripwires, +6 MediaUrls shapes, 5 stale tests rewritten) |

What was fixed, not worked around: `RAI006` through CR069's `PitsCommand`; `RAI017` by completing
`MediaUrls` so it models every `/img` address the server serves (diagram, two-segment, cache-purge)
rather than only the rendition shapes; `RAI011` by narrowing two engine writes to deltas; `RAI003`
by replacing `System.IO.Path` with `RaiFile`; `RAI012` by dropping `Id` injections that the
`PitItem` constructor had already set; `RAI007` in `AiaApiFactory` by moving seven process-global
environment variables to host-scoped `UseSetting`.

— Zébio (`7011`)
