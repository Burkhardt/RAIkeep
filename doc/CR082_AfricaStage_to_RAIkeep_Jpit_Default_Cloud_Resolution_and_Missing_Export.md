# CR082: jpit default-cloud resolution and missing export sources

**Date:** 2026-11-07  
**Requester:** Dr. Rainer Burkhardt (RAI), following Sipho's AfricaStage WP-5 findings  
**Provider:** Codex, RAIkeep / jsonpit-python  
**Target:** RAIkeep v4.6.3  
**Status:** Accepted for provider implementation at RAI's request; independent consumer CDAT pending  
**Parent:** [CR069_AIA_to_RAIkeep_PitsCommand-Tenant-Scoping-and-Public-Contracts.md](CR069_AIA_to_RAIkeep_PitsCommand-Tenant-Scoping-and-Public-Contracts.md)

## 1. Objective and context

AfricaStage's `docs/active/REPORT_SIPHO_TO_ELIZA_SOLUTION_A_INCREMENT_3_BLOCKERS.md`
§5 reproduces this defect on Python jpit v4.6.2: `list`, `status` and explicitly
targeted `grep` resolve a bare `-r AfricaStage` through configured cloud storage,
but `export Object -r AfricaStage --out-dir <dir>` resolves it locally. A missing
snapshot then exports `[]`, reports success and returns 0. The consumer cannot
distinguish missing input from a valid empty pit.

## 2. Desired behavior and constraints

1. For read commands, a bare `-r` / `--pitroot` / `--root` tenant name uses the
   configured cloud selection when `-c` / `--cloud` is omitted. Explicit provider
   selection remains authoritative. Use `OsConfig.get_cloud_root(None)` for
   single-root operations; preserve `list` discovery's configured cloud-order
   scan and `--all` behavior.
2. Explicit path syntax (`./Tenant`, absolute paths, `~/Tenant`, or paths with
   separators) remains local, including when no cloud configuration exists.
   A bare tenant name never becomes local merely because a same-named directory
   happens to exist in the working directory. Do not silently fall back locally
   when configuration or the selected cloud is unavailable.
3. Audit all root-consuming commands, including WWWA audit and report-only
   maintenance and grep's default-target form. They must honor the supplied root.
4. Before exporting a source, require its canonical `.pit` snapshot to exist.
   Missing snapshots return exit **1**, identify the full canonical path on
   **stderr**, and emit no stdout, JSON, success receipt, or replacement export.
   This applies to `--json`, `--out-dir`, compatibility `--out`, `--jq`, and
   point-in-time export. WWWA export requires all four snapshots and fails before
   output if any is missing. A real empty snapshot remains a successful `[]`.
5. Preserve read-only source handling: no source directories, process flags,
   change files or cloud data are created, rewritten or removed by these reads.
6. Preserve CR069's explicit-destination requirement for writes (`seed` / `put`,
   `set`, deletion aliases, `rename`, and `maintain --apply`). This candidate
   does not authorize implicit cloud selection for mutations. RAI was asked
   separately whether to broaden that policy; pending a ruling, the established
   safeguard remains in effect.

No C# storage-format, mutation-engine or public typed-request changes are needed.

## 3. Consumer acceptance scenarios

- **AC-1:** With disposable configured OneDrive storage and a populated Object
  snapshot, export without `-c` returns the actual cloud entities in directory
  and stdout modes. Cover all three root aliases and timestamp export.
- **AC-2:** Changing `DefaultCloudOrder` changes the default; an explicit `-c`
  selects that provider. An unknown explicit cloud fails without fallback.
- **AC-3:** A local same-named tenant directory containing different data never
  overrides the cloud tenant for reads. Verify list, status, get, history, grep,
  export, audit, and report-only maintenance, including WWWA variants.
- **AC-4:** Explicit local roots and source paths work without cloud configuration.
  Missing configuration/cloud availability never falls back to a bare local name.
- **AC-5:** A missing canonical file, even inside an existing directory, returns
  1 and its full path on stderr. Test tenant, directory and `.pit` path forms,
  all output modes, no stdout, and preservation of existing output files.
- **AC-6:** WWWA missing-member export fails without creating an output directory;
  complete WWWA export and a valid empty single snapshot succeed.
- **AC-7:** Read operations preserve their source snapshots and create no flags.
  Mutations retain CR069's explicit destination gate, including when a local
  directory shares the tenant name.
- **AC-8:** Source CLI, standalone jpit and packaged jsonpit/jpit exhibit the same
  behavior. The jpit companion depends on the matching jsonpit version.

## 4. Delivery gate

Provide a versioned implementation report and local test/package evidence for
AfricaStage/AIA's independent CDAT. Provider verification does not close the CR.
RAI runs Engenho release and provisioning manually after acceptance; this request
does not authorize the provider to execute either operation.
