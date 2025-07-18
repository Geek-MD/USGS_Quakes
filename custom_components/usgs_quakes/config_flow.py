"""Config flow for USGS Quakes integration."""

from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_LATITUDE, CONF_LONGITUDE
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult

from .const import (
    DOMAIN,
    CONF_RADIUS,
    CONF_MINIMUM_MAGNITUDE,
    CONF_FEED_TYPE,
    DEFAULT_RADIUS,
    DEFAULT_MINIMUM_MAGNITUDE,
    VALID_FEED_TYPES,
    FEED_TYPE_FRIENDLY_NAMES,
    FRIENDLY_NAME_TO_FEED_TYPE,
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
                feed_type_friendly = user_input[CONF_FEED_TYPE]
                feed_type = FRIENDLY_NAME_TO_FEED_TYPE.get(feed_type_friendly, feed_type_friendly)
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
                vol.Required(CONF_FEED_TYPE, default=FEED_TYPE_FRIENDLY_NAMES[VALID_FEED_TYPES[0]]): vol.In(list(FEED_TYPE_FRIENDLY_NAMES.values())),
            }
        )

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )
