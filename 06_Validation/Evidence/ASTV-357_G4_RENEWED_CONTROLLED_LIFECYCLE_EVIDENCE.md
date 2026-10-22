# ASTV-357 Renewed G4 Controlled Lifecycle Evidence

**Recorded:** 2026-10-22  
**Authority:** Renewed G4 human authorisation recorded in Linear ASTV-357  
**Outcome:** **PASS — RETURNED FOR G5 HUMAN ACCEPTANCE**

## Result and stop boundary

The single authorised lifecycle ran once in disposable Home Assistant staging using the accepted immutable candidate. Every required state transition and fail-closed assertion passed. The synthetic mapping was removed and the original logical baseline was reactivated before the stage was destroyed.

No production install, restart, mapping mutation, reload/Activate, NFC-reader action, MQTT action, gateway dispatch, stable-release promotion, or merge occurred. PR #71 remains draft and unmerged.

## Immutable identities

| Item | Verified evidence |
|---|---|
| Pull request | [AdvNFC PR #71](https://github.com/83degrees/AdvNFC/pull/71) — draft, unmerged |
| Lifecycle runner head | `6861a210c146272745e518e6d1aea9a8a5f78d44` |
| Controlled run | [GitHub Actions run 39811028375](https://github.com/83degrees/AdvNFC/actions/runs/39811028375) — success |
| Job | `verify-isolated-stage` / `119936991618` — success |
| Evidence artifact | `astv-357-disposable-staging-evidence-39811028375` / ID `12439363891` |
| Artifact digest | `sha256:6e617e2de8dc16bdf5ed86ee09d32cd5e5be7aeb75e89494e84dd39e5187cd72` |
| Artifact expiry | 2026-11-21 |
| Operator | GitHub actor `83degrees` |
| AdvNFC candidate | `v1.6.0-beta.dbef2f5` / `dbef2f5133d2efb6f426b348916dc0c58ec1e147` |
| AdvNFC component tree | `94ec6818fea53dd96fc7288a4afb7b25bb750715` |
| Home Assistant | `2026.9.4` / image digest `sha256:3e6710a7ab2a61311d9d899b719f6c3657791c63e8f4942cec4ebc42401d6b76` |
| Lifecycle evidence SHA-256 | `8d4d515923dd1f79594aa268955721d521119b4140c6241dea1a5973634c84d5` |
| Stage evidence SHA-256 | `4932e55d42328f59fb70bc236a390beb7ad0d934b0bcede470604a5f75aa08e8` |
| Home Assistant log SHA-256 | `35dfc4b7cdc606173ccfe7f77f4bf4c56b567205c4db31105ab1bfaee39d0c9e` |

The accepted ASTV-360 schema-boundary prerequisite was independently verified as successful run `39808740655`. The lifecycle harness resolved the new tag to the exact accepted commit before assembling the stage.

## Isolation and prerequisites

The retained evidence proves:

- container network mode `none` and published ports `{}`;
- dropped capabilities `["ALL"]` and `no-new-privileges`;
- container image ID `sha256:cd74b0e02cee84de9f53b0f8fc079c8979796b81a6b02e1ee0cd09f038703afd`;
- direct `python3 -m homeassistant --config /config` execution;
- private temporary `/config`, corrected from runner `1001:1001 / 0755` to measured HA process `0:0 / 0700`;
- successful private write proof created by the restricted HA process;
- read-only ASTV catalogue double with `mutation_supported=false`, `activation_applicable=false`, and eight exact fixture intents;
- inert staging sink with external dispatch capability `false`;
- no production credential, endpoint, MQTT topic, reader, device, or production listener configuration in the assembled stage;
- gateway spy absent at every captured state and at completion;
- `automatic_retries: 0` and exactly one attempt for every operation;
- unconditional container cleanup with `container_removed=true`.

## Initial baseline

Before mutation, stage status and both active and persisted mappings matched the fixture exactly:

- 12 active and 12 persisted mappings;
- active and persisted revision `v1-986df5539173dad03cf231dd5fd094dbdc6024d1786ad721b18b84fe332c4173`;
- `activation_required=false`, `last_activation_error=null`;
- persisted file SHA-256 `9ae20b4b4df8b7d711cc031d8c40d7edc4dbeec1f1cf3d1d637d9dfad480acde`;
- synthetic UID `A3570001` absent;
- schema-v1 record validation accepted UID `A3570001`, label `ASTV-357 isolated validation`, no area override, and action `astv_intent` / `classic_fm` without changing state.

## Exact lifecycle evidence

| Step | Returned result | Active / persisted | Revision and activation evidence |
|---|---|---:|---|
| Create → Save | `ok=true`, `operation=create`; initial synthetic record returned | 12 / 13 | active remained baseline; persisted became `v1-8dc066001488ee2e05e7864ca13bd040dfc018f1998c69877d178d09c14397fe`; activation required; active lookup still absent |
| Activate created | `ok=true`, `operation=activate` | 13 / 13 | both revisions `v1-8dc066…397fe`; activation clear; active lookup exactly initial record |
| Edit → Save | `ok=true`, `operation=update`; label changed to `ASTV-357 isolated validation updated`; area set to `astv_357_staging_area` | 13 / 13 | active remained `v1-8dc066…397fe`; persisted became `v1-513945202e7b48f1e649879b324d286923c659d978b75d2971dc1a3b4e9d1436`; activation required; active lookup still initial record |
| Activate edited | `ok=true`, `operation=activate` | 13 / 13 | both revisions `v1-513945…d1436`; activation clear; active lookup exactly updated record |
| Reject duplicate | `ok=false`, `error.code=already_exists` for baseline UID `04689C36C82A81` | 13 / 13 | status, active list, synthetic lookup, persisted revision and persisted bytes unchanged |
| Delete → Save | `ok=true`, `operation=delete`, UID `A3570001` returned | 13 / 12 | active remained `v1-513945…d1436`; persisted returned to baseline revision `v1-986df…4173`; activation required; updated record remained active until activation |
| Final Activate | `ok=true`, `operation=activate` | 12 / 12 | both revisions exactly baseline `v1-986df…4173`; activation clear; synthetic lookup absent |

The recorded lifecycle order is exactly:

`create_save`, `activate_created`, `edit_save`, `activate_updated`, `reject_baseline_duplicate`, `delete_save`, `activate_deleted`.

All returned envelopes, full status/list responses, persisted snapshots, timestamps, and gateway assertions are retained in `lifecycle-evidence.json` inside the immutable artifact.

## Rollback and final equality

The authorised delete → Save → final Activate path was the object-scoped rollback. Final active mappings and final persisted mappings are logically identical to the complete original 12-record baseline, the synthetic UID is absent, counts are `12/12`, both revisions exactly equal the original revision, and activation is not required.

The persisted file is not byte-identical after the lifecycle: baseline SHA-256 `9ae20b…0acde`, final SHA-256 `e4110e…48e7`. This is expected serializer normalization. It did not change the logical mappings or the content-derived revision; the artifact records `logical_exact=true`, `byte_exact=false`, and final revision exactly `v1-986df…4173`. No claim of byte-level restoration is made.

The gateway sink recorded zero invocations. The final isolation check passed, and cleanup destroyed the entire stage, providing a second containment boundary after logical rollback.

## Log review

There were no AdvNFC lifecycle or service failures. The retained log contains only known environment/staging-double diagnostics:

- custom-integration warnings for AdvNFC and the two test doubles;
- network source-detection and Analytics/zeroconf errors caused by the deliberately absent network interface;
- missing `services.yaml` descriptions for the two programmatically registered staging doubles;
- an upstream Python `rich` syntax warning.

The local WebSocket remained healthy, all staging-double responses were verified, the controlled lifecycle passed, and cleanup succeeded. These diagnostics do not indicate isolation drift or a failed lifecycle gate.

## Independent production invariance

Read-only production status and mapping inventory were captured immediately before dispatch and again after stage disposal. Both observations reported:

- state `active`;
- active/persisted count `12/12`;
- active and persisted revision `v1-986df5539173dad03cf231dd5fd094dbdc6024d1786ad721b18b84fe332c4173`;
- `activation_required=false`, `last_activation_error=null`;
- the same exact 12 mapping records;
- synthetic UID `A3570001` absent.

Production was not modified.

## G5 human gate

This evidence is returned for G5 human acceptance. It does not authorise production deployment, installation, restart, mapping change, reload/Activate, stable promotion, or merge. PR #71 must remain draft and unmerged pending the human decision.
