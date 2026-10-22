"""Provision and read-only verify the ASTV-357 disposable HA stage."""

from __future__ import annotations

import asyncio
from datetime import UTC, datetime
import json
from pathlib import Path
import urllib.parse
import urllib.request

import aiohttp

BASE_URL = "http://127.0.0.1:8123"
CLIENT_ID = "http://127.0.0.1:8123/"
EXPECTED_REVISION = "v1-986df5539173dad03cf231dd5fd094dbdc6024d1786ad721b18b84fe332c4173"
EXPECTED_UIDS = [
    "04689C36C82A81", "04E38B36C82A81", "04EA9236C82A81",
    "689C36C82A81", "7AB06354E000", "DEADBEEF", "DEADLBC",
    "DEADMORNING", "DEADNEWSBRIEF", "DEADSMOOTH", "E38B36C82A81",
    "EA9236C82A81",
]
EXPECTED_INTENTS = [
    "bbc_radio_2", "classic_fm", "gold_radio", "lbc_news", "lbc_radio",
    "morning_routine", "news_briefing", "smooth_radio",
]


def post_json(path: str, payload: dict[str, object]) -> dict:
    request = urllib.request.Request(
        BASE_URL + path,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=10) as response:
        return json.load(response)


def create_stage_token() -> str:
    user = post_json(
        "/api/onboarding/users",
        {
            "client_id": CLIENT_ID,
            "name": "ASTV-357 staging verifier",
            "username": "astv357-stage",
            "password": "ephemeral-not-retained-ASTV357",
            "language": "en",
        },
    )
    data = urllib.parse.urlencode(
        {"grant_type": "authorization_code", "code": user["auth_code"], "client_id": CLIENT_ID}
    ).encode("ascii")
    request = urllib.request.Request(BASE_URL + "/auth/token", data=data, method="POST")
    with urllib.request.urlopen(request, timeout=10) as response:
        return json.load(response)["access_token"]


async def ws_command(socket: aiohttp.ClientWebSocketResponse, command_id: int, **command):
    await socket.send_json({"id": command_id, **command})
    response = await socket.receive_json(timeout=15)
    if not response.get("success"):
        raise RuntimeError(f"WebSocket command failed: {response}")
    return response.get("result")


async def call_service(socket, command_id: int, domain: str, service: str, data=None):
    result = await ws_command(
        socket,
        command_id,
        type="call_service",
        domain=domain,
        service=service,
        service_data=data or {},
        return_response=True,
    )
    return result["response"]


async def verify(token: str) -> dict[str, object]:
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(BASE_URL.replace("http", "ws") + "/api/websocket") as socket:
            auth_required = await socket.receive_json(timeout=10)
            assert auth_required["type"] == "auth_required"
            await socket.send_json({"type": "auth", "access_token": token})
            auth_result = await socket.receive_json(timeout=10)
            assert auth_result["type"] == "auth_ok", auth_result

            area = await ws_command(socket, 1, type="config/area_registry/create", name="ASTV-357 staging area")
            status = await call_service(socket, 2, "advnfc", "get_administration_status")
            mappings = await call_service(socket, 3, "advnfc", "list_tag_mappings")
            capabilities = await call_service(socket, 4, "astv_intent_catalogue", "get_administration_capabilities")
            intents = await call_service(socket, 5, "astv_intent_catalogue", "list_intent_records", {"limit": 200})
            services = await ws_command(socket, 6, type="get_services")

    observed_uids = [mapping["uid"] for mapping in mappings["mappings"]]
    observed_intents = [record["intent_id"] for record in intents["records"]]
    assert status["ok"] is True
    assert status["state"] == "active"
    assert status["active_count"] == status["persisted_count"] == 12
    assert status["active_revision"] == status["persisted_revision"] == EXPECTED_REVISION
    assert status["activation_required"] is False
    assert status["last_activation_error"] is None
    assert observed_uids == EXPECTED_UIDS
    assert "A3570001" not in observed_uids
    assert capabilities["mutation_supported"] is False
    assert capabilities["activation_applicable"] is False
    assert observed_intents == EXPECTED_INTENTS
    assert "record_invocation" in services["astv_staging_sink"]
    assert not Path("/config/ASTV-357/gateway-spy.jsonl").exists()

    return {
        "observed_at": datetime.now(UTC).isoformat(),
        "home_assistant_version": auth_result["ha_version"],
        "stage_name": "ASTV-357 Disposable Staging",
        "stage_area": {"id": area["area_id"], "name": area["name"]},
        "advnfc": {
            "manifest_version": "1.6.0",
            "accepted_tag": "v1.6.0-beta.288e3df",
            "accepted_sha": "288e3df5187a5c37e44feda202cc570f9eb539e0",
            "status": status,
            "uids": observed_uids,
            "reserved_uid_absent": True,
        },
        "astv_catalogue_double": {
            "capabilities": capabilities,
            "active_revision": intents["active_revision"],
            "intent_ids": observed_intents,
        },
        "gateway_sink": {
            "service_registered": True,
            "spy_file_absent": True,
            "external_dispatch_capability": False,
        },
        "lifecycle_calls_executed": [],
    }


async def main() -> None:
    token = create_stage_token()
    evidence = await verify(token)
    Path("/config/staging/stage-evidence.json").write_text(
        json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    asyncio.run(main())

