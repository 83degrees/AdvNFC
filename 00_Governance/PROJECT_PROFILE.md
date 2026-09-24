# PROJECT_PROFILE: AdvNFC

## Profile conformance

This profile contains the required product-profile subjects and is established under the approved Central Governance authority.

## Document status

- Governance state: current
- Product runtime state: Home Assistant NFC-entry path and the governed Raspberry Pi reader agent are deployed and active in production

## Product identity

- Product name: AdvNFC
- Repository: `83degrees/AdvNFC`
- DDR origin code: `04`

## Linear work routing

- Default Linear team: `ASTV`
- Product work container: `AdvNFC`
- Routing note: AdvNFC currently uses the existing ASTV Linear team because no dedicated AdvNFC team exists in the workspace. This does not transfer product ownership to ASTV.

## Purpose

AdvNFC is the NFC interaction and intent-production product. Its deployed Home Assistant path consumes configured NFC-reader events, filters invalid reader transitions, resolves scanned UIDs through its governed tag mapping, and submits the resulting canonical intent invocation to a downstream intent consumer through a governed interface. AdvNFC also governs the deployed Raspberry Pi reader-agent software that acquires physical NFC UIDs and publishes the established reader events consumed by Home Assistant.

## Scope

### In scope

- Raspberry Pi NFC reader-agent software, including UID acquisition, established same-card suppression/reset behavior, reader identity, and construction of the existing reader outputs.
- Reader-agent service definition and deployment configuration boundary.
- Consumption of configured NFC reader-event state from Home Assistant.
- Filtering invalid, unavailable, unknown, and recovery transitions before UID processing.
- UID normalization.
- Tag-record lookup and validation.
- AdvNFC tag-mapping ownership.
- Extraction of canonical `intent_id`.
- Extraction of an optional tag-level area override.
- Preservation of the originating Home Assistant trigger entity.
- Construction and submission of the downstream canonical intent invocation.
- AdvNFC-owned validation, observability, testing, deployment, and rollback for the NFC-to-intent-production path.

### Out of scope

- Intent-catalogue ownership or intent-record interpretation.
- Final target-area resolution and area precedence after the invocation crosses into ASTV.
- Intent routing, playback-method selection, endpoint selection, or execution dispatch.
- MediaCat or AdvMedia internals.
- Ownership of Home Assistant, the MQTT broker/infrastructure, Raspberry Pi OS, USB/platform internals, libnfc itself, or NFC reader hardware.
- ASTV execution engines or external Google Home / Google Assistant / Matter behavior.

## Ownership and boundaries

| Boundary or capability | Relationship | Owner | Notes |
| --- | --- | --- | --- |
| NFC interaction-to-intent-production pipeline | owned | AdvNFC | Includes the governed reader-agent software, reader-event consumption, filtering, UID normalization, tag lookup/validation, mapping, and invocation construction. |
| AdvNFC tag mapping | owned | AdvNFC | Maps normalized UID values to AdvNFC tag records containing the canonical downstream intent reference and optional caller area override. |
| ASTV Intent Invocation interface | consumed | ASTV | Provider-owned contract defines `intent_id`, optional `input_area_override`, optional `trigger_entity`, and failure semantics. |
| Home Assistant runtime | external | Home Assistant | AdvNFC consumes configured entities and actions; runtime truth remains external to this repository. |
| AdvNFC reader agent | owned | AdvNFC | Governed reader-agent source is deployed on `pi-nfc-02` as `advnfc-reader-agent.service`; the legacy `assistive-card-listener.service` is retired and non-authoritative. |
| MQTT broker and transport infrastructure | external | Infrastructure owner | AdvNFC publishes/consumes configured MQTT topics but does not own the broker or network transport. |
| NFC reader hardware / Raspberry Pi platform | external | Hardware / platform owners | AdvNFC owns the reader-agent software, not the ACR122U hardware, Raspberry Pi OS, USB stack, or libnfc implementation. |

## Approved architecture location

- Approved architecture location: `01_Architecture/ADVNFC_ARCHITECTURE.md`
- Governed diagram: `01_Architecture/Diagrams/ADVNFC_ARCHITECTURE.drawio`
- Architecture state: current architecture; deployed production baseline
- Material DDRs: none at bootstrap

The Markdown file is the semantic architecture authority. The diagram is its governed representation.

## Contracts provided

| Contract | Status/version | Provider/owner | Authoritative location | Local use |
| --- | --- | --- | --- | --- |
| `ADVNFC_READER_EVENT_MQTT_INTERFACE.md` | candidate v3.0.0 | AdvNFC | `03_Contracts/ADVNFC_READER_EVENT_MQTT_INTERFACE.md` | Governs reader-agent MQTT publications consumed by downstream infrastructure, including the Home Assistant reader-sensor path. |

## Contracts consumed

| Contract | Status/version | Provider/owner | Authoritative location | Local use |
| --- | --- | --- | --- | --- |
| `ASTV_INTENT_INVOCATION_INTERFACE.md` | current v1.0.0 | ASTV | `ASTV/03_Contracts/ASTV_INTENT_INVOCATION_INTERFACE.md` | Canonical downstream intent invocation from AdvNFC into `script.astv_intent_gateway`. |

The provider-owned ASTV contract is the sole operational authority for the cross-product request. AdvNFC must not maintain an authoritative duplicate.

## Product dependencies

| Dependency | Type | Owner | Governed interface/evidence | Required state | Failure boundary |
| --- | --- | --- | --- | --- | --- |
| Home Assistant | platform | Home Assistant | Future verified production evidence | Configured reader entities and required script/action surfaces available | No usable reader event reaches AdvNFC or downstream invocation cannot be issued. |
| MQTT broker / network transport | external | Infrastructure owner | `ADVNFC_READER_EVENT_MQTT_INTERFACE.md` plus production evidence | Reader-agent publications can reach Home Assistant | No reader event reaches the configured Home Assistant entities. |
| libnfc / ACR122U reader platform | external | Platform / hardware owners | ASTV-246 runtime evidence | `nfc-list` can acquire NFCID1 from the attached reader | Reader agent cannot acquire a UID. |
| ASTV | product/service | ASTV | `ASTV_INTENT_INVOCATION_INTERFACE.md` | Contracted `script.astv_intent_gateway` entry point available | Invocation fails/stops at the provider-defined ASTV boundary. |
| AdvNFC tag mapping | data | AdvNFC | Future `advnfc_tag_mapping.yaml` source baseline | Mapping file present and loadable | Unknown or invalid tag stops visibly before ASTV invocation. |

## Implementation namespace / naming identity

- Implementation namespace / naming identity: `advnfc_`

AdvNFC owns the `advnfc_` prefix for its Home Assistant scripts, automations, data files, and package naming.

Current Home Assistant implementation identities are:

- `automation.advnfc_tag_listener`
- `script.advnfc_uid_gateway`
- `script.advnfc_find_tag_record`
- `advnfc_tag_mapping.yaml`
- `packages/advnfc`

These names are the active AdvNFC Home Assistant identities following the accepted production cutover. The governed reader-agent source additionally uses `04_Source/reader_agent/`, and `advnfc-reader-agent.service` is deployed and active on `pi-nfc-02`; the legacy `assistive-card-listener.service` is retired and non-authoritative.

## Production and evidence route

- Production route: the Home Assistant NFC-entry implementation is active in `ha-starburst` and invokes ASTV through the governed Intent Invocation interface. The governed Raspberry Pi reader agent is deployed on `pi-nfc-02` as `advnfc-reader-agent.service`.
- Current production fact: AdvNFC owns and runs both the governed reader-agent software and the Home Assistant NFC-entry path; ASTV begins at the Intent Invocation boundary. The legacy `assistive-card-listener.service` is retired and non-authoritative. During ASTV-257 coexistence, `pi-nfc-02` remains on its unchanged legacy `assistive/nfc/pi-nfc-02/last_uid` topic while replacement/test readers use the candidate `advnfc/<reader>/last_uid` namespace.
- Evidence route: future AdvNFC production evidence must follow the centrally governed Production Evidence Standard.
- Secrets and mutable-state boundary: credentials, secrets, mutable Home Assistant state, and production snapshots remain outside this repository.
- Validation evidence route: Linear records governed work and validation; Git/GitHub records exact candidate and accepted repository states.

## Repository source baseline

ASTV-242 establishes the candidate AdvNFC runtime source baseline under:

- `04_Source/config/packages/advnfc/advnfc_automations.yaml`
- `04_Source/config/packages/advnfc/advnfc_scripts.yaml`
- `04_Source/config/AdvNFC/advnfc_tag_mapping.yaml`

These files are the accepted AdvNFC Home Assistant source baseline following production cutover.

ASTV-247 additionally establishes the Raspberry Pi reader-agent source baseline under:

- `04_Source/reader_agent/advnfc_reader_agent.sh`
- `04_Source/reader_agent/systemd/advnfc-reader-agent.service`
- `04_Source/reader_agent/reader-agent.env.example`

The reader-agent source preserves the captured `pi-nfc-02` behavior while moving secrets outside source control. ASTV-249 established its governed production deployment on `pi-nfc-02`.
