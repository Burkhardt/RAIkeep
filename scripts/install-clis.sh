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
DEFAULT_VERSION="${DEFAULT_VERSION:-4.5.0}"

# Parse arguments: version and targets
VERSION=""
TARGETS=()

ALL_KNOWN_TARGETS=("Nkosikazi" "Mzansi" "Mdlaka")

is_target() {
	local val="$1"
	local lower
	lower="$(echo "$val" | tr '[:upper:]' '[:lower:]')"
	case "$lower" in
		nkosikazi|local|mzansi|mdlaka|mhlaka|mlaka|all|*@*) return 0 ;;
		*) return 1 ;;
	esac
}

normalize_target() {
	local val="$1"
	local lower
	lower="$(echo "$val" | tr '[:upper:]' '[:lower:]')"
	case "$lower" in
		nkosikazi|local) echo "Nkosikazi" ;;
		mzansi) echo "Mzansi" ;;
		mdlaka|mhlaka|mlaka) echo "Mdlaka" ;;
		all) echo "all" ;;
		*@*)
			local user="${val%%@*}"
			local host="${val##*@}"
			local host_lower="$(echo "$host" | tr '[:upper:]' '[:lower:]')"
			case "$host_lower" in
				mdlaka|mhlaka|mlaka) echo "${user}@Mdlaka" ;;
				mzansi) echo "${user}@Mzansi" ;;
				*) echo "$val" ;;
			esac
			;;
		*) echo "$val" ;;
	esac
}

resolve_ssh_target() {
	local machine="$1"
	if [[ "$machine" == *"@"* ]]; then
		local user="${machine%%@*}"
		local host="${machine##*@}"
		local host_lower="$(echo "$host" | tr '[:upper:]' '[:lower:]')"
		case "$host_lower" in
			mdlaka|mhlaka|mlaka) echo "${user}@Mdlaka" ;;
			mzansi) echo "${user}@Mzansi" ;;
			*) echo "$machine" ;;
		esac
		return
	fi

	local lower="$(echo "$machine" | tr '[:upper:]' '[:lower:]')"
	case "$lower" in
		mdlaka|mhlaka|mlaka)
			local u="${MDLAKA_SSH_USER:-umshadisi}"
			echo "${u}@Mdlaka"
			;;
		*)
			echo "$machine"
			;;
	esac
}

for arg in "$@"; do
	if [[ -z "$VERSION" ]] && [[ "$arg" =~ ^v?[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
		VERSION="${arg#v}"
	elif is_target "$arg"; then
		TARGETS+=("$(normalize_target "$arg")")
	else
		echo "Unknown argument or invalid version: $arg" >&2
		echo "Usage: $0 [VERSION] [Nkosikazi|Mzansi|Mdlaka|all]" >&2
		exit 1
	fi
done

VERSION="${VERSION:-$DEFAULT_VERSION}"

# Expand "all" or default to all if no targets specified
FINAL_TARGETS=()
if [[ ${#TARGETS[@]} -eq 0 ]]; then
	FINAL_TARGETS=("${ALL_KNOWN_TARGETS[@]}")
else
	for t in "${TARGETS[@]}"; do
		if [[ "$t" == "all" ]]; then
			FINAL_TARGETS=("${ALL_KNOWN_TARGETS[@]}")
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

export PATH="/opt/homebrew/bin:/opt/homebrew/sbin:$HOME/.dotnet/tools:$HOME/.dotnet:$HOME/.local/bin:/usr/local/share/dotnet:/opt/dotnet:/usr/local/bin:$PATH"

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

	local venv_dir="$HOME/.local/share/jsonpit-venv"
	if python3 -m venv "$venv_dir" 2>/dev/null; then
		"$venv_dir/bin/pip" install --upgrade --no-cache-dir "$py_spec" 2>&1 | sed 's/^/      /'
		mkdir -p "$HOME/.local/bin"
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

	if [[ "$target_machine" == "Nkosikazi" ]]; then
		# Run locally
		bash -s -- "$ver" <<< "$PAYLOAD_SCRIPT"
	else
		# Run remotely via SSH
		local ssh_target
		ssh_target="$(resolve_ssh_target "$target_machine")"
		if ! ssh -o ConnectTimeout=8 -o BatchMode=yes "$ssh_target" exit 2>/dev/null; then
			echo "  ⚠️ Warning: Cannot connect via SSH to $ssh_target (timed out or key auth needed). Skipping."
			return 1
		fi
		ssh -o ConnectTimeout=15 -T "$ssh_target" "bash -s -- $ver" <<< "$PAYLOAD_SCRIPT"
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
