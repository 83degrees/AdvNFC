# AdvNFC Architecture

## Purpose and authority

This document defines the semantic target architecture of AdvNFC.

AdvNFC owns the NFC interaction-to-intent-production path. It consumes configured Home Assistant reader events, filters unusable reader transitions, resolves a scanned UID through AdvNFC-owned tag data, validates the resulting tag record, and invokes the provider-owned ASTV Intent Invocation interface.

This document is authoritative for AdvNFC product architecture. The governed diagram at `Diagrams/ADVNFC_ARCHITECTURE.drawio` is its visual representation. Exact deployed Home Assistant configuration and production evidence establish runtime facts only.

## Architecture status

The architecture below is the bootstrap target established by ASTV-240. It is not yet the deployed production state.

At bootstrap, the equivalent active behavior still resides in ASTV Phase 0. Subsequent governed extraction and cutover work will implement this architecture under the AdvNFC namespace and then retire the duplicated ASTV ownership only after successful proving.

The bootstrap therefore changes product authority and target architecture only; it does not itself alter Home Assistant runtime behavior.

## End-to-end target flow

The target flow is:

`External NFC interaction` → `MQTT / configured HA reader sensor` → `AdvNFC Tag Listener` → `AdvNFC UID Gateway` → `AdvNFC Find Tag Record` → `AdvNFC Tag Mapping` → `ASTV Intent Invocation interface` → `ASTV Intent Gateway`

AdvNFC ends at the contracted ASTV invocation boundary.

## External NFC input and reader delivery

NFC reader hardware and MQTT transport are external infrastructure.

AdvNFC consumes configured Home Assistant sensor state changes representing NFC UID reads. The initial extraction is expected to preserve the current configured reader sources unless separately changed through governed work.

Reader hardware identity, MQTT topic implementation, and transport ownership remain outside AdvNFC.

## AdvNFC Tag Listener

Target entity:

`automation.advnfc_tag_listener`

Responsibilities:

- listen to the configured NFC reader entities;
- reject transitions to or from `unknown` or `unavailable` at the Home Assistant trigger boundary;
- allow genuine valid UID-bearing state changes to continue;
- supply the normalized downstream invocation context to `script.advnfc_uid_gateway`, including:
  - scanned `uid`;
  - originating `trigger_entity`.

The initial extraction must preserve the existing stale-UID replay protection semantics rather than redesigning them.

## AdvNFC UID Gateway

Target entity:

`script.advnfc_uid_gateway`

Inputs:

- `uid`
- `trigger_entity`

Responsibilities:

1. call `script.advnfc_find_tag_record` with the supplied UID;
2. stop visibly when no tag record is found;
3. stop visibly when the tag record contains no usable `intent_id`;
4. extract:
   - canonical `intent_id`;
   - optional tag-level `area_override`;
5. invoke the provider-owned ASTV Intent Invocation interface with:
   - `intent_id`;
   - `input_area_override` from the optional tag-level `area_override`;
   - `trigger_entity`.

The UID Gateway does not resolve ASTV intent records, resolve the final target area, select an ASTV intent engine, or perform downstream execution.

## AdvNFC Find Tag Record

Target entity:

`script.advnfc_find_tag_record`

Input:

- `uid`

Return:

- tag-record response

Data dependency:

- `advnfc_tag_mapping.yaml`

The function normalizes the supplied UID using string conversion, trimming, and uppercasing, then performs exact lookup against the AdvNFC tag mapping.

An unknown UID returns an empty record. The lookup function remains side-effect-free.

## AdvNFC Tag Mapping

Target data source:

`advnfc_tag_mapping.yaml`

The mapping is owned by AdvNFC.

Each usable tag record supplies at least:

- `intent_id`

and may optionally supply:

- `area_override`

The mapping does not contain ASTV intent-record internals, execution configuration, MediaCat records, endpoint definitions, or other downstream orchestration data.

## ASTV Intent Invocation boundary

AdvNFC consumes the provider-owned ASTV contract:

`ASTV/03_Contracts/ASTV_INTENT_INVOCATION_INTERFACE.md`

The boundary request is:

- `intent_id` — required;
- `input_area_override` — optional;
- `trigger_entity` — optional.

No UID, tag record, MQTT topic, or reader-protocol data crosses the product boundary.

ASTV owns all semantics after the invocation crosses into `script.astv_intent_gateway`, including:

- intent-catalogue lookup;
- ASTV intent-record interpretation;
- final target-area resolution;
- intent routing;
- preparation and selection;
- execution.

## Area semantics at the boundary

AdvNFC may provide an explicit tag-level caller override as `input_area_override` and may preserve the originating `trigger_entity`.

AdvNFC does not resolve the final ASTV target area.

Under the consumed ASTV contract, ASTV owns the precedence:

1. caller `input_area_override`;
2. ASTV intent-record `area_override`;
3. Home Assistant area of `trigger_entity`.

This precedence must remain a provider concern and must not be duplicated into AdvNFC.

## Failure boundaries

AdvNFC owns visible stopping behavior for:

- filtered invalid/recovery reader transitions;
- unknown UID / missing tag record;
- invalid tag record with no usable `intent_id`;
- inability to construct the contracted downstream invocation.

Once the contracted invocation is issued, downstream failure behavior belongs to ASTV and its consumed/provider contracts.

AdvNFC does not automatically select another tag, intent, area, or execution path after failure.

## Migration invariant

The initial extraction must be behavior-preserving.

For the same usable reader event and equivalent tag mapping, the AdvNFC implementation must produce the same ASTV Intent Invocation request as the current ASTV Phase 0 path:

- same canonical `intent_id`;
- same optional caller area override;
- same originating trigger entity.

Functional redesign of reader protocol, tag schema, area precedence, or ASTV behavior is outside the initial carve-out.

## Current versus target ownership

### Current deployed state before cutover

ASTV Phase 0 currently owns and runs the active Tag Listener, UID Gateway, Find Tag Record, and tag mapping.

### Target AdvNFC state

AdvNFC owns equivalent responsibilities under the `advnfc_` namespace and invokes ASTV only through the provider-owned Intent Invocation interface.

### Retirement rule

ASTV Phase 0 source and ownership are retired only after the AdvNFC implementation is deployed and successfully proven through the separate governed cutover work.
