"""Options flow for USGS Quakes integration."""

from __future__ import annotations

from typing import Any

from homeassistant import config_entries
from homeassistant.core import callback
import voluptuous as vol

from .const import (
    DOMAIN,
    CONF_RADIUS,
    CONF_MINIMUM_MAGNITUDE,
    CONF_FEED_TYPE,
    VALID_FEED_TYPES,
    DEFAULT_RADIUS,
    DEFAULT_MINIMUM_MAGNITUDE,
)


class UsgsQuakesOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options flow for USGS Quakes."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Manage the options for the custom integration."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        current = self.config_entry.options

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_FEED_TYPE,
                        default=current.get(CONF_FEED_TYPE, self.config_entry.data[CONF_FEED_TYPE]),
                    ): vol.In(VALID_FEED_TYPES),
                    vol.Required(
                        CONF_RADIUS,
                        default=current.get(CONF_RADIUS, self.config_entry.data.get(CONF_RADIUS, DEFAULT_RADIUS)),
                    ): vol.Coerce(float),
                    vol.Required(
                        CONF_MINIMUM_MAGNITUDE,
                        default=current.get(
                            CONF_MINIMUM_MAGNITUDE,
                            self.config_entry.data.get(CONF_MINIMUM_MAGNITUDE, DEFAULT_MINIMUM_MAGNITUDE),
                        ),
                    ): vol.Coerce(float),
                }
            ),
        )


@callback
def async_get_options_flow(
    config_entry: config_entries.ConfigEntry,
) -> UsgsQuakesOptionsFlowHandler:
    """Get the options flow for this handler."""
    return UsgsQuakesOptionsFlowHandler(config_entry)
