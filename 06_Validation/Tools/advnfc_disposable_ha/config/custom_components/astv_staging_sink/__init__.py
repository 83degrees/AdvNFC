"""File-only, non-dispatching ASTV gateway spy for AdvNFC validation."""

from __future__ import annotations

from datetime import UTC, datetime
import json
from pathlib import Path

from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers.service import async_register_admin_service
from homeassistant.helpers.typing import ConfigType

DOMAIN = "astv_staging_sink"


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Register a sink that can only append to staging-local evidence."""

    target = Path(hass.config.path("AdvNFC-validation", "gateway-spy.jsonl"))

    def append_record(record: dict[str, str]) -> None:
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(record, sort_keys=True) + "\n")

    async def record_invocation(call: ServiceCall) -> None:
        record = {
            "observed_at": datetime.now(UTC).isoformat(),
            "intent_id": str(call.data.get("intent_id", "")),
            "input_area_override": str(call.data.get("input_area_override", "")),
            "trigger_entity": str(call.data.get("trigger_entity", "")),
        }
        await hass.async_add_executor_job(append_record, record)

    async_register_admin_service(hass, DOMAIN, "record_invocation", record_invocation)
    return True

