#!/usr/bin/env python3
# **Version:** v1.0.0
# **Status:** Approved
# **Approval tag:** `central-gov-checks-v1.0.0`
# **Approval date:** 2026-09-27

"""Central Governance pull-request checks."""

import argparse
import pathlib
import sys

RUNTIME_ROOT = "04_Source"
REQUIRED_RUNTIME_BASE = "beta"
PROMOTION_HEAD = "beta"
PROMOTION_BASE = "main"


def is_runtime_path(path):
    normalized = pathlib.PurePosixPath(path).as_posix().lstrip("./")
    return normalized == RUNTIME_ROOT or normalized.startswith(f"{RUNTIME_ROOT}/")


def evaluate_wf01_route(head_branch, base_branch, changed_files, beta_exists):
    runtime_files = [path for path in changed_files if is_runtime_path(path)]
    if not runtime_files:
        return True, "No runtime implementation changed; WF-01 beta routing is not required."
    if not beta_exists:
        return False, "Runtime change detected but the required persistent beta branch does not exist."
    if head_branch == PROMOTION_HEAD and base_branch == PROMOTION_BASE:
        return True, "Runtime change is a governed beta-to-main G6 promotion."
    if base_branch != REQUIRED_RUNTIME_BASE:
        return False, f"Runtime change detected; PR must target '{REQUIRED_RUNTIME_BASE}', not '{base_branch}'."
    return True, "Runtime change targets the required persistent beta branch."


def parse_bool(value):
    normalized = value.strip().lower()
    if normalized in {"true", "1", "yes"}:
        return True
    if normalized in {"false", "0", "no"}:
        return False
    raise argparse.ArgumentTypeError("value must be true or false")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--head", required=True)
    parser.add_argument("--base", required=True)
    parser.add_argument("--beta-exists", required=True, type=parse_bool)
    parser.add_argument("--changed-files-file", required=True)
    args = parser.parse_args(argv)

    changed_files = [
        line.strip()
        for line in pathlib.Path(args.changed_files_file).read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    allowed, reason = evaluate_wf01_route(
        args.head,
        args.base,
        changed_files,
        args.beta_exists,
    )
    print(f"{'PASS' if allowed else 'FAIL'}: {args.repository}: WF-01 routing: {reason}")
    return 0 if allowed else 1


if __name__ == "__main__":
    sys.exit(main())
