from homeassistant import config_entries
from homeassistant.const import CONF_LATITUDE, CONF_LONGITUDE
import voluptuous as vol

from .const import (
    DOMAIN,
    CONF_RADIUS,
    CONF_MINIMUM_MAGNITUDE,
    CONF_FEED_TYPE,
    DEFAULT_RADIUS,
    DEFAULT_MINIMUM_MAGNITUDE,
)


class USGSQuakesConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        if user_input is not None:
            return self.async_create_entry(title="USGS Quakes", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_LATITUDE): float,
                vol.Required(CONF_LONGITUDE): float,
                vol.Optional(CONF_RADIUS, default=DEFAULT_RADIUS): float,
                vol.Optional(CONF_MINIMUM_MAGNITUDE, default=DEFAULT_MINIMUM_MAGNITUDE): float,
                vol.Required(CONF_FEED_TYPE): str,
            }),
        )
