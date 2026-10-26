# Google Drive and OneDrive on Windows 11 with WSL2

This guide exposes Windows cloud-storage folders to Ubuntu in WSL2, then uses
Amafu to configure RAIkeep. Windows runs the cloud clients; WSL accesses their
files through mounted paths. Amafu discovers directories and writes configuration;
it does not mount Windows drives, download placeholders, or operate a sync client.

The commands below describe a setup to verify on your Windows machine. The
automated checks below exercise discovery and file access on an existing setup;
they do not replay Windows client installation or configure mounts at startup.

## Prepare the Windows folders

For Google Drive, this example uses a streaming drive assigned to `G:` with a
`My Drive\GDriveData` folder. Check the actual drive letter in Drive for desktop
settings and File Explorer. Streaming requires Drive for desktop to be running;
mirroring keeps a local copy instead. See Google's
[streaming and mirroring documentation](https://support.google.com/drive/answer/13401938?hl=en).

For OneDrive, locate the intended account's folder in File Explorer and create or
locate its `OneDriveData` directory. Select **Always keep on this device** for data
that must be available locally, then let downloading finish. See Microsoft's
[Files On-Demand documentation](https://support.microsoft.com/en-us/onedrive/save-disk-space-with-onedrive-files-on-demand-for-windows).

| Provider | Example Windows location | WSL location | Stable Linux path |
| --- | --- | --- | --- |
| Google Drive | `G:\My Drive\GDriveData` | `/mnt/g/My Drive/GDriveData` | `/srv/ServerData/GDriveData` |
| OneDrive | `C:\Users\ExampleUser\OneDrive\OneDriveData` | `/mnt/c/Users/ExampleUser/OneDrive/OneDriveData` | `/srv/ServerData/OneDriveData` |

Replace `ExampleUser` and any account-specific folder names with the actual paths.
Windows placeholders and virtual drives may behave differently through WSL than
through File Explorer. A drive-letter mount is an option to test, not a guarantee
that an `Input/output error` will disappear.

## Mount the Google Drive volume in WSL

Run these commands inside Ubuntu after the Windows drive is available. If `/mnt/g`
is already mounted correctly, use that mount instead of mounting it again.

```sh
sudo mkdir -p /mnt/g
sudo mount -t drvfs G: /mnt/g -o "metadata,uid=$(id -u),gid=$(id -g),umask=022"
ls -la "/mnt/g/My Drive/GDriveData"
```

DrvFs exposes Windows files to WSL. Its `metadata`, `uid`, `gid`, and mask options
control Linux permission handling; Windows permissions still apply. See
[Microsoft's WSL configuration reference](https://learn.microsoft.com/en-us/windows/wsl/wsl-config).

Verify that you can read an existing file's contents, rather than relying only on
a directory listing. If that fails, check the same file in Windows and its local
availability before configuring RAIkeep.

For mounting at WSL startup, print an `/etc/fstab` entry using your actual Linux
user and group IDs:

```sh
printf 'G: /mnt/g drvfs metadata,uid=%s,gid=%s,umask=022 0 0\n' "$(id -u)" "$(id -g)"
sudoedit /etc/fstab
```

Add the printed line once. WSL processes this file at startup when
`[automount] mountFsTab=true` in `/etc/wsl.conf` (the default). The Windows virtual
drive may become available later; if mounting at startup fails, start Drive for
desktop on Windows and then run `sudo mount /mnt/g` inside WSL.

## Create stable Linux paths

After both source directories are accessible, create their links. These commands
assume the two destination links do not already exist; inspect an existing entry
before changing it.

```sh
sudo mkdir -p /srv/ServerData
sudo ln -sT "/mnt/g/My Drive/GDriveData" /srv/ServerData/GDriveData
sudo ln -sT "/mnt/c/Users/ExampleUser/OneDrive/OneDriveData" /srv/ServerData/OneDriveData
ls -la /srv/ServerData/GDriveData/
ls -la /srv/ServerData/OneDriveData/
```

The links provide stable application paths while files remain in their Windows
cloud folders. They do not initiate synchronization.

Use `G:\My Drive\GDriveData` in Windows applications and the Linux paths above in
WSL. A WSL shortcut does not guarantee that Windows can browse the mounted drive
again through `\\wsl.localhost\Ubuntu\mnt\g` or a Linux symlink to it. On Themba,
native `G:` access and WSL access both worked while this UNC route failed, even
for the same user. This is a separate access route from those covered by the
file round-trip tests. Microsoft's
[WSL interoperability reference](https://learn.microsoft.com/en-us/windows/dev-environment/wsl-interop)
describes the Windows-drive and Linux-UNC paths separately.

## Detect and configure with Amafu

Preview discovery and the proposed configuration:

```sh
amafu detect --json --dry-run
amafu init --create-links --dry-run
```

On Linux, Amafu checks existing `~/.CloudStorage/` shortcuts first, then accessible
paths in an existing `~/.config/RAIkeep.json5`, then conventional directories under
`/srv/ServerData/`. With no earlier overrides, the setup above should discover
`GoogleDrive` and `OneDrive` at the corresponding `*Data` paths. Other configured
or detected providers may also appear.

For a new configuration, run:

```sh
amafu init --create-links
```

This creates `~/.CloudStorage/GoogleDrive` and `~/.CloudStorage/OneDrive` shortcuts
where needed and uses those clean paths in `~/.config/RAIkeep.json5`.

If a configuration already exists, `init` refuses to overwrite it. Use the
reconciliation preview instead, review its changes, then apply them explicitly:

```sh
amafu reconcile
amafu reconcile --apply
```

Discovery establishes that directories exist. It does not certify that files are
downloaded or that changes have reached another machine. Verify synchronization
separately with a small test file before relying on the setup for shared Pits.

## Run the Windows/WSL integration tests

From the RAIkeep checkout on your development machine, run:

```sh
bash scripts/test-amafu-wsl.sh Themba
```

The name must identify a WSL Observer in `Os.Config.Observers` with working SSH
access. The development machine needs the .NET 10 SDK and `tar`. The Observer
needs the .NET 10 runtime, Python 3, `tar`, `nsenter`, `setpriv`, and Windows
interoperability through `wslpath`, `powershell.exe`, and `wsl.exe`. The namespace
check uses WSL's root-user command option to enter existing mount namespaces,
then drops to the configured Linux user's IDs before accessing cloud files.
Its cloud folders must already be mounted and configured.

The runner builds Amafu from the current checkout and uploads that build to an
isolated remote directory through `OsLib.SshSystem`. It leaves installed tools
alone. The four tests check:

- Discovery and `init --create-links --dry-run` produce the expected clean
  configuration paths without changing the existing configuration or shortcuts.
- Google Drive files written through WSL can be read and updated through Windows,
  with the Windows response then readable through WSL.
- The same round trip works for OneDrive.
- Existing user shells in every discovered mount namespace can enumerate the
  cloud directories and write, read, and remove a probe as the Linux user.

Cloud paths come from the Observer's Amafu discovery. File probes use unique
subdirectories inside those cloud trees and remove their files afterward. A
missing provider fails its test explicitly. These tests establish local
Windows/WSL access, not replication to another machine.

A live run on Themba on 2026-10-26 passed all four checks using the current
4.5.14 Amafu source build. Initially Google Drive was unavailable because WSL had
two stale mounts at `/mnt/g`, although Windows exposed `G:`. Normally unmounting
both entries and mounting the existing volume once restored SSH access, but
interactive terminals had a separate stale mount namespace. That namespace also
required a normal unmount and remount. The final checks verified cloud reads and
writes as the Linux user in both views. These repairs changed running mounts
only; startup configuration and installed tools were left unchanged.

## Troubleshooting

- **Empty or unavailable mount:** check that the correct Windows account and
  drive are available, then retry the mount. An ordinary empty mount-point
  directory is not proof that its drive is mounted.
- **Input/output error:** try reading the file in Windows, ensure it is available
  locally, and retry in WSL. The error alone does not identify a particular cloud
  driver or prove that remounting will fix it.
- **Windows sees `G:` but WSL reports “No such device”:** inspect
  `findmnt --mountpoint /mnt/g`. Stale or stacked mounts may need to be unmounted
  before mounting the existing Windows volume again. Stop dependent work first;
  do not stack another mount on top or force an unmount of an active filesystem.
- **SSH works but an existing terminal fails:** compare
  `readlink /proc/self/ns/mnt` in both sessions. The same username may be running
  in different mount namespaces, so a repair in one view need not repair the
  other. Verify actual directory enumeration and file access as the user in the
  affected view; successful metadata access as root is insufficient. Microsoft's
  [DrvFs architecture documentation](https://github.com/microsoft/WSL/blob/master/doc/docs/technical-documentation/drvfs.md)
  explains WSL's separate elevated and non-elevated mount namespaces.
- **Permission denied:** check Windows access rights and the mount's Linux user
  and group IDs. Do not assume every Ubuntu user has ID `1000`.
- **Paths containing spaces:** quote them as shown above. Stable symlinks simplify
  application configuration but do not change the target filesystem's behavior.
