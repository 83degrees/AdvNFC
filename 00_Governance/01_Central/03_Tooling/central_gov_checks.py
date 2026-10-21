#!/usr/bin/env python3
# **Version:** v1.4.0
# **Status:** Approved
# **Approval tag:** `central-gov-checks-v1.4.0`
# **Approval date:** 2026-10-21

"""Central Governance pull-request checks."""

import argparse
import pathlib
import re
import sys

CANONICAL_IMPLEMENTATION_ROOT = "04_Implementation"
LEGACY_IMPLEMENTATION_ROOT = "04_Source"
HACS_INTEGRATION_ROOT = "custom_components"
RUNTIME_ROOTS = {
    CANONICAL_IMPLEMENTATION_ROOT,
    LEGACY_IMPLEMENTATION_ROOT,
    HACS_INTEGRATION_ROOT,
}
HOME_ASSISTANT_APP_ROOTS = {
    "04_Implementation/haos/source/apps",
    LEGACY_IMPLEMENTATION_ROOT,
}
REQUIRED_RUNTIME_BASE = "beta"
PROMOTION_BASE = "main"
HOME_ASSISTANT_REPOSITORY_MANIFEST = "repository.yaml"
HOME_ASSISTANT_CONFIG_SUFFIXES = {".json", ".yaml", ".yml"}


def is_under(path, root):
    normalized = pathlib.PurePosixPath(path).as_posix().lstrip("./")
    return normalized == root or normalized.startswith(f"{root}/")


def is_runtime_path(path):
    return any(is_under(path, root) for root in RUNTIME_ROOTS)


def is_home_assistant_app_path(path):
    return any(is_under(path, root) for root in HOME_ASSISTANT_APP_ROOTS)


def is_commit_sha(value):
    return bool(re.fullmatch(r"[0-9a-fA-F]{40}", value or ""))


def evaluate_wf01_route(
    head_branch,
    base_branch,
    changed_files,
    beta_exists,
    repository="",
    head_repository="",
    head_sha="",
    beta_sha="",
):
    runtime_files = [path for path in changed_files if is_runtime_path(path)]
    if not runtime_files:
        return True, "No runtime implementation changed; WF-01 beta routing is not required."
    if not beta_exists:
        return False, "Runtime change detected but the required persistent beta branch does not exist."
    if base_branch == PROMOTION_BASE:
        if not repository or head_repository != repository:
            return False, (
                "Runtime promotion to main must originate from the same repository as the "
                "trusted persistent beta ref."
            )
        if not is_commit_sha(head_sha) or not is_commit_sha(beta_sha):
            return False, (
                "Runtime promotion to main requires valid immutable candidate HEAD and trusted "
                "persistent beta commit identities."
            )
        if head_sha.lower() != beta_sha.lower():
            return False, (
                "Runtime promotion candidate HEAD does not exactly match the trusted persistent "
                "beta commit."
            )
        return True, (
            "Runtime change is a mechanically verified beta-to-main G6 promotion candidate; "
            "separate human G5/G6 authority remains required."
        )
    if base_branch != REQUIRED_RUNTIME_BASE:
        return False, f"Runtime change detected; PR must target '{REQUIRED_RUNTIME_BASE}', not '{base_branch}'."
    return True, "Runtime change targets the required persistent beta branch."


def find_home_assistant_app_configs(repository_root):
    repository_root = pathlib.Path(repository_root)
    repository_files = [
        candidate.relative_to(repository_root).as_posix()
        for candidate in repository_root.rglob("*")
        if candidate.is_file()
    ]
    return find_home_assistant_app_configs_in_paths(repository_files)


def find_home_assistant_app_configs_in_paths(repository_files):
    configs = []
    for path in repository_files:
        candidate = pathlib.PurePosixPath(path)
        if not candidate.name.startswith("config."):
            continue
        if candidate.suffix not in HOME_ASSISTANT_CONFIG_SUFFIXES:
            continue
        if any(part.startswith(".") or part == "rootfs" for part in candidate.parts):
            continue
        configs.append(candidate.as_posix())
    return sorted(configs)


def evaluate_home_assistant_app_layout(repository_root):
    repository_root = pathlib.Path(repository_root)
    repository_files = [
        candidate.relative_to(repository_root).as_posix()
        for candidate in repository_root.rglob("*")
        if candidate.is_file()
    ]
    return evaluate_home_assistant_app_layout_paths(repository_files)


def evaluate_home_assistant_app_layout_paths(repository_files):
    if HOME_ASSISTANT_REPOSITORY_MANIFEST not in repository_files:
        return True, "No root repository.yaml; Home Assistant App layout check is not applicable."

    configs = find_home_assistant_app_configs_in_paths(repository_files)
    if not configs:
        return False, "Root repository.yaml exists but no recursively discoverable App config was found."

    noncanonical = [path for path in configs if not is_home_assistant_app_path(path)]
    if noncanonical:
        return False, (
            "Root repository.yaml exists but App config must be under canonical "
            "'04_Implementation/haos/source/apps/**' or transitionally supported "
            "'04_Source/**': "
            + ", ".join(noncanonical)
        )

    return True, (
        "Root repository.yaml is metadata and all recursively discoverable App config is under "
        "the canonical or transitionally supported App source path."
    )


def parse_bool(value):
    normalized = value.strip().lower()
    if normalized in {"true", "1", "yes"}:
        return True
    if normalized in {"false", "0", "no"}:
        return False
    raise argparse.ArgumentTypeError("value must be true or false")


def read_changed_files(path):
    data = pathlib.Path(path).read_bytes()
    if b"\0" in data:
        raw_paths = data.split(b"\0")
        return [path.decode("utf-8", errors="surrogateescape") for path in raw_paths if path]
    return [
        line.strip()
        for line in data.decode("utf-8", errors="surrogateescape").splitlines()
        if line.strip()
    ]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--head", required=True)
    parser.add_argument("--head-repository", default="")
    parser.add_argument("--head-sha", default="")
    parser.add_argument("--base", required=True)
    parser.add_argument("--beta-exists", required=True, type=parse_bool)
    parser.add_argument("--beta-sha", default="")
    parser.add_argument("--changed-files-file", required=True)
    parser.add_argument("--repository-files-file")
    parser.add_argument("--repository-root", default=".")
    args = parser.parse_args(argv)

    changed_files = read_changed_files(args.changed_files_file)
    allowed, reason = evaluate_wf01_route(
        args.head,
        args.base,
        changed_files,
        args.beta_exists,
        repository=args.repository,
        head_repository=args.head_repository,
        head_sha=args.head_sha,
        beta_sha=args.beta_sha,
    )
    print(f"{'PASS' if allowed else 'FAIL'}: {args.repository}: WF-01 routing: {reason}")
    if args.repository_files_file:
        repository_files = read_changed_files(args.repository_files_file)
        layout_allowed, layout_reason = evaluate_home_assistant_app_layout_paths(
            repository_files
        )
    else:
        layout_allowed, layout_reason = evaluate_home_assistant_app_layout(
            args.repository_root
        )
    print(
        f"{'PASS' if layout_allowed else 'FAIL'}: {args.repository}: "
        f"Home Assistant App layout: {layout_reason}"
    )
    return 0 if allowed and layout_allowed else 1


if __name__ == "__main__":
    sys.exit(main())
