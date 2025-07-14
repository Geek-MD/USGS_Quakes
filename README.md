# USGS Quakes

**USGS Quakes** is a custom integration for [Home Assistant](https://www.home-assistant.io/) that provides geolocation entities for earthquakes reported by the [USGS Earthquake Hazards Program](https://earthquake.usgs.gov/earthquakes/feed/).

> ✅ Supports configuration via the Home Assistant UI  
> 🔁 Uses `DataUpdateCoordinator` for efficient updates  
> 🌍 Entities are created dynamically from the USGS GeoJSON feed  
> 🔒 Only one instance can be configured (v1.0.0)

---

## 📦 Installation

1. Copy this folder to your Home Assistant custom components directory:

    ```bash
    custom_components/usgs_quakes/
    ```

2. Ensure your `configuration.yaml` allows custom integrations.

3. Restart Home Assistant.

---

## ⚙️ Configuration

Go to **Settings > Devices & Services > Add Integration** and search for **USGS Quakes**.

You’ll need to provide:

- **Latitude / Longitude**: Center location for the search
- **Radius (km)**: Area around your location to include in the feed
- **Minimum Magnitude**: Filter to show only significant quakes
- **Feed Type**: Select one of the 20 feed options provided by USGS (e.g., `past_hour_m1.0`, `past_day_all`, etc.)

Only one instance is allowed in this version.

---

## 📡 Feed Types

Feed types are based on the official USGS GeoJSON feed identifiers. Some examples:

- `past_hour_all`
- `past_day_m2.5`
- `past_week_significant`
- `past_month_all`

See full list at:  
👉 [https://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php](https://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php)

---

## 🛰️ Entity Details

Each earthquake creates a `geo_location` entity with:

- **Name**: Earthquake title
- **Latitude / Longitude**
- **Magnitude**
- **Time**
- **Status**
- **Place**
- **Updated timestamp**

---

## 🛠️ Known Limitations

- Only a single instance can be configured (multi-instance support will be added in future versions).
- No options flow yet (editing requires removing and re-adding the integration).
- No persistent history of past events (only current events in feed).

---

## 📘 Documentation

For more information and updates:  
**GitHub**: [https://github.com/Geek-MD/USGS_Quakes](https://github.com/Geek-MD/USGS_Quakes)

---

## 👨‍💻 Author

Developed by [Geek-MD](https://github.com/Geek-MD)

---

## 📄 License

MIT License
