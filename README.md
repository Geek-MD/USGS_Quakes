[![Geek-MD - USGS Quakes](https://img.shields.io/static/v1?label=Geek-MD&message=USGS%20Quakes&color=blue&logo=github)](https://github.com/Geek-MD/USGS_Quakes)
[![Stars](https://img.shields.io/github/stars/Geek-MD/USGS_Quakes?style=social)](https://github.com/Geek-MD/USGS_Quakes)
[![Forks](https://img.shields.io/github/forks/Geek-MD/USGS_Quakes?style=social)](https://github.com/Geek-MD/USGS_Quakes)

[![GitHub Release](https://img.shields.io/github/release/Geek-MD/USGS_Quakes?include_prereleases&sort=semver&color=blue)](https://github.com/Geek-MD/USGS_Quakes/releases)
[![License](https://img.shields.io/badge/License-MIT-blue)](https://github.com/Geek-MD/USGS_Quakes/blob/main/LICENSE)
[![HACS Custom Repository](https://img.shields.io/badge/HACS-Custom%20Repository-blue)](https://hacs.xyz/)

[![Ruff + Mypy + Hassfest](https://github.com/Geek-MD/USGS_Quakes/actions/workflows/validate.yaml/badge.svg)](https://github.com/Geek-MD/USGS_Quakes/actions/workflows/validate.yaml)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)

<img width="200" height="200" alt="icon" src="https://github.com/Geek-MD/USGS_Quakes/blob/main/custom_components/usgs_earthquakes_feed/brand/icon.png?raw=true" />

# USGS Quakes

**USGS Quakes** is a custom integration for [Home Assistant](https://www.home-assistant.io) that monitors earthquake events from the [USGS Earthquake Hazards Program](https://earthquake.usgs.gov/). It provides `geo_location` entities for each event matching your filter criteria.

> [!IMPORTANT]
> Starting from **v1.2.0**, this integration uses the domain `usgs_earthquakes_feed`, which **overrides the built-in Home Assistant core integration** of the same name. In the integrations overview, it will display a special icon in the upper-right corner of the integration card indicating it overrides a core integration.
>
> If you were using the previous **`usgs_quakes`** domain (v1.1.x or earlier), you must **remove the old integration and set it up again** after upgrading to v1.2.0.

---

## 🌍 Features

- Monitors earthquakes from the USGS GeoJSON feed.
- Filters by:
  - **Minimum Magnitude (Mw)**
  - **Maximum Distance** from your location (Radius)
- Creates `geo_location` entities for each event.
- Includes a special sensor `sensor.usgs_earthquakes_feed_latest` that:
  - State is the timestamp of the most recent **new** earthquake event
  - Exposes new events via the `latest_events` attribute (only events detected in the current update cycle; empty when no new earthquakes have arrived)
  - Fires a `usgs_earthquakes_feed_new_events` event on the HA event bus whenever new earthquakes are detected
- Includes a `format_events` action that returns earthquake events as formatted text via a response variable

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
2. Copy the folder `custom_components/usgs_earthquakes_feed/` into your Home Assistant `config/custom_components/` directory.
3. Restart Home Assistant.
4. Add the integration via the UI.

---

### ⚠️ Migrating from `usgs_quakes` (v1.1.x → v1.2.0)

Version 1.2.0 changed the integration domain from `usgs_quakes` to `usgs_earthquakes_feed`. Home Assistant treats these as two different integrations, so a one-time manual migration is required:

1. Go to **Settings → Devices & Services**.
2. Find the **USGS Quakes** entry with domain `usgs_quakes` and **delete** it.
3. Install v1.2.0 (via HACS or manually) and restart Home Assistant.
4. Go to **Settings → Devices & Services → Add Integration** and set up **USGS Quakes** again.

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

## 🧪 Sensor: `sensor.usgs_earthquakes_feed_latest`

This sensor exposes:

- `state`: Timestamp of the most recent **new** earthquake event (only changes when new earthquakes are detected)
- `latest_events`: List of new earthquakes detected in the current update cycle, ordered from newest to oldest. Empty when no new earthquakes have arrived since the last update.

> **How it works:**
> - **First run** (or after HA restart): `latest_events` contains all earthquakes that match your filter criteria.
> - **Subsequent updates with no new earthquakes**: `latest_events` is empty (`[]`) and the sensor state does not change.
> - **New earthquake detected**: `latest_events` contains only the new event(s), the sensor state updates to the newest event's timestamp.

---

## 📣 Event: `usgs_earthquakes_feed_new_events`

Every time new earthquakes are detected the integration fires this event on the HA event bus. You can use it as an automation trigger:

```yaml
trigger:
  - platform: event
    event_type: usgs_earthquakes_feed_new_events
```

The event data contains:

| Field | Description |
|---|---|
| `entry_id` | Config-entry ID of the integration instance |
| `count` | Number of new events detected |
| `events` | List of new earthquake event dicts |

### Example automation using the event:

```yaml
automation:
  - alias: "Notify on new earthquake"
    trigger:
      - platform: event
        event_type: usgs_earthquakes_feed_new_events
    action:
      - service: notify.mobile_app_my_phone
        data:
          title: "🌍 New Earthquake"
          message: >
            {{ trigger.event.data.count }} new earthquake(s) detected.
            Latest: {{ trigger.event.data.events[0].title }}
```

---

## 📋 Action: `usgs_earthquakes_feed.format_events`

Returns the stored earthquake events formatted as human-readable text via a response variable.

### Example automation:

```yaml
action: usgs_earthquakes_feed.format_events
response_variable: result
# result.formatted_events contains multiline text, e.g.:
```

### Example output:

```
M 5.2 - Near Valparaíso, Chile
Lugar: 8 km NW of Valparaíso
Magnitud: 5.2 Mw
Fecha/Hora: 2025-09-18 04:33:22
Localización: https://www.google.com/maps?q=-33.0458,-71.6197
```

---

## 🚀 Services / Actions

### Force Feed Refresh

Call the following service to manually refresh the earthquake feed:

```yaml
service: usgs_earthquakes_feed.force_feed_update
```

You can trigger this from Developer Tools, automations, or UI buttons.

### Get Formatted Events

Call this action to retrieve the stored events as formatted text (response variable required):

```yaml
action: usgs_earthquakes_feed.format_events
response_variable: quake_report
```

The variable `quake_report.formatted_events` will contain a multiline string with event details.

---

## 📓 Notes

- On first setup (or after HA restart), **all events** matching the filters are treated as new and included in `latest_events`.
- On subsequent updates, only **new events** (based on USGS `id`) are included in `latest_events`.
- When no new earthquakes are detected, `latest_events` is empty (`[]`) and the sensor state does not change.
- Events in `latest_events` are ordered from newest to oldest.
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
