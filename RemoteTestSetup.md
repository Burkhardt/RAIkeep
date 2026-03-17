# Remote Test Setup

Date: 2026-03-13

## Short Answer

The current setup is now config-driven.

1. Local cloud provider roots use `osconfig.json`.
2. Remote observer topology uses `remote-test-config.json`.
3. Remote cloud roots are read from the remote machine's own `osconfig.json` over ssh.

So the answer is:

- local cloud root: `~/.config/RAIkeep/osconfig.json` on macOS and Linux
- remote ssh target: `~/.config/RAIkeep/remote-test-config.json`
- remote Google Drive root: taken from Mzansi's `~/.config/RAIkeep/osconfig.json`

## What Uses Config Files

OsLib resolves local cloud roots through `Os.Config` and `osconfig.json`.

Default config location:

- macOS / Linux: `~/.config/RAIkeep/osconfig.json`
- Windows: `%APPDATA%\RAIkeep\osconfig.json`

For the current remote tests, the important local config value is usually:

- `cloud.googledrive`

Example:

```json
{
	"cloud": {
		"googledrive": "/Users/rsb/Library/CloudStorage/GoogleDrive-.../My Drive/"
	}
}
```

If this entry is missing, OsLib may still discover the local Google Drive root automatically. But for stable test behavior, explicit config is better.

## What Uses Remote Test Config

The current remote Google Drive sync tests use a dedicated remote test config file.

Default location:

- macOS / Linux: `~/.config/RAIkeep/remote-test-config.json`
- Windows: `%APPDATA%\RAIkeep\remote-test-config.json`

Minimal current example:

```json
{
	"observers": {
		"mzansi": {
			"sshTarget": "rsb@Mzansi"
		}
	},
	"apis": {},
	"scenarios": {}
}
```

This is consumed by the reusable OsLib helper `RemoteCloudSyncProbe.TryCreate(...)`.

## Current Test Flow

For the current Google Drive remote-sync tests:

1. `Nkosikasi` runs the test.
2. OsLib resolves the local Google Drive root from `osconfig.json` or provider discovery.
3. OsLib reads `remote-test-config.json` to know how to reach `Mzansi` via ssh.
4. OsLib reads Mzansi's `~/.config/RAIkeep/osconfig.json` over ssh to determine the remote Google Drive root.
5. The test writes locally on `Nkosikasi`.
6. The remote observer polls the synced filesystem on `Mzansi` over ssh.

## Recommended Setup On Nkosikasi

### 1. Confirm local Google Drive root

Make sure your local Google Drive root is either:

- correctly discoverable by OsLib
- or explicitly configured in `~/.config/RAIkeep/osconfig.json`

Recommended explicit config:

```json
{
	"cloud": {
		"googledrive": "/Users/RSB/Library/CloudStorage/GoogleDrive-.../My Drive/"
	}
}
```

### 2. Confirm SSH access to Mzansi

From a shell on `Nkosikasi`, this should work without interactive surprises:

```bash
ssh rsb@Mzansi "printf ready"
```

Expected output:

```text
ready
```

If that does not work cleanly, the tests will skip or fail before any cloud sync logic is exercised.

### 3. Create or confirm `remote-test-config.json`

Recommended minimal file on `Nkosikasi`:

```json
{
	"observers": {
		"mzansi": {
			"sshTarget": "rsb@Mzansi"
		}
	},
	"apis": {},
	"scenarios": {}
}
```

### 4. Confirm the remote Google Drive root through Mzansi's `osconfig.json`

From `Nkosikasi`, manually inspect the remote config:

```bash
ssh rsb@Mzansi "cat ~/.config/RAIkeep/osconfig.json"
```

Make sure `cloud.googledrive` exists there and points at the synced root that should be observed on Mzansi.

## Minimal Manual Verification

Before debugging the full test, verify these three things manually.

### Local discovery

Run any OsLib cloud-related test or inspect the effective config to ensure Google Drive is found locally.

### Remote SSH connectivity

```bash
ssh rsb@Mzansi "printf ready"
```

### Remote config visibility

```bash
ssh rsb@Mzansi "test -f ~/.config/RAIkeep/osconfig.json && printf ready || printf missing"
```

### Remote Google Drive root visibility

Use the `cloud.googledrive` value from the remote `osconfig.json`, then check that path explicitly if needed.

## Which Tests Use This Setup

Currently these tests use the remote `Mzansi` setup:

- `OsLib/OsLib.Tests/GoogleDriveRemoteSyncTests.cs`
- `JsonPit/JsonPit.Tests/GoogleDriveRemoteSyncTests.cs`

Both currently target:

- Google Drive only
- `Nkosikasi` as the writer/test runner
- `Mzansi` as the remote observer over ssh

## Debugging Entry Point

The simplest current real remote-sync debugger entry point is:

- `TextFile_CreateUpdateDelete_PropagatesToMzansiOverGoogleDrive`

in:

- `OsLib/OsLib.Tests/GoogleDriveRemoteSyncTests.cs`

That test already performs real ssh-backed remote checks through OsLib abstractions.

## Important Current Distinction

Remote observer details are intentionally not stored in `osconfig.json`.

Right now:

- provider roots are stored in each machine's `osconfig.json`
- remote observer connection details are stored in `remote-test-config.json`

That keeps machine-local runtime config separate from remote test topology.

## Current Direction

The reusable remote-test configuration model now exists.

For now, the authoritative setup is:

1. local provider roots in `osconfig.json`
2. remote observer ssh targets in `remote-test-config.json`
3. remote provider roots in the remote machine's own `osconfig.json`

## Quick Copy/Paste Verification

```bash
cat ~/.config/RAIkeep/remote-test-config.json
ssh rsb@Mzansi "printf ready"
ssh rsb@Mzansi "cat ~/.config/RAIkeep/osconfig.json"
```

If SSH prints `ready` and the remote `osconfig.json` contains a valid `cloud.googledrive`, the current config-driven remote Google Drive tests have the minimum setup they need.