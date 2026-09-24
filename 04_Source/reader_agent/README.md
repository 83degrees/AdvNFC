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

`curl` was present in the captured legacy baseline solely for the Home Assistant
webhook output. ASTV-256 removes that compatibility output from the candidate,
so `curl` is no longer a reader-agent runtime dependency.

## ASTV-256 cleanup candidate

For each newly accepted UID the candidate emits one governed output:

- retained raw UID on `assistive/nfc/<reader>/last_uid`.

The historical Home Assistant webhook `assistive_card_scan` and generic
non-retained MQTT event `assistive/nfc/event` are removed from this candidate.
MQTT remains the reader transport.

The reader identity remains `hostname -s` unless explicitly overridden.
Polling remains 0.20 seconds, post-send debounce remains 0.80 seconds, and the
same UID becomes eligible again after eight consecutive empty polling cycles.

## Intentional extraction difference

The captured runtime embedded its MQTT password directly in the shell script.
The governed AdvNFC candidate does **not** reproduce that secret. Deployment
configuration is supplied through `/etc/advnfc/reader-agent.env`; a non-secret
example is included in this directory.

ASTV-256 additionally removes migration-era compatibility outputs that are not
part of the Home Assistant AdvNFC consumption path. The retained per-reader MQTT
topic, payload, reader identity, polling, debounce, and reset semantics remain
unchanged. The namespace rename is intentionally deferred to ASTV-257.

## Target deployment layout

- Script: `/opt/advnfc/reader_agent/advnfc_reader_agent.sh`
- Environment: `/etc/advnfc/reader-agent.env`
- systemd unit: `advnfc-reader-agent.service`

ASTV-249 established the governed production reader-agent deployment. ASTV-256
is a repository/Beta cleanup candidate only and must not be deployed to
`pi-nfc-02`; runtime validation will use a separate test reader device.
