"""Options flow for USGS Quakes integration."""

from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult

from .const import (
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


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle USGS Quakes options."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None) -> FlowResult:
        if user_input is not None:
            try:
                feed_type = FRIENDLY_NAME_TO_FEED_TYPE[user_input[CONF_FEED_TYPE]]
            except KeyError:
                return self.async_show_form(
                    step_id="init",
                    data_schema=self._get_schema(),
                    errors={"base": "invalid_input"},
                )

            return self.async_create_entry(
                title="",
                data={
                    CONF_RADIUS: user_input[CONF_RADIUS],
                    CONF_MINIMUM_MAGNITUDE: user_input[CONF_MINIMUM_MAGNITUDE],
                    CONF_FEED_TYPE: feed_type,
                },
            )

        return self.async_show_form(
            step_id="init",
            data_schema=self._get_schema(),
        )

    def _get_schema(self) -> vol.Schema:
        current_data = {**self.config_entry.data, **self.config_entry.options}
        current_feed_id = current_data.get(CONF_FEED_TYPE)
        current_friendly_name = FEED_TYPE_FRIENDLY_NAMES.get(current_feed_id, FRIENDLY_NAMES[0])

        return vol.Schema(
            {
                vol.Required(
                    CONF_RADIUS,
                    default=current_data.get(CONF_RADIUS, DEFAULT_RADIUS),
                ): vol.Coerce(float),
                vol.Required(
                    CONF_MINIMUM_MAGNITUDE,
                    default=current_data.get(CONF_MINIMUM_MAGNITUDE, DEFAULT_MINIMUM_MAGNITUDE),
                ): vol.Coerce(float),
                vol.Required(
                    CONF_FEED_TYPE,
                    default=current_friendly_name,
                ): vol.In(FRIENDLY_NAMES),
            }
        )


@callback
def async_get_options_flow(
    config_entry: config_entries.ConfigEntry,
) -> OptionsFlowHandler:
    return OptionsFlowHandler(config_entry)
