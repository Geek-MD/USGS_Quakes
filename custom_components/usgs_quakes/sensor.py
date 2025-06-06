from datetime import timedelta
import logging

from aio_geojson_usgs_earthquakes.usgs_earthquake_feed import USGSEarthquakeFeed
from aio_geojson_usgs_earthquakes.feed_entry import USGSEarthquakeFeedEntry

from homeassistant.components.sensor import SensorEntity
from homeassistant.components.geo_location import ATTR_SOURCE, GeoLocationEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity, DataUpdateCoordinator
from homeassistant.util.unit_system import METRIC_SYSTEM

from .const import (
    DOMAIN,
    CONF_LATITUDE,
    CONF_LONGITUDE,
    CONF_RADIUS,
    CONF_MINIMUM_MAGNITUDE,
    CONF_FEED_TYPE
)

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(minutes=5)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    latitude = entry.data[CONF_LATITUDE]
    longitude = entry.data[CONF_LONGITUDE]
    radius = entry.data[CONF_RADIUS]
    min_magnitude = entry.data.get(CONF_MINIMUM_MAGNITUDE, 0.0)
    feed_type = entry.data.get(CONF_FEED_TYPE, "past_day_all")

    feed = USGSEarthquakeFeed(
        home_coordinates=(latitude, longitude),
        filter_radius=radius,
        filter_minimum_magnitude=min_magnitude,
        feed_type=feed_type
    )

    coordinator = USGSDataUpdateCoordinator(hass, feed)
    await coordinator.async_refresh()

    sensor = USGSEarthquakeSensor(coordinator, entry)
    async_add_entities([sensor], True)

    geo_entities = [
        USGSEarthquakeGeoLocation(entry.entry_id, event)
        for event in coordinator.entries
    ]
    async_add_entities(geo_entities, True)


class USGSDataUpdateCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, feed: USGSEarthquakeFeed):
        super().__init__(
            hass,
            _LOGGER,
            name="USGS Quakes Feed Coordinator",
            update_interval=SCAN_INTERVAL,
        )
        self.feed = feed
        self.entries: list[USGSEarthquakeFeedEntry] = []

    async def _async_update_data(self):
        status, entries = await self.feed.update()
        if status == "OK" and entries:
            self.entries = entries
        return self.entries


class USGSEarthquakeSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator: USGSDataUpdateCoordinator, entry: ConfigEntry):
        super().__init__(coordinator)
        self._attr_name = "Nearby Earthquakes"
        self._attr_unique_id = "usgs_quakes_latest"
        self._entry = entry

    @property
    def native_value(self):
        if not self.coordinator.entries:
            return None

        latest = self.coordinator.entries[0]
        magnitude = latest.magnitude
        distance_km = latest.distance or 0.0

        if self.hass.config.units is METRIC_SYSTEM:
            distance = round(distance_km, 1)
            unit = "km"
        else:
            distance = round(distance_km * 0.621371, 1)
            unit = "mi"

        return f"{magnitude} ({distance} {unit})"

    @property
    def extra_state_attributes(self):
        if not self.coordinator.entries:
            return {}

        latest = self.coordinator.entries[0]
        distance_km = latest.distance or 0.0

        if self.hass.config.units is METRIC_SYSTEM:
            distance = round(distance_km, 1)
            unit = "km"
        else:
            distance = round(distance_km * 0.621371, 1)
            unit = "mi"

        recent_events = [
            {
                "id": e.external_id,
                "title": e.title,
                "magnitude": e.magnitude,
                "time": e.published.isoformat(),
                "coordinates": e.coordinates,
                "alert": e.alert,
                "url": e.external_id,
                "distance_km": e.distance
            }
            for e in self.coordinator.entries
        ]

        return {
            "place": latest.title,
            "magnitude": latest.magnitude,
            "coordinates": latest.coordinates,
            "time": latest.published,
            "status": latest.status,
            "alert": latest.alert,
            "url": latest.external_id,
            "distance": distance,
            "distance_unit": unit,
            "recent_events": recent_events
        }


class USGSEarthquakeGeoLocation(GeoLocationEntity):
    def __init__(self, config_entry_id: str, event: USGSEarthquakeFeedEntry):
        self._event = event
        self._attr_unique_id = f"usgs_quake_{event.external_id.split('/')[-1]}"
        self._attr_name = event.title
        self._attr_latitude = event.coordinates[1]
        self._attr_longitude = event.coordinates[0]
        self._attr_source = DOMAIN
        self._attr_unit_of_measurement = "km"
        self._attr_extra_state_attributes = {
            "magnitude": event.magnitude,
            "time": event.published.isoformat(),
            "alert": event.alert,
            "url": event.external_id,
        }
        self._attr_location_accuracy = None
        self._attr_icon = "mdi:map-marker-alert"

    @property
    def latitude(self):
        return self._attr_latitude

    @property
    def longitude(self):
        return self._attr_longitude

    @property
    def source(self):
        return DOMAIN

    @property
    def extra_state_attributes(self):
        return self._attr_extra_state_attributes
