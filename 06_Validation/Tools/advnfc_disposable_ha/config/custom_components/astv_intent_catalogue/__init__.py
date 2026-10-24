"""Read-only ASTV catalogue double for disposable AdvNFC validation."""

from __future__ import annotations

from homeassistant.core import HomeAssistant, ServiceCall, ServiceResponse, SupportsResponse
from homeassistant.helpers.typing import ConfigType

DOMAIN = "astv_intent_catalogue"
REVISION = "synthetic-v1"
RECORDS = [
    {
        "intent_id": "validation_primary",
        "record": {
            "intent": "validation.noop",
            "title": "Synthetic primary target",
            "params": {},
        },
    },
    {
        "intent_id": "validation_secondary",
        "record": {
            "intent": "validation.noop",
            "title": "Synthetic secondary target",
            "params": {},
        },
    },
]


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Register only the two read operations consumed by the AdvNFC panel."""

    async def capabilities(call: ServiceCall) -> ServiceResponse:
        return {
            "ok": True,
            "interface_id": "astv.intent_catalogue.administration",
            "interface_version": "1.1.0",
            "schema_id": "astv.intent_catalogue",
            "schema_version": "1.0.0",
            "mode": "read_only_stage_double",
            "mutation_supported": False,
            "activation_applicable": False,
            "capabilities": ["discovery", "active.list"],
            "operations": {
                "discovery": "get_administration_capabilities",
                "active_list": "list_intent_records",
            },
            "limits": {"list_default": 100, "list_maximum": 200},
        }

    async def list_records(call: ServiceCall) -> ServiceResponse:
        return {
            "ok": True,
            "interface_id": "astv.intent_catalogue.administration",
            "interface_version": "1.1.0",
            "schema_id": "astv.intent_catalogue",
            "schema_version": "1.0.0",
            "active_revision": REVISION,
            "count": len(RECORDS),
            "total_count": len(RECORDS),
            "records": RECORDS,
            "next_cursor": None,
        }

    hass.services.async_register(
        DOMAIN,
        "get_administration_capabilities",
        capabilities,
        supports_response=SupportsResponse.ONLY,
    )
    hass.services.async_register(
        DOMAIN,
        "list_intent_records",
        list_records,
        supports_response=SupportsResponse.ONLY,
    )
    return True

