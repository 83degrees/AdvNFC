# AdvNFC Reader Event MQTT Interface

## Document status

- Interface: AdvNFC Reader Event MQTT Interface
- Provider/owner: AdvNFC
- Version: 3.0.0
- Status: candidate
- Change authority: ASTV-257
- Production status: candidate coexistence contract; `pi-nfc-02` remains on the legacy production topic until physical retirement, while replacement/test readers use the new AdvNFC namespace

## Purpose

This contract defines the MQTT publication emitted by the AdvNFC reader agent and consumed by downstream infrastructure, including the Home Assistant reader-sensor path.

Version 3.0.0 establishes the AdvNFC-owned MQTT namespace for replacement/test readers while preserving a temporary, explicit legacy exception for the still-active production reader `pi-nfc-02`. MQTT remains the reader transport.

The migration does not change UID payload, retain behavior, reader identity, polling, debounce, reset semantics, tag meaning, or the downstream AdvNFC/ASTV invocation boundary.

## Publisher identity

The publisher is the AdvNFC reader agent running on an NFC reader node.

The default reader identity is:

`hostname -s`

The reader identity is used as the `<reader>` topic segment.

## Per-reader Last UID State

### Canonical topic pattern

`advnfc/<reader>/last_uid`

For a replacement/test reader whose reader identity is `pi-nfc-99`:

`advnfc/pi-nfc-99/last_uid`

### Temporary production legacy exception

Until `pi-nfc-02` is physically retired, its already-deployed reader agent remains unchanged and continues to publish:

`assistive/nfc/pi-nfc-02/last_uid`

`pi-nfc-02` must not be remotely reconfigured to the new namespace under ASTV-257.

### Retain

Retained.

### QoS

The publisher does not specify QoS to `mosquitto_pub`; therefore the client default applies.

### Payload

Raw uppercase UID string only.

Example:

```text
DEADLBC
```

No JSON wrapper is used on this topic.

## Publication semantics

A UID is eligible for publication when the reader agent observes a non-empty UID that differs from its currently remembered UID.

After publication:

- the UID is remembered;
- repeated reads of the same continuously present card are suppressed;
- the agent applies the configured post-send debounce;
- the remembered UID is cleared only after the configured consecutive-empty-poll threshold is reached.

The current defaults remain:

- poll interval: 0.20 seconds;
- post-send debounce: 0.80 seconds;
- empty reset threshold: 8 polls.

Consumers must not depend on sub-second timing as a durable ordering guarantee.

## Home Assistant consumption

The AdvNFC Home Assistant path consumes retained per-reader state through configured MQTT-backed sensor entities. During the coexistence period:

- `sensor.pi_nfc_02_last_uid` continues to consume `assistive/nfc/pi-nfc-02/last_uid`;
- the replacement/test reader sensor consumes the equivalent `advnfc/<reader>/last_uid` topic for that reader identity.

Both sensor entities may feed `automation.advnfc_tag_listener`. A physical reader publishes on exactly one namespace, so coexistence must not be implemented by dual-publishing the same scan from one reader.

## Removed compatibility outputs

The retained Version 2.0.0 cleanup removes these migration-era reader-agent outputs:

- Home Assistant webhook `assistive_card_scan`;
- non-retained generic MQTT event `assistive/nfc/event`.

Neither output is part of the current governed AdvNFC Tag Listener input path.

The webhook removal also removes the reader-agent dependency on `curl`.

## Delivery and failure boundary

AdvNFC owns construction of the topic and payload at the reader-agent boundary.

AdvNFC does not own:

- MQTT broker availability;
- network transport;
- Home Assistant MQTT integration;
- retained-message delivery performed by the broker.

The reader agent invokes `mosquitto_pub` synchronously but does not implement an application-level acknowledgement, retry queue, or deduplication across process restarts.

A consumer must therefore not infer guaranteed exactly-once delivery from this interface.

## Consumer rules

Consumers may rely on:

- uppercase UID payloads;
- reader identity in the retained topic as defined above;
- retained behavior of the per-reader `last_uid` topic.

Consumers must not infer:

- tag meaning;
- `intent_id`;
- area selection;
- ASTV routing semantics;
- physical-reader hardware details beyond the reader identity exposed by this contract;
- exactly-once delivery.

## Migration and rollback

ASTV-257 uses reader-by-reader coexistence rather than dual publication:

1. leave `pi-nfc-02` unchanged on `assistive/nfc/pi-nfc-02/last_uid`;
2. configure the replacement/test reader to publish `advnfc/<reader>/last_uid`;
3. update only that replacement/test reader's Home Assistant MQTT consumer to the new topic while retaining the legacy `pi-nfc-02` consumer;
4. validate NFC -> MQTT -> Home Assistant -> AdvNFC -> ASTV on the replacement/test reader;
5. physically replace `pi-nfc-02` only after acceptance;
6. retire the legacy consumer/topic authority only after the physical swap is accepted.

Rollback before physical cutover is to stop using the replacement/test reader and restore its previous governed package/configuration and Home Assistant consumer mapping. `pi-nfc-02` remains available on the unchanged legacy path throughout that validation period.

## Out of scope

This interface does not govern:

- tag-to-intent mapping;
- ASTV intent invocation;
- MQTT credentials;
- broker configuration;
- reader runtime-profile selection, which is governed separately by ASTV-258.

## Compatibility

Version 3.0.0 changes the canonical retained topic from `assistive/nfc/<reader>/last_uid` to `advnfc/<reader>/last_uid`, so MQTT consumers must be migrated reader by reader.

The payload, retain semantics, reader identity semantics, polling, debounce, and reset behavior are unchanged. The legacy `pi-nfc-02` exception is temporary migration compatibility, not the new canonical interface.

Any later incompatible change to topic structure, payload shape, retain semantics, or reader identity semantics requires a further governed compatibility assessment and contract version change.
