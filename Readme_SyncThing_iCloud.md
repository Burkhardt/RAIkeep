# Syncthing & iCloud Cross-Platform Bridge Architecture

This document outlines the architecture, configuration, and troubleshooting steps for the cross-platform mesh network that synchronizes Apple iCloud Drive data across macOS, Ubuntu Linux, and Windows (WSL) environments using Syncthing.

## 🌍 Architecture Overview

This setup bypasses Apple's iCloud sandbox restrictions and clunky commercial cloud wrappers by establishing a secure, bi-directional, peer-to-peer mesh network. 

* **Master Data Source:** macOS iCloud Drive (Idwala)
* **Protocol:** Syncthing (BEP - Block Exchange Protocol)
* **Target Environments:** Ubuntu Server (Mzansi), Windows/WSL (Ixhiba)
* **Proxy/Security:** Caddy Reverse Proxy with Let's Encrypt SSL (Mzansi)

### Node Topology

| Node Name | OS | Role | Local Path |
| :--- | :--- | :--- | :--- |
| **Idwala** | macOS | Primary iCloud Bridge | `/Users/RSB/Library/Mobile Documents/com~apple~CloudDocs/ICloudDriveData` |
| **Mzansi** | Ubuntu Server | Compute / Storage | `/srv/ServerData/ICloudDriveData` |
| **Ixhiba** | Windows Pro + WSL | Dev Environment | `C:\ServerData\ICloudDriveData` (WSL: `/mnt/c/ServerData/ICloudDriveData`) |
| **Nkosikazi** | macOS | Secondary Mac | `/Users/RSB/Library/Mobile Documents/com~apple~CloudDocs/ICloudDriveData` |

---

## 🍎 macOS Setup (Idwala / Nkosikazi)

macOS strictly sandboxes the iCloud Drive directory. Syncthing will silently fail to read files (showing 0 Bytes) unless explicitly granted permission.

### 1. The "Full Disk Access" Requirement
1. Open **System Preferences > Security & Privacy > Privacy**.
2. Select **Full Disk Access**.
3. Add **Syncthing** to the list and ensure it is checked.
4. **Restart Syncthing** completely for the permissions to take effect.

### 2. Critical System Settings
* **Optimize Mac Storage MUST BE OFF:** (System Preferences > Apple ID > iCloud). If enabled, macOS will convert local files into 1kb `.icloud` stubs, which Syncthing will then propagate to the Linux/Windows servers, effectively deleting your local server copies.
* **Ghost Files:** If a file has a cloud icon with a downward arrow in Finder, it is not physically on the disk. Double-click it to download it before Syncthing can read it.

---

## 🐧 Ubuntu Server Setup (Mzansi)

Mzansi runs Syncthing as a background service, exposed securely via a Caddy reverse proxy at `https://sync.africastage.org`.

### 1. Caddy Reverse Proxy Configuration
Do **not** use header spoofing (`header_up Host localhost`). It breaks Syncthing's internal routing.
```caddyfile
sync.africastage.org {
    reverse_proxy 127.0.0.1:8384
}
```

### 2. Bypassing the "Host check error"
Syncthing prevents DNS Rebinding attacks by rejecting requests not addressed to `localhost`. You must explicitly tell it to trust the proxy.
1. Edit `/home/rsb/.local/state/syncthing/config.xml` (Verify path with `syncthing -paths`).
2. Inside the `<gui>` tag, add: `<insecureSkipHostcheck>true</insecureSkipHostcheck>`

### 3. Fixing the "ERR_TOO_MANY_REDIRECTS" Infinite Loop
Since Caddy handles HTTPS externally, Syncthing's internal TLS must be disabled to prevent an encryption loop.
1. Edit `/home/rsb/.local/state/syncthing/config.xml`.
2. Change the GUI tag to: `<gui enabled="true" tls="false" debugging="false">`
3. Restart the service: `systemctl --user restart syncthing`

---

## 🪟 Windows Pro & WSL Setup (Ixhiba)

Do **not** install Syncthing via `apt` inside WSL, as WSL processes can suspend. Run it natively in Windows using **SyncTrayzor**.

### 1. The SyncTrayzor Version Conflict
**CRITICAL:** Do *not* use the original `canton7` SyncTrayzor release. It attempts to boot the modern Syncthing v2.0 engine using deprecated command-line flags (`-n`), causing it to crash immediately.
* **Use the maintained fork:** Download the installer from the [GermanCoding SyncTrayzor repository](https://github.com/GermanCoding/SyncTrayzor/releases).
* Use the `Setup-x64.exe` installer to automatically handle Windows Defender firewall rules and background startup.

### 2. Pathing Strategy for WSL
Avoid placing the sync folder in `C:\Users\Administrator\...` due to potential Windows UAC permission friction when accessed aggressively by Linux processes.
* **Native Windows Path:** `C:\ServerData\ICloudDriveData`
* **WSL Ubuntu Path:** `/mnt/c/ServerData/ICloudDriveData`

---

## 🔗 Rebuilding the Mesh (Disaster Recovery)

If the database ever corrupts or folders become unlinked, follow this exact sequence to re-establish the connection without creating duplicated "ghost" folders.

### 1. Introduce the Devices
1. Get the **Device ID** from the new machine (Actions > Show ID).
2. Go to the **Master Node (Idwala)** UI.
3. Click **Add Remote Device**, paste the ID, and Save.

### 2. Push from the Master
Syncthing folders are linked by hidden `Folder IDs` (e.g., `psvj7-uy5t2`), not their names. **Never manually create the folder on the receiving machine first.**
1. On **Idwala**, edit the existing `ICloudDriveData` folder.
2. Go to the **Sharing** tab and check the box for the new machine. Save.

### 3. Catch on the Receiver
1. Wait for the yellow banner on the receiving machine (Mzansi or Ixhiba): *"Idwala wants to share folder ICloudDriveData"*.
2. Click **Add**.
3. **Crucial:** Change the default pre-filled path (which usually points to the home directory) to the absolute server path (e.g., `/srv/ServerData/ICloudDriveData`).
4. Set Folder Type to **Send & Receive**. Save.

### Handling Mismatched Folders
If a folder is manually created on the receiving end, Idwala will show the folder as "Unshared" while the remote machine shows an empty folder as "Up to Date".
1. On the receiving machine, **Edit > Remove** the ghost folder.
2. Wait 30 seconds for the yellow prompt from Idwala to reappear, and accept it properly to merge the Folder IDs.
