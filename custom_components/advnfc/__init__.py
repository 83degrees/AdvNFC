"""Home Assistant runtime integration for AdvNFC tag mappings."""

from __future__ import annotations

import logging
from pathlib import Path

from homeassistant.const import Platform
from homeassistant.core import (
    HomeAssistant,
    ServiceCall,
    ServiceResponse,
    SupportsResponse,
)
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import area_registry as ar
from homeassistant.helpers import discovery
from homeassistant.helpers.dispatcher import async_dispatcher_send
from homeassistant.helpers.typing import ConfigType

from .mapping import TagMappingStore, TagMappingValidationError

DOMAIN = "advnfc"
SERVICE_FIND_TAG_RECORD = "find_tag_record"
SERVICE_RELOAD_TAG_MAPPING = "reload_tag_mapping"
DATA_STORE = "tag_mapping_store"
SIGNAL_TAG_MAPPING_UPDATED = "advnfc_tag_mapping_updated"

_LOGGER = logging.getLogger(__name__)


def _mapping_path(hass: HomeAssistant) -> Path:
    return Path(hass.config.path("AdvNFC", "advnfc_tag_mapping.yaml"))


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
        raise HomeAssistantError(f"AdvNFC tag mapping rejected: {error}") from error
    async_dispatcher_send(hass, SIGNAL_TAG_MAPPING_UPDATED)
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
    hass.async_create_task(
        discovery.async_load_platform(hass, Platform.SENSOR, DOMAIN, {}, config)
    )
    return True
