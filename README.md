[![Geek-MD - USGS Quakes](https://img.shields.io/static/v1?label=Geek-MD&message=USGS%20Quakes&color=blue&logo=github)](https://github.com/Geek-MD/USGS_Quakes)
[![Stars](https://img.shields.io/github/stars/Geek-MD/USGS_Quakes?style=social)](https://github.com/Geek-MD/USGS_Quakes)
[![Forks](https://img.shields.io/github/forks/Geek-MD/USGS_Quakes?style=social)](https://github.com/Geek-MD/USGS_Quakes)

[![GitHub Release](https://img.shields.io/github/release/Geek-MD/USGS_Quakes?include_prereleases&sort=semver&color=blue)](https://github.com/Geek-MD/USGS_Quakes/releases)
[![License](https://img.shields.io/badge/License-MIT-blue)](#license)
![HACS Custom Repository](https://img.shields.io/badge/HACS-Custom%20Repository-blue)
[![Ruff](https://github.com/Geek-MD/USGS_Quakes/actions/workflows/ci.yaml/badge.svg?branch=develop&label=Ruff)](https://github.com/Geek-MD/USGS_Quakes/actions/workflows/ci.yaml)

<img width="200" height="200" alt="image" src="https://github.com/Geek-MD/USGS_Quakes/blob/main/icon.png?raw=true" />

# USGS Quakes

**USGS Quakes** is a custom integration for [Home Assistant](https://www.home-assistant.io) that monitors earthquake events from the [USGS Earthquake Hazards Program](https://earthquake.usgs.gov/). It provides `geo_location` entities for each event matching your filter criteria.

---

## Features

- Monitors earthquakes from USGS based on the selected feed type.
- Filters events by:
  - Minimum magnitude (Mw)
  - Maximum distance (radius) from your location
- Creates `geo_location` entities for each qualifying earthquake.
- Includes a special sensor `sensor.usgs_quakes_latest` that:
  - Stores only new events that were not previously seen (based on `id`)
  - Presents a human-readable summary with event details:
    - Title
    - Place
    - Magnitude
    - Date and time (local)
    - Location (Google Maps link)

---

## What's New in v1.1.0

This version introduces new **Lovelace cards** for improved visualization and interaction:

- **Earthquake Map Card**  
  Automatically shows a map with all earthquakes as geo markers.

- **Event List Card**  
  A manual card that lists recent events with clickable Google Maps links.

- **Update Button Card**  
  A manual card with a button to trigger an immediate feed update.

These cards are available in the `lovelace/` folder of the integration.

---

## Requirements

- Home Assistant 2024.6.0 or later
- Internet access to connect to the USGS feed

---

## Installation

### Option 1: Using HACS (recommended)

1. Open HACS in Home Assistant.
2. Go to “Integrations” → “Custom repositories”.
3. Add:
   ```
   https://github.com/Geek-MD/USGS_Quakes
   ```
   as a **Integration** type.
4. Install the integration and restart Home Assistant.
5. Go to Settings → Devices & Services → Add Integration → **USGS Quakes**.

### Option 2: Manual installation

1. Download this repository.
2. Copy the folder `custom_components/usgs_quakes/` into your Home Assistant `custom_components/` directory.
3. Restart Home Assistant.
4. Add the integration from the UI.

---

## Configuration

All configuration is done via the UI.

### Fields

- **Latitude / Longitude**: Center point for filtering.
- **Radius (Km)**: Distance from the center point to search for events.
- **Minimum Magnitude (Mw)**: Events below this magnitude are ignored.
- **Feed Type**: Select the feed source. Friendly names are shown in the UI.

You can later modify the radius, magnitude and feed type from the integration options.

---

## Feed Types Supported

A total of 20 USGS feed types are supported, including:

- Past Hour / Day / Week / Month - All earthquakes
- Significant Earthquakes (summary)
- Filtered by magnitude (1.0+, 2.5+, 4.5+)

See [USGS GeoJSON Documentation](https://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php) for details.

---

## Sensor: `sensor.usgs_quakes_latest`

This sensor contains:

- `state`: Timestamp of the most recent earthquake event (in ISO format)
- `events`: A list of new earthquake events (max 50)
- `formatted_events`: A multiline string summary of the new events

### Example formatted output:

```
M 4.3 - 10 km NE of Townsville, Chile
Place: 10 km NE of Townsville, Chile
Magnitude: 4.3 Mw
Date/Time: 2025-09-18 04:33:22
Location: https://www.google.com/maps?q=-30.1234,-71.5678
```

---

## Lovelace Cards

The following cards are included in `custom_components/usgs_quakes/lovelace/`:

### Map Card (Automatically added)

This map card displays earthquake markers using the geo entities. No manual action is required.

### Event List Card

Displays each event as a list with clickable locations.

To add manually:

1. Go to your dashboard.
2. Click **Edit** → **Add Card** → **Manual**.
3. Paste the contents of:

```
custom_components/usgs_quakes/lovelace/event_list_card.yaml
```

### Update Button Card

Triggers a manual update of the USGS feed.

To add manually:

1. Go to your dashboard.
2. Click **Edit** → **Add Card** → **Manual**.
3. Paste the contents of:

```
custom_components/usgs_quakes/lovelace/update_button_card.yaml
```

---

## Manual Update Service

The service `usgs_quakes.force_feed_update` can be triggered manually from **Developer Tools > Services** in Home Assistant, or from automations/scripts. This will immediately refresh the earthquake feed and update entities.

```yaml
service: usgs_quakes.force_feed_update
```

---

## Notes

- On the first run, the sensor stores **all events** that meet the configured filters.
- On subsequent updates, it stores **only new events** that were not seen previously (based on their `id`).
- Events are ordered from newest to oldest.

---

## Known Issues

- Only one instance is supported at a time (currently).
- Feed entries older than the last scan might be skipped.

---

## Credits

Developed by [@Geek-MD](https://github.com/Geek-MD)

Feed powered by [USGS GeoJSON Earthquake Feeds](https://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php)

---

## License

MIT © Edison Montes [_@GeekMD_](https://github.com/Geek-MD)
