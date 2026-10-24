"""Provision and read-only verify the disposable AdvNFC Home Assistant stage."""

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
PASSWORD_PATH = Path("/config/staging/onboarding-password")
EVIDENCE_PATH = Path("/evidence/baseline-evidence.json")
SPY_PATH = Path("/config/AdvNFC-validation/gateway-spy.jsonl")
EXPECTED_UIDS = ["A3660001", "A3660002"]
EXPECTED_INTENTS = ["validation_primary", "validation_secondary"]
RESERVED_UID = "A366FFFF"


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
    """Create a one-run account and return a token without persisting either secret."""

    password = PASSWORD_PATH.read_text(encoding="utf-8").strip()
    try:
        user = post_json(
            "/api/onboarding/users",
            {
                "client_id": CLIENT_ID,
                "name": "AdvNFC disposable validation",
                "username": "advnfc-validation",
                "password": password,
                "language": "en",
            },
        )
    finally:
        PASSWORD_PATH.unlink(missing_ok=True)
    data = urllib.parse.urlencode(
        {
            "grant_type": "authorization_code",
            "code": user["auth_code"],
            "client_id": CLIENT_ID,
        }
    ).encode("ascii")
    request = urllib.request.Request(BASE_URL + "/auth/token", data=data, method="POST")
    with urllib.request.urlopen(request, timeout=10) as response:
        return json.load(response)["access_token"]


async def ws_command(
    socket: aiohttp.ClientWebSocketResponse, command_id: int, **command
):
    await socket.send_json({"id": command_id, **command})
    response = await socket.receive_json(timeout=15)
    if not response.get("success"):
        raise RuntimeError(f"WebSocket command failed: {response}")
    return response.get("result")


async def call_service(
    socket: aiohttp.ClientWebSocketResponse,
    command_id: int,
    domain: str,
    service: str,
    data=None,
):
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
        async with session.ws_connect(
            BASE_URL.replace("http", "ws") + "/api/websocket"
        ) as socket:
            assert (await socket.receive_json(timeout=10))["type"] == "auth_required"
            await socket.send_json({"type": "auth", "access_token": token})
            auth_result = await socket.receive_json(timeout=10)
            assert auth_result["type"] == "auth_ok", auth_result

            area = await ws_command(
                socket,
                1,
                type="config/area_registry/create",
                name="AdvNFC validation area",
            )
            config = await ws_command(socket, 2, type="get_config")
            advnfc_capabilities = await call_service(
                socket, 3, "advnfc", "get_administration_capabilities"
            )
            status = await call_service(
                socket, 4, "advnfc", "get_administration_status"
            )
            mappings = await call_service(socket, 5, "advnfc", "list_tag_mappings")
            capabilities = await call_service(
                socket, 6, "astv_intent_catalogue", "get_administration_capabilities"
            )
            intents = await call_service(
                socket,
                7,
                "astv_intent_catalogue",
                "list_intent_records",
                {"limit": 200},
            )
            services = await ws_command(socket, 8, type="get_services")

    observed_uids = [mapping["uid"] for mapping in mappings["mappings"]]
    observed_intents = [record["intent_id"] for record in intents["records"]]
    assert status["ok"] is True
    assert status["state"] == "active"
    assert status["active_count"] == status["persisted_count"] == 2
    assert status["active_revision"] == status["persisted_revision"]
    assert status["activation_required"] is False
    assert status["last_activation_error"] is None
    assert observed_uids == EXPECTED_UIDS
    assert RESERVED_UID not in observed_uids
    assert capabilities["mutation_supported"] is False
    assert capabilities["activation_applicable"] is False
    assert observed_intents == EXPECTED_INTENTS
    assert "record_invocation" in services["astv_staging_sink"]
    assert not SPY_PATH.exists()

    return {
        "observed_at": datetime.now(UTC).isoformat(),
        "home_assistant_version": auth_result["ha_version"],
        "health": {
            "websocket_authenticated": True,
            "state": config["state"],
            "version": config["version"],
        },
        "stage_name": "AdvNFC Disposable Validation",
        "stage_area": {"id": area["area_id"], "name": area["name"]},
        "advnfc": {
            "capabilities": advnfc_capabilities,
            "status": status,
            "list_response": mappings,
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
    EVIDENCE_PATH.write_text(
        json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    asyncio.run(main())
