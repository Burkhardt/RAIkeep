#!/usr/bin/env python3
"""Write one version's GitHub Release body from a consolidated major file."""

from pathlib import Path
import re
import sys


def extract(source: Path, version: str) -> str:
	text = source.read_text(encoding="utf-8")
	sections = list(re.finditer(r"^## (\d+(?:\.\d+)+)$", text, re.MULTILINE))
	matches = [index for index, section in enumerate(sections) if section.group(1) == version]
	if len(matches) != 1:
		raise ValueError(f"Expected exactly one '## {version}' section in {source}; found {len(matches)}.")
	index = matches[0]
	start = sections[index].start()
	end = sections[index + 1].start() if index + 1 < len(sections) else len(text)
	body = text[start:end].strip()
	return re.sub(r"\n+---\s*$", "", body).rstrip() + "\n"


def main() -> int:
	if len(sys.argv) != 4:
		print("Usage: extract-release-notes.py <major-file.md> <version> <output.md>", file=sys.stderr)
		return 2
	source, version, destination = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
	try:
		body = extract(source, version)
	except (OSError, ValueError) as error:
		print(error, file=sys.stderr)
		return 1
	destination.write_text(body, encoding="utf-8")
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
