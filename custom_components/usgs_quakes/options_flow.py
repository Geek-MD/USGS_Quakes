from homeassistant import config_entries
import voluptuous as vol
from homeassistant.const import CONF_LATITUDE, CONF_LONGITUDE, CONF_RADIUS
from homeassistant.helpers.selector import selector

from .const import (
    DOMAIN,
    CONF_FEED_TYPE,
    CONF_MINIMUM_MAGNITUDE,
    FEED_TYPE_FRIENDLY_NAMES,
    FRIENDLY_NAME_TO_FEED_TYPE,
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
        current = {**self.config_entry.data, **self.config_entry.options}

        if user_input is not None:
            return self.async_create_entry(
                title="",
                data={
                    CONF_FEED_TYPE: FRIENDLY_NAME_TO_FEED_TYPE[user_input["feed_type_friendly"]],
                    CONF_LATITUDE: user_input[CONF_LATITUDE],
                    CONF_LONGITUDE: user_input[CONF_LONGITUDE],
                    CONF_RADIUS: user_input[CONF_RADIUS],
                    CONF_MINIMUM_MAGNITUDE: user_input[CONF_MINIMUM_MAGNITUDE],
                }
            )

        current_feed_type = current.get(CONF_FEED_TYPE)
        default_friendly = FEED_TYPE_FRIENDLY_NAMES.get(current_feed_type, list(FEED_TYPE_FRIENDLY_NAMES.values())[0])

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required("feed_type_friendly", default=default_friendly): selector({
                    "select": {
                        "options": list(FEED_TYPE_FRIENDLY_NAMES.values()),
                        "mode": "dropdown"
                    }
                }),
                vol.Required(CONF_LATITUDE, default=current.get(CONF_LATITUDE)): vol.Coerce(float),
                vol.Required(CONF_LONGITUDE, default=current.get(CONF_LONGITUDE)): vol.Coerce(float),
                vol.Required(CONF_RADIUS, default=current.get(CONF_RADIUS, DEFAULT_RADIUS_IN_KM)): vol.Coerce(float),
                vol.Required(CONF_MINIMUM_MAGNITUDE, default=current.get(CONF_MINIMUM_MAGNITUDE, DEFAULT_MINIMUM_MAGNITUDE)): vol.Coerce(float),
            })
        )
