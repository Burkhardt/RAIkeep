"""Find source files in the working trees pinned by the umbrella repository."""
from pathlib import Path
import subprocess


def sources(root: Path, *patterns: str) -> list[Path]:
    projects = [root]
    for entry in subprocess.check_output(["git", "ls-files", "--stage", "-z"], cwd=root).split(b"\0"):
        if entry.startswith(b"160000 "):
            project = root / entry.split(b"\t", 1)[1].decode()
            if not (project / ".git").exists():
                raise RuntimeError(f"Missing submodule checkout: {project}")
            projects.append(project)

    files = []
    for project in projects:
        names = subprocess.check_output(
            ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z", *patterns],
            cwd=project,
        ).decode().split("\0")
        files.extend(project / name for name in names
                     if name and (project / name).is_file())
    return sorted(set(files))
