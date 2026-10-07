import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
HA_CONFIG = ROOT / "04_Implementation" / "haos" / "source" / "config"
AUTOMATIONS = HA_CONFIG / "packages" / "advnfc" / "advnfc_automations.yaml"
SCRIPTS = HA_CONFIG / "packages" / "advnfc" / "advnfc_scripts.yaml"
MAPPING = HA_CONFIG / "AdvNFC" / "advnfc_tag_mapping.yaml"
INTEGRATION = ROOT / "custom_components" / "advnfc" / "__init__.py"
SENSOR = ROOT / "custom_components" / "advnfc" / "sensor.py"
DEPLOYMENT = ROOT / "08_Deployment" / "ADVNFC_HAOS_CONFIG_DEPLOYMENT_RUNBOOK.md"
HACS_DEPLOYMENT = ROOT / "08_Deployment" / "ADVNFC_HACS_DEPLOYMENT_RUNBOOK.md"
MANIFEST = ROOT / "custom_components" / "advnfc" / "manifest.json"


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _valid_reader_transition(old: str, new: str) -> bool:
    invalid = {"unknown", "unavailable"}
    return old not in invalid and new not in invalid and old != new


def _normalize_uid(uid: object) -> str:
    return str(uid).strip().upper()


def _contract_payload(tag_record: dict, trigger_entity: str) -> dict[str, str]:
    intent_id = str(tag_record.get("action", {}).get("intent_id", "")).strip().lower()
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
    assert "action: advnfc.find_tag_record" in source


def test_integration_activation_is_configuration_owned_not_script_owned():
    package = yaml.safe_load(_text(SCRIPTS))
    assert "advnfc" not in package
    deployment = _text(DEPLOYMENT)
    assert "/config/configuration.yaml" in deployment
    assert "`advnfc:`" in deployment


def test_capability_state_uses_registered_sensor_platform():
    integration = _text(INTEGRATION)
    sensor = _text(SENSOR)
    assert "hass.states.async_set" not in integration
    assert "Platform.SENSOR" in integration
    assert "discovery.async_load_platform" in integration
    assert "class AdvNFCTagMappingSensor(SensorEntity)" in sensor
    assert '_attr_unique_id = "advnfc_tag_mapping"' in sensor
    assert "async_add_entities([AdvNFCTagMappingSensor(store)])" in sensor


def test_capability_sensor_updates_after_successful_mapping_activation():
    integration = _text(INTEGRATION)
    sensor = _text(SENSOR)
    assert "async_dispatcher_send(hass, SIGNAL_TAG_MAPPING_UPDATED)" in integration
    assert "async_dispatcher_connect(" in sensor
    assert "self.async_write_ha_state" in sensor
    assert '"revision": snapshot.revision' in sensor


def test_administration_interface_has_distinct_minor_version():
    manifest = json.loads(_text(MANIFEST))
    assert manifest["version"] == "1.2.0"
    assert "`1.2.0`" in _text(HACS_DEPLOYMENT)


def test_tag_mapping_preserves_existing_phase_zero_records():
    source = _text(MAPPING)
    for intent_id in (
        "classic_fm", "lbc_news", "gold_radio", "bbc_radio_2",
        "smooth_radio", "lbc_radio", "news_briefing", "morning_routine",
    ):
        assert f"intent_id: {intent_id}" in source


def test_missing_tag_record_stops_before_astv_invocation():
    source = _text(SCRIPTS)
    gateway = source[source.index("  advnfc_uid_gateway:"):]
    missing_check = gateway.index("title: No Tag Record Found")
    selector_call = gateway.index("action: script.advnfc_select_tag_action")
    assert missing_check < selector_call
    assert "stop: No tag record found" in source
    assert "error: false" in source


def test_uid_gateway_does_not_repeat_typed_action_validation():
    source = _text(SCRIPTS)
    gateway = source[source.index("  advnfc_uid_gateway:"):]
    assert "title: Invalid Tag Record" not in gateway
    assert "stop: Invalid tag record" not in gateway
    assert "action: script.advnfc_select_tag_action" in gateway


def test_select_tag_action_uses_established_choose_structure():
    source = _text(SCRIPTS)
    selector_start = source.index("  advnfc_select_tag_action:")
    selector_end = source.index("  advnfc_uid_gateway:")
    selector = source[selector_start:selector_end]
    assert "alias: Choose Tag Action based on action_type" in selector
    assert "choose:" in selector
    assert "alias: ASTV Intent" in selector
    assert "value_template: '{{ action_type == ''astv_intent'' }}'" in selector
    assert "default:" in selector
    assert "stop: Unsupported tag action" in selector


def test_contract_payload_preserves_intent_override_and_trigger_entity():
    payload = _contract_payload(
        {"action": {"intent_id": " Classic_FM "}, "area_override": " kitchen "},
        "sensor.pi_nfc_02_last_uid",
    )
    assert payload == {
        "intent_id": "classic_fm",
        "input_area_override": "kitchen",
        "trigger_entity": "sensor.pi_nfc_02_last_uid",
    }


def test_contract_payload_allows_blank_area_override():
    payload = _contract_payload(
        {"action": {"intent_id": "classic_fm"}},
        "sensor.pi_nfc_99_last_uid",
    )
    assert payload["input_area_override"] == ""


def test_invalid_record_model_rejects_blank_intent_id():
    for record in ({}, {"action": {}}, {"action": {"intent_id": "   "}}):
        try:
            _contract_payload(record, "sensor.pi_nfc_02_last_uid")
        except ValueError:
            pass
        else:
            raise AssertionError("blank intent_id must be rejected")


def test_select_tag_action_uses_exact_astv_contract_without_uid():
    package = yaml.safe_load(_text(SCRIPTS))
    selector = package["script"]["advnfc_select_tag_action"]
    choose_action = selector["sequence"][1]["choose"][0]["sequence"][0]
    assert choose_action["action"] == "script.astv_intent_gateway"
    assert set(choose_action["data"]) == {
        "intent_id",
        "input_area_override",
        "trigger_entity",
    }


def test_advnfc_lookup_owns_mapping_and_astv_only_receives_canonical_invocation():
    source = _text(SCRIPTS)
    assert "action: advnfc.find_tag_record" in source
    assert "action: script.advnfc_find_tag_record" in source
    assert "action: script.advnfc_select_tag_action" in source
    assert "action: script.astv_intent_gateway" in source
    assert "script.astv_find_tag_record" not in source
