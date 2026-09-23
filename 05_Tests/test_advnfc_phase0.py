from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
AUTOMATIONS = ROOT / "04_Source/config/packages/advnfc/advnfc_automations.yaml"
SCRIPTS = ROOT / "04_Source/config/packages/advnfc/advnfc_scripts.yaml"
MAPPING = ROOT / "04_Source/config/assistive/advnfc_tag_mapping.yaml"


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _parse_simple_tag_mapping(text: str) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    current: str | None = None
    for raw in text.splitlines():
        if not raw.strip():
            continue
        if not raw.startswith(" "):
            current = raw.rstrip(":").strip()
            result[current] = {}
            continue
        key, value = raw.strip().split(":", 1)
        result[current][key.strip()] = value.strip()
    return result


def _valid_reader_transition(old: str, new: str) -> bool:
    invalid = {"unknown", "unavailable"}
    return old not in invalid and new not in invalid and old != new


def _normalize_uid(uid: object) -> str:
    return str(uid).strip().upper()


def _contract_payload(tag_record: dict[str, str], trigger_entity: str) -> dict[str, str]:
    intent_id = str(tag_record.get("intent_id", "")).strip()
    if not intent_id:
        raise ValueError("Invalid tag record")
    return {
        "intent_id": intent_id,
        "input_area_override": str(tag_record.get("area_override", "")).strip(),
        "trigger_entity": trigger_entity,
    }


def test_listener_preserves_configured_reader_sources_and_recovery_filtering():
    source = _text(AUTOMATIONS)
    assert "sensor.pi_nfc_02_last_uid" in source
    assert "sensor.pi_nfc_99_last_uid" in source
    assert "not_from:\n      - unknown\n      - unavailable" in source
    assert "not_to:\n      - unknown\n      - unavailable" in source
    assert "action: script.advnfc_uid_gateway" in source
    assert "uid: '{{ trigger.to_state.state | upper }}'" in source
    assert "trigger_entity: '{{ trigger.entity_id }}'" in source


def test_reader_transition_behavior_matches_extracted_phase_zero_semantics():
    assert _valid_reader_transition("AAA", "BBB")
    assert not _valid_reader_transition("AAA", "AAA")
    assert not _valid_reader_transition("unknown", "AAA")
    assert not _valid_reader_transition("unavailable", "AAA")
    assert not _valid_reader_transition("AAA", "unknown")
    assert not _valid_reader_transition("AAA", "unavailable")


def test_uid_normalization_is_trim_and_uppercase():
    assert _normalize_uid("  7ab06354e000  ") == "7AB06354E000"
    source = _text(SCRIPTS)
    assert "lookup_uid: '{{ uid | string | trim | upper }}'" in source


def test_tag_mapping_preserves_existing_phase_zero_records():
    mapping = _parse_simple_tag_mapping(_text(MAPPING))
    assert mapping["7AB06354E000"]["intent_id"] == "classic_fm"
    assert mapping["E38B36C82A81"]["intent_id"] == "classic_fm"
    assert mapping["689C36C82A81"]["intent_id"] == "lbc_news"
    assert mapping["EA9236C82A81"]["intent_id"] == "gold_radio"
    assert mapping["DEADBEEF"]["intent_id"] == "bbc_radio_2"
    assert mapping["DEADSMOOTH"]["intent_id"] == "smooth_radio"
    assert mapping["DEADLBC"]["intent_id"] == "lbc_radio"
    assert mapping["DEADNEWSBRIEF"]["intent_id"] == "news_briefing"
    assert mapping["DEADMORNING"]["intent_id"] == "morning_routine"


def test_missing_tag_record_stops_before_astv_invocation():
    source = _text(SCRIPTS)
    missing_check = source.index("title: No Tag Record Found")
    astv_call = source.index("action: script.astv_intent_gateway")
    assert missing_check < astv_call
    assert "stop: No tag record found" in source
    assert "error: false" in source


def test_invalid_tag_record_stops_before_astv_invocation():
    source = _text(SCRIPTS)
    invalid_check = source.index("title: Invalid Tag Record")
    astv_call = source.index("action: script.astv_intent_gateway")
    assert invalid_check < astv_call
    assert "stop: Invalid tag record" in source


def test_contract_payload_preserves_intent_override_and_trigger_entity():
    payload = _contract_payload(
        {"intent_id": " classic_fm ", "area_override": " kitchen "},
        "sensor.pi_nfc_02_last_uid",
    )
    assert payload == {
        "intent_id": "classic_fm",
        "input_area_override": "kitchen",
        "trigger_entity": "sensor.pi_nfc_02_last_uid",
    }


def test_contract_payload_allows_blank_area_override():
    payload = _contract_payload(
        {"intent_id": "classic_fm"},
        "sensor.pi_nfc_99_last_uid",
    )
    assert payload["input_area_override"] == ""


def test_invalid_record_model_rejects_blank_intent_id():
    for record in ({}, {"intent_id": ""}, {"intent_id": "   "}):
        try:
            _contract_payload(record, "sensor.pi_nfc_02_last_uid")
        except ValueError:
            pass
        else:
            raise AssertionError("blank intent_id must be rejected")


def test_astv_invocation_uses_exact_three_field_contract_and_does_not_send_uid():
    source = _text(SCRIPTS)
    match = re.search(
        r"- action: script\.astv_intent_gateway\n"
        r"\s+data:\n"
        r"\s+intent_id:.*\n"
        r"\s+input_area_override:.*\n"
        r"\s+trigger_entity:.*",
        source,
    )
    assert match is not None
    block = match.group(0)
    assert "intent_id:" in block
    assert "input_area_override:" in block
    assert "trigger_entity:" in block
    assert "\n        uid:" not in block


def test_advnfc_lookup_owns_mapping_and_astv_only_receives_canonical_invocation():
    source = _text(SCRIPTS)
    assert "!include ../../assistive/advnfc_tag_mapping.yaml" in source
    assert "action: script.advnfc_find_tag_record" in source
    assert "action: script.astv_intent_gateway" in source
    assert "script.astv_find_tag_record" not in source
