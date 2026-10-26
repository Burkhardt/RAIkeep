#!/usr/bin/env python3
"""Verify that an OsLibCore package ships the documented public pits contract."""

import argparse
from pathlib import Path
import xml.etree.ElementTree as ET
import zipfile


def verify(package: Path) -> None:
	with zipfile.ZipFile(package) as archive:
		paths = [name for name in archive.namelist() if name.endswith("/OsLib.xml")]
		if len(paths) != 1:
			raise ValueError(f"Expected one packaged OsLib.xml; found {paths}.")
		root = ET.fromstring(archive.read(paths[0]))
	members = {node.attrib["name"]: node for node in root.findall("members/member")}
	expected = {}
	for name, properties in {
		"PitsCommandOptions": "Tenant PitRoot CloudProvider RemoteTarget Debug NoLogo RetainWindow",
		"PitsSeedRequest": "Target Source StandardInput RequireExisting Options",
		"PitsTarget": "PitName IsWwwa",
		"PitsCommand": "CandidateExecutables",
	}.items():
		expected[f"T:OsLib.{name}"] = 1
		for prop in properties.split():
			expected[f"P:OsLib.{name}.{prop}"] = 1
	for name, methods in {
		"PitsSeedRequest": "ForPit FromStandardInput ForWwwa",
		"PitsTarget": "Pit Wwwa",
		"PitsCommand": "#ctor ForManagedAssembly OverSsh BuildSeedArguments BuildExportArguments BuildAuditArguments BuildDeletePropertyArguments BuildDeleteItemArguments BuildMaintainArguments Seed SeedAsync Export ExportAsync Audit AuditAsync DeleteProperty DeletePropertyAsync DeleteItem DeleteItemAsync Maintain MaintainAsync Run RunAsync",
	}.items():
		for method in methods.split():
			expected[f"M:OsLib.{name}.{method}"] = 2 if method in {"Run", "RunAsync"} else 1
	errors = []
	for name, count in expected.items():
		matching = [node for key, node in members.items() if key.split("(", 1)[0] == name]
		if len(matching) != count or any(not "".join(node.findtext("summary", default="")).strip() for node in matching):
			errors.append(f"{name}: expected {count} documented contract member(s), found {len(matching)}.")
	seed = members.get("T:OsLib.PitsSeedRequest")
	if seed is None or "Tenant" not in "".join(seed.find("example").itertext() if seed.find("example") is not None else []):
		errors.append("PitsSeedRequest must ship a factory/with-expression example including Tenant.")
	if errors:
		raise ValueError("\n".join(errors))
	print(f"Verified {sum(expected.values())} public pits XML contracts in {package.name}.")


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("package", type=Path)
	verify(parser.parse_args().package)
