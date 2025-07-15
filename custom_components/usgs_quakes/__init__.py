from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .geo_location import setup_platform

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    await setup_platform(hass, entry)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    # No dynamic unload logic
    return True
