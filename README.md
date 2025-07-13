# 🌎 USGS Quakes

**USGS Quakes** is a custom integration for [Home Assistant](https://www.home-assistant.io/) that tracks earthquake activity using the [U.S. Geological Survey (USGS)](https://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php) GeoJSON feeds.

> Based on the official `usgs_earthquakes_feed` integration from Home Assistant Core, adapted to run as a custom component.

---

## 📦 Features

- Dynamically creates `geo_location` entities for recent earthquake events.
- Supports all 20 official USGS feeds (e.g., *Past Hour M4.5+*, *Past Day All Earthquakes*, etc.).
- Configurable filtering by:
  - Minimum magnitude (Mw).
  - Distance radius from a chosen location (in kilometers).
- Automatic updates every 5 minutes.
- Setup via the Home Assistant UI.

---

## 🔧 Installation

1. Copy the folder `usgs_quakes` to your `config/custom_components/` directory: `custom_components/usgs_quakes/`
3. Restart Home Assistant.

4. Go to **Settings > Devices & Services > Integrations** and click **“+ Add Integration”**.

5. Search for `USGS Quakes` and configure:
- Feed type.
- Location (latitude & longitude).
- Radius (in km).
- Minimum magnitude.

---

## 🌐 Supported Feeds

| Feed ID                          | Description                     |
|----------------------------------|---------------------------------|
| `past_hour_all_earthquakes`     | All earthquakes (last hour)     |
| `past_hour_m45_earthquakes`     | M4.5+ earthquakes (last hour)   |
| `past_day_significant_earthquakes` | Significant quakes (24h)     |
| ...                              | *See full list in codebase*     |

Supports all feeds listed in the [USGS GeoJSON documentation](https://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php).

---

## 📌 Notes

- Requires Home Assistant **2024.6.0** or later.
- Uses the `aio-geojson-usgs-earthquakes==0.3` library.
- Only **one instance** of this integration should be configured at a time.

---

## 🧑‍💻 Credits

Developed by [@Geek-MD](https://github.com/Geek-MD)  
Inspired by the original USGS feed integration by [@exxamalte](https://github.com/exxamalte)

---

## 📖 License

This project is licensed under the MIT License.
