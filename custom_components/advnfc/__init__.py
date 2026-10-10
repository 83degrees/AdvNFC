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
from homeassistant.helpers import area_registry as ar
from homeassistant.helpers import discovery
from homeassistant.helpers.dispatcher import async_dispatcher_send
from homeassistant.helpers.service import async_register_admin_service
from homeassistant.helpers.typing import ConfigType

from .mapping import TagMappingStore, TagMappingValidationError

DOMAIN = "advnfc"
SERVICE_FIND_TAG_RECORD = "find_tag_record"
SERVICE_RELOAD_TAG_MAPPING = "reload_tag_mapping"
SERVICE_GET_ADMINISTRATION_CAPABILITIES = "get_administration_capabilities"
SERVICE_GET_ADMINISTRATION_STATUS = "get_administration_status"
SERVICE_LIST_TAG_MAPPINGS = "list_tag_mappings"
SERVICE_GET_TAG_MAPPING = "get_tag_mapping"
SERVICE_QUERY_TAG_MAPPINGS = "query_tag_mappings"
SERVICE_VALIDATE_TAG_MAPPING = "validate_tag_mapping"
SERVICE_VALIDATE_TAG_MAPPING_RECORD = "validate_tag_mapping_record"
SERVICE_CREATE_TAG_MAPPING = "create_tag_mapping"
SERVICE_UPDATE_TAG_MAPPING = "update_tag_mapping"
SERVICE_DELETE_TAG_MAPPING = "delete_tag_mapping"
DATA_STORE = "tag_mapping_store"
SIGNAL_TAG_MAPPING_UPDATED = "advnfc_tag_mapping_updated"

_LOGGER = logging.getLogger(__name__)


def _mapping_path(hass: HomeAssistant) -> Path:
    return Path(hass.config.path("AdvNFC", "advnfc_tag_mapping.yaml"))


async def _async_activate(hass: HomeAssistant, store: TagMappingStore) -> ServiceResponse:
    area_registry = ar.async_get(hass)
    area_ids = {area.id for area in area_registry.async_list_areas()}
    response = await hass.async_add_executor_job(
        store.administration_activate,
        _mapping_path(hass),
        area_ids.__contains__,
    )
    async_dispatcher_send(hass, SIGNAL_TAG_MAPPING_UPDATED)
    return response


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Load the initial mapping and register AdvNFC service actions."""

    store = TagMappingStore()
    hass.data.setdefault(DOMAIN, {})[DATA_STORE] = store

    async def find_tag_record(call: ServiceCall) -> ServiceResponse:
        return store.find(call.data.get("uid", ""))

    async def get_administration_capabilities(
        call: ServiceCall,
    ) -> ServiceResponse:
        return store.administration_capabilities()

    async def list_tag_mappings(call: ServiceCall) -> ServiceResponse:
        return store.administration_list()

    async def get_administration_status(call: ServiceCall) -> ServiceResponse:
        areas = area_ids()
        response = await hass.async_add_executor_job(
            store.administration_status,
            _mapping_path(hass),
            areas.__contains__,
        )
        async_dispatcher_send(hass, SIGNAL_TAG_MAPPING_UPDATED)
        return response

    async def get_tag_mapping(call: ServiceCall) -> ServiceResponse:
        return store.administration_get(call.data.get("uid", ""))

    async def query_tag_mappings(call: ServiceCall) -> ServiceResponse:
        return store.administration_query(
            call.data.get("action_type", ""),
            call.data.get("intent_id", ""),
        )

    def area_ids() -> set[str]:
        return {area.id for area in ar.async_get(hass).async_list_areas()}

    async def validate_tag_mapping(call: ServiceCall) -> ServiceResponse:
        areas = area_ids()
        return await hass.async_add_executor_job(
            store.administration_validate_document,
            call.data.get("candidate", {}),
            areas.__contains__,
        )

    async def validate_tag_mapping_record(call: ServiceCall) -> ServiceResponse:
        areas = area_ids()
        return await hass.async_add_executor_job(
            store.administration_validate_record,
            call.data.get("mapping", {}),
            areas.__contains__,
        )

    async def mutate_tag_mapping(
        call: ServiceCall, operation: str
    ) -> ServiceResponse:
        areas = area_ids()
        method = getattr(store, f"administration_{operation}")
        value = (
            call.data.get("uid", "")
            if operation == "delete"
            else call.data.get("mapping", {})
        )
        response = await hass.async_add_executor_job(
            method,
            _mapping_path(hass),
            call.data.get("expected_revision", ""),
            value,
            areas.__contains__,
        )
        if response["ok"]:
            async_dispatcher_send(hass, SIGNAL_TAG_MAPPING_UPDATED)
        return response

    async def create_tag_mapping(call: ServiceCall) -> ServiceResponse:
        return await mutate_tag_mapping(call, "create")

    async def update_tag_mapping(call: ServiceCall) -> ServiceResponse:
        return await mutate_tag_mapping(call, "update")

    async def delete_tag_mapping(call: ServiceCall) -> ServiceResponse:
        return await mutate_tag_mapping(call, "delete")

    try:
        await hass.async_add_executor_job(
            store.load_and_activate,
            _mapping_path(hass),
            area_ids().__contains__,
        )
    except (OSError, TagMappingValidationError) as error:
        _LOGGER.error("%s", error)
        return False

    async def reload_tag_mapping(call: ServiceCall) -> ServiceResponse:
        return await _async_activate(hass, store)

    hass.services.async_register(
        DOMAIN,
        SERVICE_FIND_TAG_RECORD,
        find_tag_record,
        supports_response=SupportsResponse.ONLY,
    )
    async_register_admin_service(
        hass,
        DOMAIN,
        SERVICE_RELOAD_TAG_MAPPING,
        reload_tag_mapping,
        supports_response=SupportsResponse.ONLY,
    )
    hass.services.async_register(
        DOMAIN,
        SERVICE_GET_ADMINISTRATION_CAPABILITIES,
        get_administration_capabilities,
        supports_response=SupportsResponse.ONLY,
    )
    hass.services.async_register(
        DOMAIN,
        SERVICE_LIST_TAG_MAPPINGS,
        list_tag_mappings,
        supports_response=SupportsResponse.ONLY,
    )
    hass.services.async_register(
        DOMAIN,
        SERVICE_GET_ADMINISTRATION_STATUS,
        get_administration_status,
        supports_response=SupportsResponse.ONLY,
    )
    hass.services.async_register(
        DOMAIN,
        SERVICE_GET_TAG_MAPPING,
        get_tag_mapping,
        supports_response=SupportsResponse.ONLY,
    )
    hass.services.async_register(
        DOMAIN,
        SERVICE_QUERY_TAG_MAPPINGS,
        query_tag_mappings,
        supports_response=SupportsResponse.ONLY,
    )
    async_register_admin_service(
        hass,
        DOMAIN,
        SERVICE_VALIDATE_TAG_MAPPING,
        validate_tag_mapping,
        supports_response=SupportsResponse.ONLY,
    )
    async_register_admin_service(
        hass,
        DOMAIN,
        SERVICE_VALIDATE_TAG_MAPPING_RECORD,
        validate_tag_mapping_record,
        supports_response=SupportsResponse.ONLY,
    )
    async_register_admin_service(
        hass,
        DOMAIN,
        SERVICE_CREATE_TAG_MAPPING,
        create_tag_mapping,
        supports_response=SupportsResponse.ONLY,
    )
    async_register_admin_service(
        hass,
        DOMAIN,
        SERVICE_UPDATE_TAG_MAPPING,
        update_tag_mapping,
        supports_response=SupportsResponse.ONLY,
    )
    async_register_admin_service(
        hass,
        DOMAIN,
        SERVICE_DELETE_TAG_MAPPING,
        delete_tag_mapping,
        supports_response=SupportsResponse.ONLY,
    )
    hass.async_create_task(
        discovery.async_load_platform(hass, Platform.SENSOR, DOMAIN, {}, config)
    )
    return True
