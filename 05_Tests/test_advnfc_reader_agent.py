from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "04_Source" / "reader_agent" / "advnfc_reader_agent.sh"
SERVICE = ROOT / "04_Source" / "reader_agent" / "systemd" / "advnfc-reader-agent.service"
ENV_EXAMPLE = ROOT / "04_Source" / "reader_agent" / "reader-agent.env.example"

script = SCRIPT.read_text()
service = SERVICE.read_text()
env_example = ENV_EXAMPLE.read_text()


def test_uid_extraction_matches_captured_runtime():
    assert "nfc-list 2>/dev/null" in script
    assert "UID \\(NFCID1\\)" in script
    assert "printf toupper($i)" in script


def test_reader_identity_defaults_to_short_hostname():
    assert 'READER="${READER:-$(hostname -s)}"' in script


def test_captured_timing_and_reset_defaults_are_preserved():
    assert 'POLL_S="${POLL_S:-0.20}"' in script
    assert 'DEBOUNCE_S="${DEBOUNCE_S:-0.80}"' in script
    assert 'EMPTY_RESET_LOOPS="${EMPTY_RESET_LOOPS:-8}"' in script
    assert 'if [[ "$uid" != "$prev" ]]' in script
    assert 'if (( empty_count >= EMPTY_RESET_LOOPS ))' in script
    assert 'prev=""' in script


def test_retained_last_uid_is_the_only_reader_output():
    assert script.count("/usr/bin/mosquitto_pub") == 1
    assert '-t "assistive/nfc/$READER/last_uid" -r' in script
    assert "assistive/nfc/event" not in script
    assert "WEBHOOK_ID" not in script
    assert "WEBHOOK_URL" not in script
    assert "curl " not in script


def test_retained_payload_is_raw_uid():
    assert '-m "$uid"' in script


def test_mqtt_password_is_not_embedded_in_source():
    assert "83degrees" not in script
    assert "83degrees" not in service
    assert "83degrees" not in env_example
    assert "MQTT_PASS must be supplied through the deployment environment" in script
    assert "MQTT_PASS=REPLACE_WITH_DEPLOYMENT_SECRET" in env_example


def test_legacy_webhook_configuration_is_removed():
    assert "HA_BASE_URL" not in env_example
    assert "WEBHOOK_ID" not in env_example
    assert "webhook" not in service.lower()


def test_systemd_uses_external_environment_and_governed_target_path():
    assert "EnvironmentFile=/etc/advnfc/reader-agent.env" in service
    assert "ExecStart=/opt/advnfc/reader_agent/advnfc_reader_agent.sh" in service
    assert "User=advnfc" in service
    assert "Group=advnfc" in service
    assert "ConditionPathExists=/etc/advnfc/reader-agent.env" in service
    assert "Restart=always" in service
    assert "RestartSec=1s" in service


def test_no_astv_or_tag_mapping_logic_is_on_reader_agent():
    lowered = script.lower()
    assert "astv" not in lowered
    assert "intent_id" not in lowered
    assert "tag_mapping" not in lowered
