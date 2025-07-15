"""Config flow for USGS Quakes integration."""
from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_LATITUDE, CONF_LONGITUDE
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.selector import selector

from .const import (
    CONF_FEED_TYPE,
    CONF_RADIUS,
    CONF_MINIMUM_MAGNITUDE,
    DOMAIN,
    VALID_FEED_TYPES,
)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for USGS Quakes."""

    VERSION = 1

    async def async_step_user(self, user_input: dict | None = None) -> FlowResult:
        """Handle the initial step."""
        if user_input is not None:
            return self.async_create_entry(title="USGS Quakes", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_LATITUDE): float,
                vol.Required(CONF_LONGITUDE): float,
                vol.Required(CONF_FEED_TYPE, default="all_earthquakes"):
                    vol.In(VALID_FEED_TYPES),
                vol.Required(CONF_RADIUS, default=500.0): float,
                vol.Required(CONF_MINIMUM_MAGNITUDE, default=0.0): float,
            }),
        )


class OptionsFlowHandler(config_entries.OptionsFlowWithConfigEntry):
    """Handle options flow for USGS Quakes."""

    async def async_step_init(self, user_input: dict | None = None) -> FlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required(
                    CONF_RADIUS, default=self.config_entry.options.get(CONF_RADIUS, 500.0)
                ): float,
                vol.Required(
                    CONF_MINIMUM_MAGNITUDE,
                    default=self.config_entry.options.get(CONF_MINIMUM_MAGNITUDE, 0.0),
                ): float,
            }),
        )


async def async_get_options_flow(config_entry: config_entries.ConfigEntry) -> OptionsFlowHandler:
    """Get the options flow."""
    return OptionsFlowHandler(config_entry)
