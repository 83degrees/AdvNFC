"""Verify AdvNFC administration service schemas without changing state."""

from __future__ import annotations

import asyncio
from copy import deepcopy
from datetime import UTC, datetime
import hashlib
import json
from pathlib import Path

import aiohttp

from verify_baseline import (
    BASE_URL,
    RESERVED_UID,
    SPY_PATH,
    call_service,
    create_stage_token,
    verify,
    ws_command,
)


EVIDENCE_PATH = Path("/evidence/schema-evidence.json")
MAPPING_PATH = Path("/config/AdvNFC/advnfc_tag_mapping.yaml")
STALE_REVISION = "v1-deliberately-stale-schema-probe"
REQUIRED_SERVICES = [
    "validate_tag_mapping",
    "validate_tag_mapping_record",
    "create_tag_mapping",
    "update_tag_mapping",
    "delete_tag_mapping",
]
PROBE_RECORD = {
    "uid": RESERVED_UID,
    "label": "Synthetic schema probe",
    "action": {"type": "astv_intent", "intent_id": "validation_primary"},
}


class CommandIds:
    def __init__(self) -> None:
        self.value = 100

    def next(self) -> int:
        self.value += 1
        return self.value


def observed_at() -> str:
    return datetime.now(UTC).isoformat()


def file_sha256() -> str:
    return hashlib.sha256(MAPPING_PATH.read_bytes()).hexdigest()


async def boundary_rejection(
    socket: aiohttp.ClientWebSocketResponse,
    command_id: int,
    service: str,
    data: dict[str, object],
) -> dict[str, object]:
    await socket.send_json(
        {
            "id": command_id,
            "type": "call_service",
            "domain": "advnfc",
            "service": service,
            "service_data": data,
            "return_response": True,
        }
    )
    response = await socket.receive_json(timeout=15)
    assert response.get("success") is False, response
    error = response.get("error", {})
    assert error.get("code") == "invalid_format", response
    return response


async def read_provider_state(
    socket: aiohttp.ClientWebSocketResponse, ids: CommandIds
) -> dict[str, object]:
    status = await call_service(
        socket, ids.next(), "advnfc", "get_administration_status"
    )
    mappings = await call_service(socket, ids.next(), "advnfc", "list_tag_mappings")
    lookup = await call_service(
        socket, ids.next(), "advnfc", "find_tag_record", {"uid": RESERVED_UID}
    )
    return {
        "status": status,
        "mappings": mappings,
        "reserved_uid_lookup": lookup,
        "mapping_sha256": file_sha256(),
    }


def candidate_document(records: list[dict[str, object]]) -> dict[str, object]:
    return {"tag_mapping_schema_version": 1, "mappings": deepcopy(records)}


async def run_schema_probe(token: str) -> dict[str, object]:
    ids = CommandIds()
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(
            BASE_URL.replace("http", "ws") + "/api/websocket"
        ) as socket:
            assert (await socket.receive_json(timeout=10))["type"] == "auth_required"
            await socket.send_json({"type": "auth", "access_token": token})
            assert (await socket.receive_json(timeout=10))["type"] == "auth_ok"

            current_user = await ws_command(
                socket, ids.next(), type="auth/current_user"
            )
            assert current_user["is_admin"] is True
            services = await ws_command(socket, ids.next(), type="get_services")
            for service in REQUIRED_SERVICES:
                assert service in services["advnfc"]

            before = await read_provider_state(socket, ids)
            baseline_records = before["mappings"]["mappings"]
            assert before["status"]["ok"] is True
            assert before["status"]["active_count"] == 2
            assert before["status"]["persisted_count"] == 2
            assert before["status"]["activation_required"] is False
            assert all(record["uid"] != RESERVED_UID for record in baseline_records)
            assert before["reserved_uid_lookup"] == {}

            accepted = {
                "validate_tag_mapping": await call_service(
                    socket,
                    ids.next(),
                    "advnfc",
                    "validate_tag_mapping",
                    {"candidate": candidate_document(baseline_records)},
                ),
                "validate_tag_mapping_record": await call_service(
                    socket,
                    ids.next(),
                    "advnfc",
                    "validate_tag_mapping_record",
                    {"mapping": PROBE_RECORD},
                ),
                "create_tag_mapping": await call_service(
                    socket,
                    ids.next(),
                    "advnfc",
                    "create_tag_mapping",
                    {"expected_revision": STALE_REVISION, "mapping": PROBE_RECORD},
                ),
                "update_tag_mapping": await call_service(
                    socket,
                    ids.next(),
                    "advnfc",
                    "update_tag_mapping",
                    {"expected_revision": STALE_REVISION, "mapping": PROBE_RECORD},
                ),
                "delete_tag_mapping": await call_service(
                    socket,
                    ids.next(),
                    "advnfc",
                    "delete_tag_mapping",
                    {
                        "expected_revision": STALE_REVISION,
                        "uid": baseline_records[0]["uid"],
                    },
                ),
            }
            assert accepted["validate_tag_mapping"]["ok"] is True
            assert accepted["validate_tag_mapping_record"]["ok"] is True
            for service in (
                "create_tag_mapping",
                "update_tag_mapping",
                "delete_tag_mapping",
            ):
                assert accepted[service]["ok"] is False
                assert accepted[service]["error"]["code"] == "stale_revision"

            valid_payloads = {
                "validate_tag_mapping": {
                    "candidate": candidate_document(baseline_records)
                },
                "validate_tag_mapping_record": {"mapping": PROBE_RECORD},
                "create_tag_mapping": {
                    "expected_revision": STALE_REVISION,
                    "mapping": PROBE_RECORD,
                },
                "update_tag_mapping": {
                    "expected_revision": STALE_REVISION,
                    "mapping": PROBE_RECORD,
                },
                "delete_tag_mapping": {
                    "expected_revision": STALE_REVISION,
                    "uid": baseline_records[0]["uid"],
                },
            }
            malformed_payloads = {
                "validate_tag_mapping": {"candidate": "not-an-object"},
                "validate_tag_mapping_record": {"mapping": "not-an-object"},
                "create_tag_mapping": {
                    "expected_revision": 7,
                    "mapping": PROBE_RECORD,
                },
                "update_tag_mapping": {
                    "expected_revision": STALE_REVISION,
                    "mapping": "not-an-object",
                },
                "delete_tag_mapping": {
                    "expected_revision": STALE_REVISION,
                    "uid": 7,
                },
            }
            rejected: dict[str, object] = {}
            for service in REQUIRED_SERVICES:
                rejected[f"{service}_extra"] = await boundary_rejection(
                    socket,
                    ids.next(),
                    service,
                    {**valid_payloads[service], "unexpected": True},
                )
                rejected[f"{service}_malformed"] = await boundary_rejection(
                    socket, ids.next(), service, malformed_payloads[service]
                )

            after = await read_provider_state(socket, ids)

    assert after == before
    assert not SPY_PATH.exists()
    return {
        "outcome": "pass",
        "observed_at": observed_at(),
        "authority": "ASTV-366 preserved non-mutating administration schema probe",
        "source_probe": "ASTV-360",
        "administrator": {
            "user_id": current_user["id"],
            "is_admin": current_user["is_admin"],
        },
        "registered_services": REQUIRED_SERVICES,
        "accepted_provider_responses": accepted,
        "boundary_rejections": rejected,
        "before": before,
        "after": after,
        "mutation_result": "no_persisted_or_active_change",
        "mutation_service_probes": [
            "create_tag_mapping: stale revision",
            "update_tag_mapping: stale revision",
            "delete_tag_mapping: stale revision",
        ],
        "lifecycle_calls_executed": [],
        "reload_or_activation_calls": 0,
        "automatic_retries": 0,
        "gateway_sink_invocations": 0,
    }


async def main() -> None:
    token = create_stage_token()
    baseline = await verify(token)
    evidence = await run_schema_probe(token)
    evidence["stage_baseline"] = baseline
    EVIDENCE_PATH.write_text(
        json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    asyncio.run(main())
