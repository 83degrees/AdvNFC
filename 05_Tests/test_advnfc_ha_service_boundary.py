"""Home Assistant 2026.9.4 service-boundary tests for AdvNFC administration."""

from __future__ import annotations

import asyncio
from pathlib import Path
from types import SimpleNamespace

import pytest
import voluptuous as vol
from homeassistant.core import Context, HomeAssistant, SupportsResponse
from homeassistant.exceptions import Unauthorized
from homeassistant.helpers import area_registry as ar

from custom_components import advnfc


INITIAL_MAPPING = """tag_mapping_schema_version: 1
tags:
  A1:
    label: Existing radio
    action: {type: astv_intent, intent_id: classic_fm}
"""


def _record(uid: str = "B2", label: str = "New radio") -> dict:
    return {
        "uid": uid,
        "label": label,
        "action": {"type": "astv_intent", "intent_id": "gold_radio"},
    }


class _Auth:
    async def async_get_user(self, user_id: str):
        if user_id == "admin":
            return SimpleNamespace(is_admin=True)
        if user_id == "member":
            return SimpleNamespace(is_admin=False)
        return None


async def _async_setup_hass(tmp_path: Path, monkeypatch):
    mapping_dir = tmp_path / "AdvNFC"
    mapping_dir.mkdir()
    mapping_path = mapping_dir / "advnfc_tag_mapping.yaml"
    mapping_path.write_text(INITIAL_MAPPING, encoding="utf-8")

    hass = HomeAssistant(str(tmp_path))
    hass.auth = _Auth()
    await ar.async_load(hass, load_empty=True)

    async def no_frontend_registration(_hass):
        return None

    async def no_platform_discovery(*_args, **_kwargs):
        return None

    monkeypatch.setattr(advnfc, "async_register_frontend", no_frontend_registration)
    monkeypatch.setattr(
        advnfc.discovery, "async_load_platform", no_platform_discovery
    )

    assert await advnfc.async_setup(hass, {})
    await hass.async_block_till_done()
    return hass, mapping_path


async def _async_call(hass, service: str, data: dict, user_id: str = "admin"):
    return await hass.services.async_call(
        advnfc.DOMAIN,
        service,
        data,
        blocking=True,
        context=Context(user_id=user_id),
        return_response=True,
    )


def _run(test):
    asyncio.run(test)


def test_real_ha_boundary_accepts_every_documented_payload(tmp_path, monkeypatch):
    async def exercise():
        hass, mapping_path = await _async_setup_hass(tmp_path, monkeypatch)
        try:
            for service in (
                advnfc.SERVICE_VALIDATE_TAG_MAPPING,
                advnfc.SERVICE_VALIDATE_TAG_MAPPING_RECORD,
                advnfc.SERVICE_CREATE_TAG_MAPPING,
                advnfc.SERVICE_UPDATE_TAG_MAPPING,
                advnfc.SERVICE_DELETE_TAG_MAPPING,
            ):
                assert (
                    hass.services.supports_response(advnfc.DOMAIN, service)
                    is SupportsResponse.ONLY
                )

            validated = await _async_call(
                hass,
                advnfc.SERVICE_VALIDATE_TAG_MAPPING,
                {
                    "candidate": {
                        "tag_mapping_schema_version": 1,
                        "mappings": [_record()],
                    }
                },
            )
            assert validated["ok"] is True
            assert validated["mappings"] == [_record()]

            record = await _async_call(
                hass,
                advnfc.SERVICE_VALIDATE_TAG_MAPPING_RECORD,
                {"mapping": _record(" b2 ")},
            )
            assert record["ok"] is True
            assert record["mapping"]["uid"] == "B2"

            store = hass.data[advnfc.DOMAIN][advnfc.DATA_STORE]
            assert store.active is not None
            active_revision = store.active.revision

            created = await _async_call(
                hass,
                advnfc.SERVICE_CREATE_TAG_MAPPING,
                {"expected_revision": active_revision, "mapping": _record()},
            )
            assert created["ok"] is True
            assert store.active.revision == active_revision

            updated = await _async_call(
                hass,
                advnfc.SERVICE_UPDATE_TAG_MAPPING,
                {
                    "expected_revision": created["persisted_revision"],
                    "mapping": _record(label="Updated radio"),
                },
            )
            assert updated["ok"] is True
            assert store.active.revision == active_revision

            deleted = await _async_call(
                hass,
                advnfc.SERVICE_DELETE_TAG_MAPPING,
                {
                    "expected_revision": updated["persisted_revision"],
                    "uid": " b2 ",
                },
            )
            assert deleted["ok"] is True
            assert store.active.revision == active_revision
            assert "B2" not in mapping_path.read_text(encoding="utf-8")
        finally:
            await hass.async_stop(force=True)

    _run(exercise())


@pytest.mark.parametrize(
    ("service", "data"),
    [
        (advnfc.SERVICE_VALIDATE_TAG_MAPPING, {}),
        (advnfc.SERVICE_VALIDATE_TAG_MAPPING, {"candidate": []}),
        (
            advnfc.SERVICE_VALIDATE_TAG_MAPPING,
            {"candidate": {}, "unexpected": True},
        ),
        (advnfc.SERVICE_VALIDATE_TAG_MAPPING_RECORD, {"mapping": []}),
        (
            advnfc.SERVICE_VALIDATE_TAG_MAPPING_RECORD,
            {"mapping": {}, "unexpected": True},
        ),
        (
            advnfc.SERVICE_CREATE_TAG_MAPPING,
            {"expected_revision": 7, "mapping": _record()},
        ),
        (
            advnfc.SERVICE_CREATE_TAG_MAPPING,
            {
                "expected_revision": "v1-test",
                "mapping": _record(),
                "unexpected": True,
            },
        ),
        (
            advnfc.SERVICE_UPDATE_TAG_MAPPING,
            {"mapping": _record()},
        ),
        (
            advnfc.SERVICE_UPDATE_TAG_MAPPING,
            {"expected_revision": "v1-test", "mapping": []},
        ),
        (
            advnfc.SERVICE_DELETE_TAG_MAPPING,
            {"expected_revision": "v1-test", "uid": 7},
        ),
        (
            advnfc.SERVICE_DELETE_TAG_MAPPING,
            {
                "expected_revision": "v1-test",
                "uid": "B2",
                "unexpected": True,
            },
        ),
    ],
)
def test_real_ha_boundary_rejects_malformed_or_extra_fields_without_mutation(
    tmp_path, monkeypatch, service, data
):
    async def exercise():
        hass, mapping_path = await _async_setup_hass(tmp_path, monkeypatch)
        try:
            before = mapping_path.read_bytes()
            with pytest.raises(vol.Invalid):
                await _async_call(hass, service, data)
            assert mapping_path.read_bytes() == before
        finally:
            await hass.async_stop(force=True)

    _run(exercise())


def test_real_ha_boundary_denies_non_admin_before_mutation(tmp_path, monkeypatch):
    async def exercise():
        hass, mapping_path = await _async_setup_hass(tmp_path, monkeypatch)
        try:
            before = mapping_path.read_bytes()
            store = hass.data[advnfc.DOMAIN][advnfc.DATA_STORE]
            assert store.active is not None
            with pytest.raises(Unauthorized):
                await _async_call(
                    hass,
                    advnfc.SERVICE_CREATE_TAG_MAPPING,
                    {
                        "expected_revision": store.active.revision,
                        "mapping": _record(),
                    },
                    user_id="member",
                )
            assert mapping_path.read_bytes() == before
            assert store.activation_required is False
        finally:
            await hass.async_stop(force=True)

    _run(exercise())


def test_real_ha_boundary_preserves_provider_failure_envelope_and_state(
    tmp_path, monkeypatch
):
    async def exercise():
        hass, mapping_path = await _async_setup_hass(tmp_path, monkeypatch)
        try:
            before = mapping_path.read_bytes()
            invalid_record = {**_record(), "unexpected": True}
            response = await _async_call(
                hass,
                advnfc.SERVICE_VALIDATE_TAG_MAPPING_RECORD,
                {"mapping": invalid_record},
            )
            assert response["ok"] is False
            assert response["error"]["code"] == "invalid_candidate"
            assert response["interface_version"] == 3
            assert response["tag_mapping_schema_version"] == 1
            assert mapping_path.read_bytes() == before
        finally:
            await hass.async_stop(force=True)

    _run(exercise())
