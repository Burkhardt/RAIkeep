using System;
using System.IO;
using System.Reflection;
using System.Linq;
using JsonPit;
using OsLib;
public static class Icons
{
	public const char Error = '\uea87';
	public const char Warning = '\uf071';
	public const char Success = '\ueab2';
	public const char Info = '\uea74';
	public const char Help = '\uf059';
	public const char NotAvailable = '\ueabd';
	public const char File = '\uea7b';
	public const char Folder = '\uea83';
	public const char Download = '\ueac2';
	public const char Upload = '\ueac3';
	public const char Banner = '\ueb1e';
	public const char NoBanner = '\ueb24';
}
public static class Messages
{
	public static bool Debug { get; set; } = false;
	public static string? CloudProvider { get; set; }
	public static RaiPath? PitRoot { get; set; }
	// Opened up access modifier so Program.cs can read the list
	public static readonly string[] WwwaFiles = { "Person", "Object", "Place", "Activity" };
	public static string? Destination { get; set; }
	public static string? Source { get; set; }
	public static bool Wwwa { get; set; }
	public static bool Banner { get; set; }
	public static string[] Help =>
	[
		$"-h, --help\t\t{Icons.Help}\tprint out all options, replace source and destination with passed-in parameters",
		$"-v, --version\t\t{Icons.Info}\tprint version info",
		$"-n, --nologo\t\t{(Banner ? Icons.Banner : Icons.NoBanner)}\tDo not display the banner",
		$"-s, --source\t\t{Icons.File}|{Icons.Folder}\t{SourceDescription()}",
		$"-d, --destination\t{Icons.File}|{Icons.Folder}\t{DestinationDescription()}",
		$"--wwwa\t\t\t{(Wwwa ? Icons.Success : Icons.NotAvailable)}\tRead 4 JSON/JSON5 files into 4 JsonPits",
		$"\t\tSource: {BuildWwwaStatusIcons(false)}",
		$"\t\tCloud:  {BuildWwwaStatusIcons(true)}",
		$"--source\t\t{Icons.File} {WwwaSourceFileStatus("Person")}",
		$"--destination\t\t{Icons.Upload} {WwwaDestinationFileStatus("Person")}",
		$"--source\t\t{Icons.File} {WwwaSourceFileStatus("Object")}",
		$"--destination\t\t{Icons.Upload} {WwwaDestinationFileStatus("Object")}",
		$"--source\t\t{Icons.File} {WwwaSourceFileStatus("Place")}",
		$"--destination\t\t{Icons.Upload} {WwwaDestinationFileStatus("Place")}",
		$"--source\t\t{Icons.File} {WwwaSourceFileStatus("Activity")}",
		$"--destination\t\t{Icons.Upload} {WwwaDestinationFileStatus("Activity")}",
		$"{Icons.Info} PitRoot\t\t{Icons.Folder} {(PitRoot?.Exists() == true ? Icons.Success : Icons.NotAvailable)} {Icons.Upload}\t{CloudProvider}: {PitRoot?.FullPath}",
		$"--source:\t\t{(Wwwa ? Icons.Folder : Icons.File)}\t{SourceDisplayPath()}",
		$"--destination:\t\t{(Wwwa ? Icons.Folder : Icons.File)} {Icons.Upload}\t{DestinationDisplayPath()}",
	];
	private static string SourceDescription()
	{
		return !Wwwa && !string.IsNullOrWhiteSpace(Source)
			? new RaiFile(Source).FullName
			: "Single JSON or JSON5 file or WWWA source directory";
	}
	private static string DestinationDescription()
	{
		return !string.IsNullOrWhiteSpace(Destination)
			? new RaiPath(Destination).Path
			: "JsonPit destination directory or canonical file path";
	}
	private static string SourceDisplayPath()
	{
		if (string.IsNullOrWhiteSpace(Source))
			return "<source_path_required>";
		return Wwwa ? new RaiPath(Source).Path : new RaiFile(Source).FullName;
	}
	private static string DestinationDisplayPath()
	{
		if (string.IsNullOrWhiteSpace(Destination))
			return "<destination_path_or_output>";
		return new RaiPath(Destination).Path;
	}
	private static string BuildWwwaStatusIcons(bool isCloud)
	{
		var baseLocation = isCloud ? Destination : Source;
		if (string.IsNullOrWhiteSpace(baseLocation))
			return string.Join(" ", WwwaFiles.Select(_ => Icons.NotAvailable)) + '\t';
		string icons = "";
		foreach (var file in WwwaFiles)
		{
			var exists = isCloud
				? new PitFile(new RaiPath(baseLocation), file).Exists()
				: (EitherFileExists(new RaiFile(new RaiPath(baseLocation), file).FullName, "json5", "json") != null);
			if (icons.Length > 0)
				icons += " ";
			icons += exists ? Icons.Success : Icons.NotAvailable;
		}
		icons += '\t';
		return icons;
	}
	private static string WwwaSourceFileStatus(string file)
	{
		if (string.IsNullOrWhiteSpace(Source))
			return $"{Icons.NotAvailable}\t{file}.json5";
		var baseFile = new RaiFile(new RaiPath(Source), file).FullName;
		var exists = EitherFileExists(baseFile, "json5", "json");
		return $"{(exists != null ? Icons.Success : Icons.NotAvailable)}\t{baseFile}.{exists}";
	}
	private static string WwwaDestinationFileStatus(string file)
	{
		if (string.IsNullOrWhiteSpace(Destination))
			return $"{Icons.NotAvailable}\t{file}.pit";
		// Rely on JsonPit canonical structure
		var canonicalDest = new RaiPath(Destination) / file;
		var pitFile = new PitFile(canonicalDest, file);
		return $"{(pitFile.Exists() ? Icons.Success : Icons.NotAvailable)}\t{pitFile.FullName}";
	}
	public static string? EitherFileExists(string? file, string ext1, string? ext2, string? ext3 = null, string? ext4 = null)
	{
		var extensions = new string?[] { ext1, ext2, ext3, ext4 };
		foreach (var extension in extensions)
		{
			if (extension == null) continue;
			var f = new RaiFile(file) { Ext = extension };
			if (f.Exists()) return extension;
		}
		return null;
	}
	public static void WriteHighlighted(string text, ConsoleColor foreground = ConsoleColor.Black, ConsoleColor? background = null)
	{
		var oldForeground = Console.ForegroundColor;
		var oldBackground = Console.BackgroundColor;
		Console.ForegroundColor = foreground;
		Console.BackgroundColor = background ?? oldBackground;
		Console.WriteLine(text);
		Console.ForegroundColor = oldForeground;
		Console.BackgroundColor = oldBackground;
	}
	public static void WriteError(string text) => WriteHighlighted(text, ConsoleColor.DarkRed, ConsoleColor.White);
	public static void WriteSuccess(string text) => WriteHighlighted(text, ConsoleColor.DarkGreen);
	public static void WriteInfo(string text) => WriteHighlighted(text, ConsoleColor.Blue);
	public static void WriteDebug(string text) { if (Debug) WriteHighlighted(text, ConsoleColor.DarkYellow); }
	public static void WriteLine(string text, char underlineChar = '=')
	{
		for (int i = 0; i < text.Length; i++) Console.Write(underlineChar);
		Console.WriteLine();
	}
	public static void WriteBanner(string text)
	{
		WriteLine(text);
		Console.WriteLine(text);
		WriteLine(text);
	}
	public static void WriteHelp()
	{
		foreach (var line in Help) WriteSuccess(line);
	}
}
internal static class Program
{
	private static int Main(string[] args)
	{
		try
		{
			if (HasOption(args, "-v", "--version"))
			{
				Messages.WriteSuccess(GetVersion());
				return 0;
			}
			#region READ & MAP PARAMETERS
			Messages.Debug = HasOption(args, "-b", "--debug");
			Messages.Banner = !HasOption(args, "-n", "--nologo");
			bool showHelp = HasOption(args, "-h", "--help");
			bool wwwa = Messages.Wwwa = HasOption(args, "-wwwa", "--wwwa");
			string? cloudProvider = Messages.CloudProvider = ParamValue(args, "-c", "--cloudprovider", "--cloud");
			var sourceParam = Messages.Source = ParamValue(args, "-s", "--source");
			var destParam = ParamValue(args, "-d", "--destination", "--dest", "—d") ?? "output";
			#endregion
			#region RESOLVE BASE PATHS
			if (string.IsNullOrWhiteSpace(cloudProvider))
			{
				Messages.Destination = destParam;
			}
			else
			{
				string? cloudDir = Os.Config?.Cloud?[cloudProvider];
				if (string.IsNullOrWhiteSpace(cloudDir))
				{
					Messages.WriteError($"The requested cloud provider '{cloudProvider}' is missing or empty in {Os.DefaultConfigFileLocation}.");
					return 1;
				}
				Messages.PitRoot = new RaiPath(cloudDir);
				Messages.Destination = (Messages.PitRoot / destParam).FullPath;
			}
			#endregion
			#region VALIDATE & SETUP OBJECTS
			RaiPath? wwwaSourceDir = null;
			RaiPath? wwwaDestDir = null;
			TextFile? singleSourceFile = null;
			RaiPath? singleDestPath = null;
			bool hasExecutionIntent = false;
			if (wwwa)
			{
				if (string.IsNullOrWhiteSpace(sourceParam))
				{
					Messages.WriteError("WWWA mode requires a source directory specified with -s or --source.");
					return 1;
				}
				Messages.Source = sourceParam.EndsWith(Os.DIR) ? sourceParam : sourceParam + Os.DIR;
				Messages.Destination = Messages.Destination!.EndsWith(Os.DIR) ? Messages.Destination : Messages.Destination + Os.DIR;
				wwwaSourceDir = new RaiPath(Messages.Source);
				wwwaDestDir = new RaiPath(Messages.Destination);
				hasExecutionIntent = true;
			}
			else if (!string.IsNullOrWhiteSpace(sourceParam))
			{
				singleSourceFile = new TextFile(sourceParam);
				if (!singleSourceFile.Exists())
				{
					Messages.WriteError($"Source file '{singleSourceFile.FullName}' does not exist.");
					return 1;
				}
				... hier weiter mit RaiPath.SplitRaiPathAndName
				if (Messages.Destination.EndsWith(Os.DIR))
				{
					(singleDestPath, _) = RaiPath.SplitRaiPathAndName(Messages.Destination);
				}
				else {
					splitResult
				}
				singleDestPath = new RaiPath(Messages.Destination);
				hasExecutionIntent = true;
			}
			#endregion
			#region LOGGING & HELP
			if (Messages.Banner)
				Messages.WriteBanner($"{Icons.Info} AfricaStage Pit Seeder CLI");
			if (hasExecutionIntent)
			{
				Messages.WriteDebug($"Source: {Messages.Source}");
				Messages.WriteDebug($"Destination: {Messages.Destination}");
				Messages.WriteDebug($"WWWA Mode: {wwwa}");
			}
			if (showHelp || !hasExecutionIntent)
			{
				Messages.WriteHelp();
				if (!hasExecutionIntent) return showHelp ? 0 : 1;
			}
			#endregion
			#region REAL WORK EXECUTION
			if (wwwa)
			{
				Messages.WriteInfo($"WWWA RunBulkSeed({wwwaSourceDir!.Path}, {wwwaDestDir!.Path}) started...");
				var rc = RunBulkSeed(wwwaSourceDir, wwwaDestDir);
				Messages.WriteInfo($"WWWA RunBulkSeed({wwwaSourceDir.Path}, {wwwaDestDir.Path}) completed.");
				return rc;
			}
			if (singleSourceFile != null && singleDestPath != null)
			{
				return RunSingleSeed(singleSourceFile, singleDestPath);
			}
			#endregion
		}
		catch (ArgumentException ex)
		{
			Messages.WriteError($"CLI Error: {ex.Message}");
		}
		catch (Exception ex)
		{
			Messages.WriteError($"An internal error occurred.\n{ex.Message}");
		}
		return 1;
	}
	#region Helpers for argument parsing
	private static string? ParamValue(string[] options, params string[] aliases)
		=> aliases.Select(a => Array.IndexOf(options, a)).Where(i => i >= 0)
			.Select(i => i + 1 < options.Length && !options[i + 1].StartsWith("-")
				? options[i + 1]
				: throw new ArgumentException($"The option '{options[i]}' requires a value."))
			.FirstOrDefault();
	private static bool HasOption(string[] options, params string[] aliases)
		=> aliases.Any(options.Contains);
	private static string GetVersion()
	{
		var assembly = Assembly.GetEntryAssembly();
		var name = assembly?.GetName().Name?.ToLowerInvariant() ?? "pits";
		var version = assembly?
			.GetCustomAttribute<AssemblyInformationalVersionAttribute>()?
			.InformationalVersion
			.Split('+')[0]
			?? assembly?.GetName().Version?.ToString()
			?? "unknown";
		return $"{name} v{version}";
	}
	#endregion
	#region Seeding Methods
	private static void SeedPit(TextFile source, RaiPath targetPath)
	{
		Messages.WriteInfo($"Seeding pit from source file: {source.FullName} \n\tto destination: {targetPath.Path}");
		var pit = new Pit(targetPath, readOnly: false);
		Messages.WriteDebug($"{Icons.Info} Processing {pit.JsonFile.Name} Pit...");
		pit.AddItems(source.ReadAllText());
		pit.Save();
		Messages.WriteSuccess($"{Icons.Success} Initialized and saved {pit.JsonFile.Name} to {pit.JsonFile.FullName}");
	}
	private static int RunBulkSeed(RaiPath sourceDir, RaiPath destDir)
	{
		Messages.WriteInfo($"{Icons.Info} Initiating WWWA Bulk Seed from: {sourceDir.Path}");
		foreach (var name in Messages.WwwaFiles)
		{
			var sourceFile = new TextFile(sourceDir, name, ext: "json5");
			var targetPath = destDir / name;
			Messages.WriteDebug($"SeedPit({sourceFile.FullName}, {targetPath.Path})...");
			SeedPit(sourceFile, targetPath);
			Messages.WriteDebug($"SeedPit({sourceFile.FullName}, {targetPath.Path}) completed.");
		}
		Messages.WriteSuccess($"{Icons.Success} WWWA bulk seeding complete. Data saved to {destDir.Path}");
		return 0;
	}
	private static int RunSingleSeed(TextFile source, RaiPath destination)
	{
		SeedPit(source, destination);
		return 0;
	}
	#endregion
}
