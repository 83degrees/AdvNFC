# AdvNFC Reader Event MQTT Interface

## Document status

- Interface: AdvNFC Reader Event MQTT Interface
- Provider/owner: AdvNFC
- Version: 2.0.0
- Status: candidate
- Change authority: ASTV-256
- Production status: not deployed; production remains on the accepted 1.0.0 behavior until separately validated and promoted

## Purpose

This contract defines the MQTT publication emitted by the AdvNFC reader agent and consumed by downstream infrastructure, including the Home Assistant reader-sensor path.

Version 2.0.0 removes migration-era compatibility outputs that are not part of the current AdvNFC Home Assistant consumption path. MQTT remains the reader transport.

This contract does not rename the retained topic namespace. Namespace migration is governed separately by ASTV-257.

## Publisher identity

The publisher is the AdvNFC reader agent running on an NFC reader node.

The default reader identity is:

`hostname -s`

The reader identity is used as the `<reader>` topic segment.

## Per-reader Last UID State

### Topic pattern

`assistive/nfc/<reader>/last_uid`

For the current production reader:

`assistive/nfc/pi-nfc-02/last_uid`

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

The AdvNFC Home Assistant path consumes the retained per-reader state topic through configured MQTT-backed sensor entities such as:

- `sensor.pi_nfc_02_last_uid`
- `sensor.pi_nfc_99_last_uid`

Home Assistant state transitions are subsequently filtered by `automation.advnfc_tag_listener`.

## Removed compatibility outputs

Version 2.0.0 removes these migration-era reader-agent outputs:

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

## Out of scope

This interface does not govern:

- tag-to-intent mapping;
- ASTV intent invocation;
- MQTT credentials;
- broker configuration;
- future topic namespace redesign.

## Compatibility

Version 2.0.0 is intentionally incompatible with version 1.0.0 for consumers of the removed webhook or generic event output.

Consumers of the retained `assistive/nfc/<reader>/last_uid` topic retain the same topic pattern, payload, retain semantics, reader identity semantics, polling, debounce, and reset behavior.

Any later incompatible change to the retained topic structure, payload shape, retain semantics, or reader identity semantics requires a further governed compatibility assessment and contract version change.
