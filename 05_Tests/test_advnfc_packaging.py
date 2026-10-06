from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
RPI_SOURCE = ROOT / "04_Implementation" / "rpi_os" / "source"
READER_AGENT_PATH = RPI_SOURCE / "opt" / "advnfc" / "reader_agent" / "advnfc_reader_agent.sh"
READER_AGENT = READER_AGENT_PATH.read_text()
PACKAGING = ROOT / "04_Implementation" / "rpi_os" / "packaging" / "deb"
BUILD = (PACKAGING / "build_deb.sh").read_text()
CHECK_PATH = RPI_SOURCE / "usr" / "local" / "sbin" / "advnfc-reader-agent-check"
CHECK = CHECK_PATH.read_text()
INIT = (RPI_SOURCE / "usr" / "local" / "sbin" / "advnfc-reader-agent-init").read_text()
PROFILE = (RPI_SOURCE / "usr" / "local" / "sbin" / "advnfc-profile").read_text()
SERVICE = (RPI_SOURCE / "lib" / "systemd" / "system" / "advnfc-reader-agent.service").read_text()
UDEV_RULE = (RPI_SOURCE / "lib" / "udev" / "rules.d" / "99-advnfc-acr122u.rules").read_text()


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
    assert 'if [[ ! -e "$target" ]]' in INIT
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


def test_package_installs_late_final_acr122u_access_rule():
    assert "99-advnfc-acr122u.rules" in BUILD
    assert "70-advnfc-acr122u.rules" not in BUILD
    assert 'ATTR{idVendor}=="072f"' in UDEV_RULE
    assert 'ATTR{idProduct}=="2200"' in UDEV_RULE
    assert 'MODE:="0660"' in UDEV_RULE
    assert 'GROUP:="advnfc"' in UDEV_RULE


def test_build_fails_closed_without_exact_source_identity_and_writes_digest():
    assert "40-character commit" in BUILD
    assert 'sha256sum "$OUT" >"$OUT.sha256"' in BUILD


def test_readiness_check_validates_profile_and_reader_stack():
    assert "advnfc-profile validate" in CHECK
    assert "lsusb -d 072f:2200" in CHECK
    assert "runuser -u advnfc -- timeout 8 nfc-list" in CHECK
    assert "ACR122U USB device group is advnfc" in CHECK
    assert "mosquitto_pub" in CHECK


def test_readiness_allows_reader_to_settle_after_service_stop():
    stop = 'systemctl stop "$service"'
    probe = 'runuser -u advnfc -- timeout 8 nfc-list'
    assert stop in CHECK
    assert "sleep 3" in CHECK
    assert CHECK.index(stop) < CHECK.index("sleep 3") < CHECK.index(probe)


def _reader_output_ok(output: str, rc: int = 0) -> bool:
    command = (
        f'source "{CHECK_PATH}"; '
        'reader_output_ok "$1" "$2"'
    )
    result = subprocess.run(
        ["bash", "-c", command, "bash", str(rc), output],
        cwd=ROOT,
        check=False,
    )
    return result.returncode == 0


def test_readiness_accepts_clean_reader_open():
    assert _reader_output_ok(
        "nfc-list uses libnfc 1.8.0\n"
        "NFC device: ACS / ACR122U PICC Interface opened\n"
        "0 ISO14443A passive target(s) found:\n"
    )


def test_readiness_rejects_usb_permission_error_even_when_device_text_present():
    assert not _reader_output_ok(
        "nfc-list uses libnfc 1.8.0\n"
        "NFC device: ACS / ACR122U PICC Interface opened\n"
        "error   libnfc.driver.acr122_usb Unable to claim USB interface (Operation not permitted)\n"
        "nfc-list: ERROR: Unable to open NFC device: acr122_usb:001:004\n"
    )


def test_readiness_rejects_busy_reader_error():
    assert not _reader_output_ok(
        "NFC device: ACS / ACR122U PICC Interface opened\n"
        "error libnfc.driver.acr122_usb Unable to write to USB (Device or resource busy)\n"
    )


def test_profile_switch_has_validation_and_rollback():
    assert "validate_profile(name, require_secret=True)" in PROFILE
    assert "Activation failed" in PROFILE
    assert "Restored previous profile" in PROFILE
    assert "atomic_select(previous)" in PROFILE


def test_fresh_install_does_not_start_unconfigured_service():
    assert "Fresh installs do not start the service" in BUILD


def test_reader_agent_preserves_complete_nfcid1():
    assert 'for(i=3;i<=NF;i++) printf toupper($i)' in READER_AGENT
    sample = "       UID (NFCID1): 04  fd  26  37  c8  2a  81  \n"
    result = subprocess.run(
        ["awk", r"/UID \(NFCID1\):/{for(i=3;i<=NF;i++) printf toupper($i)}"],
        input=sample,
        text=True,
        capture_output=True,
        check=True,
    )
    assert result.stdout == "04FD2637C82A81"


def test_legacy_source_tree_is_removed():
    assert not (ROOT / "04_Source").exists()
