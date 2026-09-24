from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGING = ROOT / "04_Source" / "reader_agent" / "packaging"
BUILD = (PACKAGING / "build_deb.sh").read_text()
CHECK = (PACKAGING / "advnfc-reader-agent-check").read_text()
INIT = (PACKAGING / "advnfc-reader-agent-init").read_text()
PROFILE = (PACKAGING / "advnfc-profile").read_text()
SERVICE = (ROOT / "04_Source" / "reader_agent" / "systemd" / "advnfc-reader-agent.service").read_text()


def test_package_is_architecture_independent():
    assert 'ARCH="all"' in BUILD
    assert "Architecture: $ARCH" in BUILD


def test_package_declares_runtime_dependencies():
    for dep in ("adduser", "util-linux", "libnfc-bin", "mosquitto-clients", "usbutils", "udev", "systemd", "python3", "python3-yaml"):
        assert dep in BUILD


def test_package_installs_profile_tool_and_examples():
    assert "/usr/local/sbin/advnfc-profile" in BUILD
    assert "/usr/share/advnfc/profiles" in BUILD
    assert "/usr/share/advnfc/secrets" in BUILD


def test_package_keeps_node_profiles_and_secrets_external():
    assert "if [[ ! -e \"$target\" ]]" in INIT
    assert "rm -rf /etc/advnfc" not in BUILD
    assert "/etc/advnfc/active-profile.yaml" not in BUILD


def test_package_records_version_and_git_identity():
    assert "/opt/advnfc/reader_agent/VERSION" in BUILD
    assert "git_sha=" in BUILD
    assert "version=" in BUILD


def test_package_creates_dedicated_runtime_account():
    assert "adduser --system" in BUILD
    assert "User=advnfc" in SERVICE
    assert "Group=advnfc" in SERVICE


def test_package_installs_acr122u_access_rule():
    assert 'ATTR{idVendor}=="072f"' in BUILD
    assert 'ATTR{idProduct}=="2200"' in BUILD
    assert 'GROUP="advnfc"' in BUILD


def test_readiness_check_validates_profile_and_reader_stack():
    assert "advnfc-profile validate" in CHECK
    assert "lsusb -d 072f:2200" in CHECK
    assert "runuser -u advnfc -- timeout 8 nfc-list" in CHECK
    assert "mosquitto_pub" in CHECK


def test_profile_switch_has_validation_and_rollback():
    assert "validate_profile(name, require_secret=True)" in PROFILE
    assert "Activation failed" in PROFILE
    assert "Restored previous profile" in PROFILE
    assert "atomic_select(previous)" in PROFILE


def test_fresh_install_does_not_start_unconfigured_service():
    assert "Fresh installs do not start the service" in BUILD
