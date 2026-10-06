"""Validate AdvNFC's HACS layout and release after authorised promotion."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import subprocess
import sys


DOMAIN = "advnfc"
REPOSITORY = "83degrees/AdvNFC"
SEMVER = re.compile(r"[0-9]+\.[0-9]+\.[0-9]+")
TAG = re.compile(r"v[0-9]+\.[0-9]+\.[0-9]+(?:-beta\.[0-9a-f]{7,40})?")


class ReleaseError(RuntimeError):
    """Report a fail-closed validation or release error."""


def _run(
    *command: str,
    cwd: Path,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        check=check,
        capture_output=True,
        text=True,
    )


def _load_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ReleaseError(f"invalid JSON at {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ReleaseError(f"expected a JSON object at {path}")
    return value


def validate_layout(root: Path) -> str:
    """Validate the version-addressable HACS repository tree."""
    integrations_root = root / "custom_components"
    integrations = (
        sorted(path.name for path in integrations_root.iterdir() if path.is_dir())
        if integrations_root.is_dir()
        else []
    )
    if integrations != [DOMAIN]:
        raise ReleaseError("custom_components must contain exactly advnfc")

    hacs = _load_json(root / "hacs.json")
    if hacs.get("name") != "AdvNFC":
        raise ReleaseError("hacs.json must name AdvNFC")
    if hacs.get("render_readme") is not True:
        raise ReleaseError("hacs.json must render the repository README")
    if not (root / "README.md").is_file():
        raise ReleaseError("README.md is required when render_readme is enabled")

    manifest = _load_json(root / "custom_components" / DOMAIN / "manifest.json")
    required = {"domain", "name", "version", "codeowners"}
    missing = sorted(required.difference(manifest))
    if missing:
        raise ReleaseError(f"manifest.json is missing: {', '.join(missing)}")
    if manifest["domain"] != DOMAIN:
        raise ReleaseError("manifest domain does not identify AdvNFC")
    version = manifest["version"]
    if not isinstance(version, str) or not SEMVER.fullmatch(version):
        raise ReleaseError("manifest version must be stable X.Y.Z SemVer")
    return version


def _commit(root: Path, revision: str) -> str:
    try:
        return _run("git", "rev-parse", f"{revision}^{{commit}}", cwd=root).stdout.strip()
    except subprocess.CalledProcessError as exc:
        raise ReleaseError(f"cannot resolve Git revision {revision}") from exc


def _existing_tag(root: Path, tag: str) -> str | None:
    result = _run(
        "git",
        "rev-parse",
        "--verify",
        f"refs/tags/{tag}^{{commit}}",
        cwd=root,
        check=False,
    )
    return result.stdout.strip() if result.returncode == 0 else None


def _verify_remote_lightweight_tag(root: Path, tag: str, expected_sha: str) -> None:
    result = _run(
        "git",
        "ls-remote",
        "--exit-code",
        "--tags",
        "origin",
        f"refs/tags/{tag}",
        cwd=root,
        check=False,
    )
    fields = result.stdout.split()
    if result.returncode != 0 or len(fields) < 2 or fields[0] != expected_sha:
        raise ReleaseError(
            f"remote lightweight tag {tag} does not resolve to {expected_sha}"
        )


def release(
    root: Path,
    stable_sha: str,
    beta_tag: str,
    promotion_evidence: str | None,
) -> str:
    """Create an immutable stable tag and GitHub Release after validation."""
    version = validate_layout(root)
    stable_tag = f"v{version}"
    if not TAG.fullmatch(beta_tag) or not beta_tag.startswith(f"{stable_tag}-beta."):
        raise ReleaseError(f"Beta tag must use {stable_tag}-beta.<short-sha>")

    stable_sha = _commit(root, stable_sha)
    if _commit(root, "HEAD") != stable_sha:
        raise ReleaseError("checked-out HEAD does not equal the selected stable SHA")
    beta_sha = _commit(root, f"refs/tags/{beta_tag}")
    _verify_remote_lightweight_tag(root, beta_tag, beta_sha)
    if beta_sha != stable_sha and not promotion_evidence:
        raise ReleaseError(
            "promotion-equivalence evidence is required when Beta and stable SHAs differ"
        )

    existing = _existing_tag(root, stable_tag)
    if existing and existing != stable_sha:
        raise ReleaseError(
            f"existing stable tag {stable_tag} resolves to contradictory SHA {existing}"
        )
    if not existing:
        _run("git", "tag", stable_tag, stable_sha, cwd=root)
        _run("git", "push", "origin", f"refs/tags/{stable_tag}", cwd=root)

    _verify_remote_lightweight_tag(root, stable_tag, stable_sha)
    current_release = _run(
        "gh",
        "release",
        "view",
        stable_tag,
        "--repo",
        REPOSITORY,
        "--json",
        "tagName",
        cwd=root,
        check=False,
    )
    if current_release.returncode != 0:
        notes = (
            f"AdvNFC {stable_tag}\n\n"
            f"Beta identity: `{beta_tag}` / `{beta_sha}`\n\n"
            f"Stable identity: `{stable_sha}`"
        )
        if promotion_evidence:
            notes += f"\n\nPromotion-equivalence evidence: {promotion_evidence}"
        _run(
            "gh",
            "release",
            "create",
            stable_tag,
            "--repo",
            REPOSITORY,
            "--target",
            stable_sha,
            "--verify-tag",
            "--title",
            f"AdvNFC {stable_tag}",
            "--notes",
            notes,
            cwd=root,
        )
    return stable_tag


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    subcommands = parser.add_subparsers(dest="command", required=True)
    subcommands.add_parser("validate")
    release_parser = subcommands.add_parser("release")
    release_parser.add_argument("--stable-sha", required=True)
    release_parser.add_argument("--beta-tag", required=True)
    release_parser.add_argument("--promotion-evidence")
    return parser


def main() -> int:
    args = _parser().parse_args()
    root = args.root.resolve()
    try:
        if args.command == "validate":
            version = validate_layout(root)
            print(f"valid HACS repository metadata for AdvNFC {version}")
        else:
            stable_tag = release(
                root,
                args.stable_sha,
                args.beta_tag,
                args.promotion_evidence,
            )
            print(f"stable release {stable_tag} is present at {args.stable_sha}")
    except (ReleaseError, subprocess.CalledProcessError) as exc:
        print(f"HACS release failure: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
