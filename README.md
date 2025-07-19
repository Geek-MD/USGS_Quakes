# USGS Quakes

**USGS Quakes** is a custom integration for [Home Assistant](https://www.home-assistant.io) that monitors earthquake events from the [USGS Earthquake Hazards Program](https://earthquake.usgs.gov/). It provides `geo_location` entities for each event matching your filter criteria.

![USGS Logo](https://earthquake.usgs.gov/favicon.ico)

## Features

- Fetches earthquake data directly from USGS GeoJSON feeds.
- Creates `geo_location` entities for each event.
- Filters by:
  - Location (latitude, longitude, radius)
  - Minimum magnitude
  - Feed type (e.g., past day, past week, significant earthquakes, etc.)
- Uses **friendly names** in the UI for easier selection of feed types.
- Updates automatically every 5 minutes.
- Entities include full metadata (magnitude, location, time, etc.).
- Fully configurable via Home Assistant UI.
- **Automatically reloads and regenerates entities** when options are changed.

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

All configuration is done via the Home Assistant UI.

### Fields

- **Latitude / Longitude**: Center point for filtering.
- **Radius (Km)**: Distance from the center point to search for events.
- **Minimum Magnitude (Mw)**: Events below this magnitude are ignored.
- **Feed Type**: Select the feed source using friendly names like “Past Week - M2.5+”.

You can later modify the **radius**, **minimum magnitude**, or **feed type** from the integration's **Configure** menu.

Any changes applied are immediately reflected — the integration reloads and regenerates the relevant entities automatically.

## Feed Types Supported

A total of 20 USGS feed types are supported, including:

- Past Hour / Day / Week / Month – All Earthquakes
- Significant Earthquakes (summary)
- Filtered by magnitude (1.0+, 2.5+, 4.5+)

These feeds are listed in the UI with human-friendly labels. Internally, they map to official [USGS feed IDs](https://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php).

## Known Issues

- Only one instance is supported at a time (currently).
- Feed entries older than the last scan might be skipped.

## Credits

Developed by [@Geek-MD](https://github.com/Geek-MD)

Feed powered by [USGS GeoJSON Earthquake Feeds](https://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php)
