# AdvNFC Architecture

## Purpose and Sources of Truth

This document records the semantic target architecture of AdvNFC: its active components, calls, returned values, data dependencies, and external boundary.

The governed diagram at `Diagrams/ADVNFC_ARCHITECTURE.drawio` represents this semantic architecture. This document is authoritative for AdvNFC architecture and dependencies. Verified live Home Assistant YAML/configuration establishes deployed/runtime facts only, including current entity IDs, inputs, response variables, and service calls.

## Architecture Status and Timeframes

The architecture below is the target AdvNFC architecture established by ASTV-240.

It is derived directly from the current approved ASTV Phase 0 architecture. Until the separately governed extraction and cutover work completes, the active deployed implementation remains the ASTV Phase 0 implementation.

The intended carve-out is behavior-preserving. The Phase 0 semantics below are retained as closely as possible, with only:

- ownership and entity names changed from ASTV to AdvNFC; and
- the existing direct call to `script.astv_intent_gateway` formalized as consumption of the provider-owned ASTV Intent Invocation interface.

## End-to-End Flow

The active NFC path being carved out enters through external NFC input, reaches the configured reader sensors over MQTT, and passes through Tag Listener and UID Gateway before downstream ASTV processing continues through Intent Gateway.

AdvNFC receives the external NFC input through the MQTT-fed reader sensors and resolves the tag UID to its canonical `intent_id`. AdvNFC then invokes ASTV through the governed ASTV Intent Invocation interface.

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
| External NFC input | External input | Delivered over MQTT to the configured NFC reader sensors |
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

The extraction must preserve the current ASTV Phase 0 behavior.

For the same valid reader state change and equivalent tag mapping, AdvNFC must produce the same ASTV Intent Invocation values as the current ASTV Phase 0 path:

- the same `intent_id`;
- the same optional `input_area_override`;
- the same `trigger_entity`.

Functional redesign of the reader inputs, transition filtering, UID normalization, tag mapping semantics, gateway failure behavior, or ASTV area-resolution semantics is outside the initial carve-out.

## Current and Target Ownership

Until production cutover, the active Tag Listener, UID Gateway, Find Tag Record, and tag mapping remain part of the deployed ASTV Phase 0 implementation.

After successful cutover, those responsibilities move to AdvNFC under:

- `automation.advnfc_tag_listener`
- `script.advnfc_uid_gateway`
- `script.advnfc_find_tag_record`
- `advnfc_tag_mapping.yaml`

ASTV then begins at the provider-owned Intent Invocation boundary.
