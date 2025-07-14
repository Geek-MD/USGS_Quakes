from datetime import timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from aio_geojson_usgs_earthquakes import USGS_EARTHQUAKE_FEED, FeedManager
from .const import *

class UsgsEarthquakeFeedCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        self.hass = hass
        self.entry = entry

        latitude = entry.data[CONF_LATITUDE]
        longitude = entry.data[CONF_LONGITUDE]
        radius = entry.data.get(CONF_RADIUS, DEFAULT_RADIUS)
        minimum_magnitude = entry.data.get(CONF_MINIMUM_MAGNITUDE, DEFAULT_MINIMUM_MAGNITUDE)
        feed_type = entry.data[CONF_FEED_TYPE]
        url = USGS_EARTHQUAKE_FEED[feed_type]

        self.feed_manager = FeedManager(
            self._generate_callback, url, (latitude, longitude), filter_radius=radius,
            minimum_magnitude=minimum_magnitude, websession=hass.helpers.aiohttp_client.async_get_clientsession(hass)
        )

        super().__init__(
            hass,
            logger=hass.helpers.logger.async_get_logger(__name__),
            name=f"USGS Quakes ({feed_type})",
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL)
        )

    async def _async_update_data(self):
        await self.feed_manager.update()

    def _generate_callback(self, event_type, entity):
        # Future enhancement: we could track created/removed earthquakes
        pass
