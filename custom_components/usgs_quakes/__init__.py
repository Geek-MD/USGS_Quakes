from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_LATITUDE, CONF_LONGITUDE
from homeassistant.data_entry_flow import FlowResult
from .const import DOMAIN, CONF_RADIUS, CONF_MINIMUM_MAGNITUDE, CONF_FEED_TYPE, DEFAULT_RADIUS, DEFAULT_MINIMUM_MAGNITUDE, DEFAULT_FEED_TYPE


class USGSConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for USGS Quakes."""

    VERSION = 1

    async def async_step_user(self, user_input=None) -> FlowResult:
        if user_input is not None:
            return self.async_create_entry(title="USGS Quakes", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_LATITUDE, default=self.hass.config.latitude): float,
                vol.Required(CONF_LONGITUDE, default=self.hass.config.longitude): float,
                vol.Optional(CONF_RADIUS, default=DEFAULT_RADIUS): float,
                vol.Optional(CONF_MINIMUM_MAGNITUDE, default=DEFAULT_MINIMUM_MAGNITUDE): float,
                vol.Optional(CONF_FEED_TYPE, default=DEFAULT_FEED_TYPE): str,
            }),
        )
