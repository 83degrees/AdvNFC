from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGING = ROOT / "04_Source" / "reader_agent" / "packaging"
BUILD = (PACKAGING / "build_deb.sh").read_text()
CHECK = (PACKAGING / "advnfc-reader-agent-check").read_text()
INIT = (PACKAGING / "advnfc-reader-agent-init").read_text()
SERVICE = (ROOT / "04_Source" / "reader_agent" / "systemd" / "advnfc-reader-agent.service").read_text()


def test_package_declares_runtime_dependencies():
    for dep in ("adduser", "util-linux", "libnfc-bin", "mosquitto-clients", "usbutils", "udev", "systemd"):
        assert dep in BUILD


def test_package_keeps_node_config_external():
    assert "/etc/advnfc/reader-agent.env" not in BUILD
    assert "/usr/share/advnfc/reader-agent.env.example" in BUILD
    assert "already exists; leaving it unchanged" in INIT


def test_package_records_version_and_git_identity():
    assert "/opt/advnfc/reader_agent/VERSION" in BUILD
    assert "git_sha=" in BUILD
    assert "version=" in BUILD


def test_package_creates_dedicated_runtime_account():
    assert "adduser --system" in BUILD
    assert "User=advnfc" in SERVICE


def test_package_installs_acr122u_access_rule():
    assert 'ATTR{idVendor}=="072f"' in BUILD
    assert 'ATTR{idProduct}=="2200"' in BUILD
    assert 'GROUP="advnfc"' in BUILD


def test_readiness_check_covers_reader_stack():
    assert "lsusb -d 072f:2200" in CHECK
    assert "runuser -u advnfc -- timeout 8 nfc-list" in CHECK
    assert "mosquitto_pub" in CHECK
    assert "MQTT_PASS=REPLACE_WITH_DEPLOYMENT_SECRET" in CHECK


def test_fresh_install_does_not_start_unconfigured_service():
    assert "Fresh installs do not start the service" in BUILD
    assert "systemctl is-active --quiet advnfc-reader-agent.service" in BUILD


def test_remove_preserves_etc_advnfc():
    assert "rm -rf /etc/advnfc" not in BUILD
