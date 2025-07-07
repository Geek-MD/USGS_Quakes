from __future__ import annotations

import logging

from homeassistant.components.geo_location import GeoLocationEvent
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from aio_geojson_usgs_earthquakes.usgs_earthquake_feed import USGSEarthquakeFeed, USGS_EARTHQUAKE_FEED

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]

    async def _update_entities():
        async_add_entities([], True)
        entities = [
            USGSEarthquakeGeoLocation(entry.entry_id, event)
            for event in coordinator.entries
        ]
        async_add_entities(entities, True)

    coordinator.async_add_listener(_update_entities)
    await coordinator.async_request_refresh()


class USGSEarthquakeGeoLocation(GeoLocationEvent):
    def __init__(self, config_entry_id: str, event: FeedEntry):
        self._event = event
        self._attr_unique_id = f"usgs_quake_{hash(event.external_id)}"
        self._attr_name = event.title
        self._attr_source = "usgs"
        self._attr_unit_of_measurement = "km"
        self._attr_location = (event.coordinates[1], event.coordinates[0])
        self._attr_extra_state_attributes = {
            "magnitude": event.magnitude,
            "status": event.status,
            "alert": event.alert,
            "url": event.external_id,
            "time": event.published.isoformat(),
        }

    @property
    def latitude(self):
        return self._event.coordinates[1]

    @property
    def longitude(self):
        return self._event.coordinates[0]

    @property
    def location_accuracy(self):
        return None

    @property
    def source(self):
        return "usgs"
