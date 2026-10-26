using System.Text;
using Newtonsoft.Json.Linq;
using OsLib;

namespace Amafu.Observer.Tests;

/// <summary>
/// Live tests of the documented Windows/WSL setup. Run scripts/test-amafu-wsl.sh;
/// cloud paths come from the observer's Amafu discovery, never from fixtures.
/// </summary>
[Trait("Category", "LiveCloud")]
public sealed class WindowsWslCloudTests(WslObserver observer, ITestOutputHelper output)
	: IClassFixture<WslObserver>
{
	[Fact]
	public void DetectionAndInitPreview_UseCleanPathsWithoutChangingConfiguration()
	{
		observer.RequireEnabled();
		var before = observer.ConfigurationState();
		var detection = observer.Detect();
		var providers = (JArray)detection["providers"]!;
		Assert.NotEmpty(providers);
		var preview = JObject.Parse(observer.Run(observer.Amafu + " init --create-links --dry-run"));
		foreach (var provider in providers.OfType<JObject>())
		{
			var name = (string)provider["name"]!;
			Assert.Equal($"~/.CloudStorage/{name}/", (string?)preview["Cloud"]?[name]);
			output.WriteLine($"{name}: {provider["path"]} -> {preview["Cloud"]?[name]}");
		}
		Assert.Equal(before, observer.ConfigurationState());
	}

	[Theory]
	[InlineData("GoogleDrive")]
	[InlineData("OneDrive")]
	public void CloudFiles_RoundTripBetweenWslAndWindows(string family)
	{
		observer.RequireEnabled();
		var providers = ((JArray)observer.Detect()["providers"]!).OfType<JObject>()
			.Where(p => (string?)p["provider"] == family).ToArray();
		Assert.True(providers.Length > 0,
			$"{family} is not discoverable on the observer. Check its configured path and Windows drive mount.");
		foreach (var provider in providers)
		{
			var payload = Convert.ToBase64String(Encoding.UTF8.GetBytes(provider.ToString()));
			var script = "python3 - " + WslObserver.Quote(payload) + " <<'PY'\n" + RoundTripScript + "\nPY";
			var result = JObject.Parse(observer.Run(script));
			Assert.True((bool)result["roundTrip"]!);
			Assert.True((bool)result["cleaned"]!);
			output.WriteLine(result.ToString());
		}
	}

	[Fact]
	public void ExistingUserShells_CanReadAndWriteCloudsInEveryMountNamespace()
	{
		observer.RequireEnabled();
		var providers = (JArray)observer.Detect()["providers"]!;
		Assert.NotEmpty(providers);
		var payload = Convert.ToBase64String(Encoding.UTF8.GetBytes(providers.ToString()));
		var result = JObject.Parse(observer.Run("python3 - " + WslObserver.Quote(payload)
			+ " <<'PY'\n" + NamespaceScript + "\nPY"));
		Assert.True((bool)result["success"]!, result.ToString());
		Assert.NotEmpty((JArray)result["checks"]!);
		output.WriteLine(result.ToString());
	}

	// WSL can expose different Windows-drive mounts to SSH and interactive shells.
	// Root is used only to enter an existing namespace; cloud I/O runs as the user.
	private const string NamespaceScript = """"
import base64, json, os, subprocess, sys
payload = json.loads(base64.b64decode(sys.argv[1]))
context = {'providers': payload, 'uid': os.getuid(), 'gid': os.getgid(), 'home': os.path.expanduser('~')}
root_script = r'''
import base64, json, os, pathlib, subprocess, sys
context = json.loads(base64.b64decode(sys.argv[1]))
namespaces = {}
for p in sorted(pathlib.Path('/proc').iterdir(), key=lambda p: int(p.name) if p.name.isdigit() else -1):
    if not p.name.isdigit(): continue
    try:
        if p.stat().st_uid != context['uid']: continue
        if (p / 'comm').read_text().strip() not in ('bash', 'zsh', 'fish'): continue
        namespace = os.readlink(p / 'ns/mnt')
        namespaces.setdefault(namespace, p.name)
    except OSError:
        continue
if not namespaces: raise RuntimeError('No existing user shell mount namespaces found')
probe_script = r"""
import base64, json, os, pathlib, shutil, sys, uuid
providers = json.loads(base64.b64decode(sys.argv[1]))
checks = []
for provider in providers:
    root = pathlib.Path(os.path.expanduser(provider['path']))
    with os.scandir(root) as entries:
        next(entries, None)
    run = root / 'RAIkeep' / 'amafu-wsl-tests' / uuid.uuid4().hex
    run.mkdir(parents=True, exist_ok=False)
    try:
        marker = run / 'namespace.txt'
        token = uuid.uuid4().hex
        marker.write_text(token, encoding='utf-8')
        assert marker.read_text(encoding='utf-8') == token
    finally:
        shutil.rmtree(run)
    checks.append({'provider': provider['name'], 'namespace': os.readlink('/proc/self/ns/mnt'),
                   'uid': os.getuid(), 'readWrite': True, 'cleaned': not run.exists()})
print(json.dumps(checks))
"""
encoded_probe = base64.b64encode(probe_script.encode()).decode('ascii')
providers = base64.b64encode(json.dumps(context['providers']).encode()).decode('ascii')
checks = []
for namespace, pid in namespaces.items():
    command = ['nsenter', '--target', pid, '--mount', '--', 'setpriv',
               '--reuid', str(context['uid']), '--regid', str(context['gid']), '--init-groups',
               'env', 'HOME=' + context['home'],
               'python3', '-c', "exec(__import__('base64').b64decode('" + encoded_probe + "'))", providers]
    result = subprocess.run(command, capture_output=True, text=True, timeout=30)
    if result.returncode:
        raise RuntimeError(namespace + ' failed: ' + result.stderr)
    checks.extend(json.loads(result.stdout))
print(json.dumps({'success': True, 'checks': checks}))
'''
encoded_context = base64.b64encode(json.dumps(context).encode()).decode('ascii')
result = subprocess.run(['wsl.exe', '--distribution', os.environ['WSL_DISTRO_NAME'], '--user', 'root',
                         '--exec', '/usr/bin/python3', '-', encoded_context], input=root_script,
                        capture_output=True, text=True, timeout=90)
if result.returncode:
    raise RuntimeError('Interactive namespace check failed: ' + result.stderr)
print(result.stdout)
"""";

	// The probe lives inside the discovered cloud tree. Windows must read the WSL
	// bytes and write a response that WSL can read. Only this unique run is removed.
	private const string RoundTripScript = """
import base64, json, os, pathlib, re, shutil, subprocess, sys, uuid
provider = json.loads(base64.b64decode(sys.argv[1]))
root = pathlib.Path(os.path.expanduser(provider['path']))
run = root / 'RAIkeep' / 'amafu-wsl-tests' / uuid.uuid4().hex
token = 'WSL-Windows-' + uuid.uuid4().hex + '-café'
run.mkdir(parents=True, exist_ok=False)
try:
    marker = run / 'probe.txt'
    marker.write_text(token, encoding='utf-8')
    windows = subprocess.check_output(['wslpath', '-w', str(marker.resolve())], text=True).strip()
    if not re.match(r'^[A-Za-z]:\\', windows):
        raise RuntimeError('Expected a Windows drive path, got ' + windows)
    def ps_quote(value):
        return "'" + value.replace("'", "''") + "'"
    command = (
        "$ErrorActionPreference = 'Stop'; "
        "$p=" + ps_quote(windows) + "; $expected=" + ps_quote(token) + "; "
        "if ([IO.File]::ReadAllText($p) -cne $expected) { throw 'Windows read mismatch' }; "
        "[IO.File]::WriteAllText($p, $expected + '-Windows', [Text.UTF8Encoding]::new($false))"
    )
    encoded = base64.b64encode(command.encode('utf-16-le')).decode('ascii')
    subprocess.run(['powershell.exe', '-NoLogo', '-NoProfile', '-NonInteractive',
                    '-EncodedCommand', encoded], check=True, timeout=45, capture_output=True)
    assert marker.read_text(encoding='utf-8') == token + '-Windows', 'WSL read mismatch'
finally:
    shutil.rmtree(run)
print(json.dumps({'provider': provider['name'], 'root': str(root),
                  'windowsPath': windows, 'roundTrip': True, 'cleaned': not run.exists()}))
""";
}

public sealed class WslObserver : IDisposable
{
	private readonly string? target;
	private readonly string? directory;
	public string Amafu => "DOTNET_NOLOGO=1 DOTNET_CLI_TELEMETRY_OPTOUT=1 dotnet " + Quote(directory + "/amafu.dll");

	public WslObserver()
	{
		var publish = Environment.GetEnvironmentVariable("RAIKEEP_AMAFU_WSL_PUBLISH");
		if (string.IsNullOrEmpty(publish)) return;
		Assert.True(new RaiPath(publish).Exists(), "Published Amafu directory is missing.");
		var name = Environment.GetEnvironmentVariable("RAIKEEP_WSL_OBSERVER") ?? "Themba";
		var config = (JObject)Os.Config;
		var observer = ((JArray?)config["Observers"])?.OfType<JObject>()
			.SingleOrDefault(o => string.Equals((string?)o["Name"], name, StringComparison.OrdinalIgnoreCase));
		target = (string?)observer?["SshTarget"];
		Assert.False(string.IsNullOrWhiteSpace(target), $"Observer '{name}' is not configured in Os.Config.Observers.");
		try
		{
			Assert.Contains("microsoft", Run("uname -r").ToLowerInvariant());
			directory = Run("mktemp -d /tmp/raikeep-amafu-wsl.XXXXXXXX").Trim();
			Assert.Matches(@"^/tmp/raikeep-amafu-wsl\.[A-Za-z0-9]+$", directory);
			var archive = new RaiFile(Os.TempDir, "amafu-wsl-" + Guid.NewGuid().ToString("N"), "tgz");
			try
			{
				var pack = new RaiSystem("tar", new[] { "-czf", archive.FullName, "-C", publish, "." }).ExecResult(30000);
				Assert.True(pack.Succeeded, "Archive failed: " + pack.StandardError);
				var encoded = Convert.ToBase64String(archive.ReadAllBytesAsync().GetAwaiter().GetResult());
				var copy = new SshSystem(target, "base64 --decode | tar -xzf - -C " + Quote(directory),
					["-o", "BatchMode=yes", "-o", "ConnectTimeout=10"]) { StandardInput = encoded }.ExecResult(60000);
				Assert.True(copy.Succeeded, $"Upload failed (exit {copy.ExitCode}, timeout {copy.TimedOut}): {copy.StandardError}");
			}
			finally { if (archive.Exists()) archive.rm(); }
			Run("command -v dotnet; command -v python3; command -v powershell.exe; command -v wslpath");
		}
		catch { Dispose(); throw; }
	}

	public void RequireEnabled()
	{
		if (target is null) Assert.Skip("Run scripts/test-amafu-wsl.sh to enable the live WSL tests.");
	}

	public JObject Detect() => JObject.Parse(Run(Amafu + " detect --json --dry-run"));

	public string ConfigurationState() => Run("sha256sum \"$HOME/.config/RAIkeep.json5\"; " +
		"if [ -d \"$HOME/.CloudStorage\" ]; then find \"$HOME/.CloudStorage\" -maxdepth 1 -printf '%f %l\\n' | sort; fi");

	public string Run(string script)
	{
		var encoded = Convert.ToBase64String(Encoding.UTF8.GetBytes("set -euo pipefail\n" + script));
		var command = $"printf '%s' '{encoded}' | base64 --decode | /bin/bash -l";
		var result = SshSystem.ExecuteRemoteCommand(target!, command, 120000,
			["-o", "BatchMode=yes", "-o", "ConnectTimeout=10"]);
		Assert.True(result.Succeeded, $"Remote command failed (exit {result.ExitCode}): {result.StandardError}");
		return result.StandardOutput;
	}

	public void Dispose()
	{
		if (directory is not null && System.Text.RegularExpressions.Regex.IsMatch(directory,
			@"^/tmp/raikeep-amafu-wsl\.[A-Za-z0-9]+$"))
			Run("rm -rf -- " + Quote(directory));
	}

	public static string Quote(string value) => "'" + value.Replace("'", "'\\''") + "'";
}
