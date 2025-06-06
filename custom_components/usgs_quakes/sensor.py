from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfLength
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from aio_geojson_client.usgs_earthquake_feed import USGSEarthquakeFeed
from aio_geojson_client.feed_entry import FeedEntry

from .const import (
    DOMAIN,
    CONF_LATITUDE,
    CONF_LONGITUDE,
    CONF_RADIUS,
    CONF_MINIMUM_MAGNITUDE,
    CONF_FEED_TYPE,
)

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(minutes=5)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    coordinator: USGSDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    await coordinator.async_refresh()
    async_add_entities([USGSEarthquakeSensor(coordinator, hass)], True)


class USGSDataUpdateCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, feed: USGSEarthquakeFeed):
        super().__init__(
            hass,
            _LOGGER,
            name="USGS Quakes Feed Coordinator",
            update_interval=SCAN_INTERVAL,
        )
        self.feed = feed
        self.entries: list[FeedEntry] = []

    async def _async_update_data(self):
        status, entries = await self.feed.update()
        if status == "OK" and entries:
            self.entries = entries
        return self.entries


class USGSEarthquakeSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator: USGSDataUpdateCoordinator, hass: HomeAssistant):
        super().__init__(coordinator)
        self._hass = hass
        self._attr_name = "Nearby Earthquakes"
        self._attr_unique_id = "usgs_quakes_latest"

    @property
    def native_value(self):
        if self.coordinator.entries:
            return self.coordinator.entries[0].magnitude
        return None

    @property
    def extra_state_attributes(self):
        if not self.coordinator.entries:
            return {}

        latest = self.coordinator.entries[0]

        # Determine unit system and convert distance
        is_metric = self._hass.config.units.name == "metric"
        unit = "km" if is_metric else "mi"
        distance = latest.distance if is_metric else round(latest.distance * 0.621371, 2)

        # Build recent events list
        recent = [
            {
                "title": e.title,
                "magnitude": e.magnitude,
                "time": e.published.isoformat(),
                "url": e.external_id,
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
            "distance": round(distance, 2),
            "distance_unit": unit,
            "recent_events": recent,
        }
