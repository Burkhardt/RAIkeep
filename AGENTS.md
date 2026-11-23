# RAIkeep contributor conventions

## Cloud configuration and tests

This agreement applies to every RAIkeep custodian and every C# and Python
test, including unit tests, CLI tests, and release checks. Treat the user's
actual `~/.config/RAIkeep.json5` as read-only, on disk and after loading it.
Never edit, replace, shadow, or override it for testing. This includes
redirecting `HOME` to a substitute config, mocking the configuration loader,
and changing provider mappings in memory.

For cloud tests, read `TestCloud` from that configuration and resolve its
configured cloud drive. When it selects Dropbox, create an isolated,
run-specific test directory inside the actual Dropbox root. Clean up only
the directory owned by that run. A temporary directory named `Dropbox`
does not qualify. If the runner lacks the required configuration or drive,
skip the cloud-dependent test and report the reason. This applies to GitHub
Actions as well as developer machines.

Only an explicit exemption from Dr. Burkhardt permits a deviation. Apply it
only to the tests and conditions he authorized.

## Public commit subjects

GitHub’s commit list is a public release ledger. Write each subject as a short,
plain-English description of the delivered behavior. Do not prefix subjects with
`feat:`, `fix:`, `chore:`, `docs:`, `release:`, or `Prepare`.

Use the user-visible change when one exists:

- `Clean EventFile naming and legacy hash validation`
- `Add async unzip and typed CR049 command support`
- `Add strict pits seed request`

For a commit that only synchronizes a release and has no stronger behavioral
summary, use `Coordinated X.Y.Z release`.

Do not rewrite published history solely to change older commit subjects.

## CLI help presentation

Follow [cli-style.md](https://github.com/Burkhardt/RAIkeep/blob/main/doc/cli-style.md)
when changing help screens. Use space-padded columns, shared glyph colors,
consistent syntax highlights, and bold/italic emphasis. Preserve plain redirected
output and machine-output contracts. Keep the standalone Amafu formatter source
synchronized with OsLib via `python3 scripts/sync-cli-style.py --check`.
