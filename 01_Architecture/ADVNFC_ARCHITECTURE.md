# AdvNFC Architecture

## Purpose and Sources of Truth

This document records the semantic target architecture of AdvNFC: its active components, calls, returned values, data dependencies, and external boundary.

The governed diagram at `Diagrams/ADVNFC_ARCHITECTURE.drawio` represents this semantic architecture. This document is authoritative for AdvNFC architecture and dependencies. Verified live Home Assistant YAML/configuration establishes deployed/runtime facts only, including current entity IDs, inputs, response variables, and service calls.

## Architecture Status and Timeframes

The Home Assistant portion of this architecture is the deployed AdvNFC runtime established by the completed ASTV Phase 0 carve-out. ASTV now begins at the provider-owned Intent Invocation boundary.

ASTV-247 extends AdvNFC source authority upstream to the Raspberry Pi reader-agent software captured from `pi-nfc-02`. That reader-agent source is a governed deployment candidate only until ASTV-249 performs and proves the production deployment.

The reader-agent import is behavior-preserving. Existing UID acquisition, same-card suppression/reset behavior, Home Assistant webhook output, MQTT event output, retained per-reader `last_uid` output, topic names, payloads, polling, and debounce semantics are retained. The only intentional source-boundary change is removal of the embedded MQTT secret from source control.

## End-to-End Flow

The current production flow is:

1. A physical NFC tag is read by the ACR122U attached to the Raspberry Pi reader node.
2. The currently deployed reader agent acquires the NFCID1 through `nfc-list`, normalizes it to uppercase, applies same-card suppression/reset behavior, and publishes the existing outputs.
3. The retained per-reader MQTT state `assistive/nfc/<reader>/last_uid` is consumed by Home Assistant and represented by the configured reader sensor.
4. AdvNFC Tag Listener filters invalid/recovery transitions and calls AdvNFC UID Gateway.
5. AdvNFC resolves the governed tag mapping and invokes ASTV through the provider-owned Intent Invocation interface.

After ASTV-249, step 2 is performed by the governed AdvNFC reader-agent source in this repository. Until then, the live Pi script remains runtime evidence rather than a repository-deployed artifact.

## Raspberry Pi Reader Agent

### Physical Reader and UID Acquisition

The reader-agent candidate runs on a Raspberry Pi with an attached ACS ACR122U. It uses the external `libnfc` tool `nfc-list` and extracts the NFCID1 using the captured AWK expression, producing an uppercase UID.

The reader identity defaults to `hostname -s`. The captured `pi-nfc-02` runtime uses:

- polling interval: 0.20 seconds;
- post-send debounce: 0.80 seconds;
- same-card suppression: do not re-send the same UID while continuously present;
- reset rule: clear the remembered UID after eight consecutive empty polls.

### Reader Outputs

The two MQTT publications are governed by:

`03_Contracts/ADVNFC_READER_EVENT_MQTT_INTERFACE.md`

For each newly accepted UID, the reader agent preserves all three captured outputs:

1. Home Assistant webhook `assistive_card_scan` with JSON fields `uid` and `reader`;
2. non-retained MQTT event `assistive/nfc/event` with JSON fields `uid`, `reader`, and `ts`;
3. retained MQTT state `assistive/nfc/<reader>/last_uid` containing the raw uppercase UID.

The Home Assistant AdvNFC path currently consumes the retained per-reader `last_uid` state. The webhook and generic MQTT event are retained during this migration because ASTV-247 is behavior-preserving; any later retirement requires separate evidence and governance.

### Reader-Agent Deployment Boundary

AdvNFC owns the reader-agent source and its systemd/service configuration. Raspberry Pi OS, USB/platform behavior, the ACR122U hardware, `libnfc`, network transport, and MQTT broker remain external dependencies.

Deployment-specific configuration is supplied outside source control. The MQTT password is not stored in the repository.

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
- Stops with `Invalid Tag Record` when `intent_id` is absent or blank.
- On success, temporarily creates `Tag Record Found` with UID, trigger entity, resolved intent ID, and optional tag area override.
- Invokes the provider-owned ASTV Intent Invocation interface at `script.astv_intent_gateway` with:
  - `intent_id` from `tag_record_response.intent_id`
  - `input_area_override` from optional `tag_record_response.area_override`
  - `trigger_entity`

UID Gateway does not resolve the catalogue request or area itself and does not call Select Intent Engine directly.

#### AdvNFC - Fn: Find Tag Record

- Entity: `script.advnfc_find_tag_record`
- Input: `uid`
- Return: `tag_record_response`
- Data dependency:
  - AdvNFC Tag Mapping
  - `advnfc_tag_mapping.yaml`

The function normalizes the supplied UID using string conversion, trimming, and uppercasing, then performs an exact mapping lookup. It returns `{}` for an unknown UID and remains side-effect-free.

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
| ACR122U + Raspberry Pi platform | External hardware/platform | Provides physical NFC reads to the governed reader-agent software |
| `libnfc` / `nfc-list` | External runtime dependency | Produces NFCID1 input consumed by the reader agent |
| AdvNFC reader agent | AdvNFC-owned software | Acquires UID, applies captured suppression/reset behavior, and emits the existing webhook/MQTT outputs |
| MQTT broker / network transport | External infrastructure | Carries reader-agent MQTT publications defined by `ADVNFC_READER_EVENT_MQTT_INTERFACE.md` to Home Assistant |
| `sensor.pi_nfc_02_last_uid`, `sensor.pi_nfc_99_last_uid` | MQTT-fed Home Assistant sensors | State-change inputs evaluated by AdvNFC - Tag Listener; transitions to or from `unknown` or `unavailable` are excluded at the Home Assistant trigger boundary before UID Gateway invocation |
| `advnfc_tag_mapping.yaml` | Data source | Active AdvNFC Find Tag Record lookup after cutover |
| ASTV Intent Invocation interface | External product contract | AdvNFC invokes `script.astv_intent_gateway` with `intent_id`, optional `input_area_override`, and optional `trigger_entity` |

## Interface Naming and Return Boundaries

Exact established names are preserved where they describe the existing Phase 0 behavior. In particular:

- `uid`
- `trigger_entity`
- `tag_record_response`
- `intent_id`
- `input_area_override`

A caller's `response_variable` name describes how that caller captures a result. A child's returned payload name describes the child's own interface. These names are not renamed merely for documentary consistency.

## Migration Invariant

The Home Assistant carve-out preserves the former ASTV Phase 0 behavior. The reader-agent import additionally preserves the captured `pi-nfc-02` acquisition and publication behavior.

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
- `advnfc_tag_mapping.yaml`

ASTV begins at the provider-owned Intent Invocation boundary.

ASTV-247 establishes AdvNFC source authority for the Raspberry Pi reader-agent candidate under `04_Source/reader_agent/`. The currently deployed Pi script remains active until ASTV-249 performs controlled deployment and proving.
