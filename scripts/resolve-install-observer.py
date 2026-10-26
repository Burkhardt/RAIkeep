#!/usr/bin/env python3
"""Resolve fleet SSH logins from the shared RAIkeep configuration."""

from pathlib import Path
import argparse
import runpy
import sys


def observers(configuration: dict) -> list[dict]:
	items = configuration.get("Observers", [])
	if not isinstance(items, list) or any(not isinstance(item, dict) for item in items):
		raise ValueError("Observers must be an array of objects")
	return items


def resolve(name: str, configuration: dict) -> str:
	for observer in observers(configuration):
		target = observer.get("SshTarget", "")
		if not isinstance(target, str):
			raise ValueError("Observer SshTarget must be a string")
		if name.casefold() in {str(observer.get("Name", "")).casefold(), target.casefold(), target.rsplit("@", 1)[-1].casefold()}:
			if not target or target.startswith("-") or any(c.isspace() for c in target):
				raise ValueError(f"Observer {name!r} has an invalid SSH target")
			return target
	return name


def fleet(configuration: dict) -> list[str]:
	result = []
	seen = set()
	for observer in observers(configuration):
		name = observer.get("Name", "")
		if not isinstance(name, str) or not name or name.casefold() in seen or name.startswith("-") or any(c in name for c in "\r\n"):
			raise ValueError(f"Missing, duplicate, or invalid Observer name: {name!r}")
		resolve(name, configuration)  # Validate its SSH target before listing any destinations.
		seen.add(name.casefold())
		result.append(name)
	if not result:
		raise ValueError("No Observers configured. Add Observers or select an explicit target such as local.")
	return result


if __name__ == "__main__":
	arguments = argparse.ArgumentParser(description=__doc__)
	arguments.add_argument("name", nargs="?")
	arguments.add_argument("--config", type=Path, default=Path.home() / ".config/RAIkeep.json5")
	arguments.add_argument("--list", action="store_true")
	args = arguments.parse_args()
	args.config = args.config.expanduser()
	try:
		data = {}
		if args.config.exists():
			parser = Path(__file__).resolve().parent.parent / "JsonPit.Python/jsonpit/config.py"
			if parser.exists():
				loads = runpy.run_path(str(parser))["loads_json5"]
			else:
				from jsonpit.config import loads_json5 as loads
			data = loads(args.config.read_text())
			if not isinstance(data, dict):
				raise ValueError("RAIkeep configuration must be an object")
		if args.list:
			print("\n".join(fleet(data)))
		elif args.name:
			print(resolve(args.name, data))
		else:
			arguments.error("provide a target name or --list")
	except (ValueError, OSError, ImportError) as error:
		print(f"Cannot read Observer destinations from {args.config}: {error}", file=sys.stderr)
		sys.exit(2)
