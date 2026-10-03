#!/usr/bin/env python3
"""
Convenience entry point for version bumping across the RAIkeep platform.
Delegates directly to validate-release.py --bump <version>.
"""

import subprocess
import sys
from pathlib import Path


def main():
	if len(sys.argv) < 2:
		print("Usage: python3 scripts/bump-version.py <new_version>")
		sys.exit(1)

	version = sys.argv[1].lstrip("v")
	script = Path(__file__).resolve().parent / "validate-release.py"
	res = subprocess.run([sys.executable, str(script), "--bump", version])
	sys.exit(res.returncode)


if __name__ == "__main__":
	main()
