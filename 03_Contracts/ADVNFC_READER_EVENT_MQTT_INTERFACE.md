# AdvNFC Reader Event MQTT Interface

## Document status

- Interface: AdvNFC Reader Event MQTT Interface
- Provider/owner: AdvNFC
- Version: 1.0.0
- Status: current candidate
- Baseline authority: captured `pi-nfc-02` runtime evidence from ASTV-246

## Purpose

This contract defines the MQTT publications emitted by the AdvNFC reader agent and consumed by downstream infrastructure, including the Home Assistant reader-sensor path.

It formalises the current production semantics only. It does not rename topics or redesign reader behavior.

## Publisher identity

The publisher is the AdvNFC reader agent running on an NFC reader node.

The default reader identity is:

`hostname -s`

For the captured production node this resolves to:

`pi-nfc-02`

The reader identity is used as the `<reader>` topic segment and in the event payload.

## Topic 1: Reader Event

### Topic

`assistive/nfc/event`

### Retain

Not retained.

### QoS

The publisher does not specify QoS to `mosquitto_pub`; therefore the client default applies.

### Payload

JSON object with exactly these current fields:

- `uid` — uppercase UID string extracted from NFCID1;
- `reader` — reader identity;
- `ts` — ISO-8601 timestamp generated at send time.

Example shape:

```json
{
  "uid": "DEADLBC",
  "reader": "pi-nfc-02",
  "ts": "2026-09-23T21:00:00+01:00"
}
```

The example is illustrative only; consumers must not treat the example values as fixed.

## Topic 2: Per-reader Last UID State

### Topic pattern

`assistive/nfc/<reader>/last_uid`

For the captured production node:

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
- the agent applies the captured post-send debounce;
- the remembered UID is cleared only after the configured consecutive-empty-poll threshold is reached.

The current captured defaults are:

- poll interval: 0.20 seconds;
- post-send debounce: 0.80 seconds;
- empty reset threshold: 8 polls.

These timing values describe current publisher behavior. Consumers must not depend on sub-second timing as a durable ordering guarantee.

## Home Assistant consumption

The current Home Assistant AdvNFC path consumes the retained per-reader state topic through configured MQTT-backed sensor entities such as:

- `sensor.pi_nfc_02_last_uid`
- `sensor.pi_nfc_99_last_uid`

Home Assistant state transitions are subsequently filtered by `automation.advnfc_tag_listener`.

The generic `assistive/nfc/event` topic is a separate publication and is not the current Tag Listener input.

## Delivery and failure boundary

AdvNFC owns construction of the topic and payload at the reader-agent boundary.

AdvNFC does not own:

- MQTT broker availability;
- network transport;
- Home Assistant MQTT integration;
- retained-message delivery performed by the broker.

The current reader agent invokes `mosquitto_pub` synchronously but does not implement an application-level acknowledgement, retry queue, or deduplication across process restarts.

A consumer must therefore not infer guaranteed exactly-once delivery from this interface.

## Consumer rules

Consumers may rely on:

- uppercase UID payloads;
- reader identity in the topic and event payload as defined above;
- retained behavior of the per-reader `last_uid` topic;
- the event topic being non-retained under the current interface.

Consumers must not infer:

- tag meaning;
- `intent_id`;
- area selection;
- ASTV routing semantics;
- physical-reader hardware details beyond the reader identity exposed by this contract;
- exactly-once delivery.

## Out of scope

This interface does not govern:

- the Home Assistant webhook output `assistive_card_scan`;
- tag-to-intent mapping;
- ASTV intent invocation;
- MQTT credentials;
- broker configuration;
- future topic namespace redesign.

## Compatibility

Version 1.0.0 formalises the captured production behavior. Any incompatible change to topic structure, payload shape, retain semantics, or reader identity semantics requires governed compatibility assessment and a contract version change.
