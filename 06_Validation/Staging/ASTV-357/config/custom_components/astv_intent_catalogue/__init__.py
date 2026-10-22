"""Read-only ASTV catalogue double for the ASTV-357 disposable stage."""

from __future__ import annotations

from homeassistant.core import HomeAssistant, ServiceCall, ServiceResponse, SupportsResponse
from homeassistant.helpers.typing import ConfigType

DOMAIN = "astv_intent_catalogue"
REVISION = "sha256:98790a0ecc161e218e845c57a673ff6a4d54e984076b7eddc0547cd164638e8e"
RECORDS = [
    {"intent_id": "bbc_radio_2", "record": {"intent": "media.play_source", "title": "Play BBC Radio 2", "params": {"output": {"domain": "audio"}, "catalogue_id": "curated_media", "item_id": "bbc_radio_2"}}},
    {"intent_id": "classic_fm", "record": {"intent": "media.play_source", "title": "Play Classic FM", "params": {"output": {"domain": "audio"}, "catalogue_id": "curated_media", "item_id": "classic_fm"}}},
    {"intent_id": "gold_radio", "record": {"intent": "media.play_source", "title": "Play Gold Radio", "params": {"output": {"domain": "audio"}, "catalogue_id": "curated_media", "item_id": "gold_radio"}}},
    {"intent_id": "lbc_news", "record": {"intent": "media.play_source", "title": "Play LBC News", "params": {"output": {"domain": "audio"}, "catalogue_id": "curated_media", "item_id": "lbc_news"}}},
    {"intent_id": "lbc_radio", "record": {"intent": "media.play_source", "title": "LBC", "params": {"output": {"domain": "audio"}, "catalogue_id": "curated_media", "item_id": "lbc_radio"}}},
    {"intent_id": "morning_routine", "record": {"intent": "routine.run", "routine": "morning", "title": "Good Morning Routine", "params": {}}},
    {"intent_id": "news_briefing", "record": {"intent": "media.play_source", "title": "News Briefing", "params": {"output": {"domain": "audio"}, "catalogue_id": "curated_media", "item_id": "news_briefing"}}},
    {"intent_id": "smooth_radio", "record": {"intent": "media.play_source", "title": "Smooth Radio", "params": {"output": {"domain": "audio"}, "catalogue_id": "curated_media", "item_id": "smooth_radio"}}},
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

