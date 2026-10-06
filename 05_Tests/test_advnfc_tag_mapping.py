from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
MAPPING_MODULE = ROOT / "custom_components" / "advnfc" / "mapping.py"
SPEC = spec_from_file_location("advnfc_mapping", MAPPING_MODULE)
assert SPEC is not None and SPEC.loader is not None
mapping = module_from_spec(SPEC)
sys.modules[SPEC.name] = mapping
SPEC.loader.exec_module(mapping)


def _document(tags: str = "{}") -> str:
    return f"tag_mapping_schema_version: 1\ntags: {tags}\n"


def _one_tag(**overrides: str) -> str:
    label = overrides.get("label", "Kitchen radio")
    area = overrides.get("area", "")
    action_type = overrides.get("action_type", "astv_intent")
    intent_id = overrides.get("intent_id", "classic_fm")
    area_line = f"\n    area_override: {area}" if area else ""
    return _document(
        f"\n  7AB06354E000:\n"
        f"    label: {label}{area_line}\n"
        f"    action:\n"
        f"      type: {action_type}\n"
        f"      intent_id: {intent_id}"
    )


def _validate(text: str, areas: set[str] | None = None):
    areas = areas or set()
    return mapping.validate_document(
        mapping.parse_yaml_document(text), areas.__contains__
    )


def test_valid_schema_v1_load_and_normalized_runtime_record():
    tags = _validate(_one_tag(intent_id=" Classic_FM "))
    snapshot = mapping.TagMappingSnapshot(1, tags)
    assert snapshot.find(" 7ab06354e000 ") == {
        "uid": "7AB06354E000",
        "label": "Kitchen radio",
        "action": {"type": "astv_intent", "intent_id": "classic_fm"},
    }


def test_empty_tags_mapping_is_valid():
    assert dict(_validate(_document())) == {}


@pytest.mark.parametrize(
    "uid",
    ["7ab06354e000", "7AB0-6354", ""],
)
def test_stored_uid_must_be_canonical_uppercase(uid: str):
    text = _one_tag().replace("7AB06354E000", uid)
    with pytest.raises(mapping.TagMappingValidationError):
        _validate(text)


def test_quoted_uid_with_surrounding_whitespace_is_rejected():
    text = _one_tag().replace("7AB06354E000:", "' 7AB06354E000 ':")
    with pytest.raises(mapping.TagMappingValidationError):
        _validate(text)


def test_duplicate_uid_or_yaml_key_is_rejected():
    text = _document(
        "\n  DEADBEEF:\n"
        "    label: First\n"
        "    action: {type: astv_intent, intent_id: classic_fm}\n"
        "  DEADBEEF:\n"
        "    label: Second\n"
        "    action: {type: astv_intent, intent_id: gold_radio}"
    )
    with pytest.raises(mapping.TagMappingValidationError, match="duplicate YAML key"):
        mapping.parse_yaml_document(text)


@pytest.mark.parametrize(
    "text",
    [
        _document() + "extra: true\n",
        _one_tag().replace("    action:\n", "    unknown: true\n    action:\n"),
        _one_tag().replace(
            "      intent_id: classic_fm",
            "      intent_id: classic_fm\n      unknown: true",
        ),
    ],
)
def test_unknown_root_tag_and_action_fields_are_rejected(text: str):
    with pytest.raises(mapping.TagMappingValidationError, match="unknown fields"):
        _validate(text)


@pytest.mark.parametrize(
    "text",
    [
        _one_tag().replace("    label: Kitchen radio\n", ""),
        _one_tag(label="''"),
        _one_tag().replace("    action:\n", ""),
        _one_tag().replace("      type: astv_intent\n", ""),
        _one_tag().replace("      intent_id: classic_fm", ""),
        _one_tag(intent_id="''"),
    ],
)
def test_missing_or_blank_required_fields_are_rejected(text: str):
    with pytest.raises(mapping.TagMappingValidationError):
        _validate(text)


def test_unknown_action_type_is_rejected():
    with pytest.raises(mapping.TagMappingValidationError, match="unsupported"):
        _validate(_one_tag(action_type="ha_action"))


@pytest.mark.parametrize("intent_id", ["classic fm", "classic-fm", "_classic", "classic_"])
def test_structurally_invalid_intent_id_is_rejected(intent_id: str):
    with pytest.raises(mapping.TagMappingValidationError, match="structurally invalid"):
        _validate(_one_tag(intent_id=intent_id))


def test_area_override_must_resolve():
    with pytest.raises(mapping.TagMappingValidationError, match="does not resolve"):
        _validate(_one_tag(area="kitchen"), areas={"bedroom"})
    tags = _validate(_one_tag(area="kitchen"), areas={"kitchen"})
    assert tags["7AB06354E000"]["area_override"] == "kitchen"


def test_blank_area_override_is_rejected_when_present():
    text = _one_tag().replace("    action:\n", "    area_override: ''\n    action:\n")
    with pytest.raises(mapping.TagMappingValidationError, match="non-blank"):
        _validate(text)


def test_multiple_tags_may_reference_the_same_intent():
    text = _document(
        "\n  A1:\n"
        "    label: One\n"
        "    action: {type: astv_intent, intent_id: classic_fm}\n"
        "  B2:\n"
        "    label: Two\n"
        "    action: {type: astv_intent, intent_id: classic_fm}"
    )
    tags = _validate(text)
    assert len(tags) == 2


def test_snapshot_is_immutable():
    tags = _validate(_one_tag())
    with pytest.raises(TypeError):
        tags["7AB06354E000"] = {}  # type: ignore[index]
    with pytest.raises(TypeError):
        tags["7AB06354E000"]["label"] = "Changed"  # type: ignore[index]


def test_failed_reload_retains_previous_active_snapshot(tmp_path: Path):
    candidate = tmp_path / "advnfc_tag_mapping.yaml"
    store = mapping.TagMappingStore()
    candidate.write_text(_one_tag(), encoding="utf-8")
    first = store.load_and_activate(candidate, set().__contains__)

    candidate.write_text(_one_tag(action_type="unknown"), encoding="utf-8")
    with pytest.raises(mapping.TagMappingValidationError):
        store.load_and_activate(candidate, set().__contains__)

    assert store.active is first
    assert store.find("7ab06354e000")["action"]["intent_id"] == "classic_fm"


def test_governed_mapping_contains_all_migrated_records():
    tags = _validate(
        (ROOT / "04_Implementation/haos/source/config/AdvNFC/advnfc_tag_mapping.yaml").read_text(
            encoding="utf-8"
        )
    )
    assert {record["action"]["intent_id"] for record in tags.values()} == {
        "classic_fm",
        "lbc_news",
        "gold_radio",
        "bbc_radio_2",
        "smooth_radio",
        "lbc_radio",
        "news_briefing",
        "morning_routine",
    }
