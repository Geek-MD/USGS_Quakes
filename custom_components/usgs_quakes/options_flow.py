from homeassistant import config_entries
import voluptuous as vol
from homeassistant.const import CONF_LATITUDE, CONF_LONGITUDE, CONF_RADIUS

from .const import (
    DOMAIN,
    VALID_FEED_TYPES,
    FEED_FRIENDLY_NAMES,
    FRIENDLY_NAME_TO_FEED_TYPE,
    DEFAULT_RADIUS_IN_KM,
    DEFAULT_MINIMUM_MAGNITUDE,
)

CONF_FEED_TYPE = "feed_type"
CONF_MINIMUM_MAGNITUDE = "minimum_magnitude"

def _get_friendly_feed_selector():
    """Create selector with friendly names as keys and internal ids as values."""
    return {FEED_FRIENDLY_NAMES[feed]: feed for feed in VALID_FEED_TYPES}

class UsgsQuakesOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle a config flow options."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        current = self.config_entry.data

        # Convert internal feed_type to friendly name for display
        current_feed = FEED_FRIENDLY_NAMES.get(current.get(CONF_FEED_TYPE), list(FEED_FRIENDLY_NAMES.values())[0])

        schema = vol.Schema({
            vol.Required(CONF_FEED_TYPE, default=current_feed): vol.In(_get_friendly_feed_selector()),
            vol.Required(CONF_LATITUDE, default=current.get(CONF_LATITUDE)): vol.Coerce(float),
            vol.Required(CONF_LONGITUDE, default=current.get(CONF_LONGITUDE)): vol.Coerce(float),
            vol.Required(CONF_RADIUS, default=current.get(CONF_RADIUS, DEFAULT_RADIUS_IN_KM)): vol.Coerce(float),
            vol.Required(CONF_MINIMUM_MAGNITUDE, default=current.get(CONF_MINIMUM_MAGNITUDE, DEFAULT_MINIMUM_MAGNITUDE)): vol.Coerce(float),
        })

        return self.async_show_form(step_id="init", data_schema=schema)
