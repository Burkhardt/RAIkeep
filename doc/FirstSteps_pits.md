# First steps with pits: weather in your iCloud Drive

Create a `Weather` pit, fetch Cape Town weather with `curl`, and save the JSON with `pits`.

You need `pits` 4.5.0 or later, `curl`, and `jq`. Run these commands in your Mac's Terminal, or over SSH as the macOS user whose iCloud Drive you want to use. iCloud Drive must be enabled for that user.

## 1. Check your iCloud configuration

```bash
pits -h -c ICloudDrive
```

The help output should show your iCloud path. If you have not created a RAIkeep configuration yet, run `amafu init`, then try again. `amafu init --dry-run` only previews the configuration; it does not save it.

With Amafu 4.5.4 or later, we recommend `amafu init --create-links` for a new
configuration. It creates the `~/.CloudStorage/ICloudDrive` shortcut and writes
`"ICloudDrive": "~/.CloudStorage/ICloudDrive/"` into the configuration. Preview
with `amafu init --create-links --dry-run`. For an existing configuration, use
`amafu reconcile` to preview the migration, then `amafu reconcile --apply` to
apply it with a backup. `amafu detect --create-links` only creates shortcuts;
it does not update an existing configuration.

Plain `amafu init` uses the physical path instead. Inside `~/.config/RAIkeep.json5`, a quoted path uses ordinary spaces and tildes, without shell backslashes:

```json
"ICloudDrive": "~/Library/Mobile Documents/com~apple~CloudDocs/"
```

## 2. Create your first pit and item

```bash
printf '%s\n' '[{"Id":"CapeTown","City":"Cape Town"}]' \
  | pits seed Weather -c ICloudDrive -r RAIkeep/FirstSteps --source -
```

`seed` creates the pit when needed and saves the item. No separate create or save command is required.

- `Weather` is the pit's name.
- `CapeTown` is the item's `Id`.
- `-c ICloudDrive` selects your configured iCloud root.
- `-r RAIkeep/FirstSteps` selects a folder below that root.
- `--source -` reads JSON from the pipe.

The pit file lives at `RAIkeep/FirstSteps/Weather/Weather.pit` inside your configured iCloud root. You can browse to it in Finder.

Read back your item:

```bash
pits export Weather -c ICloudDrive -r RAIkeep/FirstSteps -n --json \
  | jq '.[] | {Id, City}'
```

```json
{
  "Id": "CapeTown",
  "City": "Cape Town"
}
```

## 3. Fetch and save some weather

This example uses the [Open-Meteo weather API](https://open-meteo.com/en/docs), which provides current model-based weather data without an API key for this exercise. The requested times are in UTC.

```bash
set -o pipefail

curl -fsS 'https://api.open-meteo.com/v1/forecast?latitude=-33.9258&longitude=18.4232&current=temperature_2m,relative_humidity_2m,wind_speed_10m&timezone=UTC' \
  | jq '[{Id: "CapeTown", Weather: .}]' \
  | pits seed Weather -c ICloudDrive -r RAIkeep/FirstSteps --source - --require-existing
```

`curl` fetches the JSON. `jq` wraps the response in an item with `Id: "CapeTown"`, keeping the complete API response under `Weather`, including its units. `pits` adds those attributes to the existing item; its `City` stays intact. `--require-existing` catches a mistyped or missing item ID.

## 4. Read your saved weather

```bash
pits export Weather -c ICloudDrive -r RAIkeep/FirstSteps -n --json \
  | jq '.[] | select(.Id == "CapeTown") | {
      City,
      TimeUTC: .Weather.current.time,
      Temperature: .Weather.current.temperature_2m,
      Unit: .Weather.current_units.temperature_2m,
      Humidity: .Weather.current.relative_humidity_2m
    }'
```

You are now reading the saved pit, not calling the weather service. Repeat step 3 later to update the same item. JsonPit adds changes to its retained history instead of replacing the whole item. iCloud synchronizes the pit files to other Macs using the same account; allow time for synchronization before reading them elsewhere.
