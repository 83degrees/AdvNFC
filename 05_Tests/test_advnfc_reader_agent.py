from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "04_Source" / "reader_agent" / "advnfc_reader_agent.sh"
SERVICE = ROOT / "04_Source" / "reader_agent" / "systemd" / "advnfc-reader-agent.service"
PROFILE_TOOL = ROOT / "04_Source" / "reader_agent" / "packaging" / "advnfc-profile"

script = SCRIPT.read_text()
service = SERVICE.read_text()
profile_tool = PROFILE_TOOL.read_text()


def test_uid_extraction_matches_captured_runtime():
    assert "nfc-list 2>/dev/null" in script
    assert "UID \\(NFCID1\\)" in script
    assert "printf toupper($i)" in script


def test_reader_identity_defaults_to_short_hostname():
    assert 'READER="${READER_OVERRIDE:-$(hostname -s)}"' in script


def test_captured_timing_and_reset_defaults_are_preserved():
    assert 'POLL_S="${POLL_S:-0.20}"' in script
    assert 'DEBOUNCE_S="${DEBOUNCE_S:-0.80}"' in script
    assert 'EMPTY_RESET_LOOPS="${EMPTY_RESET_LOOPS:-8}"' in script
    assert 'if [[ "$uid" != "$prev" ]]' in script
    assert "if (( empty_count >= EMPTY_RESET_LOOPS ))" in script


def test_runtime_config_comes_from_active_profile():
    assert "advnfc-profile runtime-shell" in script
    assert "ha-starburst.little-dory.ts.net" not in script
    assert 'MQTT_TOPIC="${MQTT_TOPIC_PATTERN//' in script
    assert '-t "$MQTT_TOPIC" -r' in script


def test_service_validates_profile_before_start():
    assert "ConditionPathExists=/etc/advnfc/active-profile.yaml" in service
    assert "ExecStartPre=/usr/local/sbin/advnfc-profile validate" in service
    assert "EnvironmentFile=" not in service


def test_profile_tool_keeps_secret_out_of_status():
    assert "Credential configured:" in profile_tool
    assert "MQTT password:" not in profile_tool


def test_no_astv_or_tag_mapping_logic_is_on_reader_agent():
    lowered = script.lower()
    assert "astv" not in lowered
    assert "intent_id" not in lowered
    assert "tag_mapping" not in lowered
