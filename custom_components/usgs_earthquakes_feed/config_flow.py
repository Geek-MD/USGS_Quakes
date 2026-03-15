"""Config flow for USGS Quakes integration."""

from __future__ import annotations

from typing import Any
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_LATITUDE, CONF_LONGITUDE
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
)

FRIENDLY_NAME_TO_FEED_TYPE = {v: k for k, v in FEED_TYPE_FRIENDLY_NAMES.items()}
FRIENDLY_NAMES = list(FRIENDLY_NAME_TO_FEED_TYPE.keys())


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):  # type: ignore[call-arg]
    """Handle a config flow for USGS Quakes."""

    VERSION = 1
    DOMAIN = DOMAIN

    @staticmethod
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> OptionsFlowHandler:
        """Get the options flow for this handler."""
        return OptionsFlowHandler(config_entry)

    async def async_step_user(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> FlowResult:
        # --- Esta es la línea clave para permitir SOLO UNA instancia ---
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")
        # --------------------------------------------------------------

        errors: dict[str, str] = {}

        if user_input is not None:
            try:
                latitude = float(user_input.get(CONF_LATITUDE, 0.0))
                longitude = float(user_input.get(CONF_LONGITUDE, 0.0))
                radius = float(user_input.get(CONF_RADIUS, 0.0))
                minimum_magnitude = float(user_input.get(CONF_MINIMUM_MAGNITUDE, 0.0))
                feed_type = FRIENDLY_NAME_TO_FEED_TYPE[str(user_input[CONF_FEED_TYPE])]
            except (ValueError, TypeError, KeyError):
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
                vol.Required(CONF_FEED_TYPE, default=FEED_TYPE_FRIENDLY_NAMES[VALID_FEED_TYPES[0]]): vol.In(FRIENDLY_NAMES),
            }
        )

        return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options flow for USGS Quakes."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options."""
        errors: dict[str, str] = {}

        if user_input is not None:
            try:
                radius = float(user_input.get(CONF_RADIUS, 0.0))
                minimum_magnitude = float(user_input.get(CONF_MINIMUM_MAGNITUDE, 0.0))
                feed_type = FRIENDLY_NAME_TO_FEED_TYPE[str(user_input[CONF_FEED_TYPE])]
            except (ValueError, TypeError, KeyError):
                errors["base"] = "invalid_input"
            else:
                return self.async_create_entry(
                    title="",
                    data={
                        CONF_RADIUS: radius,
                        CONF_MINIMUM_MAGNITUDE: minimum_magnitude,
                        CONF_FEED_TYPE: feed_type,
                    },
                )

        # Get current values from options (if set) or fall back to data
        current_radius = self.config_entry.options.get(
            CONF_RADIUS, self.config_entry.data.get(CONF_RADIUS, DEFAULT_RADIUS)
        )
        current_magnitude = self.config_entry.options.get(
            CONF_MINIMUM_MAGNITUDE,
            self.config_entry.data.get(CONF_MINIMUM_MAGNITUDE, DEFAULT_MINIMUM_MAGNITUDE),
        )
        current_feed_type = self.config_entry.options.get(
            CONF_FEED_TYPE, self.config_entry.data.get(CONF_FEED_TYPE, VALID_FEED_TYPES[0])
        )
        current_feed_friendly = FEED_TYPE_FRIENDLY_NAMES.get(
            current_feed_type, FEED_TYPE_FRIENDLY_NAMES[VALID_FEED_TYPES[0]]
        )

        data_schema = vol.Schema(
            {
                vol.Required(CONF_RADIUS, default=current_radius): vol.Coerce(float),
                vol.Required(
                    CONF_MINIMUM_MAGNITUDE, default=current_magnitude
                ): vol.Coerce(float),
                vol.Required(CONF_FEED_TYPE, default=current_feed_friendly): vol.In(
                    FRIENDLY_NAMES
                ),
            }
        )

        return self.async_show_form(step_id="init", data_schema=data_schema, errors=errors)
