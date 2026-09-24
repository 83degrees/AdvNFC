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

## ASTV-257 namespace candidate

For each newly accepted UID the candidate emits one governed output:

- retained raw UID on `advnfc/<reader>/last_uid`.

The historical Home Assistant webhook `assistive_card_scan` and generic
non-retained MQTT event `assistive/nfc/event` remain removed. MQTT remains the
reader transport.

The currently deployed `pi-nfc-02` service is an explicit temporary exception:
it remains untouched on `assistive/nfc/pi-nfc-02/last_uid` until physical
retirement. This candidate is for the separately validated replacement/test
reader and must not be remotely deployed to `pi-nfc-02`.

The reader identity remains `hostname -s` unless explicitly overridden.
Polling remains 0.20 seconds, post-send debounce remains 0.80 seconds, and the
same UID becomes eligible again after eight consecutive empty polling cycles.

## Intentional extraction difference

The captured runtime embedded its MQTT password directly in the shell script.
The governed AdvNFC candidate does **not** reproduce that secret. Deployment
configuration is supplied through `/etc/advnfc/reader-agent.env`; a non-secret
example is included in this directory.

ASTV-256 removed migration-era compatibility outputs that are not part of the
Home Assistant AdvNFC consumption path. ASTV-257 now changes only the canonical
retained topic namespace to `advnfc/<reader>/last_uid`; payload, reader identity,
polling, debounce, and reset semantics remain unchanged.

## Deployment model

ASTV-255 introduces a versioned Debian package for repeatable reader-node
installation, upgrade and rollback.

Package-owned software:

- Script: `/opt/advnfc/reader_agent/advnfc_reader_agent.sh`
- Version identity: `/opt/advnfc/reader_agent/VERSION`
- systemd unit: `advnfc-reader-agent.service`
- readiness tool: `advnfc-reader-agent-check`
- configuration initializer: `advnfc-reader-agent-init`
- ACR122U udev access rule
- non-secret environment example

Node-local state remains outside package ownership:

- `/etc/advnfc/reader-agent.env`
- MQTT credentials and node-specific values

The service uses the dedicated system account `advnfc`. This removes the
packaging dependency on a particular interactive login account such as
`pi01`.

See `packaging/README.md` for build, install, upgrade, rollback and uninstall
procedures.

The ASTV-255 package is to be validated on a separate test reader device before
it is considered for any production reader deployment.


## ASTV-258 runtime profiles

Environment-specific non-secret configuration is supplied by a named YAML profile under `/etc/advnfc/profiles`. The stable selector `/etc/advnfc/active-profile.yaml` identifies the active profile.

Profiles contain MQTT host, port, username, credential reference, the governed `advnfc/{reader}/last_uid` topic pattern, and an optional reader-identity override. MQTT passwords remain separately protected under `/etc/advnfc/secrets/<credential_ref>.env`.

The reader agent resolves the selected profile at startup through `advnfc-profile runtime-shell`; it no longer contains environment-specific broker addresses or topic prefixes. Protocol behavior such as retained publication, UID payload, polling, debounce, and reset semantics remains governed code/contract behavior rather than profile-selectable behavior.

Users manage profiles with `advnfc-profile list|status|validate|switch`. Switching validates the requested profile and secret before activation and rolls back automatically if the service cannot start successfully.
