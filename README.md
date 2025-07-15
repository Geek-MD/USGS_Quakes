# USGS Quakes

**USGS Quakes** is a custom integration for [Home Assistant](https://www.home-assistant.io) that creates geolocation entities from the USGS Earthquake Hazards Program feeds.

This integration monitors seismic activity and creates `geo_location` entities for each detected earthquake event within a defined radius and magnitude threshold.

## Features

- Retrieves earthquake data from USGS feeds.
- Creates `geo_location` entities with magnitude, location, time, and more.
- Supports 20 different USGS feed types (e.g., past hour, past day, significant, magnitude thresholds).
- Filters by radius (km) and minimum magnitude.
- Configurable through the Home Assistant UI.

## Installation

1. Copy the `usgs_quakes` folder into your `config/custom_components/` directory.
2. Restart Home Assistant.
3. Go to **Settings > Devices & Services > Integrations**, click **Add Integration**, and search for **USGS Quakes**.

## Configuration

All configuration is handled through the UI. You will be prompted to:

- Set your latitude and longitude.
- Choose a feed type.
- Define a search radius in kilometers.
- Set a minimum magnitude.

## Feed Types

The integration supports the following feed types:

- `past_hour_all_earthquakes`
- `past_hour_significant_earthquakes`
- `past_day_all_earthquakes`
- `past_day_significant_earthquakes`
- `past_day_4.5_earthquakes`
- `past_day_2.5_earthquakes`
- `past_day_1.0_earthquakes`
- `past_week_all_earthquakes`
- `past_week_significant_earthquakes`
- `past_week_4.5_earthquakes`
- `past_week_2.5_earthquakes`
- `past_week_1.0_earthquakes`
- `past_month_all_earthquakes`
- `past_month_significant_earthquakes`
- `past_month_4.5_earthquakes`
- `past_month_2.5_earthquakes`
- `past_month_1.0_earthquakes`
- `summary_significant_month`
- `summary_significant_week`
- `summary_significant_day`

## Notes

- Entity updates occur every 5 minutes.
- Events are shown as geolocation entities in Home Assistant.

## Credits

Developed by [Geek-MD](https://github.com/Geek-MD)
