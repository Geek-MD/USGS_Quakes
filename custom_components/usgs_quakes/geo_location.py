from homeassistant.components.geo_location import GeoLocationEvent
from homeassistant.helpers.entity import generate_entity_id
from homeassistant.helpers.event import async_track_time_interval
from datetime import timedelta

from aio_geojson_usgs_earthquakes import USGSEarthquakeFeedManager

from .const import DOMAIN

ENTITY_ID_FORMAT = "geo_location.usgs_quake_{}"

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
        lambda event_type, entity: _handle_event(hass, event_type, entity),
        feed_type,
        (latitude, longitude),
        radius,
        min_magnitude,
        session,
    )

    hass.data.setdefault(DOMAIN, {})[config_entry.entry_id] = {
        "manager": manager,
        "entities": {},
    }

    async def update_feed(now):
        await manager.update()

    async_track_time_interval(hass, update_feed, timedelta(minutes=5))
    await manager.update()


def _handle_event(hass, event_type, entity):
    # Puedes implementar creación de entidades reales aquí si lo deseas
    pass
