# RAIkeep contributor conventions

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
