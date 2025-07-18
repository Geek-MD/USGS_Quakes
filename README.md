# USGS Quakes

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-blue.svg?style=flat-square)](https://hacs.xyz)

**USGS Quakes** is a custom integration for Home Assistant that provides real-time earthquake geolocation data based on the [USGS Earthquake Hazards Program](https://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php).

This integration creates `geo_location` entities in Home Assistant from the USGS GeoJSON feed, filtered by location, radius, and minimum magnitude.

## Features

- 🔍 Supports all 20 official USGS feed types.
- 🌐 Filters by geographic radius and minimum magnitude.
- 📍 Uses Home Assistant's configured location by default.
- ⚠️ Updates entities every 5 minutes using the cloud-based USGS feed.
- 🧭 Distance is automatically displayed in kilometers or miles, depending on your region settings.
- 🔧 Supports reconfiguration via UI using `Options Flow`.

## Configuration

This integration is fully configurable via the Home Assistant UI.  
Go to **Settings > Devices & Services > Add Integration** and search for **USGS Quakes**.

### Initial Setup

- **Latitude / Longitude**: Defaults to your Home Assistant configured location.
- **Radius**: Radius in kilometers from the selected location.
- **Minimum Magnitude**: Filter out minor quakes below this magnitude.
- **Feed Type**: Choose the USGS feed type (e.g. `past_day_all_earthquakes`, `summary_significant_week`, etc).

### Reconfiguration (Options Flow)

After the initial setup, you can update the following values via the integration settings:

- **Radius**
- **Minimum Magnitude**
- **Feed Type**

## Example Entity

Once configured, entities will be created dynamically for each detected earthquake:

```yaml
geo_location.usgs_quake_m6_7_mexico:
  source: usgs_quakes
  latitude: 17.0
  longitude: -99.0
  magnitude: 6.7
  distance: 440.2
  place: Guerrero, Mexico
  status: reviewed
  type: earthquake
  alert: red
```

## Credits

This integration is based on the official [`usgs_earthquakes_feed`](https://github.com/home-assistant/core/tree/dev/homeassistant/components/usgs_earthquakes_feed) integration from the Home Assistant Core repository.

Additional features, such as options flow and entity-device linking, have been added and adapted by [@Geek-MD](https://github.com/Geek-MD).
