# ASTV-357 G4 Controlled Lifecycle Abort Evidence

**Recorded:** 2026-10-22  
**Authority:** Human-approved controlled disposable-staging lifecycle recorded in Linear ASTV-357  
**Outcome:** **ABORTED BEFORE FIRST MUTATION — HUMAN REVIEW REQUIRED**

## Result and stop boundary

The controlled lifecycle was dispatched once in the proven disposable staging profile. The runner reproduced the accepted Home Assistant and AdvNFC identities, passed isolation and baseline preflight, and then attempted the required non-mutating reserved-record validation. Home Assistant rejected that validation request at its service-call boundary. The runner stopped immediately, made no retry, invoked no lifecycle mutation, preserved partial evidence, and disposed the container.

No create/Save, update, delete, reload/Activate, reader, MQTT, or gateway-dispatch operation occurred. Production was not modified. PR #71 was not merged.

## Immutable run evidence

| Item | Evidence |
|---|---|
| Pull request | [AdvNFC PR #71](https://github.com/83degrees/AdvNFC/pull/71) — draft, unmerged |
| Runner head | `d8e682e1f2150ac7d9f0b198e0c4c236055cd6b8` |
| Lifecycle run | [GitHub Actions run 39759753699](https://github.com/83degrees/AdvNFC/actions/runs/39759753699) — failed closed |
| Evidence artifact | `astv-357-disposable-staging-evidence-39759753699` |
| Artifact digest | `sha256:915ff51f0aec559258f85360dbbcb49c5d4f8cdab9047d8c284be6895830d9ee` |
| Artifact expiry | 2026-11-21 |
| Operator | GitHub actor `83degrees` |
| Home Assistant | `2026.9.4`, image digest `sha256:3e6710a7ab2a61311d9d899b719f6c3657791c63e8f4942cec4ebc42401d6b76` |
| AdvNFC | `v1.6.0-beta.288e3df` / `288e3df5187a5c37e44feda202cc570f9eb539e0` |

The artifact contains `stage-evidence.json`, `lifecycle-evidence.json`, exact image/tag/permission/isolation evidence, Home Assistant logs, and disposal proof. A scan found no token, password, API key, production endpoint, MQTT topic, or `ha-starburst` identity.

## Preflight evidence

Before the rejected call, staging reported:

- private `/config` profile `0:0 / 0700` with successful private write proof;
- container network mode `none`, published ports `{}`, dropped capabilities `["ALL"]`, and `no-new-privileges`;
- Home Assistant `RUNNING` with authenticated local WebSocket access;
- AdvNFC interface v3/schema 1, active/persisted count `12/12`;
- active and persisted revision `v1-986df5539173dad03cf231dd5fd094dbdc6024d1786ad721b18b84fe332c4173`;
- `activation_required=false`, no activation error;
- exact 12-record active and persisted logical baseline;
- persisted baseline file SHA-256 `9ae20b4b4df8b7d711cc031d8c40d7edc4dbeec1f1cf3d1d637d9dfad480acde`;
- reserved UID `A3570001` absent;
- eight-intent read-only ASTV double available;
- gateway spy absent.

## Abort event

Exactly one non-mutating call was attempted:

```text
advnfc.validate_tag_mapping_record
```

Its request contained the authorized schema-v1 staging record under the documented `mapping` field. Home Assistant returned:

```text
code: invalid_format
message: not a valid option at 'mapping'
```

The partial evidence reports:

- `outcome: aborted`;
- `automatic_retries: 0`;
- `lifecycle_calls_executed: []`;
- operation `validate_reserved_record`, `mutating: false`, `attempts: 1`;
- `gateway_spy_present_at_completion: false`.

Because the failure occurred before `create_tag_mapping`, there was no uncertain write outcome and no synthetic record to reverse.

## Root cause

The accepted AdvNFC integration registers `validate_tag_mapping`, `validate_tag_mapping_record`, `create_tag_mapping`, `update_tag_mapping`, and `delete_tag_mapping` using Home Assistant's `async_register_admin_service` without passing a service-data schema. In Home Assistant 2026.9.4 that helper's default is an empty schema with extra fields prevented. Consequently, the documented `mapping`, `candidate`, `expected_revision`, and `uid` payload fields are rejected before the AdvNFC handler runs.

This is consistent with the observed boundary error and explains why the provider-store unit tests pass while the deployed Home Assistant service boundary cannot execute the parameterized administration operations. Changing JSON shape cannot solve an empty-schema rejection. `reload_tag_mapping` has no input fields, but the authorized sequence cannot lawfully skip validation/create/update/delete to reach it.

Relevant review surfaces:

- `custom_components/advnfc/__init__.py` — parameterized admin services registered without schemas;
- `custom_components/advnfc/services.yaml` — documents fields for UI presentation but does not supply runtime registration schemas;
- Home Assistant 2026.9.4 `homeassistant/helpers/service.py` — `async_register_admin_service` defaults to an empty `PREVENT_EXTRA` schema.

## Disposal and production preservation

The unconditional cleanup removed container `da4aa1d8a69e3aff788aefb038031c664ddba2668f0ea9504312afb3c68b21c8`; retained evidence states `container_removed=true`. The disposable runner destroyed all private stage state.

A fresh post-disposal production read reported:

- state `active`, active/persisted count `12/12`;
- active and persisted revision `v1-986df5539173dad03cf231dd5fd094dbdc6024d1786ad721b18b84fe332c4173`;
- `activation_required=false`, `last_activation_error=null`;
- the original 12 UIDs present and `A3570001` absent.

This matches the pre-dispatch production baseline exactly.

## Required next gate

Do not retry the lifecycle and do not bypass the Home Assistant administration boundary. The blocker requires a separately governed integration fix that supplies explicit service-data schemas, boundary-level regression tests, a reviewed new immutable AdvNFC candidate identity, and a new human decision on staging revalidation/lifecycle execution. The existing accepted tag must remain immutable. Production deployment and PR #71 merge remain unauthorised.
