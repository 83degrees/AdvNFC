# ASTV-357 G0 Validation and Rollback Plan

## Decision and stop boundary

This artefact records the G0-authorised, non-mutating preparation phase for
ASTV-357. It prepares an isolated end-to-end validation sequence and recovery
evidence for human review. It does not authorise or evidence a live create,
update, delete, Save, provider reload/activation, Home Assistant deployment or
restart, production catalogue mutation, stable release, or `main` promotion.

The proposed live lifecycle must not start until a human gives separate,
specific G4 authority for the chosen environment, exact test record, current
baseline, backup and byte-capture identities, actions, and rollback sequence.

## Authority and evidence routes

- Governing issue: `ASTV-357`
- Constitutional authority: Central Governance v11.17.0
- Product context: `00_Governance/PROJECT_PROFILE.md`
- Administration contract: `03_Contracts/ADVNFC_ADMINISTRATION_READ_INTERFACE.md`, candidate interface v3
- Common administration authority: Product Administration Interface Standard v1.0.0
- Deployment authorities:
  - `HOME_ASSISTANT_INTEGRATION_DEPLOYMENT_STANDARD.md`
  - `HOME_ASSISTANT_CONFIG_DEPLOYMENT_STANDARD.md`
- Product runbooks:
  - `08_Deployment/ADVNFC_HACS_DEPLOYMENT_RUNBOOK.md`
  - `08_Deployment/ADVNFC_HAOS_CONFIG_DEPLOYMENT_RUNBOOK.md`
- Live read-only evidence route: the configured `ha-starburst` Home Assistant connector
- Repository evidence route: Git state and isolated local test execution from persistent `beta`

Production observations below were made on 2026-10-22 through read-only Home
Assistant queries and response-only AdvNFC/ASTV administration reads. They are
evidence only of the returned state at observation time. Repository comparison
is a derived interpretation and is not presented as part of the raw live
response.

## Fresh baseline evidence

| Subject | Observed result |
| --- | --- |
| Repository routing baseline | `origin/beta` and `origin/main` both resolve to `16b5212b0791101dd149404a026ed0f102401f94` |
| Installed AdvNFC Beta | HACS reports `v1.6.0-beta.288e3df`; immutable tag resolves to `288e3df5187a5c37e44feda202cc570f9eb539e0` |
| Manifest identity | Installed-tag source declares integration version `1.6.0` |
| Frontend asset identity | Installed-tag and current `beta` frontend blob both resolve to Git blob `ff411b473fc39918bea3e132a3d4ca36ec30977b` |
| Home Assistant health | Core `2026.9.4`, Home Assistant OS `18.3`, Supervisor `2026.10.3`; instance state `RUNNING`; Supervisor reports healthy and supported |
| AdvNFC runtime | `sensor.advnfc_tag_mapping=loaded`; `automation.advnfc_tag_listener=on` |
| Active mapping state | schema `1`; count `12`; revision `v1-986df5539173dad03cf231dd5fd094dbdc6024d1786ad721b18b84fe332c4173` |
| Persisted mapping state | count `12`; same revision as active; `activation_required=false`; no last activation error |
| Administration boundary | interface `advnfc.tag_mapping.administration`, version `3`; all required read, validation, mutation, status and activation operations advertised |
| ASTV target discovery | interface `astv.intent_catalogue.administration` v1.1.0; eight active targets at revision `sha256:98790a0ecc161e218e845c57a673ff6a4d54e984076b7eddc0547cd164638e8e` |
| Existing recovery point | backup `1f751d43`, `ASTV-355_prechange_v1.6.0-beta.288e3df`, 2026-10-21 21:00:14 Europe/London; protected; Home Assistant settings included; database excluded |

The existing backup proves a current recovery point exists, but it is not the
fresh pre-test backup required for a later live phase. A new named full
Home Assistant settings backup must be created immediately before any approved
live write. Its identifier, timestamp, included parts, protection state, and
usable encryption/emergency-key route must be recorded before proceeding.

### Observed active mapping inventory

The read boundary returned the following canonical active inventory, ordered by
UID. Because active and persisted revisions are identical, this also supports
logical equivalence of the current persisted candidate, but it is not a
byte-for-byte capture of the target YAML.

| UID | Label | ASTV intent |
| --- | --- | --- |
| `04689C36C82A81` | LBC News (Shorefoot) | `lbc_news` |
| `04E38B36C82A81` | Classic FM (Shorefoot) | `classic_fm` |
| `04EA9236C82A81` | Gold Radio (Shorefoot) | `gold_radio` |
| `689C36C82A81` | LBC News | `lbc_news` |
| `7AB06354E000` | Dad - Classic FM | `classic_fm` |
| `DEADBEEF` | BBC Radio 2 | `bbc_radio_2` |
| `DEADLBC` | LBC Radio | `lbc_radio` |
| `DEADMORNING` | Morning Routine | `morning_routine` |
| `DEADNEWSBRIEF` | News Briefing | `news_briefing` |
| `DEADSMOOTH` | Smooth Radio | `smooth_radio` |
| `E38B36C82A81` | Classic FM | `classic_fm` |
| `EA9236C82A81` | Gold Radio | `gold_radio` |

### Material repository/runtime discrepancy

The governed repository mapping at commit `16b5212b...` contains nine records.
The live active and persisted state contains twelve. The three additional live
records are the `04689C36C82A81`, `04E38B36C82A81`, and `04EA9236C82A81`
Shorefoot records.

Therefore:

- the repository mapping must not be used as the rollback baseline for a
  `ha-starburst` test;
- replacing the live mapping with the repository file would remove three
  operational records and is forbidden;
- a live phase requires an exact pre-test target-byte capture stored separately
  from `/config/AdvNFC/advnfc_tag_mapping.yaml`, plus the fresh full backup;
- the twelve-record live snapshot and its revision are the current logical
  baseline; and
- the discrepancy must be explicitly accepted or separately resolved before
  any test is allowed to mutate `ha-starburst`.

The current Project Profile also states that the integration manifest is
version `1.3.0`, while the authoritative manifest, installed Beta metadata, and
immutable installed tag all identify version `1.6.0`. This is a durable
product-context inconsistency. ASTV-357 does not silently correct it because
the G0 scope is validation preparation rather than profile maintenance. It must
be surfaced for separate governed correction or explicit inclusion before this
issue completes.

## Isolation decision

### Recommended environment: disposable staging

Use a disposable Home Assistant staging instance with:

1. the immutable AdvNFC `v1.6.0-beta.288e3df` integration;
2. an isolated copy of the current twelve-record mapping baseline;
3. the AdvNFC package and top-level `advnfc:` activation;
4. an ASTV catalogue double exposing the observed eight active intent IDs;
5. an ASTV gateway spy/sink that records invocations but cannot dispatch media,
   routines, notifications, or device actions; and
6. no connection to production MQTT reader topics or production devices.

This is the only currently demonstrated non-interfering route. A synthetic UID
alone cannot prove safety on `ha-starburst`: all existing readers share the
active mapping, a physical tag could theoretically collide with the chosen UID,
and activation atomically replaces the shared runtime snapshot.

### Reserved staging test record

| Field | Proposed value | Reason |
| --- | --- | --- |
| UID | `A3570001` | Canonical uppercase alphanumeric value; absent from the observed twelve-record inventory; reserved only for ASTV-357 staging |
| Initial name | `ASTV-357 isolated validation` | Unambiguous test ownership |
| Action type | `astv_intent` | The only schema-v1 action type |
| Initial intent | `classic_fm` | Present in the observed active ASTV catalogue and already used by baseline mappings |
| Initial area override | omitted | Exercises the optional-field absence and avoids selecting an environment-specific production area |
| Edited name | `ASTV-357 isolated validation updated` | Proves complete-record update |
| Edited area override | a staging-only area ID | Exercises the optional field without naming or routing to a production area |

The record has been exercised by the isolated provider lifecycle harness. It
has deliberately not been submitted to the live validation service because the
issue requires separate human approval of the exact live UID/action.

## Isolated harness and negative-case evidence

The isolated harness uses only temporary files and mocked Home Assistant
WebSocket/provider boundaries. It cannot reach Home Assistant or the production
mapping.

| Coverage | Evidence |
| --- | --- |
| Complete create → activate → edit → activate → delete → activate cycle | Provider-store test verifies active/persisted separation at every Save, exact activation transitions, preservation of the pre-existing record, and logical restoration of the baseline |
| Duplicate UID | Provider-store test rejects normalized duplicate `A1` with `already_exists` and proves target bytes and both revisions remain unchanged |
| Invalid record/candidate | Existing provider tests reject invalid candidates and duplicate complete-candidate UIDs without writing |
| Stale revision | Provider and frontend tests prove one rejected write, no retry, and refreshed reconciliation |
| Permission denied | Provider-boundary tests prove non-admin/unknown users are rejected before path, area-registry, or provider access; frontend preserves platform permission failure separately |
| Timeout / uncertain outcome | Frontend test proves a timed-out Save is not retried and refreshes status plus active list for reconciliation |
| Activation failure | Provider test retains the previous active snapshot and supports retry; frontend test maps the failure to `activation_failed` and never reports verification |
| Atomic replacement failure | Provider test proves original bytes survive and temporary files are removed |
| Optional ASTV failure | Frontend test proves missing or incompatible ASTV discovery does not disable AdvNFC administration |
| HACS identity/cache | Packaging tests plus matching digest-addressed frontend blob confirm candidate identity and cache-busting route |
| Responsive/accessibility preparation | Panel registration proves safe-area handling; source has a 600px narrow layout, touch-sized controls, labelled fields, accessible search text, status live region, and tab `aria-current`; runtime visual/accessibility acceptance remains a later non-mutating human check |
| Reproducible CI route | The existing read-only pull-request workflow installs the declared Python dependencies and now runs the Python suite, frontend syntax check, and Node frontend suite against the exact candidate |

Preparation-suite results on the ASTV-357 issue branch:

- Node frontend adapter/editor suite: **19 passed**.
- Python suite: **70 passed, 6 subtests passed**.
- No product test failed. The Python run used the repository-declared
  dependencies and an explicit workspace test directory because the sandbox's
  default temporary directory was not writable.
- Central Governance routing check: **passed**; the candidate changes no
  runtime implementation, so the routing checker does not mechanically require
  WF-01 Beta routing. The issue branch nevertheless remains based on persistent
  `beta` to preserve the recorded issue route.

## Staged acceptance procedure

### Stage A — human review and immutable inputs

1. Human accepts disposable staging or explicitly overrides it with a proven
   `ha-starburst` isolation case.
2. Record exact environment identity, integration tag/SHA, frontend asset
   identity, mapping baseline revision/count/inventory, ASTV catalogue revision,
   test UID, test intent, staging area, authorised operator, and time window.
3. Confirm no other actor or automation will use the provider administration
   boundary during the window.
4. If production is authorised, capture exact target bytes and create a fresh
   full Home Assistant settings backup. Stop until both are independently
   identifiable and recoverable.

### Stage B — non-mutating checks

1. Confirm Core and AdvNFC health, installed immutable tag, panel asset digest,
   service capabilities, and admin identity.
2. Re-read status/list and require the accepted baseline count, inventory,
   equal active/persisted revisions, and `activation_required=false`.
3. Verify list/search/sort, full-page editor tabs, read-only Status, ASTV target
   discovery and unavailable fallback, iPhone-width layout, keyboard order,
   visible focus, accessible names, and status/error announcements.
4. Run validation-only negative inputs in the isolated harness. Do not
   manufacture production permission failures, provider outages, or damaged
   persisted state.

### Stage C — controlled lifecycle (separate authority required)

After every numbered action, capture the service response, time, counts,
revisions, `activation_required`, relevant screenshot, and active-list result.

1. Validate the reserved record without persistence.
2. Create/Save it once. Require persisted revision change, unchanged active
   revision/list/routing, and `activation_required=true`.
3. Activate once. Require active=persisted, `activation_required=false`, count
   baseline+1, and a successful controlled lookup of `A3570001`.
4. Edit only the synthetic record's name and staging-only area. Save once;
   require the prior active record still serves until activation.
5. Activate once and verify the complete edited record.
6. Attempt a duplicate of one baseline UID and require rejection with no byte,
   revision, count, active-list, or routing change.
7. Delete only `A3570001` from persisted state. Require it remains active until
   the explicit activation.
8. Activate once. Require the captured twelve-record logical baseline, original
   per-record content, baseline count, equal active/persisted revisions, and no
   activation error. Revision hashes may differ because the provider owns their
   derivation.

### Stage D — acceptance evidence

Retain or link:

- explicit G4 action authority;
- immutable candidate and environment identities;
- pre-test target-byte capture identity and fresh backup identity;
- baseline and each transition's service responses and timestamps;
- screenshots at Save/Activate boundaries and final restoration;
- test/CI results and exact commit;
- final twelve-record logical comparison and byte comparison where available;
- any warnings, limitations, aborts, or recovery actions; and
- explicit distinction between isolated-harness evidence and live runtime
  evidence.

## Stop and abort criteria

Stop before the first write when any of these is true:

- candidate, environment, operator, UID, intent, area, baseline, or authority is
  missing or ambiguous;
- installed tag/asset identity differs from the accepted input;
- count is not 12, inventory differs, revisions differ, or activation is already
  required;
- the repository/runtime three-record discrepancy has not been explicitly
  dispositioned for a production test;
- exact target bytes or the fresh usable backup cannot be identified;
- any production reader/topic/device can reach the proposed staging route; or
- another actor may write or activate the mapping during the test.

Abort immediately after a write when any of these occurs:

- response is missing, times out, is contradictory, or cannot be reconciled;
- more than one mutation attempt appears for a single authorised action;
- an existing UID is changed or removed;
- active state changes before explicit activation;
- counts, revisions, inventory, or `activation_required` differ from the
  expected transition;
- provider status becomes invalid/unavailable or records an activation error;
- the ASTV sink observes any non-test invocation or external effect; or
- exact final baseline restoration cannot be proved.

No timed-out mutation is automatically retried. Refresh status and active list,
preserve evidence, and require a new human decision after the outcome is known.

## Rollback hierarchy

1. **Before activation:** stop. The previous active snapshot remains the runtime
   authority. Reconcile persisted state, and do not activate an unexpected
   candidate.
2. **Normal synthetic-record rollback:** using the latest observed persisted
   revision, apply only the exact inverse to `A3570001`; validate that the full
   persisted candidate matches the captured baseline; then activate once and
   prove the twelve-record baseline.
3. **Exact file restoration:** if provider-level inverse operations cannot prove
   restoration, restore the separately captured pre-test bytes to
   `/config/AdvNFC/advnfc_tag_mapping.yaml` through the governed operator route,
   verify target bytes, run the Home Assistant configuration check, and perform
   one explicitly authorised provider reload. This does not use the nine-record
   repository file.
4. **Full backup restore:** last resort only if the narrow file/provider route
   cannot recover a trustworthy state. Restoring the fresh pre-test backup
   overwrites included Home Assistant state and restarts Home Assistant; it
   therefore requires a new explicit human confirmation at action time. After
   restore, verify Core health, installed AdvNFC identity, listener state,
   mapping sensor, twelve-record inventory, revisions, ASTV discovery, and logs.

The existing `1f751d43` backup is retained as prior recovery evidence but is not
a substitute for the fresh pre-live backup. HACS rollback is outside the
planned lifecycle because no integration deployment or version change is
authorised.

## G0 conclusion

The repository candidate and isolated harness are ready for human review. The
live baseline is healthy and internally consistent, but it materially differs
from the repository mapping by three operational Shorefoot records. Safe
non-interference has not been demonstrated on `ha-starburst`; disposable
staging is therefore the recommended and currently approved-by-evidence route.
No live mutation, backup creation, activation, deployment, or restart was
performed during this preparation phase.
