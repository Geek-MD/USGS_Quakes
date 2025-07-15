# USGS Quakes

**USGS Quakes** is a custom integration for [Home Assistant](https://www.home-assistant.io/) that allows you to receive real-time geolocation updates of earthquake events from the [USGS Earthquake Hazards Program](https://earthquake.usgs.gov/).

## Features

- Integration with USGS Earthquake GeoJSON feeds
- Dynamically creates `geo_location` entities for new earthquake events
- Filters by:
  - Location (latitude, longitude, radius)
  - Minimum magnitude
  - Feed type (e.g. significant, all, past hour/day/week/month)

## Configuration

This integration is configured via the Home Assistant UI. Go to **Settings > Devices & Services > Integrations**, click **Add Integration**, and search for `USGS Quakes`.

### Required Fields

- **Latitude / Longitude**: Your location
- **Feed Type**: Select one of the available USGS feed types
- **Radius (Km)**: Filter results by proximity
- **Minimum Magnitude (Mw)**: Filter results by magnitude threshold

## Feed Types

| ID                    | Description            |
|-----------------------|------------------------|
| all_earthquakes       | All Earthquakes        |
| significant_earthquakes | Significant Earthquakes |
| past_hour             | Past Hour              |
| past_day              | Past Day               |
| past_week             | Past Week              |
| past_month            | Past Month             |

## Notes

- Updates are fetched every 5 minutes.
- This integration requires internet connectivity.

## Credits

This integration is based on:
- [`aio-geojson-usgs-earthquakes`](https://pypi.org/project/aio-geojson-usgs-earthquakes/)
- [`aio-geojson-client`](https://pypi.org/project/aio-geojson-client/)
