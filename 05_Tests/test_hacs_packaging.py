"""Repository-layout checks for the governed AdvNFC HACS unit."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).parents[1]
INTEGRATION = ROOT / "custom_components" / "advnfc"
POINTER = (
    ROOT
    / "04_Implementation"
    / "haos"
    / "source"
    / "config"
    / "custom_components"
    / "advnfc"
)
VALIDATOR = (
    ROOT
    / "04_Implementation"
    / "haos"
    / "packaging"
    / "hacs"
    / "hacs_release.py"
)


def test_hacs_repository_metadata_and_manifest_are_valid() -> None:
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), "--root", str(ROOT), "validate"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    manifest = json.loads((INTEGRATION / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["domain"] == "advnfc"
    assert manifest["version"] == "1.1.0"


def test_hacs_root_is_sole_integration_source_and_pointer_is_nonduplicating() -> None:
    assert sorted(path.name for path in (ROOT / "custom_components").iterdir()) == [
        "advnfc"
    ]
    assert sorted(path.name for path in POINTER.iterdir()) == ["README.md"]
    pointer = (POINTER / "README.md").read_text(encoding="utf-8")
    assert "custom_components/advnfc/**" in pointer
    assert not (ROOT / "04_Source").exists()


def test_reader_agent_residue_is_absent_from_advnfc() -> None:
    rpi_root = ROOT / "04_Implementation" / "rpi_os"
    assert not rpi_root.exists() or not any(path.is_file() for path in rpi_root.rglob("*"))
    assert not (ROOT / ".github" / "workflows" / "reader-agent-package.yml").exists()
    assert not (ROOT / "08_Deployment" / "ADVNFC_READER_AGENT_DEB_DEPLOYMENT_RUNBOOK.md").exists()
    assert not (ROOT / "03_Contracts" / "ADVNFC_READER_EVENT_MQTT_INTERFACE.md").exists()
    for name in (
        "test_advnfc_packaging.py",
        "test_advnfc_profiles.py",
        "test_advnfc_reader_agent.py",
    ):
        assert not (ROOT / "05_Tests" / name).exists()
