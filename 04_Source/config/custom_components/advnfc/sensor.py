"""Sensor platform for AdvNFC runtime capability state."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from . import DATA_STORE, DOMAIN, SIGNAL_TAG_MAPPING_UPDATED
from .mapping import TagMappingStore


async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Register the AdvNFC capability sensor through the entity platform."""
    store: TagMappingStore = hass.data[DOMAIN][DATA_STORE]
    async_add_entities([AdvNFCTagMappingSensor(store)])


class AdvNFCTagMappingSensor(SensorEntity):
    """Expose the active AdvNFC tag-mapping snapshot."""

    _attr_name = "AdvNFC Tag Mapping"
    _attr_unique_id = "advnfc_tag_mapping"
    _attr_icon = "mdi:nfc"
    _attr_should_poll = False

    def __init__(self, store: TagMappingStore) -> None:
        self._store = store

    @property
    def native_value(self) -> str:
        """Return the active mapping state."""
        return "loaded" if self._store.active is not None else "unavailable"

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return capability details for the active mapping snapshot."""
        snapshot = self._store.active
        if snapshot is None:
            return {"schema_version": None, "mapping_count": 0}
        return {
            "schema_version": snapshot.schema_version,
            "mapping_count": snapshot.count,
        }

    async def async_added_to_hass(self) -> None:
        """Subscribe to successful mapping activations."""
        remove_listener: Callable[[], None] = async_dispatcher_connect(
            self.hass,
            SIGNAL_TAG_MAPPING_UPDATED,
            self.async_write_ha_state,
        )
        self.async_on_remove(remove_listener)
