# ASTV-355 Implementation Evidence

## Candidate scope

This evidence covers the repository candidate for the AdvNFC active-tag list
and full-page tag editor. It does not evidence Home Assistant deployment,
mapping mutation, activation, Beta operation, or end-to-end runtime acceptance.

The candidate:

- replaces the ASTV-354 read-only panel proof with the governed list/editor;
- retains the existing authenticated Home Assistant WebSocket/provider-v3
  boundary and HACS deployment route;
- preserves active-versus-persisted revision semantics and explicit activation;
- keeps schema v1 limited to required `label`, one `astv_intent` action, and
  optional `area_override`; and
- excludes Description, unassigned records, additional/multiple actions, bulk
  operations, and physical-reader capture.

## Local verification

Verified on the issue branch based on persistent `beta` commit
`0cd893d561e6d084be7408df562e385191a55062`:

| Check | Result |
| --- | --- |
| Frontend module syntax (`node --check`) | Passed |
| Frontend adapter/editor tests (`node --test`) | 16 passed |
| Full Python suite (`pytest -q`) | 68 passed, 6 subtests passed |
| Central Governance routing checker | Passed; WF-01 target is persistent `beta` |
| Git whitespace validation (`git diff --check`) | Passed |

The Python suite used the repository-declared dependency ranges and an explicit
workspace temporary directory because the sandbox-provided default temporary
directory was not writable. The initial environment-only temp-directory errors
were eliminated by that rerun; no product test failed.

## Remaining governed gates

G2 requires the pushed PR targeting `beta`, independently verified PR base,
and successful required checks on the exact review head. Human review must
accept the proposed UI and architecture state before validation or any Beta
preparation. No tag, HACS installation, Home Assistant restart, live mapping
operation, reload, merge, release, or stable promotion is authorised here.
