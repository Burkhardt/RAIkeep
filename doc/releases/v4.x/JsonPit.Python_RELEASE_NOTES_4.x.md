# jsonpit-python Release Notes 4.x

## 4.6.3

- Release version: `4.6.3`
- Coordination tag: `v4.6.3`

### Highlights
- CR082: Python jpit resolves bare export/WWWA roots through the configured default cloud and reports missing export snapshots with exit 1, empty stdout and unchanged destinations. Independent AfricaStage/AIA CDAT accepted; preserve CR069 explicit write destinations.

### Coordinated Dependencies
- Aligned with RAIkeep synchronized `4.6.3` line.

---

## 4.6.2

- Release version: `4.6.2`
- Coordination tag: `v4.6.2`

### Highlights
- CR081: jpit seed/put report actual per-entry dispositions after Save and context exit. Match C# latest-fragment deduplication before timestamping; report failed owned-window cleanup instead of silently succeeding. Do not suppress based on projected-state equality.

### Coordinated Dependencies
- Aligned with RAIkeep synchronized `4.6.2` line.

---

## 4.6.1

- Release version: `4.6.1`
- Coordination tag: `v4.6.1`

### Highlights
- Synchronize package and dependency versions to 4.6.1 for CR070. The new process run-switch API and declared rule-subject exemptions are delivered by OsLibCore and RaiGuard; this component retains its existing behavior.

### Coordinated Dependencies
- Aligned with RAIkeep synchronized `4.6.1` line.

---

## 4.6.0

- Release version: `4.6.0`
- Coordination tag: `v4.6.0`

### Highlights
- Make add(live_handle) flush pending changes without replaying the full live projection. Reject detached PitItem copies at client write boundaries and accept matching Id assertions consistently with C#. Validate JSON-array patches before accepting any row and append one combined sparse mutation. Add the instance merge alias and guard live lifecycle property setters in both tracking modes. Keep Vikela entirely optional.

### Coordinated Dependencies
- Aligned with RAIkeep synchronized `4.6.0` line.

---

## 4.5.18

- Release version: `4.5.18`
- Coordination tag: `v4.5.18`

### Highlights
- Show the executing machine as "on <machine>" in the CLI banner. Size both decorative rules to the complete heading, including the hostname; preserve bold cyan styling and plain redirected output. Apply it to both jsonpit and jpit entry points and the standalone artifact.

### Coordinated Dependencies
- Aligned with RAIkeep synchronized `4.5.18` line.

---

## 4.5.17

- Release version: `4.5.17`
- Coordination tag: `v4.5.17`

### Highlights
- Align package versions, dependencies, and documentation with the coordinated 4.5.17 release. No package-specific behavior change.

### Coordinated Dependencies
- Aligned with RAIkeep synchronized `4.5.17` line.

---

## 4.5.16

- Release version: `4.5.16`
- Coordination tag: `v4.5.16`

### Highlights
- Coordinated dependency and documentation alignment; no package-local behavior change.

### Coordinated Dependencies
- Aligned with RAIkeep synchronized `4.5.16` line.

---

## 4.5.15

- Release version: `4.5.15`
- Coordination tag: `v4.5.15`

### Highlights
- Match the approved pits help theme, including provider badge colors, required/optional notation, italic values, bold headings, and plain redirected output.
- Expose -w/--window and -x/--id-exists, retain compatibility spellings internally, and align shared root/debug options and contextual list/ls help.
- Add pits-compatible --out-dir exports, WWWA resolved-reference projection, and offset-explicit historical export envelopes. Preserve unadvertised --out file compatibility.
- Rebuild standalone jpit with the current sources and coordinate both jsonpit and jpit distributions at the same version.

### Coordinated Dependencies
- Aligned with RAIkeep synchronized `4.5.15` line.

---

## 4.5.14

- Release version: `4.5.14`
- Coordination tag: `v4.5.14`

### Highlights
- Validate and build both jsonpit and jpit distributions, pin the companion to the matching core version, and verify both installed CLI names.
- Refresh and validate the standalone executable and current documentation in the coordinated version bump.
- Publish both distributions and create the Python GitHub Release through the release chain; use one managed environment for both installer commands.

### Coordinated Dependencies
- Aligned with RAIkeep synchronized `4.5.14` line.

---

## 4.5.13

- Release version: `4.5.13`
- Coordination tag: `v4.5.13`

### Python library and CLI

The `jsonpit` library and its `jpit` and `jsonpit` commands report version 4.5.13.
Python 3.12 or newer is required. Install one pipx environment for both commands:

```bash
pipx install "jsonpit==4.5.13"
# Existing installation:
pipx upgrade jsonpit
jpit --version
jsonpit --version
```

The expected outputs are `jpit v4.5.13` and `jsonpit v4.5.13`.

### Distribution recovery

The original coordinated release published `jsonpit` 4.5.13 but omitted the
separate `jpit` companion package, standalone refresh, and GitHub Release page.
The companion is now published as 4.5.13 and pins `jsonpit==4.5.13`.

The original v4.5.13 tag and published jsonpit artifacts are unchanged. Companion
metadata and documentation were corrected in commit `2b12211`. The standalone
release download is rebuilt from the Python runtime sources at the original tag.

If both distribution names were installed into separate pipx environments, keep
one environment and restore both command links:

```bash
pipx uninstall jpit
pipx install --force "jsonpit==4.5.13"
```

Use pipx for CLI installation or a virtual environment for library installation
on systems with externally managed Python. The release assets contain both
packages' wheels/source archives and a standalone `jpit` zipapp.
