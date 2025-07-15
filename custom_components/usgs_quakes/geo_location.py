"""GeoLocation platform for USGS Quakes integration."""

from __future__ import annotations

from datetime import timedelta
import logging

from aio_geojson_client.feed_manager import FeedManager
from aio_geojson_usgs_earthquakes import USGSEarthquakeFeed

from homeassistant.components.geo_location import GeoLocationEvent
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the USGS Quakes platform."""
    latitude = entry.data["latitude"]
    longitude = entry.data["longitude"]
    radius = entry.data["radius"]
    minimum_magnitude = entry.data["minimum_magnitude"]
    feed_type = entry.data["feed_type"]

    session = async_get_clientsession(hass)

    feed = USGSEarthquakeFeed(
        session=session,
        home_coordinates=(latitude, longitude),
        filter_radius=radius,
        filter_minimum_magnitude=minimum_magnitude,
        feed_type=feed_type,
    )

    manager = FeedManager(
        hass,
        feed,
        generate_entity,
        DOMAIN,
        entry.entry_id,
    )

    hass.data[DOMAIN][entry.entry_id] = manager

    async def update_feed(now):
        await manager.update()

    async_track_time_interval(hass, update_feed, timedelta(minutes=5))
    await manager.update()


def generate_entity(external_id, unit, attributes) -> USGSQuakeEntity:
    """Generate a new USGS Quake entity."""
    return USGSQuakeEntity(external_id, unit, attributes)


class USGSQuakeEntity(GeoLocationEvent):
    """Represents a USGS Quake geo location event."""

    def __init__(self, external_id: str, unit: str, attributes: dict) -> None:
        """Initialize the USGS Quake entity."""
        self._attr_unique_id = external_id
        self._attr_source = DOMAIN
        self._attr_name = attributes.get("title")
        self._attr_unit_of_measurement = unit
        self._attr_latitude = attributes.get("latitude")
        self._attr_longitude = attributes.get("longitude")
        self._attr_distance = attributes.get("distance")
        self._attr_extra_state_attributes = attributes

    @property
    def should_poll(self) -> bool:
        """No polling needed for GeoLocation entity."""
        return False
