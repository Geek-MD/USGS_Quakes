from homeassistant import config_entries
import voluptuous as vol

from homeassistant.const import CONF_LATITUDE, CONF_LONGITUDE, CONF_RADIUS
from .const import (
    DOMAIN,
    CONF_FEED_TYPE,
    CONF_MINIMUM_MAGNITUDE,
    VALID_FEED_TYPES,
    DEFAULT_RADIUS_IN_KM,
    DEFAULT_MINIMUM_MAGNITUDE,
)


class UsgsQuakesOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle a config options flow for USGS Quakes."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        current = {**self.config_entry.data, **self.config_entry.options}

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required(CONF_FEED_TYPE, default=current.get(CONF_FEED_TYPE)): vol.In(VALID_FEED_TYPES),
                vol.Required(CONF_LATITUDE, default=current.get(CONF_LATITUDE)): vol.Coerce(float),
                vol.Required(CONF_LONGITUDE, default=current.get(CONF_LONGITUDE)): vol.Coerce(float),
                vol.Required(CONF_RADIUS, default=current.get(CONF_RADIUS, DEFAULT_RADIUS_IN_KM)): vol.Coerce(float),
                vol.Required(CONF_MINIMUM_MAGNITUDE, default=current.get(CONF_MINIMUM_MAGNITUDE, DEFAULT_MINIMUM_MAGNITUDE)): vol.Coerce(float),
            })
        )
