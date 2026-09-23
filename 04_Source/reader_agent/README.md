# AdvNFC Raspberry Pi Reader Agent

This directory contains the governed source baseline for the NFC reader agent
captured from `pi-nfc-02` under ASTV-246.

## Captured production baseline

- Runtime source: `/home/pi01/assistive_card_listener.sh`
- Captured SHA-256: `9f44b7f50a42d701a3f21b0b06b31d39bcf92cd0c8f52750f60a4d0dec067286`
- Service: `assistive-card-listener.service`
- Reader: ACS ACR122U, USB ID `072f:2200`
- UID acquisition: `nfc-list` plus the established NFCID1 AWK extraction
- Runtime dependency versions captured on pi-nfc-02:
  - `libnfc-bin 1.8.0-2`
  - `libnfc6 1.8.0-2`
  - `mosquitto-clients 2.0.11-1.2+deb12u2`
  - `curl 7.88.1-10+deb12u15`

## Behavior preserved by the governed candidate

For each newly accepted UID the agent still emits all three current outputs:

1. Home Assistant webhook `assistive_card_scan` with JSON `uid` and `reader`.
2. Non-retained MQTT event on `assistive/nfc/event` with `uid`, `reader`, and `ts`.
3. Retained raw UID on `assistive/nfc/<reader>/last_uid`.

The reader identity remains `hostname -s` unless explicitly overridden.
Polling remains 0.20 seconds, post-send debounce remains 0.80 seconds, and the
same UID becomes eligible again after eight consecutive empty polling cycles.

## Intentional extraction difference

The captured runtime embedded its MQTT password directly in the shell script.
The governed AdvNFC candidate does **not** reproduce that secret. Deployment
configuration is supplied through `/etc/advnfc/reader-agent.env`; a non-secret
example is included in this directory.

This is a security/configuration boundary only. MQTT topic names, payloads,
reader identity semantics, webhook behavior, polling, debounce, and reset
semantics are unchanged.

## Target deployment layout

- Script: `/opt/advnfc/reader_agent/advnfc_reader_agent.sh`
- Environment: `/etc/advnfc/reader-agent.env`
- systemd unit: `advnfc-reader-agent.service`

ASTV-247 establishes source authority only. Deployment and production cutover
are governed separately by ASTV-249.
