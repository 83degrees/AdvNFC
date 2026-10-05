# AdvNFC Architecture

## Purpose and Sources of Truth

This document records the semantic target architecture of AdvNFC: its active components, calls, returned values, data dependencies, and external boundary.

The governed diagram at `Diagrams/ADVNFC_ARCHITECTURE.drawio` represents this semantic architecture. This document is authoritative for AdvNFC architecture and dependencies. Verified live Home Assistant YAML/configuration establishes deployed/runtime facts only, including current entity IDs, inputs, response variables, and service calls.

## Architecture Status and Timeframes

The Home Assistant portion of this architecture is the deployed AdvNFC runtime established by the completed ASTV Phase 0 carve-out. ASTV now begins at the provider-owned Intent Invocation boundary.

The schema-v1 tag-mapping loader, immutable snapshot, normalized typed-action
record, and Select Tag Action component described below are the proposed
ASTV-299 target state. Until the accepted ASTV-299 candidate is deployed and
validated through the WF-01 Beta route, production continues to use the current
direct tag-to-intent mapping path.

ASTV-247 extended AdvNFC source authority upstream to the Raspberry Pi reader-agent software captured from `pi-nfc-02`. ASTV-249 subsequently deployed and proved that governed reader-agent baseline in production as `advnfc-reader-agent.service`.

ASTV-249 deployed the governed reader-agent baseline as `advnfc-reader-agent.service` on `pi-nfc-02`; the legacy `assistive-card-listener.service` is retired and non-authoritative. ASTV-256 removed the migration-era Home Assistant webhook and generic MQTT event outputs from the governed candidate. ASTV-257 changes the canonical retained topic namespace for replacement/test readers to `advnfc/<reader>/last_uid` while keeping `pi-nfc-02` frozen on its legacy production topic until physical retirement. MQTT remains the reader transport.

## End-to-End Flow

The current production flow is:

1. A physical NFC tag is read by the ACR122U attached to the Raspberry Pi reader node.
2. The reader agent acquires the NFCID1 through `nfc-list`, normalizes it to uppercase, applies same-card suppression/reset behavior, and publishes the retained per-reader MQTT state.
3. The retained per-reader MQTT state is consumed by Home Assistant and represented by the configured reader sensor. The canonical ASTV-257 topic is `advnfc/<reader>/last_uid`; during coexistence `pi-nfc-02` remains on `assistive/nfc/pi-nfc-02/last_uid`.
4. AdvNFC Tag Listener filters invalid/recovery transitions and calls AdvNFC UID Gateway.
5. AdvNFC resolves the governed schema-v1 tag mapping into a typed action, selects the supported action route, and invokes ASTV through the provider-owned Intent Invocation interface.

ASTV-249 established the governed production reader-agent deployment on `pi-nfc-02`. ASTV-256 is not to be deployed to that production reader; its cleaned candidate will be validated on a separate test reader device before any later production promotion is considered.

## Raspberry Pi Reader Agent

### Physical Reader and UID Acquisition

The reader agent runs on a Raspberry Pi with an attached ACS ACR122U. It uses the external `libnfc` tool `nfc-list` and extracts the NFCID1 using the captured AWK expression, producing an uppercase UID.

The reader identity defaults to `hostname -s`. The captured `pi-nfc-02` runtime uses:

- polling interval: 0.20 seconds;
- post-send debounce: 0.80 seconds;
- same-card suppression: do not re-send the same UID while continuously present;
- reset rule: clear the remembered UID after eight consecutive empty polls.

### Reader Output

The MQTT publication is governed by:

`03_Contracts/ADVNFC_READER_EVENT_MQTT_INTERFACE.md`

For each newly accepted UID, the ASTV-257 candidate publishes retained MQTT state on `advnfc/<reader>/last_uid` containing the raw uppercase UID.

The deployed `pi-nfc-02` reader is not upgraded by ASTV-257 and remains on `assistive/nfc/pi-nfc-02/last_uid` until physical retirement. Home Assistant therefore supports both reader-specific paths during coexistence, with each physical reader publishing on only one namespace. The migration-era Home Assistant webhook and generic MQTT event remain removed.

### Reader-Agent Deployment Boundary

AdvNFC owns the reader-agent source and its systemd/service configuration. Raspberry Pi OS, USB/platform behavior, the ACR122U hardware, `libnfc`, network transport, and MQTT broker remain external dependencies.

Deployment-specific configuration is supplied outside source control. The MQTT password is not stored in the repository.

### Reader-Agent Runtime Profiles

ASTV-258 separates environment-specific configuration from reader-agent code. Named schema-v1 YAML profiles are node-local under `/etc/advnfc/profiles`, with `/etc/advnfc/active-profile.yaml` as the single authoritative selector.

A profile contains non-secret MQTT host, port, username, credential reference, the governed `advnfc/{reader}/last_uid` topic pattern, and an optional reader identity override. The MQTT password is resolved separately from `/etc/advnfc/secrets/<credential_ref>.env`.

The `advnfc-profile` management command provides `list`, `status`, `validate`, and `switch`. Switching validates the candidate profile and secret before activation, changes the selector atomically, restarts the reader service, verifies activation, and restores the previous profile if activation fails.

Profiles do not control retained behavior, QoS, UID semantics, polling, debounce, reset behavior, tag meaning, or downstream ASTV behavior. Those remain governed by the reader code and interfaces.

### Reader-Agent Packaging and Update Model

ASTV-255 establishes the target deployment model for the Raspberry Pi reader agent.

The governed software unit is a versioned Debian package named `advnfc-reader-agent`. The package is built from the governed repository source and is intended to be distributed initially as a versioned GitHub Release artefact. An APT repository is not required for the initial deployment model and may be introduced later if reader-node scale or update frequency justifies it.

The package owns:

- `/opt/advnfc/reader_agent/advnfc_reader_agent.sh`;
- `/opt/advnfc/reader_agent/VERSION`;
- `advnfc-reader-agent.service`;
- the ACR122U udev access rule;
- the `advnfc-reader-agent-check` readiness command;
- the `advnfc-reader-agent-init` configuration initializer;
- a non-secret example environment file.

Node-local state is outside package ownership:

- `/etc/advnfc/reader-agent.env`;
- MQTT credentials;
- node-specific broker values;
- any future selected runtime profile or local overrides.

Package installation and upgrade must not overwrite node-local configuration or secrets.

The package creates a dedicated `advnfc` system account and runs the reader service under that identity rather than relying on a host-specific login account. The package also installs an ACR122U udev rule for USB vendor/product `072f:2200` so the service account has a deterministic hardware-access boundary.

Required runtime dependencies are declared by the Debian package and installed through the operating-system package manager. The initial dependency set includes the NFC and MQTT client tooling required by the governed reader agent plus the utilities used for deterministic readiness checks.

A fresh package install enables but does not start the reader service before node-local configuration exists. An existing active installation is restarted after an upgrade so the new governed software version becomes active while preserving the external configuration.

The installed software identity is recorded in `/opt/advnfc/reader_agent/VERSION`, including both package version and source Git commit. This provides traceability from a reader node back to the governed repository/release.

`advnfc-reader-agent-check` is the mandatory readiness mechanism before first service start and after package changes. It checks:

- required commands;
- the dedicated service account;
- presence of node-local configuration and replacement of the example MQTT password;
- detection of the ACR122U USB device;
- successful `nfc-list` communication while running as the same `advnfc` service identity;
- service enabled/active state as operational diagnostics.

Rollback uses a previously retained governed `.deb` artefact installed explicitly with package-manager downgrade support. Uninstall removes governed software/service ownership while deliberately preserving `/etc/advnfc/`.

This packaging model does not alter MQTT topic/payload semantics, tag meaning, or the downstream AdvNFC/ASTV boundary. Those remain governed independently.

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
| ACR122U + Raspberry Pi platform | External hardware/platform | Provides physical NFC reads to the governed reader-agent software |
| `libnfc` / `nfc-list` | External runtime dependency | Produces NFCID1 input consumed by the reader agent |
| AdvNFC reader agent | AdvNFC-owned software | Acquires UID, applies captured suppression/reset behavior, and emits the retained per-reader MQTT state |
| MQTT broker / network transport | External infrastructure | Carries reader-agent MQTT publications defined by `ADVNFC_READER_EVENT_MQTT_INTERFACE.md` to Home Assistant |
| `sensor.pi_nfc_02_last_uid`, `sensor.pi_nfc_99_last_uid` | MQTT-fed Home Assistant sensors | State-change inputs evaluated by AdvNFC - Tag Listener; transitions to or from `unknown` or `unavailable` are excluded at the Home Assistant trigger boundary before UID Gateway invocation |
| `advnfc_tag_mapping.yaml` | Data source | Closed schema-v1 candidate loaded and validated into one immutable active AdvNFC mapping snapshot |
| ASTV Intent Invocation interface | External product contract | AdvNFC invokes `script.astv_intent_gateway` with `intent_id`, optional `input_area_override`, and optional `trigger_entity` |

## Interface Naming and Return Boundaries

Exact established names are preserved where they describe the existing Phase 0 behavior. In particular:

- `uid`
- `trigger_entity`
- `tag_record_response`
- `tag_record`
- `action.type`
- `intent_id`
- `input_area_override`

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

ASTV begins at the provider-owned Intent Invocation boundary.

ASTV-249 established the AdvNFC reader-agent production baseline. ASTV-257 changes are validated only on the separate replacement/test reader; `pi-nfc-02` remains frozen on the legacy namespace until physical retirement.
