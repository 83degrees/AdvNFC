"""Execute a separately authorized lifecycle in disposable staging only.

This module is deliberately not reachable from the maintained workflow. Each
use requires fresh action-specific human authority and a reviewed workflow
change or equivalent controlled invocation.
"""

from __future__ import annotations

import asyncio
from copy import deepcopy
from datetime import UTC, datetime
import hashlib
import json
import os
from pathlib import Path
from typing import Any

import aiohttp
import yaml

from verify_baseline import (
    BASE_URL,
    RESERVED_UID,
    SPY_PATH,
    call_service,
    create_stage_token,
    verify,
    ws_command,
)


MAPPING_PATH = Path("/config/AdvNFC/advnfc_tag_mapping.yaml")
STAGE_EVIDENCE_PATH = Path("/evidence/baseline-evidence.json")
LIFECYCLE_EVIDENCE_PATH = Path("/evidence/lifecycle-evidence.json")
TEST_UID = RESERVED_UID
INITIAL_RECORD = {
    "uid": TEST_UID,
    "label": "Synthetic lifecycle validation",
    "action": {"type": "astv_intent", "intent_id": "validation_primary"},
}
UPDATED_RECORD = {
    "uid": TEST_UID,
    "label": "Synthetic lifecycle validation updated",
    "area_override": "advnfc_validation_area",
    "action": {"type": "astv_intent", "intent_id": "validation_primary"},
}


def observed_at() -> str:
    return datetime.now(UTC).isoformat()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def canonical(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(deepcopy(records), key=lambda record: record["uid"])


def persisted_snapshot() -> dict[str, Any]:
    raw = MAPPING_PATH.read_bytes()
    document = yaml.safe_load(raw)
    records = []
    for uid, value in document["tags"].items():
        records.append({"uid": str(uid), **deepcopy(value)})
    return {
        "captured_at": observed_at(),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "count": len(records),
        "mappings": canonical(records),
    }


class CommandIds:
    def __init__(self) -> None:
        self.value = 100

    def next(self) -> int:
        self.value += 1
        return self.value


def write_evidence(evidence: dict[str, Any]) -> None:
    LIFECYCLE_EVIDENCE_PATH.write_text(
        json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


async def read_state(
    socket: aiohttp.ClientWebSocketResponse, ids: CommandIds
) -> dict[str, Any]:
    status = await call_service(socket, ids.next(), "advnfc", "get_administration_status")
    active_list = await call_service(socket, ids.next(), "advnfc", "list_tag_mappings")
    lookup = await call_service(
        socket, ids.next(), "advnfc", "find_tag_record", {"uid": TEST_UID}
    )
    return {
        "captured_at": observed_at(),
        "status": status,
        "active_list": active_list,
        "synthetic_lookup": lookup,
        "persisted": persisted_snapshot(),
        "gateway_spy_absent": not SPY_PATH.exists(),
    }


def require_common_state(
    state: dict[str, Any], baseline: list[dict[str, Any]]
) -> None:
    require(state["status"]["ok"] is True, "provider status is not healthy")
    require(state["active_list"]["ok"] is True, "active list is not healthy")
    require(state["gateway_spy_absent"] is True, "gateway sink observed an invocation")
    active_baseline = [
        record for record in state["active_list"]["mappings"] if record["uid"] != TEST_UID
    ]
    persisted_baseline = [
        record for record in state["persisted"]["mappings"] if record["uid"] != TEST_UID
    ]
    require(canonical(active_baseline) == baseline, "pre-existing active mapping drifted")
    require(canonical(persisted_baseline) == baseline, "pre-existing persisted mapping drifted")


async def execute_call(
    socket: aiohttp.ClientWebSocketResponse,
    ids: CommandIds,
    evidence: dict[str, Any],
    *,
    name: str,
    service: str,
    data: dict[str, Any] | None = None,
    mutating: bool,
) -> tuple[dict[str, Any], dict[str, Any]]:
    entry: dict[str, Any] = {
        "name": name,
        "service": f"advnfc.{service}",
        "request": deepcopy(data or {}),
        "mutating": mutating,
        "started_at": observed_at(),
        "attempts": 1,
    }
    evidence["operations"].append(entry)
    if mutating:
        evidence["lifecycle_calls_executed"].append(name)
    write_evidence(evidence)
    try:
        response = await call_service(socket, ids.next(), "advnfc", service, data)
    except Exception as error:
        entry["outcome"] = "uncertain_no_retry"
        entry["error"] = f"{type(error).__name__}: {error}"
        entry["completed_at"] = observed_at()
        write_evidence(evidence)
        raise
    entry["response"] = response
    entry["completed_at"] = observed_at()
    entry["outcome"] = "returned"
    state = await read_state(socket, ids)
    entry["post_state"] = state
    write_evidence(evidence)
    return response, state


async def lifecycle(token: str, evidence: dict[str, Any]) -> None:
    baseline = canonical(evidence["preflight"]["advnfc"]["list_response"]["mappings"])
    require(len(baseline) == 2, "preflight baseline is not two synthetic records")
    require(all(record["uid"] != TEST_UID for record in baseline), "reserved UID already exists")
    baseline_file = persisted_snapshot()
    require(baseline_file["mappings"] == baseline, "persisted preflight differs from active baseline")
    baseline_revision = evidence["preflight"]["advnfc"]["status"]["active_revision"]
    evidence["baseline"] = {
        "revision": baseline_revision,
        "mappings": baseline,
        "file": baseline_file,
    }
    write_evidence(evidence)

    ids = CommandIds()
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(BASE_URL.replace("http", "ws") + "/api/websocket") as socket:
            require((await socket.receive_json(timeout=10))["type"] == "auth_required", "missing auth challenge")
            await socket.send_json({"type": "auth", "access_token": token})
            require((await socket.receive_json(timeout=10))["type"] == "auth_ok", "stage authentication failed")

            initial = await read_state(socket, ids)
            require_common_state(initial, baseline)
            initial_status = initial["status"]
            require(initial_status["active_count"] == initial_status["persisted_count"] == 2, "initial count mismatch")
            require(initial_status["active_revision"] == initial_status["persisted_revision"] == baseline_revision, "initial revision mismatch")
            require(initial_status["activation_required"] is False, "stage already requires activation")
            require(initial_status["last_activation_error"] is None, "stage has an activation error")
            evidence["initial_state"] = initial
            write_evidence(evidence)

            validation, validated_state = await execute_call(
                socket, ids, evidence, name="validate_reserved_record", service="validate_tag_mapping_record",
                data={"mapping": INITIAL_RECORD}, mutating=False,
            )
            require(validation["ok"] is True and validation["mapping"] == INITIAL_RECORD, "reserved record validation failed")
            require_common_state(validated_state, baseline)
            require(validated_state["status"] == initial_status, "validation changed provider status")
            require(validated_state["persisted"]["sha256"] == baseline_file["sha256"], "validation changed persisted bytes")

            created, after_create = await execute_call(
                socket, ids, evidence, name="create_save", service="create_tag_mapping",
                data={"expected_revision": initial_status["persisted_revision"], "mapping": INITIAL_RECORD}, mutating=True,
            )
            require(created["ok"] is True and created["mapping"] == INITIAL_RECORD, "create response failed")
            require_common_state(after_create, baseline)
            create_status = after_create["status"]
            require(create_status["active_count"] == 2 and create_status["persisted_count"] == 3, "create count transition failed")
            require(create_status["active_revision"] == baseline_revision, "create changed active revision")
            require(create_status["persisted_revision"] == created["persisted_revision"] != baseline_revision, "create persisted revision failed")
            require(create_status["activation_required"] is True, "create did not require activation")
            require(canonical(after_create["active_list"]["mappings"]) == baseline, "create changed active list")
            require(after_create["synthetic_lookup"] == {}, "create changed active routing before activation")
            require(after_create["persisted"]["count"] == 3 and INITIAL_RECORD in after_create["persisted"]["mappings"], "created record not persisted")

            activated_create, after_activate_create = await execute_call(
                socket, ids, evidence, name="activate_created", service="reload_tag_mapping", mutating=True,
            )
            require(activated_create["ok"] is True, "first activation failed")
            require_common_state(after_activate_create, baseline)
            first_status = after_activate_create["status"]
            require(first_status["active_count"] == first_status["persisted_count"] == 3, "first activation count failed")
            require(first_status["active_revision"] == first_status["persisted_revision"] == created["persisted_revision"], "first activation revision failed")
            require(first_status["activation_required"] is False, "first activation remained pending")
            require(after_activate_create["synthetic_lookup"] == INITIAL_RECORD, "created record did not become active")
            require(canonical(after_activate_create["active_list"]["mappings"]) == canonical([*baseline, INITIAL_RECORD]), "created active list mismatch")

            updated, after_update = await execute_call(
                socket, ids, evidence, name="edit_save", service="update_tag_mapping",
                data={"expected_revision": first_status["persisted_revision"], "mapping": UPDATED_RECORD}, mutating=True,
            )
            require(updated["ok"] is True and updated["mapping"] == UPDATED_RECORD, "update response failed")
            require_common_state(after_update, baseline)
            update_status = after_update["status"]
            require(update_status["active_count"] == update_status["persisted_count"] == 3, "update count transition failed")
            require(update_status["active_revision"] == first_status["active_revision"], "update changed active revision")
            require(update_status["persisted_revision"] == updated["persisted_revision"] != update_status["active_revision"], "update persisted revision failed")
            require(update_status["activation_required"] is True, "update did not require activation")
            require(after_update["synthetic_lookup"] == INITIAL_RECORD, "update changed active routing before activation")
            require(INITIAL_RECORD in after_update["active_list"]["mappings"], "initial active record missing after update")
            require(UPDATED_RECORD in after_update["persisted"]["mappings"], "updated record not persisted")

            activated_update, after_activate_update = await execute_call(
                socket, ids, evidence, name="activate_updated", service="reload_tag_mapping", mutating=True,
            )
            require(activated_update["ok"] is True, "second activation failed")
            require_common_state(after_activate_update, baseline)
            second_status = after_activate_update["status"]
            require(second_status["active_count"] == second_status["persisted_count"] == 3, "second activation count failed")
            require(second_status["active_revision"] == second_status["persisted_revision"] == updated["persisted_revision"], "second activation revision failed")
            require(second_status["activation_required"] is False, "second activation remained pending")
            require(after_activate_update["synthetic_lookup"] == UPDATED_RECORD, "updated record did not become active")

            duplicate_uid = baseline[0]["uid"]
            duplicate_before = deepcopy(after_activate_update)
            duplicate_record = {
                "uid": duplicate_uid,
                "label": "Synthetic forbidden duplicate",
                "action": {"type": "astv_intent", "intent_id": "validation_primary"},
            }
            duplicate, after_duplicate = await execute_call(
                socket, ids, evidence, name="reject_baseline_duplicate", service="create_tag_mapping",
                data={"expected_revision": second_status["persisted_revision"], "mapping": duplicate_record}, mutating=True,
            )
            require(duplicate["ok"] is False and duplicate["error"]["code"] == "already_exists", "duplicate was not rejected")
            require_common_state(after_duplicate, baseline)
            require(after_duplicate["status"] == duplicate_before["status"], "duplicate changed status")
            require(after_duplicate["active_list"] == duplicate_before["active_list"], "duplicate changed active list")
            require(after_duplicate["synthetic_lookup"] == duplicate_before["synthetic_lookup"], "duplicate changed routing")
            require(after_duplicate["persisted"]["sha256"] == duplicate_before["persisted"]["sha256"], "duplicate changed persisted bytes")

            deleted, after_delete = await execute_call(
                socket, ids, evidence, name="delete_save", service="delete_tag_mapping",
                data={"expected_revision": second_status["persisted_revision"], "uid": TEST_UID}, mutating=True,
            )
            require(deleted["ok"] is True and deleted["uid"] == TEST_UID, "delete response failed")
            require_common_state(after_delete, baseline)
            delete_status = after_delete["status"]
            require(delete_status["active_count"] == 3 and delete_status["persisted_count"] == 2, "delete count transition failed")
            require(delete_status["active_revision"] == second_status["active_revision"], "delete changed active revision")
            require(delete_status["persisted_revision"] == deleted["persisted_revision"], "delete persisted revision failed")
            require(delete_status["activation_required"] is True, "delete did not require activation")
            require(after_delete["synthetic_lookup"] == UPDATED_RECORD, "delete changed active routing before activation")
            require(after_delete["persisted"]["mappings"] == baseline, "delete did not restore persisted logical baseline")

            final_activation, final_state = await execute_call(
                socket, ids, evidence, name="activate_deleted", service="reload_tag_mapping", mutating=True,
            )
            require(final_activation["ok"] is True, "final activation failed")
            require_common_state(final_state, baseline)
            final_status = final_state["status"]
            require(final_status["active_count"] == final_status["persisted_count"] == 2, "final count is not baseline")
            require(final_status["active_revision"] == final_status["persisted_revision"], "final revisions differ")
            require(final_status["activation_required"] is False, "final activation remained pending")
            require(final_status["last_activation_error"] is None, "final activation recorded an error")
            require(canonical(final_state["active_list"]["mappings"]) == baseline, "final active baseline differs")
            require(final_state["persisted"]["mappings"] == baseline, "final persisted baseline differs")
            require(final_state["synthetic_lookup"] == {}, "reserved UID remained active")

            evidence["final_state"] = final_state
            evidence["baseline_restoration"] = {
                "logical_exact": True,
                "byte_exact": final_state["persisted"]["sha256"] == baseline_file["sha256"],
                "baseline_sha256": baseline_file["sha256"],
                "final_sha256": final_state["persisted"]["sha256"],
                "final_revision": final_status["active_revision"],
            }
            evidence["gateway_sink"] = {"invocations": 0, "spy_file_absent": True}


async def main() -> None:
    evidence: dict[str, Any] = {
        "authority": "fresh action-specific authority required before invocation",
        "environment": "disposable isolated Home Assistant staging only",
        "operator": os.getenv("GITHUB_ACTOR", "unknown"),
        "workflow_run_id": os.getenv("GITHUB_RUN_ID", "unknown"),
        "workflow_sha": os.getenv("GITHUB_SHA", "unknown"),
        "started_at": observed_at(),
        "outcome": "running",
        "operations": [],
        "lifecycle_calls_executed": [],
        "automatic_retries": 0,
    }
    write_evidence(evidence)
    try:
        token = create_stage_token()
        preflight = await verify(token)
        STAGE_EVIDENCE_PATH.write_text(
            json.dumps(preflight, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        evidence["preflight"] = preflight
        write_evidence(evidence)
        await lifecycle(token, evidence)
        evidence["outcome"] = "pass"
    except Exception as error:
        evidence["outcome"] = "aborted"
        evidence["abort"] = {
            "at": observed_at(),
            "error": f"{type(error).__name__}: {error}",
            "no_retry": True,
            "disposal_required": True,
        }
        raise
    finally:
        evidence["completed_at"] = observed_at()
        evidence["gateway_spy_present_at_completion"] = SPY_PATH.exists()
        write_evidence(evidence)


if __name__ == "__main__":
    asyncio.run(main())
