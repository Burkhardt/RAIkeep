# Release Notes: OsLib v4.4.6

OsLib (`OsLibCore`) v4.4.6 introduces key infrastructure enhancements supporting CR049 and JsonPit storage refinements, including clean EventFile naming, asynchronous native archive decompression, streaming process execution, and buffered standard input support.

## 1. Clean EventFile Naming & Legacy Validation

- **Clean Logical Stems:** `EventFile.ComposeNameFor` emits `{LogicalStem}.event` without SHA-256 hash suffixes, reducing directory path lengths across cloud file systems.
- **Legacy Hash Support:** `EventFile` retains full recognition and validation for legacy `{stem}_{sha256}.event` filenames, verifying payload digests on read for seamless rolling upgrades.

## 2. Asynchronous Native Archive Decompression

- **Native Unzip Harness:** Introduces asynchronous `UnzipCommand` leveraging the OS native `unzip` utility on macOS and Linux/Ubuntu.
- **Asynchronous Process Execution:** `RaiSystem` dispatches extraction off the main thread with explicit timeout, exit-code validation, and standard error capture.

## 3. Piped Standard Input Support

- **Buffered Stdin for Pits:** `PitsSeedRequest` adds direct support for streaming standard input, enabling CLI tools and callers to pipe JSON/JSON5 payloads without disk staging.

## 4. Exclusive File Writes & System Hygiene

- Provides streaming exclusive file writing and per-process environment overrides.
- Aligns dependencies on .NET 10 across all platforms.

---

This release is part of the coordinated nine-package [CR049](CR/CR049_AIA_and_jsonpit_to_RAIkeep_Live-ID-Validation_and_Zip-Image-Import.md) release. See [RAIkeep release notes](RAIkeep_RELEASE_NOTES_4.4.6.md) for umbrella coordination.
