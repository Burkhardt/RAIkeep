#!/usr/bin/env bash
set -euo pipefail

# ==============================================================================
# RAIkeep Fleet CLI Installer: provisions Unix, Windows, and WSL environments.
# CLIs: amafu, raid, iorg, pits, rail, and jpit (Python jsonpit)
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
DEFAULT_VERSION="${DEFAULT_VERSION:-4.5.15}"

# No machine names or SSH accounts are embedded in the installer.
CONFIG_FILE="${RAIKEEP_CONFIG:-$HOME/.config/RAIkeep.json5}"
FLEET_TARGETS=()

# Resolves a CLI token (case-insensitively) against the fleet
resolve_target() {
	local val="$1"
	local suffix=""
	case "$val" in
		*:windows|*:wsl) suffix=":${val##*:}"; val="${val%:*}" ;;
	esac
	local lower="$(echo "$val" | tr '[:upper:]' '[:lower:]')"

	if [[ "$lower" == "local" ]]; then
		echo "local$suffix"
		return 0
	fi
	if [[ "$lower" == "all" ]]; then
		echo "all"
		return 0
	fi

	# Observer names and explicit SSH endpoints are resolved at execution time.
	echo "$val$suffix"
}

# Parse arguments: version and targets
VERSION=""
TARGETS=()
SKIP_CLOUD_SETUP=0
DRY_RUN=0
SKIP_PYTHON=0

while [[ $# -gt 0 ]]; do
	arg="$1"; shift
	if [[ "$arg" == "-h" || "$arg" == "--help" ]]; then
		echo "Usage: $0 [VERSION] [all|local|OBSERVER[:windows|:wsl] ...] [--config FILE] [--no-cloud-setup] [--skip-python] [--dry-run]"
		echo "Default destinations and SSH logins come from Observers in ~/.config/RAIkeep.json5."
		echo "Default: the environment exposed by SSH. Use HOST:windows or HOST:wsl explicitly."
		echo "--skip-python omits jsonpit/jpit and their Python requirement on destinations."
		echo "--dry-run previews the plan and checks prerequisites without installing anything."
		echo "Examples: $0 all --dry-run; $0 ServerNode:windows --skip-python --dry-run"
		exit 0
	elif [[ "$arg" == "--config" ]]; then
		[[ $# -gt 0 ]] || { echo "--config requires a filename" >&2; exit 2; }
		CONFIG_FILE="$1"; shift
	elif [[ "$arg" == "--no-cloud-setup" ]]; then
		SKIP_CLOUD_SETUP=1
	elif [[ "$arg" == "--skip-python" ]]; then
		SKIP_PYTHON=1
	elif [[ "$arg" == "--dry-run" || "$arg" == "--check" ]]; then
		DRY_RUN=1
	elif [[ -z "$VERSION" ]] && [[ "$arg" =~ ^v?[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
		VERSION="${arg#v}"
	elif [[ "$arg" == -* ]]; then
		echo "Unknown option: $arg" >&2; exit 2
	else
		TARGETS+=("$(resolve_target "$arg")")
	fi
done

VERSION="${VERSION:-$DEFAULT_VERSION}"

# Execute through argv, not a locally evaluated shell command. The only remote
# strings below are fixed commands or encoded payloads with validated versions.
run_target_command() {
	if [[ "$INSTALL_LOCAL" == "1" ]]; then
		bash -c "$1"
	else
		ssh -o ConnectTimeout=15 -o BatchMode=yes -T -- "$INSTALL_LOGIN" "$1"
	fi
}

run_windows_payload() {
	local encoded payload
	payload="$(cat "$ROOT_DIR/scripts/install-clis-windows.ps1")" || return 1
	# Windows OpenSSH may pass through cmd.exe's command-line length limit.
	# Keep only a small bootstrap on the command line; send the script on stdin.
	encoded="$(python3 - "$VERSION" "$DRY_RUN" "$SKIP_CLOUD_SETUP" "$SKIP_PYTHON" <<'PY'
import base64, sys
command = '& ([scriptblock]::Create([Console]::In.ReadToEnd())) -Version "' + sys.argv[1] + '"'
if sys.argv[2] == '1': command += ' -DryRun'
if sys.argv[3] == '1': command += ' -NoCloudSetup'
if sys.argv[4] == '1': command += ' -SkipPython'
print(base64.b64encode(command.encode('utf-16-le')).decode('ascii'))
PY
)" || return 1
	run_target_command "powershell.exe -NoLogo -NoProfile -NonInteractive -EncodedCommand $encoded" <<< "$payload"
}

# Expand "all" or default to all if no targets specified
if [[ ${#TARGETS[@]} -eq 0 || " ${TARGETS[*]} " == *" all "* ]]; then
	fleet_names="$(python3 "$ROOT_DIR/scripts/resolve-install-observer.py" --config "$CONFIG_FILE" --list)" || exit 2
	while IFS= read -r observer; do FLEET_TARGETS+=("$observer"); done <<< "$fleet_names"
fi
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
	local mode=auto
	case "$target_machine" in
		*:windows|*:wsl) mode="${target_machine##*:}"; target_machine="${target_machine%:*}" ;;
	esac
	local platform
	INSTALL_LOCAL=0
	if [[ "$target_machine" == "local" ]]; then INSTALL_LOCAL=1; fi
	INSTALL_LOGIN="$target_machine"
	if [[ "$INSTALL_LOCAL" != "1" ]]; then
		INSTALL_LOGIN="$(python3 "$ROOT_DIR/scripts/resolve-install-observer.py" --config "$CONFIG_FILE" "$target_machine")" || return 1
	fi

	echo -e "\n------------------------------------------------------------"
	if [[ "$DRY_RUN" == "1" ]]; then
		echo "Checking [$target_machine] (Version: $ver; no installation)..."
	else
		echo "📦 Installing on [$target_machine] (Version: $ver)..."
	fi
	echo "------------------------------------------------------------"
	if [[ "$mode" == "windows" ]]; then
		run_windows_payload
		return $?
	fi
	platform="$(run_target_command 'uname -s' 2>/dev/null)" || platform=Windows
	case "$platform" in
		Linux|Darwin) ;;
		MINGW*|MSYS*|Windows)
			platform=Windows
			if [[ "$mode" != "wsl" ]]; then run_windows_payload; return $?; fi ;;
		*) echo "Unsupported SSH environment: $platform" >&2; return 1 ;;
	esac

	local PAYLOAD_SCRIPT
	read -r -d '' PAYLOAD_SCRIPT << 'EOF' || true
set -euo pipefail
VERSION="$1"
SKIP_CLOUD_SETUP="$2"
DRY_RUN="$3"
SKIP_PYTHON="$4"

export PATH="$HOME/.local/bin:$HOME/.dotnet/tools:$HOME/.dotnet:/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/share/dotnet:/opt/dotnet:/usr/local/bin:$PATH"

echo "  [1/4] Checking environment..."
if command -v dotnet >/dev/null 2>&1; then
	echo "    ✔️ dotnet found: $(dotnet --version)"
else
	echo "    ❌ ERROR: dotnet is not installed or not in PATH."
	exit 1
fi
if [[ "$SKIP_PYTHON" != "1" ]]; then
	python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3,12) else 1)' || {
	echo "Python 3.12+ is required in this Linux/macOS environment. No tools were changed." >&2
	exit 1
	}
fi
if [[ "$DRY_RUN" == "1" ]]; then
	echo "Plan: Amafu, RaidSeeder, ImgSeeder, PitSeeder, RaiGuard at $VERSION"
	if [[ "$SKIP_PYTHON" == "1" ]]; then
		echo "Python/jsonpit/jpit skipped; no Python is required on this destination."
	else
		echo "Plan: jsonpit==$VERSION (jpit and jsonpit); $(python3 --version)"
	fi
	echo "Environment ready: $(uname -s), $(dotnet --version). Dry run; no changes made."
	exit 0
fi

echo "  [2/4] Installing/Updating .NET global tools..."
install_dotnet_tool() {
	local pkg="$1"
	local v="$2"
	if dotnet tool update -g "$pkg" --version "$v" --no-cache 2>&1 | sed 's/^/      /'; then
		return 0
	elif dotnet tool install -g "$pkg" --version "$v" --no-cache 2>&1 | sed 's/^/      /'; then
		return 0
	else
		echo "      ❌ Failed to install/update $pkg at exact version $v."
		return 1
	fi
}

install_dotnet_tool "Amafu" "$VERSION"
install_dotnet_tool "RaidSeeder" "$VERSION"
install_dotnet_tool "ImgSeeder" "$VERSION"
install_dotnet_tool "PitSeeder" "$VERSION"
install_dotnet_tool "RaiGuard" "$VERSION"

echo "  [3/4] Installing/Updating Python jsonpit (jpit CLI)..."
install_jpit() {
	local py_spec="jsonpit==$VERSION"
	mkdir -p "$HOME/.local/bin"
	local venv_dir="$HOME/.local/share/jsonpit-venv"
	# One managed environment owns both CLI names. Never bypass PEP 668.
	if command -v pipx >/dev/null 2>&1; then
		pipx install --force "$py_spec" 2>&1 | sed 's/^/      /' || return 1
	elif python3 -m venv "$venv_dir" 2>/dev/null; then
		"$venv_dir/bin/python" -m pip install --upgrade --no-cache-dir "$py_spec" 2>&1 | sed 's/^/      /' || return 1
		ln -sf "$venv_dir/bin/jpit" "$HOME/.local/bin/jpit"
		ln -sf "$venv_dir/bin/jsonpit" "$HOME/.local/bin/jsonpit"
	elif command -v uv >/dev/null 2>&1; then
		uv tool install "$py_spec" --force --refresh 2>&1 | sed 's/^/      /' || return 1
	else
		echo "      ERROR: Install pipx or Python venv support (Ubuntu/Debian: sudo apt install pipx python3-venv)."
		return 1
	fi
	local tool_name actual_version
	for tool_name in jpit jsonpit; do
		actual_version="$("$HOME/.local/bin/$tool_name" --version)" || return 1
		if [[ "$actual_version" != "$tool_name v$VERSION" ]]; then
			echo "      ERROR: $tool_name reports '$actual_version'; expected '$tool_name v$VERSION'."
			return 1
		fi
	done

	# Unify Python tools into ~/.local/bin as well (including pip --user and macOS Library/Python)
	local py_user_base
	py_user_base="$(python3 -m site --user-base 2>/dev/null)/bin"
	for p_dir in "$py_user_base" "$HOME/Library/Python/"*/bin; do
		if [[ -d "$p_dir" ]]; then
			for tool_name in jpit jsonpit; do
				if [[ -f "$p_dir/$tool_name" && ! -e "$HOME/.local/bin/$tool_name" ]]; then
					ln -sf "$p_dir/$tool_name" "$HOME/.local/bin/$tool_name"
				fi
			done
		fi
	done


}
if [[ "$SKIP_PYTHON" == "1" ]]; then
	echo "Python/jsonpit/jpit skipped; existing Python tools are unchanged."
else
	install_jpit
fi

mkdir -p "$HOME/.local/bin"
# Unify .NET commands and persist their PATH even when Python is skipped.
for tool_name in amafu raid iorg pits rail; do
    if [[ -f "$HOME/.dotnet/tools/$tool_name" ]]; then
        ln -sf "$HOME/.dotnet/tools/$tool_name" "$HOME/.local/bin/$tool_name"
    fi
done

# Keep managed commands ahead of older /usr/local/bin copies in future shells.
path_line='export PATH="$HOME/.local/bin:$HOME/.dotnet/tools:$PATH"'
for rc in "$HOME/.zshenv" "$HOME/.zprofile" "$HOME/.zshrc" "$HOME/.bashrc"; do
    if ! grep -Fqx -- "$path_line" "$rc" 2>/dev/null; then
        if [[ -f "$rc" ]]; then
            cp -p "$rc" "${rc}.before-raikeep-path-$(date -u +%Y%m%dT%H%M%SZ)"
        fi
        printf "\n# RAIkeep CLI paths\n%s\n" "$path_line" >> "$rc"
        echo "    Configured PATH in $rc"
    fi
done

echo "  [4/4] Cloud Storage setup..."
if [[ "$SKIP_CLOUD_SETUP" == "1" ]]; then
	echo "    Skipped for this tools-only installation."
elif command -v amafu >/dev/null 2>&1; then
	if [[ ! -f "$HOME/.config/RAIkeep.json5" ]]; then
		amafu init --create-links 2>&1 | sed 's/^/      /' || true
	else
		amafu detect --create-links 2>&1 | sed 's/^/      /' || true
	fi
fi

CURRENT_USER="${USER:-$(id -un 2>/dev/null || whoami 2>/dev/null || echo 'user')}"
echo -e "\n  🔍 Verification results for ${CURRENT_USER} on $(hostname):"
verification_failed=0
commands=(amafu raid iorg pits rail)
if [[ "$SKIP_PYTHON" != "1" ]]; then commands+=(jpit jsonpit); fi
for cmd in "${commands[@]}"; do
	if command -v "$cmd" >/dev/null 2>&1; then
		out="$("$cmd" --version 2>&1 | head -n 1 || true)"
		if [[ "$out" == *"v$VERSION" ]]; then
			printf "    ✅ %-8s : %s\n" "$cmd" "$out"
		else
			printf "    ❌ %-8s : %s (expected v%s)\n" "$cmd" "$out" "$VERSION"
			verification_failed=1
		fi
	else
		printf "    ❌ %-8s : NOT FOUND in PATH\n" "$cmd"
		verification_failed=1
	fi
done

if [[ -d "$HOME/.CloudStorage" ]]; then
    for link in "$HOME/.CloudStorage/"*; do
        if [[ -L "$link" ]]; then
            printf '    %s -> %s\n' "${link##*/}" "$(readlink "$link")"
        fi
    done
fi
(( verification_failed == 0 ))
EOF

	if [[ "$mode" == "wsl" && "$platform" == "Darwin" ]]; then
		echo "WSL is unavailable on macOS." >&2; return 1
	elif [[ "$mode" == "wsl" && "$platform" == "Windows" ]]; then
		# A native Windows SSH endpoint uses its already installed default distro.
		# Failure never triggers WSL installation or distribution initialization.
		if run_target_command "wsl.exe --exec /bin/bash -s -- $ver $SKIP_CLOUD_SETUP $DRY_RUN $SKIP_PYTHON" <<< "$PAYLOAD_SCRIPT"; then
			return 0
		else
			echo "WSL target failed: verify that this Windows login has an operational default Linux distribution. No distribution was installed or initialized." >&2
			return 1
		fi
	else
		run_target_command "bash -s -- $ver $SKIP_CLOUD_SETUP $DRY_RUN $SKIP_PYTHON" <<< "$PAYLOAD_SCRIPT"
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
if [[ "$DRY_RUN" == "1" ]]; then echo "Prerequisite checks complete"; else echo "🏁 Provisioning Complete"; fi
echo "   Successful : ${SUCCESS_HOSTS[*]:-None}"
if [[ ${#FAILED_HOSTS[@]} -gt 0 ]]; then
	echo "   Failed/Skipped : ${FAILED_HOSTS[*]}"
fi
echo "============================================================"
[[ ${#FAILED_HOSTS[@]} -eq 0 ]]
