#!/usr/bin/env python3
"""Read-only CR077 historical-source acceptance; no application checkout is changed."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

REFS = ("1710524", "8ef1bb3", "2a66ee4", "fbf5d32")


def main():
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("--source", type=Path, required=True, help="AfricaStage git checkout (read-only)")
	parser.add_argument("--output", type=Path, required=True)
	args = parser.parse_args()
	root = Path(__file__).resolve().parent.parent
	rail = root / "RaiGuard/rail/bin/Debug/net10.0/rail.dll"
	results = []
	for ref in REFS:
		with tempfile.TemporaryDirectory(prefix="cr077-history-") as folder:
			folder = Path(folder)
			commit = subprocess.check_output(["git", "-C", str(args.source), "rev-parse", ref], text=True).strip()
			paths = subprocess.check_output(["git", "-C", str(args.source), "ls-tree", "-r", "--name-only", ref, "--", "AfricaStage.Api"], text=True).splitlines()
			for name in paths:
				if not name.endswith(".cs"): continue
				target = folder / name; target.parent.mkdir(parents=True, exist_ok=True)
				text = subprocess.check_output(["git", "-C", str(args.source), "show", f"{ref}:{name}"], text=True)
				# Preserve line count. Remove only the rule suppressions under assessment.
				text = "\n".join("" if line.strip().startswith(("#pragma warning disable RAI011", "#pragma warning restore RAI011")) else line for line in text.splitlines())
				target.write_text(text)
			assets = args.source / "AfricaStage.Api/obj/project.assets.json"
			if assets.is_file():
				target = folder / "AfricaStage.Api/obj/project.assets.json"; target.parent.mkdir(parents=True, exist_ok=True); target.write_bytes(assets.read_bytes())
			sentinel = folder / "Cr077Sentinel.cs"
			sentinel.write_text('using JsonPit; class Cr077Sentinel { void Check(Pit p) { p.Add(p.GetAt("x", System.DateTimeOffset.UtcNow)); } }')
			run = subprocess.run(["dotnet", str(rail), "check", str(folder), "--rule", "RAI011", "--json", "-n"], capture_output=True, text=True, timeout=120)
			if run.returncode not in (0, 1): raise RuntimeError(run.stdout + run.stderr)
			findings = json.loads(run.stdout)
			controls = [f for f in findings if Path(f["File"]).name == "Cr077Sentinel.cs"]
			assert len(controls) == 1, "Semantic positive control failed: no historical-source accuracy claim is valid"
			findings = [f for f in findings if Path(f["File"]).name != "Cr077Sentinel.cs"]
			for finding in findings: finding["File"] = str(Path(finding["File"]).relative_to(folder))
			sites = []
			for file, token in [("Controllers/ActivityController.cs", "acts.Add(item)"), ("Controllers/ObjectController.cs", "classItems.Add(item)"), ("Services/UseCaseInstantiator.cs", "_activityPit.Add(item)")]:
				text = (folder / "AfricaStage.Api" / file).read_text()
				lines = [index for index, line in enumerate(text.splitlines(), 1) if token in line]
				assert lines, f"Missing real fixture: {ref}:{file}"
				assert not any(f["File"] == "AfricaStage.Api/" + file and f["Line"] in lines for f in findings)
				sites.append({"File": file, "Lines": lines})
			results.append({"Ref": ref, "Commit": commit, "SourceFiles": len([p for p in paths if p.endswith('.cs')]), "Findings": findings, "PositiveControlCount": len(controls), "RealSites": sites, "ResolutionNotes": run.stderr.strip()})
	args.output.write_text(json.dumps(results, indent=2))
	for result in results: print(f"{result['Ref']}: {result['SourceFiles']} original source files, {len(result['Findings'])} proven RAI011 findings")
	return 0


if __name__ == "__main__": raise SystemExit(main())
