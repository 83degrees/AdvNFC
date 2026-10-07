from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = spec_from_file_location(
    "advnfc_admin_mapping", ROOT / "custom_components" / "advnfc" / "mapping.py"
)
assert SPEC is not None and SPEC.loader is not None
mapping = module_from_spec(SPEC)
sys.modules[SPEC.name] = mapping
SPEC.loader.exec_module(mapping)


def _snapshot():
    document = mapping.parse_yaml_document(
        """
tag_mapping_schema_version: 1
tags:
  B2:
    label: Second radio
    area_override: kitchen
    action: {type: astv_intent, intent_id: classic_fm}
  A1:
    label: First radio
    action: {type: astv_intent, intent_id: classic_fm}
  C3:
    label: News
    action: {type: astv_intent, intent_id: lbc_news}
"""
    )
    tags = mapping.validate_document(document, {"kitchen"}.__contains__)
    return mapping.TagMappingSnapshot(1, tags)


def test_capabilities_expose_stable_interface_and_active_schema():
    response = _snapshot().administration_capabilities()
    assert response == {
        "interface_id": "advnfc.tag_mapping.administration",
        "interface_version": 3,
        "tag_mapping_schema_version": 1,
        "revision": response["revision"],
        "ok": True,
        "supported_action_types": ["astv_intent"],
        "operations": [
            "capabilities",
            "list",
            "get",
            "query",
            "status",
            "validate_document",
            "validate_record",
            "create",
            "update",
            "delete",
            "activate",
        ],
    }
    assert response["revision"].startswith("v1-")


def test_list_returns_normalized_records_in_canonical_uid_order():
    response = _snapshot().administration_list()
    assert response["ok"] is True
    assert response["count"] == 3
    assert [record["uid"] for record in response["mappings"]] == ["A1", "B2", "C3"]
    assert response["mappings"][1] == {
        "uid": "B2",
        "label": "Second radio",
        "area_override": "kitchen",
        "action": {"type": "astv_intent", "intent_id": "classic_fm"},
    }


def test_get_normalizes_uid_and_returns_one_record():
    response = _snapshot().administration_get(" a1 ")
    assert response["ok"] is True
    assert response["query"] == {"uid": "A1"}
    assert response["mapping"]["label"] == "First radio"


def test_get_distinguishes_invalid_query_from_not_found():
    invalid = _snapshot().administration_get("not-valid")
    missing = _snapshot().administration_get("D4")
    assert invalid["error"]["code"] == "invalid_query"
    assert missing["error"]["code"] == "not_found"
    assert missing["query"] == {"uid": "D4"}


def test_query_normalizes_target_and_returns_all_matches():
    response = _snapshot().administration_query(" ASTV_INTENT ", " Classic_FM ")
    assert response["query"] == {
        "action": {"type": "astv_intent", "intent_id": "classic_fm"}
    }
    assert response["count"] == 2
    assert [record["uid"] for record in response["mappings"]] == ["A1", "B2"]


def test_valid_query_without_matches_returns_empty_collection():
    response = _snapshot().administration_query("astv_intent", "unknown_intent")
    assert response["ok"] is True
    assert response["count"] == 0
    assert response["mappings"] == []


def test_query_rejects_unsupported_type_and_invalid_target_shape():
    unsupported = _snapshot().administration_query("ha_action", "classic_fm")
    malformed = _snapshot().administration_query("astv_intent", "classic fm")
    assert unsupported["error"]["code"] == "invalid_query"
    assert malformed["error"]["code"] == "invalid_query"


def _record(uid: str = "D4", label: str = "New radio") -> dict:
    return {
        "uid": uid,
        "label": label,
        "action": {"type": "astv_intent", "intent_id": "gold_radio"},
    }


def _store(tmp_path: Path):
    path = tmp_path / "advnfc_tag_mapping.yaml"
    path.write_text(
        """tag_mapping_schema_version: 1
tags:
  A1:
    label: First radio
    action: {type: astv_intent, intent_id: classic_fm}
""",
        encoding="utf-8",
    )
    store = mapping.TagMappingStore()
    store.load_and_activate(path, set().__contains__)
    return store, path


def test_complete_candidate_and_record_validation_normalize_without_writing(tmp_path):
    store, path = _store(tmp_path)
    before = path.read_text(encoding="utf-8")
    record = store.administration_validate_record(
        _record(" d4 "), set().__contains__
    )
    assert record["ok"] is True
    assert record["mapping"]["uid"] == "D4"
    assert path.read_text(encoding="utf-8") == before

    invalid = store.administration_validate_document(
        {
            "tag_mapping_schema_version": 1,
            "mappings": [_record("D4"), _record(" d4 ")],
        },
        set().__contains__,
    )
    assert invalid["ok"] is False
    assert invalid["error"]["code"] == "duplicate_uid"


def test_create_update_delete_are_atomic_and_do_not_activate(tmp_path):
    store, path = _store(tmp_path)
    active = store.active
    assert active is not None

    created = store.administration_create(
        path, active.revision, _record(" d4 "), set().__contains__
    )
    assert created["ok"] is True
    assert created["mapping"]["uid"] == "D4"
    assert created["activation_required"] is True
    assert store.active is active
    assert store.find("D4") == {}

    updated = store.administration_update(
        path,
        created["persisted_revision"],
        _record("D4", "Updated radio"),
        set().__contains__,
    )
    assert updated["ok"] is True
    assert updated["mapping"]["label"] == "Updated radio"
    assert store.active is active

    deleted = store.administration_delete(
        path,
        updated["persisted_revision"],
        " d4 ",
        set().__contains__,
    )
    assert deleted["ok"] is True
    persisted = store._persisted_snapshot(path, set().__contains__)
    assert "D4" not in persisted.tags
    assert store.active is active


def test_status_distinguishes_persisted_candidate_from_active_snapshot(tmp_path):
    store, path = _store(tmp_path)
    assert store.active is not None
    created = store.administration_create(
        path, store.active.revision, _record(), set().__contains__
    )

    status = store.administration_status(path, set().__contains__)
    assert status["ok"] is True
    assert status["state"] == "activation_required"
    assert status["active_revision"] != status["persisted_revision"]
    assert status["persisted_revision"] == created["persisted_revision"]
    assert status["activation_required"] is True
    assert status["active_count"] == 1
    assert status["persisted_count"] == 2


def test_activation_succeeds_atomically_and_clears_pending_state(tmp_path):
    store, path = _store(tmp_path)
    assert store.active is not None
    created = store.administration_create(
        path, store.active.revision, _record(), set().__contains__
    )
    assert store.find("D4") == {}

    activated = store.administration_activate(path, set().__contains__)
    assert activated["ok"] is True
    assert activated["state"] == "active"
    assert activated["active_revision"] == created["persisted_revision"]
    assert activated["persisted_revision"] == created["persisted_revision"]
    assert activated["activation_required"] is False
    assert store.find("D4")["label"] == "New radio"


def test_failed_activation_retains_active_snapshot_and_retry_recovers(tmp_path):
    store, path = _store(tmp_path)
    previous_active = store.active
    assert previous_active is not None
    created = store.administration_create(
        path, previous_active.revision, _record(), set().__contains__
    )
    valid_candidate = path.read_bytes()
    path.write_text(
        "tag_mapping_schema_version: 1\ntags:\n  D4:\n    label: Broken\n",
        encoding="utf-8",
    )

    failed = store.administration_activate(path, set().__contains__)
    assert failed["ok"] is False
    assert failed["state"] == "persisted_invalid"
    assert failed["error"]["code"] == "invalid_candidate"
    assert failed["active_revision"] == previous_active.revision
    assert store.active is previous_active
    assert store.find("D4") == {}

    status = store.administration_status(path, set().__contains__)
    assert status["last_activation_error"]["code"] == "invalid_candidate"

    path.write_bytes(valid_candidate)
    recovered = store.administration_activate(path, set().__contains__)
    assert recovered["ok"] is True
    assert recovered["active_revision"] == created["persisted_revision"]
    assert recovered["activation_required"] is False
    assert store.last_activation_error is None
    assert store.find("D4")["label"] == "New radio"


def test_stale_revision_rejects_write_without_mutation(tmp_path):
    store, path = _store(tmp_path)
    before = path.read_bytes()
    response = store.administration_create(
        path, "v1-stale", _record(), set().__contains__
    )
    assert response["error"]["code"] == "stale_revision"
    assert path.read_bytes() == before


def test_invalid_candidate_rejects_write_without_mutation(tmp_path):
    store, path = _store(tmp_path)
    assert store.active is not None
    before = path.read_bytes()
    invalid = _record()
    invalid["action"]["type"] = "ha_action"
    response = store.administration_create(
        path, store.active.revision, invalid, set().__contains__
    )
    assert response["error"]["code"] == "invalid_candidate"
    assert path.read_bytes() == before


def test_atomic_replace_failure_retains_authoritative_file(tmp_path, monkeypatch):
    store, path = _store(tmp_path)
    assert store.active is not None
    before = path.read_bytes()

    def fail_replace(source, destination):
        raise OSError("simulated replacement failure")

    monkeypatch.setattr(mapping.os, "replace", fail_replace)
    response = store.administration_create(
        path, store.active.revision, _record(), set().__contains__
    )
    assert response["error"]["code"] == "atomic_write_failed"
    assert path.read_bytes() == before
    assert list(tmp_path.glob(".*.tmp")) == []


@pytest.mark.parametrize(
    ("operation", "record", "code"),
    [
        ("create", _record("A1"), "already_exists"),
        ("update", _record("D4"), "not_found"),
    ],
)
def test_create_and_update_enforce_provider_semantics(
    tmp_path, operation, record, code
):
    store, path = _store(tmp_path)
    assert store.active is not None
    response = getattr(store, f"administration_{operation}")(
        path, store.active.revision, record, set().__contains__
    )
    assert response["error"]["code"] == code
