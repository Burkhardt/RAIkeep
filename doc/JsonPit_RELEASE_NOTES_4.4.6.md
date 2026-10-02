# Release Notes: JsonPit v4.4.6

Rejects live IDs containing `{` or `<` at public write boundaries, validates complete batches before mutation, and retains historical read/export/deletion compatibility. Missing/non-string IDs cannot bypass live validation.

This is part of the coordinated nine-package [CR049](CR/CR049_AIA_and_jsonpit_to_RAIkeep_Live-ID-Validation_and_Zip-Image-Import.md) release. Package versions and fallback dependencies align at 4.4.6.

See [RAIkeep release notes](RAIkeep_RELEASE_NOTES_4.4.6.md) for shared behavior, validation, and the manual publication gate.
