from homeassistant import config_entries
import voluptuous as vol
from homeassistant.const import CONF_LATITUDE, CONF_LONGITUDE, CONF_RADIUS

from .const import (
    DOMAIN,
    DEFAULT_RADIUS_IN_KM,
    DEFAULT_MINIMUM_MAGNITUDE,
    CONF_FEED_TYPE,
    CONF_MINIMUM_MAGNITUDE,
    VALID_FEED_TYPES,
)

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for USGS Quakes."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        # 🚫 Prevent multiple instances
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        if user_input is not None:
            return self.async_create_entry(title="USGS Quakes", data=user_input)

        schema = vol.Schema({
            vol.Required(CONF_FEED_TYPE): vol.In(VALID_FEED_TYPES),
            vol.Required(CONF_LATITUDE, default=self.hass.config.latitude): vol.Coerce(float),
            vol.Required(CONF_LONGITUDE, default=self.hass.config.longitude): vol.Coerce(float),
            vol.Required(CONF_RADIUS, default=DEFAULT_RADIUS_IN_KM): vol.Coerce(float),
            vol.Required(CONF_MINIMUM_MAGNITUDE, default=DEFAULT_MINIMUM_MAGNITUDE): vol.Coerce(float),
        })

        return self.async_show_form(step_id="user", data_schema=schema)
