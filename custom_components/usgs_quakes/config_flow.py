import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_LATITUDE, CONF_LONGITUDE
from homeassistant.core import callback

from .const import (
    DOMAIN,
    CONF_RADIUS,
    CONF_MINIMUM_MAGNITUDE,
    CONF_FEED_TYPE,
    DEFAULT_RADIUS,
    DEFAULT_MINIMUM_MAGNITUDE,
)

@callback
def configured_instances(hass):
    return hass.config_entries.async_entries(DOMAIN)

class USGSQuakesConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if configured_instances(self.hass):
            return self.async_abort(reason="single_instance_allowed")

        errors = {}

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
            errors=errors,
        )
