from homeassistant.components.geo_location import GeoLocationEvent
from homeassistant.core import callback
from homeassistant.helpers.entity import generate_entity_id
from .const import DOMAIN
from .coordinator import UsgsEarthquakeFeedCoordinator

ENTITY_ID_FORMAT = "geo_location.usgs_quake_{}"

async def async_setup_entry(hass, config_entry, async_add_entities):
    coordinator: UsgsEarthquakeFeedCoordinator = hass.data[DOMAIN][config_entry.entry_id]
    entities = []

    for event_id, event in coordinator.feed_manager.entries.items():
        entity_id = generate_entity_id(ENTITY_ID_FORMAT, event_id, hass=hass)
        entities.append(USGSEarthquakeEntity(event_id, event, entity_id))

    async_add_entities(entities)

class USGSEarthquakeEntity(GeoLocationEvent):
    def __init__(self, event_id, event, entity_id):
        self._event = event
        self._event_id = event_id
        self.entity_id = entity_id
        self._attr_unique_id = f"usgs_quake_{event_id}"
        self._attr_name = event.title
        self._attr_source = DOMAIN
        self._attr_latitude = event.coordinates[0]
        self._attr_longitude = event.coordinates[1]
        self._attr_magnitude = event.magnitude
        self._attr_time = event.published

    @property
    def extra_state_attributes(self):
        return {
            "place": self._event.place,
            "status": self._event.status,
            "updated": self._event.updated,
        }
