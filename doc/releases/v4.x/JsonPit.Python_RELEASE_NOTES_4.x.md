# jsonpit-python Release Notes 4.x

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
