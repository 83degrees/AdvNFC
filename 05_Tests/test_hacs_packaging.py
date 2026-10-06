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
    assert manifest["version"] == "1.0.1"


def test_hacs_root_is_sole_integration_source_and_pointer_is_nonduplicating() -> None:
    assert sorted(path.name for path in (ROOT / "custom_components").iterdir()) == [
        "advnfc"
    ]
    assert sorted(path.name for path in POINTER.iterdir()) == ["README.md"]
    pointer = (POINTER / "README.md").read_text(encoding="utf-8")
    assert "custom_components/advnfc/**" in pointer
    assert not (ROOT / "04_Source").exists()
