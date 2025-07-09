from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .options_flow import UsgsQuakesOptionsFlowHandler

DOMAIN = "usgs_quakes"

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setups(entry, ["geo_location"])
    )
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    return await hass.config_entries.async_unload_platforms(entry, ["geo_location"])

async def async_get_options_flow(config_entry):
    return UsgsQuakesOptionsFlowHandler(config_entry)
