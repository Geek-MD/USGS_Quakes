from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_LATITUDE, CONF_LONGITUDE
from homeassistant.core import callback
from homeassistant.helpers import selector

from .const import (
    DOMAIN,
    CONF_RADIUS,
    CONF_MINIMUM_MAGNITUDE,
    CONF_FEED_TYPE,
    DEFAULT_RADIUS,
    DEFAULT_MINIMUM_MAGNITUDE,
    DEFAULT_FEED_TYPE,
    FEED_TYPES,
)


class USGSConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for USGS Quakes."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is not None:
            return self.async_create_entry(title="USGS Quakes", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_LATITUDE, default=self.hass.config.latitude): float,
                    vol.Required(CONF_LONGITUDE, default=self.hass.config.longitude): float,
                    vol.Required(CONF_RADIUS, default=DEFAULT_RADIUS): vol.All(float, vol.Range(min=0)),
                    vol.Required(CONF_MINIMUM_MAGNITUDE, default=DEFAULT_MINIMUM_MAGNITUDE): vol.All(
                        float, vol.Range(min=0)
                    ),
                    vol.Required(CONF_FEED_TYPE, default=DEFAULT_FEED_TYPE): vol.In(list(FEED_TYPES.keys())),
                }
            ),
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return USGSOptionsFlowHandler(config_entry)


class USGSOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options flow for USGS Quakes."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_RADIUS,
                        default=self.config_entry.options.get(CONF_RADIUS, DEFAULT_RADIUS),
                    ): vol.All(float, vol.Range(min=0)),
                    vol.Required(
                        CONF_MINIMUM_MAGNITUDE,
                        default=self.config_entry.options.get(CONF_MINIMUM_MAGNITUDE, DEFAULT_MINIMUM_MAGNITUDE),
                    ): vol.All(float, vol.Range(min=0)),
                    vol.Required(
                        CONF_FEED_TYPE,
                        default=self.config_entry.options.get(CONF_FEED_TYPE, DEFAULT_FEED_TYPE),
                    ): vol.In(list(FEED_TYPES.keys())),
                }
            ),
        )
