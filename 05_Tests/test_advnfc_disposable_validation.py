"""Offline controls for the maintained disposable Home Assistant harness."""

from __future__ import annotations

import ast
from pathlib import Path
import re

import yaml


ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "06_Validation" / "Tools" / "advnfc_disposable_ha"
WORKFLOW = ROOT / ".github" / "workflows" / "advnfc-disposable-validation.yml"
OLD_TOOL = ROOT / "06_Validation" / "Staging" / "ASTV-357"


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_fixture_is_minimal_and_fully_synthetic() -> None:
    mapping = yaml.safe_load(text(TOOL / "config/AdvNFC/advnfc_tag_mapping.yaml"))

    assert mapping == {
        "tag_mapping_schema_version": 1,
        "tags": {
            "A3660001": {
                "label": "Synthetic validation record one",
                "action": {
                    "type": "astv_intent",
                    "intent_id": "validation_primary",
                },
            },
            "A3660002": {
                "label": "Synthetic validation record two",
                "action": {
                    "type": "astv_intent",
                    "intent_id": "validation_secondary",
                },
            },
        },
    }


def test_workflow_is_manual_non_mutating_and_immutably_pinned() -> None:
    source = text(WORKFLOW)
    workflow = yaml.load(source, Loader=yaml.BaseLoader)

    assert set(workflow["on"]) == {"workflow_dispatch"}
    options = workflow["on"]["workflow_dispatch"]["inputs"]["mode"]["options"]
    assert options == ["baseline_read_only", "schema_non_mutating"]
    assert workflow["permissions"] == {"contents": "read"}
    assert "execute_lifecycle.py" not in source
    assert "controlled_lifecycle" not in source
    assert "push:" not in source

    action_refs = re.findall(r"uses:\s+[^@\s]+@([0-9a-f]{40})", source)
    assert len(action_refs) == 2
    assert "ghcr.io/home-assistant/home-assistant@sha256:" in source
    assert re.search(r"home-assistant@sha256:[0-9a-f]{64}", source)


def test_schema_probe_preserves_astv360_non_mutating_boundaries() -> None:
    source = text(TOOL / "scripts/verify_admin_schemas.py")
    ast.parse(source)

    for service in (
        "validate_tag_mapping",
        "validate_tag_mapping_record",
        "create_tag_mapping",
        "update_tag_mapping",
        "delete_tag_mapping",
    ):
        assert f'"{service}"' in source
    assert "stale_revision" in source
    assert "invalid_format" in source
    assert "assert after == before" in source
    assert '"reload_or_activation_calls": 0' in source
    assert "ab94c2a40fc6e4fdac340a415b962e9d6696a7bc" in text(TOOL / "README.md")


def test_credentials_and_evidence_stay_outside_tool_source() -> None:
    workflow = text(WORKFLOW)
    baseline = text(TOOL / "scripts/verify_baseline.py")

    assert "secrets.token_urlsafe(32)" in workflow
    assert "! -name onboarding-password" in workflow
    assert 'Path("/evidence/baseline-evidence.json")' in baseline
    assert "PASSWORD_PATH.unlink(missing_ok=True)" in baseline
    assert "access_token" not in workflow


def test_issue_specific_staging_source_is_consolidated() -> None:
    assert TOOL.is_dir()
    assert not OLD_TOOL.exists()
    assert (TOOL / "scripts/execute_lifecycle.py").is_file()
