from datetime import timedelta
from homeassistant.components.geo_location import GeoLocationEvent
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from aio_geojson_usgs_earthquakes import USGSEarthquakeFeed
from aio_geojson_client.feed_manager import FeedManager

from .const import DOMAIN

async def async_setup_entry(hass, config_entry, async_add_entities):
    data = config_entry.data
    latitude = data["latitude"]
    longitude = data["longitude"]
    radius = data["radius"]
    min_magnitude = data["minimum_magnitude"]
    feed_type = data["feed_type"]

    session = async_get_clientsession(hass)

    feed = USGSEarthquakeFeed(
        session=session,
        home_coordinates=(latitude, longitude),
        filter_radius=radius,
        filter_minimum_magnitude=min_magnitude,
        feed_type=feed_type,
    )

    manager = FeedManager(
        hass,
        feed,
        generate_entity,
        DOMAIN,
        config_entry.entry_id,
    )

    hass.data.setdefault(DOMAIN, {})[config_entry.entry_id] = {
        "manager": manager,
    }

    async def update_feed(now):
        await manager.update()

    async_track_time_interval(hass, update_feed, timedelta(minutes=5))
    await manager.update()

def generate_entity(external_id, unit, attributes):
    return USGSQuakeEntity(external_id, unit, attributes)

class USGSQuakeEntity(GeoLocationEvent):
    def __init__(self, external_id, unit, attributes):
        self._attr_unique_id = external_id
        self._attr_source = "usgs_quakes"
        self._attr_name = attributes.get("title")
        self._attr_unit_of_measurement = unit
        self._attr_latitude = attributes.get("latitude")
        self._attr_longitude = attributes.get("longitude")
        self._attr_distance = attributes.get("distance")
        self._attr_extra_state_attributes = attributes

    @property
    def should_poll(self):
        return False
