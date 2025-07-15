from datetime import timedelta
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from aio_geojson_usgs_earthquakes.feed_manager import USGSEarthquakeFeedManager

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant, config_entry: ConfigType, async_add_entities
) -> None:
    """Set up the USGS Earthquakes geo_location platform."""
    data = config_entry.data
    latitude = data["latitude"]
    longitude = data["longitude"]
    radius = data["radius"]
    min_magnitude = data["minimum_magnitude"]
    feed_type = data["feed_type"]

    session = async_get_clientsession(hass)

    manager = USGSEarthquakeFeedManager(
        hass,
        async_add_entities,
        feed_type,
        (latitude, longitude),
        radius,
        min_magnitude,
        session,
    )

    hass.data.setdefault(DOMAIN, {})[config_entry.entry_id] = {
        "manager": manager,
    }

    async def update(event_time):
        await manager.update()

    async_track_time_interval(hass, update, timedelta(minutes=5))
    await manager.update()
