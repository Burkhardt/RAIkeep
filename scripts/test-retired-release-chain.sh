#!/usr/bin/env bash
set -euo pipefail

if output="$(bash "$(dirname "$0")/release-chain.sh" 4.7.1 2>&1)"; then
	echo "The retired release chain unexpectedly succeeded." >&2
	exit 1
fi
[[ "$output" == *"legacy release chain is retired"* ]]
printf 'Retired release-chain guard passed.\n'
