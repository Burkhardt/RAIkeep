"""Check each C# project's compiler inputs with the Rail built from this checkout."""
import argparse
import json
from pathlib import Path
import subprocess
import sys

from guardrail_sources import sources


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-restore", action="store_true", help="Use already restored build assets")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    rail = root / "RaiGuard/rail/rail.csproj"
    build = ["dotnet", "build", rail, "-m:1", "-p:UseLocalRAIkeepSources=true"]
    if args.no_restore:
        build.append("--no-restore")
    subprocess.run(build, cwd=root, check=True)
    dll = subprocess.check_output(
        ["dotnet", "msbuild", rail, "-getProperty:TargetPath"], cwd=root, text=True
    ).strip()

    failures = 0
    for project in sources(root, "*.csproj"):
        if project.relative_to(root).as_posix() in {"OsLib/OsLib.csproj", "Amafu/amafu/amafu.csproj"}:
            continue
        items = json.loads(subprocess.check_output(
            ["dotnet", "msbuild", project, "-getItem:Compile"], cwd=root, text=True
        ))["Items"]["Compile"]
        files = [Path(item["FullPath"]) for item in items]
        if not files:
            continue  # Packaging-only project.
        result = subprocess.run(["dotnet", dll, "check", "--json", *files], cwd=root, stdout=subprocess.PIPE)
        if result.returncode not in (0, 1):
            return result.returncode
        findings = json.loads(result.stdout)
        for finding in findings:
            print(f"{finding['File']}:{finding['Line']}:{finding['Column']} {finding['RuleId']} {finding['Message']}")
        print(f"{project.relative_to(root)}: {len(findings)} findings", flush=True)
        failures += len(findings)
    print(f"Rail findings across projects: {failures}")
    return int(bool(failures))


if __name__ == "__main__":
    sys.exit(main())
