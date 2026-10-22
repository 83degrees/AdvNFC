# ASTV-357 G4 Disposable Staging Isolation Evidence

**Recorded:** 2026-10-22  
**Authority:** Latest human-approved private staging permission correction and one startup retry recorded in Linear ASTV-357  
**Outcome:** **PASS — RETURNED FOR HUMAN REVIEW BEFORE WRITE/ACTIVATION**

## Stop boundary

The single authorized startup retry completed. No AdvNFC create, Save, update, delete, reload, or Activate operation was called. No NFC reader, MQTT, production device, production automation, or gateway-dispatch operation was called. The evidence payload reports `lifecycle_calls_executed: []`.

The staging-only tuple remains absent and unexercised:

- UID: `A3570001`
- intent: `classic_fm`

## Immutable identity

| Item | Verified evidence |
|---|---|
| Pull request | [AdvNFC PR #71](https://github.com/83degrees/AdvNFC/pull/71) |
| Retry head | `1bc4eff66a2b0fc4c3e558fa4ea04793a077b8a0` |
| Single retry | [GitHub Actions run 39755947902](https://github.com/83degrees/AdvNFC/actions/runs/39755947902) — success |
| Evidence artifact | `astv-357-disposable-staging-evidence-39755947902` |
| Artifact digest | `sha256:9be7c11d490527ea702494fcb75b5d745371d34d49574d4ea0f960443808f1b7` |
| Artifact expiry | 2026-11-21 |
| Home Assistant | `2026.9.4`, state `RUNNING`, authenticated local WebSocket healthy |
| HA image digest | `sha256:3e6710a7ab2a61311d9d899b719f6c3657791c63e8f4942cec4ebc42401d6b76` |
| HA container image ID | `sha256:cd74b0e02cee84de9f53b0f8fc079c8979796b81a6b02e1ee0cd09f038703afd` |
| Accepted AdvNFC tag | `v1.6.0-beta.288e3df` |
| Accepted AdvNFC commit | `288e3df5187a5c37e44feda202cc570f9eb539e0` |
| Accepted component tree | `9dfda2538e4b509ac16ff2846c9f69e51c83c55b` |
| Stage name | `ASTV-357 Disposable Staging` |
| Stage area | `astv_357_staging_area` / `ASTV-357 staging area` |

## Narrow permission correction

The exact image declares no Docker `Config.User`. The direct Python entrypoint was therefore measured in two network-disabled, capability-dropped identity probes and returned UID `0`, GID `0`.

Only the runner-temporary private config tree was corrected:

| State | UID | GID | Mode |
|---|---:|---:|---:|
| Before | 1001 | 1001 | `0755` |
| After | 0 | 0 | `0700` |

No `chmod 777`, privileged container, security-control removal, production mount, or credential was used. A file created by the running restricted HA process at `/config/ASTV-357/private-config-write-proof` contained `private-stage-write-ok`, owner `0:0`, mode `0644`. This proves the permission correction without widening access to the private config root.

## Isolation proof

Runtime container inspection recorded:

- network mode `none`;
- published ports `{}`;
- dropped capabilities `["ALL"]`;
- security option `["no-new-privileges"]`;
- direct `python3 -m homeassistant --config /config` startup;
- private runner-temporary `/config` only;
- no production MQTT topic, reader/device endpoint, production credential, or production listener automation in the assembled configuration;
- no secret-like or production-endpoint material in the retained artifact;
- inert `astv_staging_sink.record_invocation` registered, external dispatch capability `false`, and gateway spy file absent.

The Home Assistant log's analytics/zeroconf error is the expected consequence of having no network interface. It did not affect local health or verification. The two staging-double `services.yaml` warnings concern service-description files; both services were registered programmatically and returned the verified responses below. There were no AdvNFC load or service errors.

## Read-only runtime verification

### AdvNFC staging baseline

- interface `advnfc.tag_mapping.administration`, version `3`, schema `1`;
- active count `12`, persisted count `12`;
- active and persisted revision `v1-986df5539173dad03cf231dd5fd094dbdc6024d1786ad721b18b84fe332c4173`;
- state `active`, `activation_required=false`, `last_activation_error=null`;
- baseline mapping hash remained `9ae20b4b4df8b7d711cc031d8c40d7edc4dbeec1f1cf3d1d637d9dfad480acde`;
- reserved UID `A3570001` absent.

Verified UID inventory:

`04689C36C82A81`, `04E38B36C82A81`, `04EA9236C82A81`, `689C36C82A81`, `7AB06354E000`, `DEADBEEF`, `DEADLBC`, `DEADMORNING`, `DEADNEWSBRIEF`, `DEADSMOOTH`, `E38B36C82A81`, `EA9236C82A81`.

The artifact retains the complete read-only capability, status, and list responses.

### ASTV staging catalogue double

- interface `astv.intent_catalogue.administration`, version `1.1.0`;
- mode `read_only_stage_double`;
- `mutation_supported=false`, `activation_applicable=false`;
- active revision `sha256:98790a0ecc161e218e845c57a673ff6a4d54e984076b7eddc0547cd164638e8e`;
- eight verified intents: `bbc_radio_2`, `classic_fm`, `gold_radio`, `lbc_news`, `lbc_radio`, `morning_routine`, `news_briefing`, `smooth_radio`.

The artifact retains the complete capability and list responses.

## Production preservation

A fresh read-only production query after disposal reported:

- state `active`, active/persisted count `12/12`;
- active and persisted revision both `v1-986df5539173dad03cf231dd5fd094dbdc6024d1786ad721b18b84fe332c4173`;
- `activation_required=false`, `last_activation_error=null`;
- the same 12 UIDs, with `A3570001` absent.

This matches the pre-retry production baseline. Production was not modified.

## Disposal and rollback

The unconditional cleanup removed container `694f4819f5aac05f6da7002b91e1fb9859bce9e2f61738eedc514c4bd2520711`; retained evidence states `container_removed=true`. The GitHub-hosted runner destroys the private config tree and transient HA state. The artifact intentionally excludes `.storage`, onboarding credentials, tokens, and mutable HA state.

No lifecycle rollback is required because no lifecycle call occurred. Recreating this staging identity later requires the reviewed PR head, pinned HA image digest, accepted AdvNFC tag/SHA, the 12-record fixture, and the same isolation profile.

## Human gate

The disposable stage is now proven suitable for a separately authorized controlled lifecycle, but this evidence grants no such authority. Human review must approve the exact create → Save → Activate → update → Save → Activate → delete → Save → Activate sequence and rollback/abort criteria before any call using `A3570001` is made. Production remains out of scope.
