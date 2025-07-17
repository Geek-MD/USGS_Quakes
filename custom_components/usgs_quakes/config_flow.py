"""Config flow for USGS Quakes integration."""

from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_LATITUDE, CONF_LONGITUDE
from homeassistant.data_entry_flow import FlowResult

from .const import (
    CONF_FEED_TYPE,
    CONF_MINIMUM_MAGNITUDE,
    CONF_RADIUS,
    DEFAULT_MINIMUM_MAGNITUDE,
    DEFAULT_RADIUS,
    DOMAIN,
    VALID_FEED_TYPES,
)


class UsgsQuakesConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for USGS Quakes."""

    VERSION = 1

    async def async_step_user(self, user_input=None) -> FlowResult:
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            try:
                latitude = float(user_input[CONF_LATITUDE])
                longitude = float(user_input[CONF_LONGITUDE])
                radius = float(user_input[CONF_RADIUS])
                minimum_magnitude = float(user_input[CONF_MINIMUM_MAGNITUDE])
                feed_type = user_input[CONF_FEED_TYPE]
            except (ValueError, TypeError):
                errors["base"] = "invalid_input"
            else:
                return self.async_create_entry(
                    title="USGS Quakes",
                    data={
                        CONF_LATITUDE: latitude,
                        CONF_LONGITUDE: longitude,
                        CONF_RADIUS: radius,
                        CONF_MINIMUM_MAGNITUDE: minimum_magnitude,
                        CONF_FEED_TYPE: feed_type,
                    },
                )

        data_schema = vol.Schema(
            {
                vol.Optional(CONF_LATITUDE, default=self.hass.config.latitude): vol.Coerce(float),
                vol.Optional(CONF_LONGITUDE, default=self.hass.config.longitude): vol.Coerce(float),
                vol.Required(CONF_RADIUS, default=DEFAULT_RADIUS): vol.Coerce(float),
                vol.Required(CONF_MINIMUM_MAGNITUDE, default=DEFAULT_MINIMUM_MAGNITUDE): vol.Coerce(float),
                vol.Required(CONF_FEED_TYPE, default=VALID_FEED_TYPES[0]): vol.In(VALID_FEED_TYPES),
            }
        )

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options for USGS Quakes."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None) -> FlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_RADIUS,
                        default=self.config_entry.options.get(
                            CONF_RADIUS,
                            self.config_entry.data.get(CONF_RADIUS, DEFAULT_RADIUS),
                        ),
                    ): vol.Coerce(float),
                    vol.Required(
                        CONF_MINIMUM_MAGNITUDE,
                        default=self.config_entry.options.get(
                            CONF_MINIMUM_MAGNITUDE,
                            self.config_entry.data.get(CONF_MINIMUM_MAGNITUDE, DEFAULT_MINIMUM_MAGNITUDE),
                        ),
                    ): vol.Coerce(float),
                    vol.Required(
                        CONF_FEED_TYPE,
                        default=self.config_entry.options.get(
                            CONF_FEED_TYPE,
                            self.config_entry.data.get(CONF_FEED_TYPE, VALID_FEED_TYPES[0]),
                        ),
                    ): vol.In(VALID_FEED_TYPES),
                }
            ),
        )


async def async_get_options_flow(config_entry: config_entries.ConfigEntry) -> OptionsFlowHandler:
    """Return the options flow handler."""
    return OptionsFlowHandler(config_entry)
