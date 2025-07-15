# USGS Quakes
**USGS Quakes** is a custom integration for [Home Assistant](https://www.home-assistant.io) that monitors real-time earthquake data from the [United States Geological Survey (USGS)](https://earthquake.usgs.gov/earthquakes/feed/).

This integration is based on the official USGS Earthquake Feed integration, but adds support for configuration through the Home Assistant UI (`config_flow`).

## Features
- Monitors earthquakes in near real-time from USGS.
- Allows selection of feed type (e.g., all earthquakes, significant, past hour/day/week).
- Filters by radius and minimum magnitude.
- Displays distance and magnitude for each event.
- Works as a `geo_location` entity in Home Assistant.

## Installation
1. Copy this repository to your `custom_components` directory:
   ```bash
   custom_components/usgs_quakes/
   ```
2. Restart Home Assistant.
3. Go to **Settings > Devices & Services > Integrations**, click **Add Integration**, and search for **USGS Quakes**.

## Configuration Options
- **Feed type**: Select the type of earthquake feed (e.g., all, significant).
- **Radius**: Distance (in kilometers) around your location to filter results.
- **Minimum magnitude**: Ignore earthquakes below this magnitude.
- **Latitude & Longitude**: Optional. If not provided, Home Assistant's configured location is used.

## Supported Feed Types
This integration supports all 20 feed types provided by USGS:
- `all_hour`, `1.0_hour`, `2.5_hour`, `4.5_hour`, `significant_hour`
- `all_day`, `1.0_day`, `2.5_day`, `4.5_day`, `significant_day`
- `all_week`, `1.0_week`, `2.5_week`, `4.5_week`, `significant_week`
- `all_month`, `1.0_month`, `2.5_month`, `4.5_month`, `significant_month`

## Credits
Based on the official [usgs_earthquakes_feed](https://www.home-assistant.io/integrations/usgs_earthquakes_feed) integration.

## License
MIT License
