#!/usr/bin/env python3
"""Verify fleet routing without contacting hosts or installing packages."""

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent.parent


class FleetRoutingTests(unittest.TestCase):
	def invoke(self, targets, windows_ready=True, skip_python=False, configuration=None, execute_unix=False, dry_run=True):
		with tempfile.TemporaryDirectory(prefix="raikeep-routing-") as temporary:
			root = Path(temporary)
			(root / "scripts").mkdir()
			for name in ("install-clis.sh", "install-clis-windows.ps1", "resolve-install-observer.py"):
				shutil.copyfile(ROOT / "scripts" / name, root / "scripts" / name)
			parser = root / "JsonPit.Python/jsonpit/config.py"
			parser.parent.mkdir(parents=True)
			shutil.copyfile(ROOT / "JsonPit.Python/jsonpit/config.py", parser)
			(root / ".config").mkdir()
			(root / ".config/RAIkeep.json5").write_text(configuration if configuration is not None else """{
  Observers: [
    {Name: 'Themba', SshTarget: 'worker@Themba'},
    {Name: 'Ixhiba', SshTarget: 'administrator@Ixhiba'},
  ],
}""")
			mock_bin = root / "bin"
			mock_bin.mkdir()
			ssh = mock_bin / "ssh"
			ssh.write_text("#!" + sys.executable + "\n" + r'''
import base64, json, os, pathlib, sys
host, command = sys.argv[-2:]
with open(os.environ['ROUTING_LOG'], 'a') as log:
    log.write(json.dumps({'host': host, 'command': command}) + '\n')
if command == 'uname -s':
    if host.lower().endswith('@ixhiba'): sys.exit(127)
    print('Linux')
elif command.startswith('powershell.exe '):
    script = base64.b64decode(command.split()[-1]).decode('utf-16-le')
    assert '-DryRun' in script
    assert '[Console]::In.ReadToEnd()' in script
    assert len(command) < 2000
    assert 'Find-RaiKeepPython' in sys.stdin.read()
    ready = os.environ['WINDOWS_READY'] == '1' or '-SkipPython' in script
    print(json.dumps({'Environment': 'Windows', 'Ready': ready}))
    sys.exit(0 if ready else 2)
elif command.startswith('bash -s -- ') or command.startswith('wsl.exe --exec /bin/bash -s -- '):
    payload = sys.stdin.read()
    assert 'DRY_RUN="$3"' in payload
    if os.environ.get('EXECUTE_UNIX') == '1':
        import subprocess
        env = dict(os.environ, PATH=os.environ['REMOTE_MOCK_BIN'] + ':' + os.environ['PATH'])
        result = subprocess.run(['/bin/bash', '-s', '--', *command.split()[3:]], input=payload, text=True, env=env)
        sys.exit(result.returncode)
    else:
        assert command.split()[-2] == '1', command
        print('Unix prerequisite check: ready')
else:
    raise AssertionError(command)
''')
			ssh.chmod(0o755)
			remote_bin = root / "remote-bin"
			remote_bin.mkdir()
			(remote_bin / "python3").write_text('#!/bin/bash\necho UNEXPECTED_PYTHON >> "$ROUTING_LOG"\nexit 99\n')
			(remote_bin / "python3").chmod(0o755)
			(remote_bin / "dotnet").write_text('''#!/bin/bash
if [[ "$1" == "--version" ]]; then echo 10.0.401; exit 0; fi
case "$4" in Amafu) name=amafu;; RaidSeeder) name=raid;; ImgSeeder) name=iorg;; PitSeeder) name=pits;; RaiGuard) name=rail;; *) exit 1;; esac
mkdir -p "$HOME/.dotnet/tools"
printf '#!/bin/bash\\necho "%s v4.5.14"\\n' "$name" > "$HOME/.dotnet/tools/$name"
chmod +x "$HOME/.dotnet/tools/$name"
''')
			(remote_bin / "dotnet").chmod(0o755)
			# The payload deliberately puts ~/.dotnet ahead of the inherited PATH.
			# Put both mocks there too, so no real package manager can be reached.
			(root / ".dotnet").mkdir()
			for executable in ("dotnet", "python3"):
				(root / ".dotnet" / executable).symlink_to(remote_bin / executable)
			env = os.environ | {"HOME": str(root), "PATH": str(mock_bin) + ":" + os.environ["PATH"],
				"ROUTING_LOG": str(root / "calls"), "WINDOWS_READY": "1" if windows_ready else "0",
				"EXECUTE_UNIX": "1" if execute_unix else "0", "REMOTE_MOCK_BIN": str(remote_bin)}
			flags = ["--no-cloud-setup"]
			if dry_run: flags.append("--dry-run")
			if skip_python: flags.append("--skip-python")
			result = subprocess.run(["bash", str(root / "scripts/install-clis.sh"), "4.5.14", *targets,
				*flags], env=env, text=True, capture_output=True)
			log = (root / "calls").read_text() if (root / "calls").exists() else ""
			self.assertNotIn("UNEXPECTED_PYTHON", log, result.stdout + result.stderr)
			calls = [json.loads(line) for line in log.splitlines()]
			return result, calls

	def test_themba_default_uses_configured_login_and_unix_environment(self):
		result, calls = self.invoke(["Themba"])
		self.assertEqual(0, result.returncode, result.stderr)
		self.assertTrue(all(call["host"] == "worker@Themba" for call in calls))
		self.assertTrue(calls[-1]["command"].startswith("bash -s -- "))

	def test_themba_windows_is_a_separate_explicit_environment(self):
		result, calls = self.invoke(["Themba", "Themba:windows"])
		self.assertEqual(0, result.returncode, result.stderr)
		self.assertTrue(calls[-1]["command"].startswith("powershell.exe "))
		self.assertEqual("worker@Themba", calls[-1]["host"])

	def test_ixhiba_auto_routes_to_native_powershell(self):
		result, calls = self.invoke(["Ixhiba"])
		self.assertEqual(0, result.returncode, result.stderr)
		self.assertEqual("administrator@Ixhiba", calls[-1]["host"])
		self.assertTrue(calls[-1]["command"].startswith("powershell.exe "))

	def test_ixhiba_wsl_is_explicit_and_does_not_install_a_distribution(self):
		result, calls = self.invoke(["Ixhiba:wsl"])
		self.assertEqual(0, result.returncode, result.stderr)
		self.assertTrue(calls[-1]["command"].startswith("wsl.exe --exec /bin/bash -s -- "))
		self.assertFalse(any("--install" in call["command"] for call in calls))

	def test_missing_windows_prerequisites_fail_the_check(self):
		result, calls = self.invoke(["Ixhiba"], windows_ready=False)
		self.assertNotEqual(0, result.returncode)
		self.assertIn("Failed/Skipped : Ixhiba", result.stdout)

	def test_default_fleet_comes_entirely_from_observers(self):
		config = """{Observers: [
  {Name:'ComputeOne', SshTarget:'worker@alpha.example'},
  {Name:'ComputeTwo', SshTarget:'worker@beta.example'},
]}"""
		result, calls = self.invoke([], configuration=config)
		self.assertEqual(0, result.returncode, result.stderr)
		self.assertEqual({"worker@alpha.example", "worker@beta.example"}, {c["host"] for c in calls})

	def test_empty_observers_fail_without_contacting_a_hardcoded_fleet(self):
		result, calls = self.invoke(["all"], configuration="{Observers: []}")
		self.assertNotEqual(0, result.returncode)
		self.assertEqual([], calls)
		self.assertIn("No Observers configured", result.stderr)

	def test_duplicate_observers_fail_before_contacting_servers(self):
		config = """{Observers: [
  {Name:'ServerNode', SshTarget:'worker@alpha.example'},
  {Name:'servernode', SshTarget:'worker@beta.example'},
]}"""
		result, calls = self.invoke(["all"], configuration=config)
		self.assertNotEqual(0, result.returncode)
		self.assertEqual([], calls)
		self.assertIn("duplicate", result.stderr)

	def test_malformed_observers_have_a_clear_error(self):
		result, calls = self.invoke(["all"], configuration="{Observers: {Name:'ServerNode'}}")
		self.assertNotEqual(0, result.returncode)
		self.assertEqual([], calls)
		self.assertIn("Observers must be an array", result.stderr)

	def test_skip_python_allows_windows_without_python(self):
		result, calls = self.invoke(["Ixhiba"], windows_ready=False, skip_python=True)
		self.assertEqual(0, result.returncode, result.stderr)

	def test_unix_dry_run_without_python(self):
		result, calls = self.invoke(["Themba"], skip_python=True, execute_unix=True)
		self.assertEqual(0, result.returncode, result.stdout + result.stderr)
		self.assertIn("no Python is required", result.stdout)

	def test_unix_dotnet_only_install_never_invokes_python(self):
		result, calls = self.invoke(["Themba"], skip_python=True, execute_unix=True, dry_run=False)
		self.assertEqual(0, result.returncode, result.stdout + result.stderr)
		self.assertIn("existing Python tools are unchanged", result.stdout)


if __name__ == "__main__":
	unittest.main()
