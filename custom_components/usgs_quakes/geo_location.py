from datetime import timedelta
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from aio_geojson_client.feed_manager import GeoJsonFeedManager
from aio_geojson_usgs_earthquakes.usgs_quakes_feed import USGSEarthquakeFeed

from .const import DOMAIN


async def setup_platform(hass, config_entry):
    data = config_entry.data
    latitude = data["latitude"]
    longitude = data["longitude"]
    radius = data["radius"]
    min_magnitude = data["minimum_magnitude"]
    feed_type = data["feed_type"]

    session = async_get_clientsession(hass)

    manager = GeoJsonFeedManager(
        hass,
        lambda event_type, entity: None,  # No custom entity handling
        USGSEarthquakeFeed(
            feed_type,
            session,
            (latitude, longitude),
            filter_radius=radius,
            filter_minimum_magnitude=min_magnitude,
        ),
    )

    hass.data.setdefault(DOMAIN, {})[config_entry.entry_id] = {
        "manager": manager,
    }

    async def update_feed(now):
        await manager.update()

    async_track_time_interval(hass, update_feed, timedelta(minutes=5))
    await manager.update()
