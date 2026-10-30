#!/usr/bin/env python3
"""Keep standalone Amafu's dependency-free CLI formatter identical to OsLib's."""
import argparse
from pathlib import Path


def main() -> int:
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("--check", action="store_true", help="report drift without writing")
	args = parser.parse_args()
	root = Path(__file__).resolve().parent.parent
	source = (root / "OsLib/CliHelpStyle.cs").read_bytes()
	target = root / "Amafu/amafu/Shared/CliHelpStyle.cs"
	if target.exists() and target.read_bytes() == source:
		print("CLI style source copies match.")
		return 0
	if args.check:
		print("CLI style source drift: run python3 scripts/sync-cli-style.py")
		return 1
	target.parent.mkdir(parents=True, exist_ok=True)
	target.write_bytes(source)
	print("Synchronized Amafu's standalone CLI style source.")
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
