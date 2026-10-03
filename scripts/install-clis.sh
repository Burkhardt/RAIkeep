#!/usr/bin/env bash
set -euo pipefail

# ==============================================================================
# RAIkeep Fleet CLI Installer: provisions all 5 CLIs across Nkosikazi, Mzansi, Mdlaka
# CLIs: amafu, raid, iorg, pits, and jpit (Python jsonpit)
# ==============================================================================

SCRIPT_SOURCE="${BASH_SOURCE[0]:-}"
if [[ -n "$SCRIPT_SOURCE" ]]; then
	ROOT_DIR="$(cd "$(dirname "$SCRIPT_SOURCE")/.." 2>/dev/null && pwd || true)"
else
	ROOT_DIR=""
fi
MANIFEST_FILE="${ROOT_DIR:+$ROOT_DIR/scripts/release-manifest.json}"

# Resolve default version from release-manifest.json
resolve_default_version() {
	if [[ -f "$MANIFEST_FILE" ]]; then
		python3 -c '
import json, sys
try:
	m = json.load(open("'"$MANIFEST_FILE"'"))
	print(m.get("current_version", ""))
except Exception:
	pass
'
	else
		echo ""
	fi
}

DEFAULT_VERSION="$(resolve_default_version)"
DEFAULT_VERSION="${DEFAULT_VERSION:-4.5.3}"

# ==============================================================================
# Fleet Definition
# - detect_machine_name: dynamically detects macOS ComputerName/LocalHostName or hostname
# - FLEET_TARGETS: The coordinated cluster. Can specify plain host or user@host.
# ==============================================================================
detect_machine_name() {
	if command -v scutil >/dev/null 2>&1; then
		local name
		name="$(scutil --get LocalHostName 2>/dev/null || scutil --get ComputerName 2>/dev/null || true)"
		if [[ -n "$name" ]]; then
			echo "$name"
			return 0
		fi
	fi
	hostname -s 2>/dev/null || hostname 2>/dev/null || echo "localhost"
}

CURRENT_HOST="$(detect_machine_name)"
FLEET_TARGETS=("Nkosikazi" "Mzansi" "umshadisi@Mdlaka" "Neo")

# Resolves a CLI token (case-insensitively) against the fleet
resolve_target() {
	local val="$1"
	local lower="$(echo "$val" | tr '[:upper:]' '[:lower:]')"

	if [[ "$lower" == "local" || "$lower" == "$(echo "$CURRENT_HOST" | tr '[:upper:]' '[:lower:]')" ]]; then
		echo "$CURRENT_HOST"
		return 0
	fi
	if [[ "$lower" == "all" ]]; then
		echo "all"
		return 0
	fi

	for t in "${FLEET_TARGETS[@]}"; do
		local host="${t##*@}"
		local t_lower="$(echo "$t" | tr '[:upper:]' '[:lower:]')"
		local h_lower="$(echo "$host" | tr '[:upper:]' '[:lower:]')"
		if [[ "$lower" == "$t_lower" || "$lower" == "$h_lower" ]]; then
			echo "$t"
			return 0
		fi
	done

	# Fallback for ad-hoc user@host or custom host
	echo "$val"
}

# Parse arguments: version and targets
VERSION=""
TARGETS=()

for arg in "$@"; do
	if [[ "$arg" == "-h" || "$arg" == "--help" ]]; then
		fleet_pipe="$(IFS=\|; echo "${FLEET_TARGETS[*]}")"
		echo "Usage: $0 [VERSION] [all|$fleet_pipe]"
		exit 0
	elif [[ -z "$VERSION" ]] && [[ "$arg" =~ ^v?[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
		VERSION="${arg#v}"
	else
		TARGETS+=("$(resolve_target "$arg")")
	fi
done

VERSION="${VERSION:-$DEFAULT_VERSION}"

# Expand "all" or default to all if no targets specified
FINAL_TARGETS=()
if [[ ${#TARGETS[@]} -eq 0 ]]; then
	FINAL_TARGETS=("${FLEET_TARGETS[@]}")
else
	for t in "${TARGETS[@]}"; do
		if [[ "$t" == "all" ]]; then
			FINAL_TARGETS=("${FLEET_TARGETS[@]}")
			break
		else
			FINAL_TARGETS+=("$t")
		fi
	done
fi

echo "============================================================"
echo "🚀 RAIkeep Fleet CLI Provisioner"
echo "   Target Version : $VERSION"
echo "   Target Fleet   : ${FINAL_TARGETS[*]}"
echo "============================================================"

# The remote/local execution payload
run_installation_payload() {
	local target_machine="$1"
	local ver="$2"

	echo -e "\n------------------------------------------------------------"
	echo "📦 Installing on [$target_machine] (Version: $ver)..."
	echo "------------------------------------------------------------"

	local PAYLOAD_SCRIPT
	read -r -d '' PAYLOAD_SCRIPT << 'EOF' || true
set -euo pipefail
VERSION="$1"

export PATH="$HOME/.local/bin:$HOME/.dotnet/tools:$HOME/.dotnet:/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/share/dotnet:/opt/dotnet:/usr/local/bin:$PATH"

echo "  [1/4] Checking environment..."
if command -v dotnet >/dev/null 2>&1; then
	echo "    ✔️ dotnet found: $(dotnet --version)"
else
	echo "    ❌ ERROR: dotnet is not installed or not in PATH."
	exit 1
fi

echo "  [2/4] Installing/Updating .NET global tools..."
install_dotnet_tool() {
	local pkg="$1"
	local v="$2"
	if dotnet tool update -g "$pkg" --version "$v" --no-cache 2>&1 | sed 's/^/      /'; then
		return 0
	elif dotnet tool install -g "$pkg" --version "$v" --no-cache 2>&1 | sed 's/^/      /'; then
		return 0
	elif dotnet tool update -g "$pkg" --no-cache 2>&1 | sed 's/^/      /'; then
		return 0
	elif dotnet tool install -g "$pkg" --no-cache 2>&1 | sed 's/^/      /'; then
		return 0
	else
		echo "      ⚠️ Warning: Failed to install/update $pkg."
		return 1
	fi
}

install_dotnet_tool "Amafu" "$VERSION"
install_dotnet_tool "RaidSeeder" "$VERSION"
install_dotnet_tool "ImgSeeder" "$VERSION"
install_dotnet_tool "PitSeeder" "$VERSION"

echo "  [3/4] Installing/Updating Python jsonpit (jpit CLI)..."
install_jpit() {
	local py_spec="jsonpit==$VERSION"
	if [[ "$VERSION" == "4.5.0" ]]; then
		py_spec="jsonpit==4.5.1"
	fi

	mkdir -p "$HOME/.local/bin"
	local venv_dir="$HOME/.local/share/jsonpit-venv"
	if python3 -m venv "$venv_dir" 2>/dev/null; then
		"$venv_dir/bin/pip" install --upgrade --no-cache-dir "$py_spec" 2>&1 | sed 's/^/      /'
		ln -sf "$venv_dir/bin/jpit" "$HOME/.local/bin/jpit"
		ln -sf "$venv_dir/bin/jsonpit" "$HOME/.local/bin/jsonpit"
	elif command -v uv >/dev/null 2>&1; then
		uv tool install "$py_spec" --force --refresh 2>&1 | sed 's/^/      /'
	elif command -v pipx >/dev/null 2>&1; then
		pipx install "$py_spec" --force 2>&1 | sed 's/^/      /' || pipx upgrade jsonpit 2>&1 | sed 's/^/      /'
	elif command -v pip3 >/dev/null 2>&1; then
		if pip3 install --help 2>&1 | grep -q -- '--break-system-packages'; then
			pip3 install --user --upgrade --break-system-packages "$py_spec" 2>&1 | sed 's/^/      /'
		else
			pip3 install --user --upgrade "$py_spec" 2>&1 | sed 's/^/      /'
		fi
	elif command -v pip >/dev/null 2>&1; then
		pip install --user --upgrade "$py_spec" 2>&1 | sed 's/^/      /'
	else
		echo "      ⚠️ Warning: No python3 venv, uv, pipx, pip3 or pip found. Skipping jpit."
	fi

	# Unify all .NET tools into ~/.local/bin as well
	for tool_name in amafu raid iorg pits; do
		if [[ -f "$HOME/.dotnet/tools/$tool_name" ]]; then
			ln -sf "$HOME/.dotnet/tools/$tool_name" "$HOME/.local/bin/$tool_name"
		fi
	done

	# Unify Python tools into ~/.local/bin as well (including pip --user and macOS Library/Python)
	local py_user_base
	py_user_base="$(python3 -m site --user-base 2>/dev/null)/bin"
	for p_dir in "$py_user_base" "$HOME/Library/Python/"*/bin; do
		if [[ -d "$p_dir" ]]; then
			for tool_name in jpit jsonpit; do
				if [[ -f "$p_dir/$tool_name" ]]; then
					ln -sf "$p_dir/$tool_name" "$HOME/.local/bin/$tool_name"
				fi
			done
		fi
	done

	# zsh reads .zshenv for non-interactive SSH and .zprofile for login shells.
	# Keep the managed tools ahead of older /usr/local/bin copies after path_helper.
	local path_line='export PATH="$HOME/.local/bin:$HOME/.dotnet/tools:$PATH"'
	for rc in "$HOME/.zshenv" "$HOME/.zprofile" "$HOME/.zshrc" "$HOME/.bashrc"; do
		if ! grep -Fqx -- "$path_line" "$rc" 2>/dev/null; then
			if [[ -f "$rc" ]]; then
				cp -p "$rc" "${rc}.before-raikeep-path-$(date -u +%Y%m%dT%H%M%SZ)"
			fi
			printf "\n# RAIkeep & jsonpit CLI paths\n%s\n" "$path_line" >> "$rc"
			echo "    ✔️ Configured PATH in $rc"
		fi
	done
}
install_jpit

echo "  [4/4] Setting up Cloud Storage shortcuts via amafu..."
if command -v amafu >/dev/null 2>&1; then
	if [[ ! -f "$HOME/.config/RAIkeep.json5" ]]; then
		amafu init --create-links 2>&1 | sed 's/^/      /' || true
	else
		amafu detect --create-links 2>&1 | sed 's/^/      /' || true
	fi
fi

CURRENT_USER="${USER:-$(id -un 2>/dev/null || whoami 2>/dev/null || echo 'user')}"
echo -e "\n  🔍 Verification results for ${CURRENT_USER} on $(hostname):"
for cmd in amafu raid iorg pits jpit; do
	if command -v "$cmd" >/dev/null 2>&1; then
		out="$("$cmd" --version 2>&1 | head -n 1 || true)"
		printf "    ✅ %-8s : %s\n" "$cmd" "$out"
	else
		printf "    ❌ %-8s : NOT FOUND in PATH\n" "$cmd"
	fi
done

python3 -c '
from pathlib import Path
p = Path.home() / ".CloudStorage"
if p.is_dir():
	links = [item for item in sorted(p.iterdir()) if item.is_symlink()]
	if links:
		print("\n  ☁️ Cloud Storage shortcuts in ~/.CloudStorage:")
		for item in links:
			print(f"    🔗 {item.name:<12} -> {item.resolve()}")
' 2>/dev/null || true
EOF

	local host_only="${target_machine##*@}"
	local t_lower="$(echo "$host_only" | tr '[:upper:]' '[:lower:]')"
	local c_lower="$(echo "$CURRENT_HOST" | tr '[:upper:]' '[:lower:]')"
	if [[ "$t_lower" == "local" || "$t_lower" == "$c_lower" ]]; then
		# Run locally
		bash -s -- "$ver" <<< "$PAYLOAD_SCRIPT"
	else
		# Run remotely via SSH
		if ! ssh -o ConnectTimeout=8 -o BatchMode=yes "$target_machine" exit 2>/dev/null; then
			echo "  ⚠️ Warning: Cannot connect via SSH to $target_machine (timed out or key auth needed). Skipping."
			return 1
		fi
		ssh -o ConnectTimeout=15 -T "$target_machine" "bash -s -- $ver" <<< "$PAYLOAD_SCRIPT"
	fi
}

FAILED_HOSTS=()
SUCCESS_HOSTS=()

for target in "${FINAL_TARGETS[@]}"; do
	if run_installation_payload "$target" "$VERSION"; then
		SUCCESS_HOSTS+=("$target")
	else
		FAILED_HOSTS+=("$target")
	fi
done

echo -e "\n============================================================"
echo "🏁 Provisioning Complete"
echo "   Successful : ${SUCCESS_HOSTS[*]:-None}"
if [[ ${#FAILED_HOSTS[@]} -gt 0 ]]; then
	echo "   Failed/Skipped : ${FAILED_HOSTS[*]}"
fi
echo "============================================================"
