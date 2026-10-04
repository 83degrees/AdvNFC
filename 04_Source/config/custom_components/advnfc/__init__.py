"""Home Assistant runtime integration for AdvNFC tag mappings."""

from __future__ import annotations

import logging
from pathlib import Path

from homeassistant.core import (
    HomeAssistant,
    ServiceCall,
    ServiceResponse,
    SupportsResponse,
)
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import area_registry as ar
from homeassistant.helpers.typing import ConfigType

from .mapping import TagMappingStore, TagMappingValidationError

DOMAIN = "advnfc"
SERVICE_FIND_TAG_RECORD = "find_tag_record"
SERVICE_RELOAD_TAG_MAPPING = "reload_tag_mapping"
STATE_ENTITY_ID = "sensor.advnfc_tag_mapping"
DATA_STORE = "tag_mapping_store"

_LOGGER = logging.getLogger(__name__)


def _mapping_path(hass: HomeAssistant) -> Path:
    return Path(hass.config.path("AdvNFC", "advnfc_tag_mapping.yaml"))


def _publish_capability_state(hass: HomeAssistant, store: TagMappingStore) -> None:
    snapshot = store.active
    if snapshot is None:
        hass.states.async_set(
            STATE_ENTITY_ID,
            "unavailable",
            {"schema_version": None, "mapping_count": 0},
        )
        return
    hass.states.async_set(
        STATE_ENTITY_ID,
        "loaded",
        {
            "schema_version": snapshot.schema_version,
            "mapping_count": snapshot.count,
        },
    )


async def _async_reload(hass: HomeAssistant, store: TagMappingStore) -> ServiceResponse:
    area_registry = ar.async_get(hass)
    area_ids = {area.id for area in area_registry.async_list_areas()}
    try:
        snapshot = await hass.async_add_executor_job(
            store.load_and_activate,
            _mapping_path(hass),
            area_ids.__contains__,
        )
    except (OSError, TagMappingValidationError) as error:
        _publish_capability_state(hass, store)
        raise HomeAssistantError(f"AdvNFC tag mapping rejected: {error}") from error
    _publish_capability_state(hass, store)
    return {
        "schema_version": snapshot.schema_version,
        "mapping_count": snapshot.count,
    }


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Load the initial mapping and register AdvNFC service actions."""

    store = TagMappingStore()
    hass.data.setdefault(DOMAIN, {})[DATA_STORE] = store

    async def find_tag_record(call: ServiceCall) -> ServiceResponse:
        return store.find(call.data.get("uid", ""))

    try:
        await _async_reload(hass, store)
    except HomeAssistantError as error:
        _LOGGER.error("%s", error)
        return False

    async def reload_tag_mapping(call: ServiceCall) -> ServiceResponse | None:
        response = await _async_reload(hass, store)
        return response if call.return_response else None

    hass.services.async_register(
        DOMAIN,
        SERVICE_FIND_TAG_RECORD,
        find_tag_record,
        supports_response=SupportsResponse.ONLY,
    )
    hass.services.async_register(
        DOMAIN,
        SERVICE_RELOAD_TAG_MAPPING,
        reload_tag_mapping,
        supports_response=SupportsResponse.OPTIONAL,
    )
    return True
