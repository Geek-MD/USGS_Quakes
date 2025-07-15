from datetime import timedelta
from homeassistant.helpers.event import async_track_time_interval

from aio_geojson_usgs_earthquakes.feed_manager import USGSEarthquakeFeedManager
from .const import DOMAIN


async def setup_platform(hass, config_entry):
    data = config_entry.data
    latitude = data["latitude"]
    longitude = data["longitude"]
    radius = data["radius"]
    min_magnitude = data["minimum_magnitude"]
    feed_type = data["feed_type"]

    session = hass.helpers.aiohttp_client.async_get_clientsession(hass)

    manager = USGSEarthquakeFeedManager(
        hass,
        lambda event_type, entity: None,  # No custom entity handling
        feed_type,
        (latitude, longitude),
        radius,
        min_magnitude,
        session,
    )

    hass.data.setdefault(DOMAIN, {})[config_entry.entry_id] = {
        "manager": manager,
    }

    async def update_feed(now):
        await manager.update()

    async_track_time_interval(hass, update_feed, timedelta(minutes=5))
    await manager.update()
