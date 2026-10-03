#!/usr/bin/env bash
set -euo pipefail

# ==============================================================================
# RAIkeep Fleet CLI Installer: provisions all 5 CLIs across Nkosikazi, Mzansi, Mdlaka
# CLIs: amafu, raid, iorg, pits, and jpit (Python jsonpit)
# ==============================================================================

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MANIFEST_FILE="$ROOT_DIR/scripts/release-manifest.json"

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
DEFAULT_VERSION="${DEFAULT_VERSION:-4.5.2}"

# ==============================================================================
# Fleet Definition
# - LOCAL_TARGET: Machine name for local execution (alias "local" also matches)
# - FLEET_TARGETS: The coordinated cluster. Can specify plain host or user@host.
# ==============================================================================
LOCAL_TARGET="Nkosikazi"
FLEET_TARGETS=("Nkosikazi" "Mzansi" "umshadisi@Mdlaka" "Neo")

# Resolves a CLI token (case-insensitively) against the fleet
resolve_target() {
	local val="$1"
	local lower="$(echo "$val" | tr '[:upper:]' '[:lower:]')"

	if [[ "$lower" == "local" || "$lower" == "$(echo "$LOCAL_TARGET" | tr '[:upper:]' '[:lower:]')" ]]; then
		echo "$LOCAL_TARGET"
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

echo "  [1/3] Checking environment..."
if command -v dotnet >/dev/null 2>&1; then
	echo "    ✔️ dotnet found: $(dotnet --version)"
else
	echo "    ❌ ERROR: dotnet is not installed or not in PATH."
	exit 1
fi

echo "  [2/3] Installing/Updating .NET global tools..."
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

echo "  [3/3] Installing/Updating Python jsonpit (jpit CLI)..."
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

echo -e "\n  🔍 Verification results on $(hostname):"
for cmd in amafu raid iorg pits jpit; do
	if command -v "$cmd" >/dev/null 2>&1; then
		out="$("$cmd" --version 2>&1 | head -n 1 || true)"
		printf "    ✅ %-8s : %s\n" "$cmd" "$out"
	else
		printf "    ❌ %-8s : NOT FOUND in PATH\n" "$cmd"
	fi
done
EOF

	if [[ "$target_machine" == "$LOCAL_TARGET" || "$target_machine" == "local" ]]; then
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
