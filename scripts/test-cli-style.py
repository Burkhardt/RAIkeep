#!/usr/bin/env python3
"""Verify C#/Python ANSI parity and shared pits/jpit help options using local builds."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from xml.sax.saxutils import escape


def main() -> int:
	parser = argparse.ArgumentParser(description=__doc__)
	parser.parse_args()
	root = Path(__file__).resolve().parent.parent
	sys.path.insert(0, str(root / "JsonPit.Python"))
	from jsonpit import cli_style as style
	from jsonpit.icons import Icons

	assembly = root / "OsLib/bin/Debug/net10.0/OsLib.dll"
	if not assembly.is_file():
		parser.error("Build RAIkeep.slnx before running this check.")
	cases = [
		"<tenant|path>", "(<PitName>|--wwwa)", "(--out-dir <dir>|--json)",
		"[-a|--all]", "[-c <cloud>]", "[(-r|--pitroot) <dir>]",
		"e.g. 'pits seed Activity --source patch.json5 -r <root>' seeds Activity",
		"(for piping to jq, grep, etc.)", "-w, --window", "-x, --id-exists",
		"<ISO-8601 timestamp>", "<file|->", "'single-file.json'", "",
	]
	providers = ["OneDrive", "Dropbox", "GoogleDrive", "ICloudDrive", "GoogleDriveOther"]
	with tempfile.TemporaryDirectory(prefix="raikeep-cli-style-") as temporary:
		directory = Path(temporary)
		project = directory / "StyleProbe.csproj"
		project.write_text('<Project Sdk="Microsoft.NET.Sdk"><PropertyGroup><OutputType>Exe</OutputType>'
			'<TargetFramework>net10.0</TargetFramework><ImplicitUsings>enable</ImplicitUsings>'
			'<UseAppHost>false</UseAppHost></PropertyGroup><ItemGroup><Reference Include="OsLib">'
			f'<HintPath>{escape(str(assembly))}</HintPath></Reference></ItemGroup></Project>')
		(directory / "Program.cs").write_text('''using System.Text.Json;
using OsLib;
var input = JsonSerializer.Deserialize<string[]>(Console.In.ReadToEnd())!;
var providers = new[] { "OneDrive", "Dropbox", "GoogleDrive", "ICloudDrive", "GoogleDriveOther" };
Console.Write(JsonSerializer.Serialize(new {
 syntax = input.Select(text => CliHelpStyle.Syntax(text, "36", true)).ToArray(),
 banner = CliHelpStyle.Banner("\\uea74 CLI (v1.2.3)", true),
 cloud = CliHelpStyle.CloudOptions(providers, true),
 rows = CliHelpStyle.Rows(new[] {
  new CliHelpStyle.Row("-c, --cloud", "\\uea83", "", providers),
  new CliHelpStyle.Row("--patch", "\\uea74", "alias for --id-exists") }, true).ToArray()
}));
''')
		build = subprocess.run(["dotnet", "build", str(project), "--nologo", "-v", "quiet"],
			capture_output=True, text=True, timeout=120)
		if build.returncode:
			raise RuntimeError(build.stdout + build.stderr)
		probe = subprocess.run(["dotnet", str(directory / "bin/Debug/net10.0/StyleProbe.dll")],
			input=json.dumps(cases), capture_output=True, text=True, check=True, timeout=30)
		actual = json.loads(probe.stdout)
		expected = {
			"syntax": [style.syntax(text) for text in cases],
			"banner": style.banner(f"{Icons.INFO} CLI (v1.2.3)", True),
			"cloud": style.cloud_options(providers, True),
			"rows": style.rows([style.Row("-c, --cloud", Icons.FOLDER, "", providers),
				style.Row("--patch", Icons.INFO, "alias for --id-exists")], True),
		}
		assert actual == expected, "C# and Python help styles differ"

	pits = subprocess.run(["dotnet", str(root / "PitSeeder/pits/bin/Debug/net10.0/pits.dll"), "-h", "-n"],
		capture_output=True, text=True, check=True, timeout=30).stdout
	# Import the checkout rather than an installed package. Neither help command mutates pits.
	python_help = subprocess.run([sys.executable, "-m", "jsonpit.cli", "-h", "-n"],
		cwd=root / "JsonPit.Python", capture_output=True, text=True, check=True, timeout=30).stdout
	labels = ["-h, --help", "-v, --version", "-n, --nologo", "-b, --debug", "-r, --pitroot",
		"-c, --cloud", "-s, --source", "--json", "--at", "--wwwa", "-w, --window", "-x, --id-exists", "--patch"]
	for label in labels:
		csharp = next(line for line in pits.splitlines() if line.startswith(label))
		python = next(line for line in python_help.splitlines() if line.startswith(label))
		assert csharp == python, f"Shared option differs: {label}\n{csharp}\n{python}"
	for output in [pits, python_help]:
		assert "\t" not in output and "\033" not in output
		assert "list (ls)" not in output
		for hidden in ["--retain-window", "--require-exist", "positional argument:"]:
			assert hidden not in output, f"Unadvertised alias/explanation leaked: {hidden}"

	# Export the same actual C#-written pits through both CLIs. These are explicit
	# local filesystem fixtures, not simulated CloudDrive integration tests.
	python_command = [sys.executable, "-m", "jsonpit.cli"]
	pits_command = ["dotnet", str(root / "PitSeeder/pits/bin/Debug/net10.0/pits.dll")]
	environment = os.environ.copy()
	environment["PYTHONPATH"] = str(root / "JsonPit.Python")
	def invoke(command: list[str]) -> str:
		result = subprocess.run(command, env=environment, capture_output=True, text=True, timeout=30)
		assert result.returncode == 0, f"{command}: {result.stdout}\n{result.stderr}"
		return result.stdout
	def normalize(document):
		# Newtonsoft and Python use equivalent +00:00/Z timestamp spellings.
		# Compare fixture timestamps as instants, while retaining every data field.
		if isinstance(document, list): return [normalize(item) for item in document]
		if not isinstance(document, dict): return document
		result = {key: normalize(value) for key, value in document.items()}
		for key in ["Modified", "at"]:
			if isinstance(result.get(key), str):
				result[key] = datetime.fromisoformat(result[key].replace("Z", "+00:00")).astimezone(timezone.utc).isoformat()
		return result
	with tempfile.TemporaryDirectory(prefix="raikeep-export-parity-") as temporary:
		fixture = Path(temporary)
		data = fixture / "data"
		data.mkdir()
		items = {
			"Person": {"Id": "Customer1"}, "Object": {"Id": "Order1"}, "Place": {"Id": "Office1"},
			"Activity": {"Id": "CreateOrder1", "Who": {"Owner": "Customer1"},
				"What": {"Orders": ["Order1"], "Missing": "Unknown"}, "Where": {"Office": "Office1"}},
		}
		for name, item in items.items():
			source = fixture / f"{name}.json"
			source.write_text(json.dumps([item]), encoding="utf-8")
			invoke([*pits_command, "seed", name, "--source", str(source), "-r", str(data), "-n"])
		for index, target in enumerate([["Person"], ["--wwwa"], ["Person", "--at", "2030-01-01T02:00:00+02:00"]]):
			name = "wwwa" if "--wwwa" in target else "Person"
			actual = []
			for implementation, command in [("csharp", pits_command), ("python", python_command)]:
				destination = fixture / f"{implementation}-{index}"
				invoke([*command, "export", *target, "-r", str(data), "--out-dir", str(destination), "-n"])
				document = json.loads((destination / f"{name}.json").read_text(encoding="utf-8-sig"))
				if "_export" in document: document["_export"].pop("exported")
				actual.append(normalize(document))
			assert actual[0] == actual[1], f"Directory-export parity differs for {target}:\npits: {actual[0]!r}\njpit: {actual[1]!r}"
	print(f"CLI parity passed: {len(cases)} syntax cases, banner, cloud badges, rows, {len(labels)} shared options, and 3 directory exports.")
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
