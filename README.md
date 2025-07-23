[![Geek-MD - USGS Quakes](https://img.shields.io/static/v1?label=Geek-MD&message=USGS%20Quakes&color=blue&logo=github)](https://github.com/Geek-MD/USGS_Quakes)
[![Stars](https://img.shields.io/github/stars/Geek-MD/USGS_Quakes?style=social)](https://github.com/Geek-MD/USGS_Quakes)
[![Forks](https://img.shields.io/github/forks/Geek-MD/USGS_Quakes?style=social)](https://github.com/Geek-MD/USGS_Quakes)

[![GitHub Release](https://img.shields.io/github/release/Geek-MD/USGS_Quakes?include_prereleases&sort=semver&color=blue)](https://github.com/Geek-MD/USGS_Quakes/releases)
[![License](https://img.shields.io/badge/License-MIT-blue)](#license)
![HACS Custom Repository](https://img.shields.io/badge/HACS-Custom%20Repository-blue)

![USGS Quakes Icon](https://github.com/Geek-MD/USGS_Quakes/blob/main/icon.png?raw=true)

# USGS Quakes

**USGS Quakes** is a custom integration for [Home Assistant](https://www.home-assistant.io) that monitors earthquake events from the [USGS Earthquake Hazards Program](https://earthquake.usgs.gov/). It provides `geo_location` entities for each event matching your filter criteria.

## Features

- Fetches earthquake data directly from USGS GeoJSON feeds.
- Creates `geo_location` entities for each event.
- Creates a `sensor.usgs_quakes_latest` datetime sensor showing the latest event time.
- Stores recent events as sensor attributes (filtered by configured magnitude).
- Filters by:
  - Location (latitude, longitude, radius)
  - Minimum magnitude
  - Feed type (e.g., past day, past week, significant earthquakes, etc.)
- Updates automatically every 5 minutes.
- Entities include full metadata (magnitude, location, time, etc.).
- Supports configuration via Home Assistant UI.
- Supports configuration updates via the "Configure" button in the integration panel.

## Installation

1. Copy this repository into your Home Assistant `custom_components` directory:

```bash
# Example if using Home Assistant OS or Supervised:
cd /config/custom_components
git clone https://github.com/Geek-MD/USGS_Quakes usgs_quakes
```

2. Restart Home Assistant.

3. Go to **Settings > Devices & Services > Integrations**.

4. Click **Add Integration** and search for **USGS Quakes**.

## Configuration

All configuration is done via the UI.

### Fields

- **Latitude / Longitude**: Center point for filtering.
- **Radius (Km)**: Distance from the center point to search for events.
- **Minimum Magnitude (Mw)**: Events below this magnitude are ignored.
- **Feed Type**: Select the feed source. Friendly names are shown in the UI.

You can later modify the radius, magnitude and feed type from the integration options.

## Feed Types Supported

A total of 20 USGS feed types are supported, including:

- Past Hour / Day / Week / Month - All earthquakes
- Significant Earthquakes (summary)
- Filtered by magnitude (1.0+, 2.5+, 4.5+)

See [USGS GeoJSON Documentation](https://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php) for details.

## Sensor: `sensor.usgs_quakes_latest`

This integration creates a datetime sensor reflecting the latest detected event.

- **State**: Date and time of the most recent event (in ISO format).
- **Attribute `events`**: List of up to 10 new events, each including:
  - `id`
  - `magnitude`
  - `place`
  - `time` (UTC)

This helps track and trigger automations based on recent seismic activity.

## Known Issues

- Only one instance is supported at a time (currently).
- Feed entries older than the last scan might be skipped.

## Credits

Developed by [@Geek-MD](https://github.com/Geek-MD)

Feed powered by [USGS GeoJSON Earthquake Feeds](https://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php)
