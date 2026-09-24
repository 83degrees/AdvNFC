import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "04_Source" / "reader_agent" / "packaging" / "advnfc-profile"
STAR = ROOT / "04_Source" / "reader_agent" / "profiles" / "starburst.yaml"
TEST = ROOT / "04_Source" / "reader_agent" / "profiles" / "test.yaml"


def test_two_distinct_schema_v1_profiles_exist():
    profiles = [yaml.safe_load(STAR.read_text()), yaml.safe_load(TEST.read_text())]
    assert {p["name"] for p in profiles} == {"starburst", "test"}
    for profile in profiles:
        assert profile["schema_version"] == 1
        assert profile["mqtt"]["topic_pattern"] == "advnfc/{reader}/last_uid"
        assert "password" not in str(profile).lower()
        assert profile["mqtt"]["credential_ref"]


def test_profile_tool_exposes_expected_commands():
    result = subprocess.run([sys.executable, str(TOOL), "--help"], text=True, capture_output=True)
    assert result.returncode == 0
    for command in ("list", "status", "validate", "switch"):
        assert command in result.stdout


def test_profile_tool_has_no_environment_specific_agent_fallback():
    source = TOOL.read_text()
    assert "ha-starburst.little-dory.ts.net" not in source
    assert "assistive/nfc" not in source
