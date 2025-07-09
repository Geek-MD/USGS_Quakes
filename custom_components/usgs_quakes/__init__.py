from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

DOMAIN = "usgs_quakes"

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the integration from configuration.yaml (not used)."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up USGS Quakes from a config entry."""
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setups(entry, ["geo_location"])
    )
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, ["geo_location"])

from .options_flow import UsgsQuakesOptionsFlowHandler

async def async_get_options_flow(config_entry):
    return UsgsQuakesOptionsFlowHandler(config_entry)
