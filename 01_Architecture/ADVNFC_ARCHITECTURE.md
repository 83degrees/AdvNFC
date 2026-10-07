# AdvNFC Architecture

## Purpose and Sources of Truth

This document records the semantic target architecture of AdvNFC: its active components, calls, returned values, data dependencies, and external boundary.

The governed diagram at `Diagrams/ADVNFC_ARCHITECTURE.drawio` represents this semantic architecture. This document is authoritative for AdvNFC architecture and dependencies. Verified live Home Assistant YAML/configuration establishes deployed/runtime facts only, including current entity IDs, inputs, response variables, and service calls.

## Architecture Status and Timeframes

The Home Assistant portion of this architecture is the deployed AdvNFC runtime established by the completed ASTV Phase 0 carve-out. ASTV now begins at the provider-owned Intent Invocation boundary.

The schema-v1 tag-mapping loader, immutable snapshot, normalized typed-action
record, and Select Tag Action component are the deployed AdvNFC baseline.
ASTV-324 adds a provider-owned, read-only administration boundary over that
same active snapshot without changing runtime tag routing.

ASTV-322 transferred reader-agent source, packaging, deployment and provider-contract authority to the separately governed AdvNFC Reader Agent product. AdvNFC now begins at configured Home Assistant reader-event state and consumes the provider-owned AdvNFC Reader Event MQTT Interface.

## End-to-End Flow

The current production flow is:

1. A physical NFC tag is read by the ACR122U attached to the Raspberry Pi reader node.
2. The reader agent acquires the NFCID1 through `nfc-list`, normalizes it to uppercase, applies same-card suppression/reset behavior, and publishes the retained per-reader MQTT state.
3. The retained per-reader MQTT state is consumed by Home Assistant and represented by the configured reader sensor. The canonical ASTV-257 topic is `advnfc/<reader>/last_uid`; during coexistence `pi-nfc-02` remains on `assistive/nfc/pi-nfc-02/last_uid`.
4. AdvNFC Tag Listener filters invalid/recovery transitions and calls AdvNFC UID Gateway.
5. AdvNFC resolves the governed schema-v1 tag mapping into a typed action, selects the supported action route, and invokes ASTV through the provider-owned Intent Invocation interface.

## External Reader Event Provider Boundary

AdvNFC Reader Agent is an external product that owns physical UID acquisition,
reader identity, suppression/reset behaviour, MQTT publication, runtime
profiles, service configuration, Debian packaging, deployment and rollback.
Its provider-owned contract is authoritative at:

`AdvNFC-Reader-Agent/03_Contracts/ADVNFC_READER_EVENT_MQTT_INTERFACE.md`

AdvNFC consumes only the resulting configured Home Assistant reader-sensor
state. During the candidate coexistence period, the provider contract retains
the legacy `assistive/nfc/pi-nfc-02/last_uid` path for `pi-nfc-02` while
replacement/test readers use `advnfc/<reader>/last_uid`. MQTT broker and
network transport remain external infrastructure.

## Authoritative source and deployment routes

The Home Assistant integration is distributed through HACS from the sole
authoritative root source `custom_components/advnfc/**`. The canonical
`04_Implementation/haos/source/config/custom_components/advnfc/README.md`
path is a non-duplicating deployment-map pointer.

The Home Assistant automations, scripts, and mapping remain a separate
operator-selected configuration unit beneath
`04_Implementation/haos/source/config/**`. The integration's required
top-level `advnfc:` activation remains an operator-managed entry in target
`/config/configuration.yaml`.

## NFC Entry and Tag-to-Intent Resolution

### External NFC Input and Reader Sensors

An external NFC read is delivered over MQTT to one of the configured Home Assistant reader sensors:

- `sensor.pi_nfc_02_last_uid`
- `sensor.pi_nfc_99_last_uid`

A state change on either sensor is evaluated by AdvNFC - Tag Listener. State transitions to or from `unknown` or `unavailable` are excluded at the Home Assistant trigger boundary before UID Gateway invocation.

### AdvNFC - Tag Listener

- Entity: `automation.advnfc_tag_listener`
- Sources:
  - `sensor.pi_nfc_02_last_uid`
  - `sensor.pi_nfc_99_last_uid`
- Excludes state transitions to or from `unknown` or `unavailable` at the Home Assistant trigger boundary.
- Calls `script.advnfc_uid_gateway` for each remaining state change, with:
  - `uid`
  - `trigger_entity`

No other NFC reader sensors are part of the current listener architecture being carved out.

### AdvNFC - UID Gateway

- Entity: `script.advnfc_uid_gateway`
- Inputs:
  - `uid`
  - `trigger_entity` (default `sensor.pi_nfc_99_last_uid`)
- Calls `script.advnfc_find_tag_record` with:
  - `uid`
- Captures the result as:
  - `tag_record_response`
- Stops with `No Tag Record Found` when the lookup is empty.
- On success, temporarily creates `Tag Record Found` with UID, trigger entity, resolved intent ID, and optional tag area override.
- Calls `script.advnfc_select_tag_action` with the complete normalized tag record and originating `trigger_entity`.

UID Gateway does not repeat the mapping loader's schema or typed-action
validation. It consumes only normalized records from the active validated
snapshot.

UID Gateway does not resolve the catalogue request or area itself and does not call Select Intent Engine directly.

#### AdvNFC - Fn: Find Tag Record

- Entity: `script.advnfc_find_tag_record`
- Input: `uid`
- Return: `tag_record_response`
- Data dependency:
  - AdvNFC Tag Mapping
  - `advnfc_tag_mapping.yaml`

The script delegates its lookup to the response-only `advnfc.find_tag_record` integration action. The loader normalizes the supplied UID using string conversion, trimming, and uppercasing, then performs an exact lookup against the active immutable snapshot. It returns `{}` for an unknown UID and remains side-effect-free.

The normalized result contains `uid`, `label`, optional `area_override`, and a typed `action` object. The typed action is not collapsed to `intent_id` during lookup.

### AdvNFC Tag Mapping Loader

The AdvNFC Home Assistant integration owns loading and validating
`advnfc_tag_mapping.yaml` against the closed schema defined by
`ADVNFC_TAG_MAPPING_SCHEMA_V1.md`.

The integration is activated explicitly by the top-level `advnfc:` entry in
Home Assistant `configuration.yaml`. Integration activation is not embedded in
the AdvNFC scripts package; that package owns scripts only.

Initial load and explicit reload validate the entire candidate document,
including duplicate keys, canonical UID storage, closed fields, required
values, action type and intent-ID structure, and Home Assistant area
resolution. A valid candidate atomically replaces the active immutable
snapshot. A failed reload preserves the previous snapshot.

`sensor.advnfc_tag_mapping` is a registered, non-polling Home Assistant
`SensorEntity` owned by the AdvNFC sensor platform. It has the stable unique ID
`advnfc_tag_mapping`, appears beneath the AdvNFC integration in the entity
registry, and exposes the active schema version and mapping count as runtime
capability state. A successful mapping activation dispatches an update to the
entity; a failed reload leaves the prior snapshot and sensor state unchanged.

### AdvNFC Administration Read Boundary

The Home Assistant integration exposes the provider-owned interface documented
at `03_Contracts/ADVNFC_ADMINISTRATION_READ_INTERFACE.md`. Four response-only
services provide capability discovery, normalized collection reads, canonical
UID lookup, and typed-action target query.

All results are projections of the active immutable validated snapshot.
Consumers never read `advnfc_tag_mapping.yaml`, and no administration
operation writes, activates, or reloads mapping state. Responses carry
independent administration-interface and tag-mapping-schema versions. Get
operations distinguish invalid queries from missing UIDs; valid queries with no
matches return an empty collection.

The schema-v1 query route supports `astv_intent` plus normalized
`intent_id`. AdvNFC owns query and normalization semantics but does not read
the ASTV intent catalogue or validate cross-product existence.

### AdvNFC - Select Tag Action

- Entity: `script.advnfc_select_tag_action`
- Inputs:
  - complete normalized `tag_record`
  - originating `trigger_entity`
- Uses the established selector `choose` structure to inspect
  `tag_record.action.type`, route the supported action, and fail explicitly
  through the default branch for an unsupported type.
- For schema v1 `astv_intent`, extracts normalized `intent_id` and optional
  `area_override`, then calls `script.astv_intent_gateway` with exactly:
  - `intent_id`
  - `input_area_override`
  - `trigger_entity`

No separate ASTV-specific AdvNFC handler exists in schema v1.

## ASTV Intent Invocation Boundary

AdvNFC consumes the provider-owned ASTV contract:

`ASTV/03_Contracts/ASTV_INTENT_INVOCATION_INTERFACE.md`

The interface is provided by:

`script.astv_intent_gateway`

The invocation fields are exactly those already passed by the current ASTV Phase 0 UID Gateway:

- `intent_id`
- `input_area_override`
- `trigger_entity`

No UID, tag record, MQTT topic, or reader-specific payload crosses the product boundary.

After the invocation crosses this boundary, ASTV owns intent-catalogue lookup, intent-record interpretation, final area resolution, intent routing, preparation, and execution.

The consumed ASTV contract preserves the current target-area precedence:

1. non-blank `input_area_override`;
2. non-blank `area_override` from the resolved ASTV intent record;
3. the Home Assistant area of `trigger_entity`.

AdvNFC does not reproduce or alter that precedence.

## External and Data Dependencies

| Dependency | Type | Consumer or relationship |
|---|---|---|
| AdvNFC Reader Agent | External product | Publishes retained per-reader MQTT state under `AdvNFC-Reader-Agent/03_Contracts/ADVNFC_READER_EVENT_MQTT_INTERFACE.md` |
| MQTT broker / network transport | External infrastructure | Carries provider-owned reader-agent MQTT publications to Home Assistant |
| `sensor.pi_nfc_02_last_uid`, `sensor.pi_nfc_99_last_uid` | MQTT-fed Home Assistant sensors | State-change inputs evaluated by AdvNFC - Tag Listener; transitions to or from `unknown` or `unavailable` are excluded at the Home Assistant trigger boundary before UID Gateway invocation |
| `advnfc_tag_mapping.yaml` | Data source | Closed schema-v1 candidate loaded and validated into one immutable active AdvNFC mapping snapshot |
| ASTV Intent Invocation interface | External product contract | AdvNFC invokes `script.astv_intent_gateway` with `intent_id`, optional `input_area_override`, and optional `trigger_entity` |
| AdvNFC Administration Read Interface | Provider-owned contract | Future management consumers read normalized active mappings without access to YAML internals |

## Interface Naming and Return Boundaries

Exact established names are preserved where they describe the existing Phase 0 behavior. In particular:

- `uid`
- `trigger_entity`
- `tag_record_response`
- `tag_record`
- `action.type`
- `intent_id`
- `input_area_override`
- `interface_id`
- `interface_version`
- `tag_mapping_schema_version`
- `supported_action_types`
- `error.code`

A caller's `response_variable` name describes how that caller captures a result. A child's returned payload name describes the child's own interface. These names are not renamed merely for documentary consistency.

## Migration Invariant

The Home Assistant carve-out preserves the former ASTV Phase 0 behavior. ASTV-299 adds the governed schema-v1 typed-action seam while preserving equivalent downstream ASTV invocation semantics for every migrated mapping.

For the same valid reader state change and equivalent tag mapping, AdvNFC must produce the same ASTV Intent Invocation values as the current ASTV Phase 0 path:

- the same `intent_id`;
- the same optional `input_area_override`;
- the same `trigger_entity`.

Functional redesign of the reader inputs, transition filtering, UID normalization, tag mapping semantics, gateway failure behavior, or ASTV area-resolution semantics is outside the initial carve-out.

## Current and Target Ownership

The deployed Home Assistant responsibilities are owned by AdvNFC under:

- `automation.advnfc_tag_listener`
- `script.advnfc_uid_gateway`
- `script.advnfc_find_tag_record`
- `script.advnfc_select_tag_action`
- `advnfc_tag_mapping.yaml`
- `advnfc.get_administration_capabilities`
- `advnfc.list_tag_mappings`
- `advnfc.get_tag_mapping`
- `advnfc.query_tag_mappings`

ASTV begins at the provider-owned Intent Invocation boundary.

AdvNFC owns only the Home Assistant path listed above. AdvNFC Reader Agent owns
the upstream reader runtime and publication boundary; ASTV owns downstream
intent interpretation and execution after the provider-owned Intent Invocation
boundary.
