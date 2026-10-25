#!/usr/bin/env python3
"""Exercise the installer with fake package managers and an isolated home."""

import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent.parent
INSTALLER = (ROOT / "scripts/install-clis.sh").read_text()
START = INSTALLER.index("install_jpit() {")
END = INSTALLER.index("\n}\ninstall_jpit", START) + 2
FUNCTION = INSTALLER[START:END]


class PythonInstallerTests(unittest.TestCase):
	def invoke(self, pipx_body: str | None):
		with tempfile.TemporaryDirectory(prefix="raikeep-installer-test-") as temporary:
			root = Path(temporary)
			bin_dir = root / "mock-bin"
			bin_dir.mkdir()
			def command(name, body):
				path = bin_dir / name
				path.write_text("#!/bin/bash\n" + body)
				path.chmod(0o755)
			command("python3", 'if [[ "$*" == "-m site --user-base" ]]; then echo "$HOME/.local"; exit 0; fi; exit 1\n')
			command("pip3", 'echo SYSTEM_PIP_CALLED >> "$INSTALL_TEST_LOG"; exit 1\n')
			if pipx_body is not None:
				command("pipx", pipx_body)
			env = os.environ.copy()
			env.update(HOME=str(root), PATH=str(bin_dir) + ":/usr/bin:/bin", INSTALL_TEST_LOG=str(root / "calls"))
			result = subprocess.run(["/bin/bash", "-c", "set -euo pipefail\nVERSION=4.5.13\n" + FUNCTION + "\ninstall_jpit"], env=env, text=True, capture_output=True)
			log = (root / "calls").read_text() if (root / "calls").exists() else ""
			return result, log

	def test_pipx_installs_one_pinned_environment_and_both_commands(self):
		result, log = self.invoke('''echo "$*" >> "$INSTALL_TEST_LOG"
for name in jpit jsonpit; do
  mkdir -p "$HOME/.local/bin"
  printf '#!/bin/bash\necho "%s v4.5.13"\n' "$name" > "$HOME/.local/bin/$name"
  chmod +x "$HOME/.local/bin/$name"
done
''')
		self.assertEqual(0, result.returncode, result.stderr)
		self.assertEqual("install --force jsonpit==4.5.13\n", log)

	def test_package_manager_failure_does_not_fall_back_to_system_pip(self):
		result, log = self.invoke("exit 1\n")
		self.assertNotEqual(0, result.returncode)
		self.assertNotIn("SYSTEM_PIP_CALLED", log)

	def test_missing_isolation_tools_fail_without_bypassing_pep668(self):
		result, log = self.invoke(None)
		self.assertNotEqual(0, result.returncode)
		self.assertIn("Install pipx or Python venv support", result.stdout)
		self.assertNotIn("SYSTEM_PIP_CALLED", log)


if __name__ == "__main__":
	unittest.main()
