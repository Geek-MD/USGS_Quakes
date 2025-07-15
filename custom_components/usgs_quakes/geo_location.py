from __future__ import annotations

from datetime import timedelta
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_registry import async_get
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from aio_geojson_client.feed_manager import GeoJsonFeedManager
from aio_geojson_usgs_earthquakes import USGSEarthquakeFeed

from .const import (
    CONF_MINIMUM_MAGNITUDE,
    CONF_RADIUS,
    CONF_FEED_TYPE,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, config_entry: ConfigType, async_add_entities
) -> None:
    """Set up the USGS Quakes geo_location platform from config entry."""
    config = config_entry.data
    latitude = config_entry.data["latitude"]
    longitude = config_entry.data["longitude"]
    radius = config[CONF_RADIUS]
    minimum_magnitude = config[CONF_MINIMUM_MAGNITUDE]
    feed_type = config[CONF_FEED_TYPE]

    websession = async_get_clientsession(hass)

    feed = USGSEarthquakeFeed(
        websession, feed_type, (latitude, longitude), radius, minimum_magnitude
    )

    manager = GeoJsonFeedManager(hass, _LOGGER, feed, async_add_entities)

    hass.data.setdefault(DOMAIN, {})[config_entry.entry_id] = manager

    async def update(event_time):
        await manager.update()

    async_track_time_interval(hass, update, timedelta(minutes=5))
    await manager.update()
