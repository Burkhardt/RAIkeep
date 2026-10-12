#!/usr/bin/env bash
set -euo pipefail

# Installs Amafu only. Usage: InstallAmafu.sh <native|global|system> [VERSION]
DEFAULT_VERSION="4.5.10"
MODE="${1:-}"
VERSION="${2:-$DEFAULT_VERSION}"
VERSION="${VERSION#v}"

usage() {
	cat <<'USAGE'
Usage: InstallAmafu.sh <native|global|system> [VERSION]

	native  Install the runtime-independent release binary in /usr/local/bin.
	global  Install the Amafu .NET tool in the current user's global tool directory.
	system  Install the Amafu .NET tool in /usr/local/bin.

Use sudo for native and system modes. VERSION defaults to the current coordinated release.
USAGE
}

require_root() {
	if [[ "$(id -u)" -ne 0 ]]; then
		echo "InstallAmafu.sh: '$MODE' installation needs sudo." >&2
		exit 1
	fi
}

require_dotnet() {
	if ! command -v dotnet >/dev/null 2>&1; then
		echo "InstallAmafu.sh: dotnet is required for '$MODE' installation." >&2
		exit 1
	fi
}

install_dotnet_tool() {
	local scope=("$@")
	if dotnet tool update "${scope[@]}" Amafu --version "$VERSION"; then
		return
	fi
	dotnet tool install "${scope[@]}" Amafu --version "$VERSION"
}

install_native() {
	require_root
	if ! command -v curl >/dev/null 2>&1 || ! command -v unzip >/dev/null 2>&1; then
		echo "InstallAmafu.sh: native installation requires curl and unzip." >&2
		exit 1
	fi

	local platform architecture rid archive url tmpdir
	platform="$(uname -s)"
	architecture="$(uname -m)"
	case "$platform-$architecture" in
		Darwin-arm64) rid="osx-arm64" ;;
		Darwin-x86_64) rid="osx-x64" ;;
		Linux-aarch64|Linux-arm64) rid="linux-arm64" ;;
		Linux-x86_64) rid="linux-x64" ;;
		*)
			echo "InstallAmafu.sh: unsupported native platform: $platform-$architecture." >&2
			exit 1
			;;
	esac

	archive="amafu-v${VERSION}-${rid}.zip"
	url="https://github.com/Burkhardt/Amafu/releases/download/v${VERSION}/${archive}"
	tmpdir="$(mktemp -d)"
	trap "rm -rf '$tmpdir'" EXIT
	curl --fail --location "$url" --output "$tmpdir/$archive"
	curl --fail --location "${url}.sha256" --output "$tmpdir/${archive}.sha256"
	if command -v sha256sum >/dev/null 2>&1; then
		(cd "$tmpdir" && sha256sum --check "${archive}.sha256")
	else
		(cd "$tmpdir" && shasum -a 256 --check "${archive}.sha256")
	fi
	unzip -q "$tmpdir/$archive" -d "$tmpdir"
	install -m 0755 "$tmpdir/amafu" /usr/local/bin/amafu
	rm -rf "$tmpdir"
	trap - EXIT
	amafu --version
}

case "$MODE" in
	native)
		install_native
		;;
	global)
		require_dotnet
		install_dotnet_tool --global
		;;
	system)
		require_root
		require_dotnet
		install_dotnet_tool --tool-path /usr/local/bin
		;;
	-h|--help|help|"")
		usage
		;;
	*)
		echo "InstallAmafu.sh: unknown installation mode '$MODE'." >&2
		usage >&2
		exit 2
		;;
esac
