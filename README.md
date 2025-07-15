# USGS Quakes

**USGS Quakes** is a custom integration for [Home Assistant](https://www.home-assistant.io/) that provides geolocation entities for earthquakes reported by the [USGS Earthquake Hazards Program](https://earthquake.usgs.gov/earthquakes/feed/).

> ✅ Identical behavior to the official `usgs_earthquakes_feed` integration  
> 🔁 Dynamically creates `geo_location` entities based on real-time earthquake data  
> ⚙️ Adds support for UI-based configuration using `config_flow`  
> 🌍 Uses USGS GeoJSON feeds via `aio-geojson-usgs-earthquakes==0.3`

---

## 📦 Installation

1. Copy this folder to your Home Assistant custom components directory:

    ```bash
    custom_components/usgs_quakes/
    ```

2. Restart Home Assistant.

3. Go to **Settings > Devices & Services > Add Integration** and search for **USGS Quakes**.

---

## ⚙️ Configuration

The following parameters are configurable via the UI:

- **Latitude / Longitude**: Center of your search area.
- **Radius (km)**: Earthquake search radius.
- **Minimum Magnitude**: Filter by magnitude.
- **Feed Type**: One of the 20 official USGS GeoJSON feed types.

---

## 📡 Supported Feed Types

Examples:

- `past_hour_all`
- `past_day_m2.5`
- `past_week_significant`
- `past_month_all`

For the full list of available feeds, visit:  
👉 [https://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php](https://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php)

---

## 🛰️ Entity Details

Each earthquake is represented as a `geo_location` entity, containing:

- Title and location
- Latitude / Longitude
- Magnitude
- Time of event
- Place and status metadata

---

## 📘 Documentation

Source repository:  
**GitHub**: [https://github.com/Geek-MD/USGS_Quakes](https://github.com/Geek-MD/USGS_Quakes)

---

## 👨‍💻 Author

Developed by [Geek-MD](https://github.com/Geek-MD)

---

## 📄 License

MIT License
