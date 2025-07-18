# USGS Quakes

A custom integration for Home Assistant that provides real-time earthquake data from the United States Geological Survey (USGS).

## Features

- Displays earthquakes as `geo_location` entities on the Home Assistant map.
- Filters based on:
  - Minimum magnitude
  - Radius around your location
  - USGS feed type (hourly, daily, weekly, etc.)
- Automatically updates feed every 5 minutes.
- Supports full configuration and reconfiguration via the Home Assistant UI.

## Installation

1. Copy the `usgs_quakes` folder to your `/config/custom_components/` directory.
2. Restart Home Assistant.
3. Go to **Settings > Devices & Services**, click **Add Integration**, and search for **USGS Quakes**.

## Configuration

All options are available via the UI:

- **Latitude / Longitude**: Your home coordinates (auto-filled).
- **Radius**: Distance in kilometers around your location to monitor earthquakes.
- **Minimum Magnitude**: Threshold magnitude (e.g., 2.5).
- **Feed Type**: Select the USGS feed you want (e.g., `past_day_all_earthquakes`).

You can reconfigure any of these options from the integration instance menu.

## Supported Feed Types

See the [USGS Earthquake Feeds documentation](https://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php) for full details.

## Dependencies

- [`aio-geojson-usgs-earthquakes`](https://pypi.org/project/aio-geojson-usgs-earthquakes/)
- [`aio-geojson-client`](https://pypi.org/project/aio-geojson-client/)

## Credits

Developed by [@Geek-MD](https://github.com/Geek-MD)

## License

MIT License
