# ASTV-360 Integration Schema Fix Evidence

## Authority and boundary

ASTV-360 carries G0 human approval for a discrete AdvNFC integration defect
fix through G2 human review. The approved route is WF-01 from persistent
`beta`, with the issue pull request targeting `beta`. Merge, Beta tag creation,
release, deployment, staging retry, activation/reload, production mutation,
and work on ASTV-357 pull request #71 are outside this authority.

The issue branch was created from remote `beta` commit
`5f32c5285f8dd4a2b915afced59750a8004557f6`. The previously accepted tag
`v1.6.0-beta.288e3df` is not moved, replaced, or reused.

## Defect and corrective design

Home Assistant Core 2026.9.4 defines `async_register_admin_service` with a
default `vol.Schema({}, extra=vol.PREVENT_EXTRA)`. AdvNFC supplied no schema
for its parameterised manage services, so Home Assistant rejected documented
payload fields before authorization or the provider handler.

The corrective implementation supplies a distinct closed service-data schema
for each parameterised manage operation:

| Service | Required outer fields |
| --- | --- |
| `validate_tag_mapping` | object `candidate` |
| `validate_tag_mapping_record` | object `mapping` |
| `create_tag_mapping` | string `expected_revision`, object `mapping` |
| `update_tag_mapping` | string `expected_revision`, object `mapping` |
| `delete_tag_mapping` | string `expected_revision`, string `uid` |

All schemas prevent unexpected outer fields. They deliberately validate only
the transport container types and pass accepted objects intact to the existing
closed schema-v1 provider canonicalisation and validation. Admin-only
authorization, response-only calls, revisions, mutation/activation separation,
failure envelopes, and interface v3 remain unchanged.

## Boundary-test obligations

`05_Tests/test_advnfc_ha_service_boundary.py` uses the real Home Assistant
2026.9.4 `HomeAssistant`, `ServiceRegistry`, and admin-service wrapper. It
proves:

- every documented payload crosses the registered Home Assistant boundary;
- response-only registration remains intact;
- missing, malformed, and unexpected outer fields fail before provider work;
- a non-administrator is denied before mutation;
- nested closed-schema failure remains an AdvNFC `invalid_candidate` envelope;
- validation, denial, and boundary failure do not modify persisted state; and
- accepted create/update/delete calls change only persisted state and do not
  activate it.

The exact CI dependency is `homeassistant==2026.9.4`. Its declared Python
minimum requires the workflow to use Python 3.14.

## Compatibility and rollback

This is a compatible correction to the already documented candidate v3 input
contract. It adds no operation, field, action type, transport, bulk behavior,
or consumer-visible response change. The Project Profile declares only future
management consumers, so no existing supported consumer migration is needed.

Rollback before merge is branch/PR rework or closure. If a later authorised
Beta fails, rollback uses the exact previously installed immutable version
through HACS under separate authority. No tag, release, deployment, reload, or
runtime rollback is performed at G2.

## Verification record

Pre-push local results on 2026-10-22:

| Check | Result |
| --- | --- |
| Python syntax compilation for the changed integration and HA boundary test | passed |
| Python regressions excluding the Python-3.14-only HA 2026.9.4 boundary module | 70 passed, 6 subtests passed |
| Administration frontend syntax and Node test suite | 19 passed |
| Central Governance routing checker with base `beta` | passed WF-01 routing and repository layout checks |

The exact real-HA boundary module is intentionally not represented as a local
pass: the available local interpreter is Python 3.12, while Home Assistant
2026.9.4 requires Python 3.14.2 or later. The pull-request workflow now uses
Python 3.14 and installs the exact Home Assistant version; its result is
required in the G2 handoff. Exact head SHA and review PR identity are recorded
after the candidate is committed and pushed.
