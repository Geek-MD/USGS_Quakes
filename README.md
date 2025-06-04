# USGS Quakes

**USGS Quakes** is a custom integration for [Home Assistant](https://www.home-assistant.io) that monitors nearby earthquakes using the [USGS Earthquake GeoJSON Feed](https://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php).

---

## 📦 Features

- Configurable via the Home Assistant UI (no YAML required)
- Monitors earthquakes around a user-defined location
- Filters results by radius (in km) and minimum magnitude
- Sensor entity reports the most recent nearby earthquake
- Sensor attributes include location, magnitude, coordinates, time, status, alert level, and link to the event

---

## 🧭 Installation via HACS

1. In Home Assistant, open **HACS > Integrations**.
2. Click on **⋮ > Custom repositories**.
3. Add the following repository URL:

       https://github.com/Geek-MD/USGS_Quakes

   Use category: **Integration**.

4. Install **USGS Quakes**.
5. Restart Home Assistant.

---

## ⚙️ Configuration

1. Go to **Settings > Devices & Services > Add Integration**.
2. Search for **USGS Quakes**.
3. Configure:
   - **Latitude** (your location)
   - **Longitude**
   - **Radius** (distance in km to monitor)
   - **Minimum magnitude** (e.g. 2.5)

You can later adjust filters via the **Options** menu.

---

## 📡 Sensor Entity

After configuration, the integration creates a sensor:

       sensor.usgs_quakes_latest

### Example Attributes:

    magnitude: 5.2
    place: 50 km NW of Coquimbo, Chile
    coordinates: [-71.5, -30.1]
    time: 2025-06-04T10:12:00Z
    status: reviewed
    alert: green
    url: https://earthquake.usgs.gov/earthquakes/eventpage/us7000abcd

---

## 🚧 Roadmap

- [ ] Support multiple monitored zones
- [ ] Send notifications for high-magnitude events
- [ ] Lovelace card with alert badges

---

## 🧑‍💻 Author

Developed by [@Geek-MD](https://github.com/Geek-MD)

---

## 📄 License

[MIT](LICENSE)
