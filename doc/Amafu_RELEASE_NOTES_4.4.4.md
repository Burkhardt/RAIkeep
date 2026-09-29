# Release Notes: Amafu v4.4.4

Amafu is the standalone cloud-storage discovery and RAIkeep configuration bootstrap tool introduced by accepted [`CR044_AIA_and_jsonpit_to_RAIkeep_Auto-Detect-Cloud-Drives-and-Init-Config.md`](CR/CR044_AIA_and_jsonpit_to_RAIkeep_Auto-Detect-Cloud-Drives-and-Init-Config.md).

## Highlights

- Adds `amafu detect`, `amafu init`, and the `amafu init-config` alias.
- Detects documented macOS OneDrive, Dropbox, Google Drive, and iCloud Drive locations in deterministic provider order.
- Generates standard JSON5 at `~/.config/RAIkeep.json5`, refuses overwrite unless `--force` is supplied, and supports `--dry-run` without writes.
- Runs independently of OsLib and all other RAIkeep packages. Its internal model is `AmafuConfiguration`; it does not expose or mutate `Os.Config`.
- Ships as a NuGet global tool and as zero-runtime NativeAOT binaries for macOS ARM64/x64, Linux ARM64/x64, and Windows x64.
- Automatic provider discovery is supported and tested only on macOS in 4.4.4. Linux and Windows binaries provide the command surface and documented starter-template fallback; provider detection on those systems is future work.
- Preserves the RAIkeep Nerd Font CLI visual language and rejects elevated execution to protect user-owned configuration files.

No release action occurs by preparing these notes; RAI retains the manual release gate.
