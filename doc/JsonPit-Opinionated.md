# JsonPit & OsLib: The Opinionated Platform Standard

> **Document Path:** `doc/JsonPit-Opinionated.md`  
> **Status:** Permanent Architectural Invariant & Agent Onboarding Law  
> **Authority:** Dr. Rainer Burkhardt (`RAI`, CPTO) & Adele (`7010`, PM, AIA)  
> **Scope:** Binding across all RAIkeep submodules (`OsLib`, `RaiUtils`, `RaiImage`, `RaiDiagram`, `RaidSeeder`, `JsonPit`, `ImgSeeder`, `PitSeeder`)

---

## 1. Mandatory Dogfooding: Zero Raw System.IO

**Amafu is the sole, isolated exception across the platform.**  
Amafu is permitted to touch BCL `System.IO` primitives solely because it is a standalone, zero-dependency NativeAOT bootstrap utility intended to run on unconfigured machines.

**Everywhere else in RAIkeep, direct calls to `System.IO.File`, `System.IO.Directory`, and `System.IO.Path` are STRICTLY FORBIDDEN.**

- All directory paths are strongly typed as `RaiPath` (absolute) or `RaiRelPath` (relative).
- All files are strongly typed as `RaiFile`, `CanonicalFile`, `PitFile`, or `TextFile`.
- Any PR or agent commit introducing direct BCL `System.IO` calls in product code will be rejected.

---

## 2. Pit File Representation: Never Hand-Roll Names or Extensions

In the JsonPit persistence model:
1. **Never String-Concatenate Names or Extensions:**
   - NEVER write `"{name}.pit"`, `name + ".pit"`, or `Path.Combine(..., $"{name}.pit")`.
2. **Always Use `PitFile`:**
   - Every Pit on disk is represented by the typed `PitFile` class (from `JsonPit`):
     ```csharp
     var pitFile = new PitFile(pitFolder, pitName);
     ```
   - `PitFile` inherits from `CanonicalFile`, which automatically enforces the canonical directory-by-name convention (`pitFolder / pitName / pitName.pit`) and the `.pit` extension.
3. **Checking Pit Existence:**
   ```csharp
   if (pitFile.Exists())
   {
       // Pit exists on disk
   }
   ```
4. **Inspecting Pit Metadata (Long Listings, Diagnostics):**
   ```csharp
   long bytes = pitFile.Length;             // Physical file size
   DateTimeOffset updated = pitFile.LastWriteTimeUtc; // UTC timestamp
   string path = pitFile.FullName;          // Canonical absolute path
   ```

---

## 3. Path Composition Law: Operator `/` Exclusively

- **There is no such thing as "Path Combination".** Never use or simulate `Path.Combine`.
- Paths are composed strictly using the division operator `/` on `RaiPath`:
  ```csharp
  var tenantDir = cloudRoot / tenant;
  var pitDir    = tenantDir / pitName;
  var pitFile   = new PitFile(pitDir, pitName);
  ```

---

## 4. Directory Traversal via `RaiPath`

To discover pits or subdirectories under a root:
- Never use `Directory.EnumerateDirectories` or `Directory.EnumerateFiles`.
- Use `RaiPath`'s own typed traversal methods:
  ```csharp
  foreach (var dir in root.EnumerateDirectories("*"))
  {
      var pitFile = new PitFile(dir, dir.Name);
      if (pitFile.Exists())
      {
          names.Add(dir.Name);
      }
  }
  ```

---

## 5. The Cloud Storage In-Place Invariant (CR022)

Established cloud pathnames represent durable synchronization identities:
1. **Never Create in Temp and Move to Cloud:**  
   Never create a file in `Os.TempDir` and move, swap, or rename it into a cloud directory.
2. **Never Stage-and-Replace:**  
   Temporary file stage-and-replace patterns cause cloud sync engines (OneDrive, Dropbox, Google Drive) to spawn duplicated conflict copies (e.g. `File (1).pit`).
3. **Continuous In-Place Presence:**  
   Update cloud files in place at their final established pathname.

---

## 6. The JsonPit Mutation Contract (AGENTS.md & CR040)

1. **No Read-Modify-Write:**  
   JsonPit is an append-only, sparse-attribute change stream. Never read a full record into memory to mutate and write the entire object back.
2. **Sparse Deltas Only:**  
   Append strictly the modified attribute using `new PitItem(id)`.
3. **Deletion is an Audited Lifecycle Event:**  
   Never simulate deletions with payload flags (`Deleted = true`). Use `pit.Delete(id, by)` or the CLI `pits delete-item`.
