"""Config flow for USGS Quakes integration."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_LATITUDE, CONF_LONGITUDE, CONF_RADIUS
from homeassistant.core import callback
import homeassistant.helpers.config_validation as cv

from .const import (
    DOMAIN,
    CONF_FEED_TYPE,
    CONF_MINIMUM_MAGNITUDE,
    DEFAULT_MINIMUM_MAGNITUDE,
    DEFAULT_RADIUS,
    VALID_FEED_TYPES,
)


class USGSQuakesConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for USGS Quakes."""

    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None):
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            await self.async_set_unique_id(DOMAIN)
            self._abort_if_unique_id_configured()
            return self.async_create_entry(title="USGS Quakes", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_LATITUDE, default=self.hass.config.latitude): cv.latitude,
                    vol.Required(CONF_LONGITUDE, default=self.hass.config.longitude): cv.longitude,
                    vol.Required(CONF_RADIUS, default=DEFAULT_RADIUS): vol.Coerce(float),
                    vol.Required(CONF_MINIMUM_MAGNITUDE, default=DEFAULT_MINIMUM_MAGNITUDE): vol.Coerce(float),
                    vol.Required(CONF_FEED_TYPE): vol.In(VALID_FEED_TYPES),
                }
            ),
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return USGSQuakesOptionsFlowHandler(config_entry)


class USGSQuakesOptionsFlowHandler(config_entries.OptionsFlow):
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
                        default=self.config_entry.options.get(CONF_RADIUS, self.config_entry.data[CONF_RADIUS]),
                    ): vol.Coerce(float),
                    vol.Required(
                        CONF_MINIMUM_MAGNITUDE,
                        default=self.config_entry.options.get(
                            CONF_MINIMUM_MAGNITUDE, self.config_entry.data[CONF_MINIMUM_MAGNITUDE]
                        ),
                    ): vol.Coerce(float),
                    vol.Required(
                        CONF_FEED_TYPE,
                        default=self.config_entry.options.get(CONF_FEED_TYPE, self.config_entry.data[CONF_FEED_TYPE]),
                    ): vol.In(VALID_FEED_TYPES),
                }
            ),
        )
