from homeassistant import config_entries
import voluptuous as vol
from homeassistant.const import CONF_LATITUDE, CONF_LONGITUDE
from homeassistant.helpers import config_validation as cv

from aio_geojson_usgs_earthquakes.feed import USGS_EARTHQUAKE_FEED

from .const import (
    DOMAIN,
    CONF_RADIUS,
    CONF_MINIMUM_MAGNITUDE,
    CONF_FEED_TYPE,
    DEFAULT_RADIUS,
    DEFAULT_MINIMUM_MAGNITUDE,
)


class UsgsQuakesConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="USGS Quakes", data=user_input)

        schema = vol.Schema({
            vol.Required(CONF_LATITUDE): cv.latitude,
            vol.Required(CONF_LONGITUDE): cv.longitude,
            vol.Optional(CONF_RADIUS, default=DEFAULT_RADIUS): vol.Coerce(float),
            vol.Optional(CONF_MINIMUM_MAGNITUDE, default=DEFAULT_MINIMUM_MAGNITUDE): vol.Coerce(float),
            vol.Required(CONF_FEED_TYPE): vol.In(list(USGS_EARTHQUAKE_FEED.keys())),
        })

        return self.async_show_form(step_id="user", data_schema=schema)
