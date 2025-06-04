import logging
from datetime import timedelta
from homeassistant.components.geo_location import GeoLocationEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

ENTITY_EXPIRATION = timedelta(minutes=30)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    coordinator: DataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]

    # Limpiar entidades anteriores (Home Assistant lo hace automáticamente si usamos unique_id)
    entities = [
        USGSEarthquakeGeoLocation(entry.entry_id, e)
        for e in coordinator.entries
    ]
    async_add_entities(entities, True)


class USGSEarthquakeGeoLocation(GeoLocationEntity):
    def __init__(self, config_entry_id: str, event):
        self._event = event
        self._attr_unique_id = f"usgs_quake_{event.external_id.split('/')[-1]}"
        self._attr_name = event.title
        self._attr_latitude = event.coordinates[1]
        self._attr_longitude = event.coordinates[0]
        self._attr_source = DOMAIN
        self._attr_unit_of_measurement = "km"
        self._attr_location_accuracy = None
        self._attr_icon = "mdi:map-marker-alert"
        self._attr_extra_state_attributes = {
            "magnitude": event.magnitude,
            "time": event.published.isoformat(),
            "alert": event.alert,
            "url": event.external_id,
        }

    @property
    def latitude(self):
        return self._attr_latitude

    @property
    def longitude(self):
        return self._attr_longitude

    @property
    def source(self):
        return DOMAIN

    @property
    def extra_state_attributes(self):
        return self._attr_extra_state_attributes

    @property
    def available(self):
        return True

    @property
    def should_poll(self):
        return False

    @property
    def state(self):
        return self._event.magnitude

    @property
    def attribution(self):
        return "Data from USGS Earthquake Feed"

    @property
    def icon(self):
        return self._attr_icon

    @property
    def unit_of_measurement(self):
        return self._attr_unit_of_measurement

    @property
    def location_accuracy(self):
        return self._attr_location_accuracy
