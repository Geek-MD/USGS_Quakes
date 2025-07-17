from __future__ import annotations

from datetime import timedelta
import logging

from aiohttp import ClientSession
from aio_geojson_usgs_earthquakes import USGSEarthquakeFeed
from aio_geojson_client.feed_manager import FeedManager

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.event import async_track_time_interval

from .const import (
    DOMAIN,
    CONF_LATITUDE,
    CONF_LONGITUDE,
    CONF_RADIUS,
    CONF_MINIMUM_MAGNITUDE,
    CONF_FEED_TYPE,
)

PLATFORMS: list[str] = ["geo_location"]

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up USGS Quakes from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    latitude = entry.data[CONF_LATITUDE]
    longitude = entry.data[CONF_LONGITUDE]

    # Read from options if available; fall back to data
    radius = entry.options.get(CONF_RADIUS, entry.data[CONF_RADIUS])
    minimum_magnitude = entry.options.get(CONF_MINIMUM_MAGNITUDE, entry.data[CONF_MINIMUM_MAGNITUDE])
    feed_type = entry.options.get(CONF_FEED_TYPE, entry.data[CONF_FEED_TYPE])

    session: ClientSession = async_get_clientsession(hass)

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
        lambda external_id, unit, attributes: None,
        DOMAIN,
        entry.entry_id,
    )

    hass.data[DOMAIN][entry.entry_id] = {"manager": manager}

    async def update_feed(now):
        await manager.update()

    async_track_time_interval(hass, update_feed, timedelta(minutes=5))
    await manager.update()

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
