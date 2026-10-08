# CR058: AIA to RAIkeep — Conditional WWWA Help Screen Parity in pits and jpit

> **Naming Schema:** `CR058_AIA_to_RAIkeep_Conditional-WWWA-Help-Screen-Parity-in-pits-and-jpit.md`  
> **Originating Request:** Dr. Rainer Burkhardt (`RAI`, Chief Product & Technology Officer)  
> **Consuming / Requesting PM:** Adele (`7010`, Product Manager, AIA Platform)  
> **Target Provider / Repo:** RAIkeep (`PitSeeder/pits`, `JsonPit.Python/jsonpit`, `scripts/validate-release.py`)  
> **Predecessor Releases:** `RAIkeep v4.5.5` (CR057 Pillars 1–3 completed)  
> **Date:** 2026-10-08  
> **Status:** **Ratified Platform Mandate — Authorized for Implementation**  
> **Target Release:** `RAIkeep v4.5.6`  

---

## 1. Objective & Context

### 1.1 Domain Leak in General-Purpose Storage Tooling
`pits` and `jpit` are foundational, domain-neutral storage CLIs designed to manage daemon-free distributed storage across cloud drives for any application or tenant. 

However, in C# `pits` (`PitSeeder/pits/Program.cs`), the main help screen unconditionally prints status lines for the 4 WWWA Quartet pits:
```text
  Person      ✗  Person.pit
  Object      ✗  Object.pit
  Place       ✗  Place.pit
  Activity    ✗  Activity.pit
```
When a developer or AI agent uses `pits` for generic development (e.g. creating a `Weather` tenant with `DailyHeat.pit`, or building general-purpose applications), invoking `pits -h` or `pits -h -r Weather` suddenly displays WWWA-specific entities. This is a confusing domain leak that undermines the domain-neutrality of the storage platform.

### 1.2 CLI Asymmetry Between C# and Python
Inspection of Python `jpit` (`jsonpit/cli.py`) reveals that `jpit -h` was already cleaned up to omit these hardcoded lines, creating an asymmetric experience between the two sibling CLIs:
- `jpit -h` presents a clean, generic list of subcommands and options.
- `pits -h` appends 4 hardcoded WWWA pit status lines at the bottom.

Both CLIs must behave identically, providing a clean help screen by default while making WWWA quartet discovery available when relevant.

---

## 2. Desired Behavior & Constraints

### 2.1 The Conditional Display Law
The 4 WWWA status lines (`Person`, `Object`, `Place`, `Activity`) MUST be displayed in the help screen **if and only if**:
1. **Explicit Flag:** The caller explicitly passes `--wwwa` (e.g. `pits -h --wwwa` or `jpit -h --wwwa`), **OR**
2. **Contextual Discovery:** The resolved target pit root (`-r <root>`) actually contains at least one existing WWWA pit (`Person.pit`, `Object.pit`, `Place.pit`, or `Activity.pit`).

In all other cases:
- Bare `pits -h` / `jpit -h`
- Non-WWWA roots (e.g. `pits -h -r Weather` or `jpit -h -r Weather`)
the WWWA status section MUST be completely omitted, presenting a clean, domain-neutral command reference.

### 2.2 Complete Cross-CLI Parity
1. **Generic Help Parity:**
   `pits -h` and `jpit -h` must output the same command verbs, options, and zero WWWA pit status lines.
2. **WWWA Help Parity:**
   When `--wwwa` is present (`pits -h --wwwa` and `jpit -h --wwwa`), both CLIs must display the 4 WWWA pits with identical formatting, glyph icons, and path resolution status.

### 2.3 Strict Dogfooding Invariant
All C# modifications to `PitSeeder/pits/Program.cs` must strictly obey `doc/JsonPit-Opinionated.md`:
- Pit existence must be evaluated via typed `Pit` constructors (`new Pit(..., readOnly: true, unflagged: true)`).
- Paths must use typed `RaiPath` / `RaiRelPath` with operator `/`.
- Zero raw `System.IO` primitives.

---

## 3. Suggested Acceptance Tests

1. **Default Help Screen Cleanliness:**
   - Run `pits -h -n` and `jpit -h -n`.
   - Assert neither output contains `"Person.pit"`, `"Object.pit"`, `"Place.pit"`, or `"Activity.pit"`.

2. **Non-WWWA Tenant Isolation:**
   - In a directory or cloud root without WWWA pits (e.g. `-r Weather`):
   - Run `pits -h -r Weather` and `jpit -h -r Weather`.
   - Assert WWWA status lines are omitted.

3. **Explicit `--wwwa` Flag Activation:**
   - Run `pits -h --wwwa` and `jpit -h --wwwa`.
   - Assert both CLIs display the status and resolved paths of `Person`, `Object`, `Place`, and `Activity`.

4. **Contextual WWWA Discovery:**
   - Point `-r` to a directory containing `Person.pit` (e.g. `-r AIA`):
   - Run `pits -h -r AIA` and `jpit -h -r AIA`.
   - Assert both CLIs detect the presence of the WWWA pit and display the 4-pit quartet status block.

5. **Release Validation Gate:**
   - Run `python3 scripts/validate-release.py`.
   - Assert parity checks pass cleanly with 0 failures.
