# homeassistant/components/usgs_earthquakes_feed/config_flow.py

from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import selector

from .const import DOMAIN, CONF_RADIUS, CONF_LATITUDE, CONF_LONGITUDE, CONF_MINIMUM_MAGNITUDE

class USGSQuakesConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            return self.async_create_entry(title="USGS Quakes", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_LATITUDE): float,
                vol.Required(CONF_LONGITUDE): float,
                vol.Required(CONF_RADIUS, default=100.0): float,
                vol.Optional(CONF_MINIMUM_MAGNITUDE, default=0.0): float,
            }),
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return USGSQuakesOptionsFlowHandler(config_entry)

class USGSQuakesOptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required(CONF_RADIUS, default=self.config_entry.data.get(CONF_RADIUS, 100.0)): float,
                vol.Required(CONF_MINIMUM_MAGNITUDE, default=self.config_entry.data.get(CONF_MINIMUM_MAGNITUDE, 0.0)): float,
            }),
        )
