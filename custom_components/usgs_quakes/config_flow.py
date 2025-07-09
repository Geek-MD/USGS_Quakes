from homeassistant import config_entries
import voluptuous as vol
from homeassistant.const import CONF_LATITUDE, CONF_LONGITUDE, CONF_RADIUS
from homeassistant.helpers.selector import selector

from .const import (
    DOMAIN,
    CONF_FEED_TYPE,
    CONF_MINIMUM_MAGNITUDE,
    VALID_FEED_TYPES,
    DEFAULT_RADIUS_IN_KM,
    DEFAULT_MINIMUM_MAGNITUDE,
    FEED_TYPE_FRIENDLY_NAMES,
    FRIENDLY_NAME_TO_FEED_TYPE,
)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for USGS Quakes."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            # Map friendly name to internal key
            return self.async_create_entry(
                title="USGS Quakes",
                data={
                    CONF_FEED_TYPE: FRIENDLY_NAME_TO_FEED_TYPE[user_input["feed_type_friendly"]],
                    CONF_LATITUDE: user_input[CONF_LATITUDE],
                    CONF_LONGITUDE: user_input[CONF_LONGITUDE],
                    CONF_RADIUS: user_input[CONF_RADIUS],
                    CONF_MINIMUM_MAGNITUDE: user_input[CONF_MINIMUM_MAGNITUDE],
                }
            )

        # Use friendly names in selector
        feed_friendly_names = list(FEED_TYPE_FRIENDLY_NAMES.values())

        schema = vol.Schema({
            vol.Required("feed_type_friendly", default=feed_friendly_names[0]): selector({
                "select": {
                    "options": feed_friendly_names,
                    "mode": "dropdown"
                }
            }),
            vol.Required(CONF_LATITUDE, default=self.hass.config.latitude): vol.Coerce(float),
            vol.Required(CONF_LONGITUDE, default=self.hass.config.longitude): vol.Coerce(float),
            vol.Required(CONF_RADIUS, default=DEFAULT_RADIUS_IN_KM): vol.Coerce(float),
            vol.Required(CONF_MINIMUM_MAGNITUDE, default=DEFAULT_MINIMUM_MAGNITUDE): vol.Coerce(float),
        })

        return self.async_show_form(step_id="user", data_schema=schema)
