from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys

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
    assert _snapshot().administration_capabilities() == {
        "interface_id": "advnfc.tag_mapping.administration",
        "interface_version": 1,
        "tag_mapping_schema_version": 1,
        "ok": True,
        "supported_action_types": ["astv_intent"],
        "operations": ["capabilities", "list", "get", "query"],
    }


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
