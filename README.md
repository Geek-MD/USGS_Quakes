# USGS Quakes

**USGS Quakes** is a custom integration for [Home Assistant](https://www.home-assistant.io/) that monitors earthquake activity using the [USGS Earthquake Feeds](https://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php).

It provides:

- A **sensor** (`sensor.usgs_quakes_latest`) showing the most recent nearby earthquake.
- A list of **recent events** as an attribute (`recent_events`).
- Dynamic creation of **geo_location entities** for each earthquake.
- Support for **20 different USGS feeds**, with configurable filters.

---

## Installation

Install the integration through [HACS](https://hacs.xyz/), or copy the repository folder to:

~~~plaintext
custom_components/usgs_quakes/
~~~

---

## Configuration

Add the integration via **Home Assistant UI**:

1. Go to **Settings > Devices & Services > Integrations > + Add Integration**
2. Search for `USGS Quakes`
3. Enter your:
   - Latitude and longitude
   - Radius (km)
   - Minimum magnitude
   - Feed type (select from 20 available)

You can change these settings later from the **Options menu**.

---

## Entities

### `sensor.usgs_quakes_latest`

This sensor displays:

- The magnitude and distance of the most recent earthquake.
- Attributes:
  - `place`: Description
  - `magnitude`
  - `coordinates`
  - `time`
  - `status`
  - `alert`
  - `url`
  - `distance`: Automatically shown in **kilometers or miles**, depending on your Home Assistant unit settings.
  - `distance_unit`: `"km"` or `"mi"`
  - `recent_events`: List of events from the selected feed

---

### `geo_location.usgs_quake_*`

Each earthquake event is represented as a `geo_location` entity:

- Location: Latitude and longitude of the event
- Attributes:
  - `magnitude`
  - `time`
  - `alert`
  - `url`

Entities are automatically updated and replaced whenever the feed is refreshed (every 5 minutes).

---

## Cards

You can add the following cards to your dashboard:

### Entities Card

~~~yaml
type: entities
title: Nearby Earthquake
entities:
  - entity: sensor.usgs_quakes_latest
  - type: attribute
    entity: sensor.usgs_quakes_latest
    attribute: place
    name: Location
  - type: attribute
    entity: sensor.usgs_quakes_latest
    attribute: magnitude
    name: Magnitude
  - type: attribute
    entity: sensor.usgs_quakes_latest
    attribute: distance
    name: Distance
  - type: attribute
    entity: sensor.usgs_quakes_latest
    attribute: time
    name: Time
~~~

### Map Card

~~~yaml
type: map
title: Earthquake Map
entities:
  - geo_location.usgs_quake_*
hours_to_show: 24
~~~

---

## Supported Feeds

This integration supports all 20 official USGS GeoJSON feed types, including:

- `past_hour_all`
- `past_hour_2.5`
- `past_day_significant`
- `past_7days_4.5`
- `past_30days_all`
- *(and many more)*

You can change the active feed anytime through the Options menu.

---

## Attribution

Earthquake data provided by the [United States Geological Survey (USGS)](https://earthquake.usgs.gov/).
