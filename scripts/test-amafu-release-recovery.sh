#!/usr/bin/env bash
set -euo pipefail

source "$(dirname "${BASH_SOURCE[0]}")/release-chain.sh"

fixture_dir="$(mktemp -d "${TMPDIR:-/tmp}/amafu-recovery-test.XXXXXX")"
trap 'rm -rf "$fixture_dir"' EXIT
VER=4.5.13
RELEASE_PYTHON="$(command -v python3)"
release_log="$fixture_dir/release.log"

for rid in osx-arm64 osx-x64 linux-x64 linux-arm64 win-x64; do
	mkdir -p "$fixture_dir/artifacts/amafu-$rid"
	archive="$fixture_dir/artifacts/amafu-$rid/amafu-v4.5.13-$rid.zip"
	printf '%s\n' "$rid" > "$archive"
	printf '%s  %s\n' "$(sha256_of_file "$archive")" "$(basename "$archive")" > "$archive.sha256"
done

remote_tag_commit() { :; }
gh() {
	local args=" $* " destination previous arg
	if [[ "$args" == *" run view "* ]]; then
		if [[ "$args" == *" join("* ]]; then
			printf '%s\n' 'Checkout synchronized release notes'
		elif [[ "${FAIL_NATIVE:-0}" == 1 ]]; then
			printf '%s\n' '[{"name":"publish-nuget","conclusion":"success"},{"name":"NativeAOT osx-arm64","conclusion":"failure"},{"name":"NativeAOT osx-x64","conclusion":"success"},{"name":"NativeAOT linux-x64","conclusion":"success"},{"name":"NativeAOT linux-arm64","conclusion":"success"},{"name":"NativeAOT win-x64","conclusion":"success"},{"name":"publish-native-release","conclusion":"failure"}]'
		else
			printf '%s\n' '[{"name":"publish-nuget","conclusion":"success"},{"name":"NativeAOT osx-arm64","conclusion":"success"},{"name":"NativeAOT osx-x64","conclusion":"success"},{"name":"NativeAOT linux-x64","conclusion":"success"},{"name":"NativeAOT linux-arm64","conclusion":"success"},{"name":"NativeAOT win-x64","conclusion":"success"},{"name":"publish-native-release","conclusion":"failure"}]'
		fi
	elif [[ "$args" == *" run download "* ]]; then
		previous=""
		for arg in "$@"; do
			if [[ "$previous" == --dir ]]; then destination="$arg"; break; fi
			previous="$arg"
		done
		cp -R "$fixture_dir/artifacts/." "$destination/"
	elif [[ "$args" == *" release view "* ]]; then
		return 1
	elif [[ "$args" == *" release create "* || "$args" == *" release upload "* ]]; then
		printf '%s\n' "$args" >> "$release_log"
	else
		printf 'Unexpected gh call: %s\n' "$args" >&2
		return 1
	fi
}

recover_amafu_native_release 123 v4.5.13
[[ "$(wc -l < "$release_log" | tr -d ' ')" == 2 ]]
grep -q ' release create ' "$release_log"
grep -q ' release upload ' "$release_log"

: > "$release_log"
FAIL_NATIVE=1
if recover_amafu_native_release 123 v4.5.13; then
	echo 'A failed native build must not be recovered.' >&2
	exit 1
fi
[[ ! -s "$release_log" ]]

echo 'Amafu release recovery checks passed.'
