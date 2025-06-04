from datetime import timedelta
import logging

from aio_geojson_usgs_earthquakes import USGSEarthquakeFeed
from aio_geojson_usgs_earthquakes.feed_entry import USGSEarthquakeFeedEntry

from homeassistant.components.sensor import SensorEntity
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

    async_add_entities([USGSEarthquakeSensor(coordinator)], True)


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
    def __init__(self, coordinator: USGSDataUpdateCoordinator):
        super().__init__(coordinator)
        self._attr_name = "Nearby Earthquakes"
        self._attr_unique_id = "usgs_quakes_latest"

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

        return {
            "place": latest.title,
            "magnitude": latest.magnitude,
            "coordinates": latest.coordinates,
            "time": latest.published,
            "status": latest.status,
            "alert": latest.alert,
            "url": latest.external_id,
            "distance": distance,
            "distance_unit": unit
        }
