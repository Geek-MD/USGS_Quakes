[![Geek-MD - USGS Quakes](https://img.shields.io/static/v1?label=Geek-MD&message=USGS%20Quakes&color=blue&logo=github)](https://github.com/Geek-MD/USGS_Quakes)
[![Stars](https://img.shields.io/github/stars/Geek-MD/USGS_Quakes?style=social)](https://github.com/Geek-MD/USGS_Quakes)
[![Forks](https://img.shields.io/github/forks/Geek-MD/USGS_Quakes?style=social)](https://github.com/Geek-MD/USGS_Quakes)

[![GitHub Release](https://img.shields.io/github/release/Geek-MD/USGS_Quakes?include_prereleases&sort=semver&color=blue)](https://github.com/Geek-MD/USGS_Quakes/releases)
[![License](https://img.shields.io/badge/License-MIT-blue)](https://github.com/Geek-MD/USGS_Quakes/blob/main/LICENSE)
[![HACS Custom Repository](https://img.shields.io/badge/HACS-Custom%20Repository-blue)](https://hacs.xyz/)

[![Ruff + Mypy + Hassfest](https://github.com/Geek-MD/USGS_Quakes/actions/workflows/validate.yaml/badge.svg)](https://github.com/Geek-MD/USGS_Quakes/actions/workflows/validate.yaml)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)

<img width="200" height="200" alt="icon" src="https://github.com/Geek-MD/USGS_Quakes/blob/main/icon.png?raw=true" />

# USGS Quakes

**USGS Quakes** is a custom integration for [Home Assistant](https://www.home-assistant.io) that monitors earthquake events from the [USGS Earthquake Hazards Program](https://earthquake.usgs.gov/). It provides `geo_location` entities for each event matching your filter criteria.

---

## 🌍 Features

- Monitors earthquakes from the USGS GeoJSON feed.
- Filters by:
  - **Minimum Magnitude (Mw)**
  - **Maximum Distance** from your location (Radius)
- Creates `geo_location` entities for each event.
- Includes a special sensor `sensor.usgs_quakes_latest` that:
  - Stores only **new** earthquake events (based on their unique `id`)
  - Exposes a formatted list of recent events:
    - Title
    - Place
    - Magnitude
    - Date/time (local)
    - Google Maps link to epicenter

---

## ⚙️ Requirements

- Home Assistant 2024.6.0 or newer
- Internet access to fetch data from USGS

---

## 📦 Installation

### Option 1: HACS (recommended)

1. Open HACS in Home Assistant.
2. Go to **Integrations → Custom Repositories**.
3. Add this repository:
   ```
   https://github.com/Geek-MD/USGS_Quakes
   ```
   Select type: **Integration**
4. Install and restart Home Assistant.
5. Go to **Settings → Devices & Services → Add Integration** and select **USGS Quakes**.

---

### Option 2: Manual Installation

1. Download this repository.
2. Copy the folder `custom_components/usgs_quakes/` into your Home Assistant `config/custom_components/` directory.
3. Restart Home Assistant.
4. Add the integration via the UI.

---

## 🔧 Configuration

All configuration is done through the UI.

### Options

- **Latitude / Longitude** – Your location
- **Radius (Km)** – Max distance to include earthquakes
- **Minimum Magnitude (Mw)** – Ignore earthquakes below this
- **Feed Type** – Select from 20 different USGS feeds (past hour, day, week, etc.)

You can modify these settings anytime from the integration’s **Options** menu.

---

## 📡 Feed Types

Supported USGS feed types include:

- All earthquakes (past hour, day, week, month)
- Only significant events
- Filtered by magnitude: 1.0+, 2.5+, 4.5+

Full list: [USGS GeoJSON Feed Documentation](https://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php)

---

## 🧪 Sensor: `sensor.usgs_quakes_latest`

This sensor exposes:

- `state`: Timestamp of the latest event
- `events`: List of the last 10 new earthquakes
- `formatted_events`: Multiline string with summary info

### Example:

```
M 5.2 - Near Valparaíso, Chile
Place: 8 km NW of Valparaíso
Magnitude: 5.2 Mw
Date/Time: 2025-09-18 04:33:22
Location: https://www.google.com/maps?q=-33.0458,-71.6197
```

---

## 🚀 Manual Feed Refresh

Call the following service to manually refresh the earthquake feed:

```yaml
service: usgs_quakes.force_feed_update
```

You can trigger this from Developer Tools, automations, or UI buttons.

---

## 💡 Optional Lovelace Cards

For visualizing data in Lovelace, install the **USGS Quakes Cards** from [USGS Quakes Cards](https://github.com/Geek-MD/usgs_quakes_cards) repository:

- Map of recent earthquakes
- List of formatted events
- Button to manually refresh the feed

These cards are **not included in this repository** and must be added manually or via HACS (coming soon).

---

## 📓 Notes

- On first setup, **all events** matching the filters are included.
- On updates, only **new events** (based on USGS `id`) are added.
- Sensor shows events in reverse chronological order (newest first).
- All magnitude and distance values follow standard units (Mw, km).

---

## 🙋‍♂️ Credits

Developed by [@Geek-MD](https://github.com/Geek-MD)  
Powered by [USGS GeoJSON Feed](https://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php)

Special thanks to [@AdamsLab01](https://github.com/AdamsLab01) for reporting critical bugs and improvements.

---

## 📄 License

MIT © Edison Montes [_@GeekMD_](https://github.com/Geek-MD)

---

<div align="center">
  
💻 **Proudly developed with GitHub Copilot** 🚀

</div>
