# PROJECT_PROFILE: AdvNFC

## Profile conformance

This profile contains the required product-profile subjects and is established under the approved Central Governance authority.

## Document status

- Governance state: current
- Product runtime state: Home Assistant NFC-entry path is deployed and active in production; reader events are supplied by the external AdvNFC Reader Agent product

## Product identity

- Product name: AdvNFC
- Repository: `83degrees/AdvNFC`
- DDR origin code: `04`

## Linear work routing

- Default Linear team: `ASTV`
- Product work container: `AdvNFC`
- Routing note: AdvNFC currently uses the existing ASTV Linear team because no dedicated AdvNFC team exists in the workspace. This does not transfer product ownership to ASTV.

## Purpose

AdvNFC is the Home Assistant NFC interaction and intent-production product. Its deployed path consumes configured NFC-reader events supplied through the provider-owned AdvNFC Reader Event MQTT Interface, filters invalid reader transitions, resolves scanned UIDs through its governed tag mapping, and submits the resulting canonical intent invocation to a downstream intent consumer through a governed interface.

## Scope

### In scope

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
- Ownership of Home Assistant or external Google Home / Google Assistant / Matter behavior.
- ASTV execution engines.
- AdvNFC Reader Agent runtime source, Debian packaging, service configuration, release lifecycle, runtime profiles, or provider-contract ownership.
- NFC reader hardware, Raspberry Pi OS, USB/platform internals, libnfc, MQTT broker implementation, or network transport.

## Ownership and boundaries

| Boundary or capability | Relationship | Owner | Notes |
| --- | --- | --- | --- |
| Home Assistant NFC-event-to-intent-production pipeline | owned | AdvNFC | Begins at configured Home Assistant reader-event state and includes filtering, UID normalization, tag lookup/validation, mapping, and invocation construction. |
| AdvNFC tag mapping | owned | AdvNFC | Maps normalized UID values to AdvNFC tag records containing the canonical downstream intent reference and optional caller area override. |
| ASTV Intent Invocation interface | consumed | ASTV | Provider-owned contract defines `intent_id`, optional `input_area_override`, optional `trigger_entity`, and failure semantics. |
| Home Assistant runtime | external | Home Assistant | AdvNFC consumes configured entities and actions; runtime truth remains external to this repository. |
| AdvNFC Reader Agent | consumed external product | AdvNFC Reader Agent | Publishes reader events under the provider-owned MQTT interface; its runtime, package, service, configuration, release lifecycle, and contract authority are outside this repository. |
| MQTT broker and transport infrastructure | external | Infrastructure owner | AdvNFC consumes configured Home Assistant reader entities and does not own reader publication, the broker, or network transport. |

## Approved architecture location

- Approved architecture location: `01_Architecture/ADVNFC_ARCHITECTURE.md`
- Governed diagram: `01_Architecture/Diagrams/ADVNFC_ARCHITECTURE.drawio`
- Architecture state: current architecture; deployed production baseline
- Material DDRs: none at bootstrap

The Markdown file is the semantic architecture authority. The diagram is its governed representation.

## Contracts provided

| Contract | Status/version | Consumers | Authoritative location | Purpose |
| --- | --- | --- | --- | --- |
| `ADVNFC_ADMINISTRATION_READ_INTERFACE.md` | candidate interface v1 | Future AdvNFC management consumers | `03_Contracts/ADVNFC_ADMINISTRATION_READ_INTERFACE.md` | Read-only capability, list, get and downstream-target query boundary over normalized active tag mappings. |

## Contracts consumed

| Contract | Status/version | Provider/owner | Authoritative location | Local use |
| --- | --- | --- | --- | --- |
| `ADVNFC_READER_EVENT_MQTT_INTERFACE.md` | candidate v3.0.0 | AdvNFC Reader Agent | `AdvNFC-Reader-Agent/03_Contracts/ADVNFC_READER_EVENT_MQTT_INTERFACE.md` | Governs external reader-agent MQTT publications consumed by the configured Home Assistant reader-sensor path. |
| `ASTV_INTENT_INVOCATION_INTERFACE.md` | current v1.0.0 | ASTV | `ASTV/03_Contracts/ASTV_INTENT_INVOCATION_INTERFACE.md` | Canonical downstream intent invocation from AdvNFC into `script.astv_intent_gateway`. |

Each provider-owned contract is the sole authority for its cross-product interface. AdvNFC must not maintain an authoritative duplicate.

## Product dependencies

| Dependency | Type | Owner | Governed interface/evidence | Required state | Failure boundary |
| --- | --- | --- | --- | --- | --- |
| Home Assistant | platform | Home Assistant | Future verified production evidence | Configured reader entities and required script/action surfaces available | No usable reader event reaches AdvNFC or downstream invocation cannot be issued. |
| AdvNFC Reader Agent | product/service | AdvNFC Reader Agent | `AdvNFC-Reader-Agent/03_Contracts/ADVNFC_READER_EVENT_MQTT_INTERFACE.md` plus provider production evidence | Contracted reader publications reach the configured Home Assistant entities | No usable reader event reaches AdvNFC. |
| MQTT broker / network transport | external | Infrastructure owner | Provider-owned reader-event contract plus production evidence | Reader-agent publications can reach Home Assistant | No reader event reaches the configured Home Assistant entities. |
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
- `advnfc.get_administration_capabilities`
- `advnfc.list_tag_mappings`
- `advnfc.get_tag_mapping`
- `advnfc.query_tag_mappings`
- `packages/advnfc`

These names are the active AdvNFC Home Assistant identities following the accepted production cutover. Reader-agent service identities belong to the external AdvNFC Reader Agent product.

## Deployable units

| Deployable unit | Type | Authoritative source | Target | Mechanism | Detailed authority and runbook |
| --- | --- | --- | --- | --- | --- |
| AdvNFC Home Assistant custom integration | `haos_integration` | `custom_components/advnfc/**` | Home Assistant `/config/custom_components/advnfc/**` | `hacs` | `HOME_ASSISTANT_INTEGRATION_DEPLOYMENT_STANDARD.md` and `08_Deployment/ADVNFC_HACS_DEPLOYMENT_RUNBOOK.md` |
| AdvNFC Home Assistant configuration | `haos_config` | `04_Implementation/haos/source/config/**` | `ha-starburst` Home Assistant `/config/**` | `operator_selected` | `HOME_ASSISTANT_CONFIG_DEPLOYMENT_STANDARD.md` and `08_Deployment/ADVNFC_HAOS_CONFIG_DEPLOYMENT_RUNBOOK.md` |

The HACS integration uses the approved root-source exception. The pointer at
`04_Implementation/haos/source/config/custom_components/advnfc/README.md`
keeps the canonical deployment map navigable without duplicating integration
source. Root `hacs.json` and `.github/workflows/hacs-release.yml` are thin,
platform-required entrypoints; project-controlled HACS release machinery is at
`04_Implementation/haos/packaging/hacs/**`.

The Home Assistant configuration unit includes the AdvNFC package files and
tag mapping. Its required top-level `advnfc:` activation in
`/config/configuration.yaml` remains an operator-managed target step; the
repository does not introduce a different runtime configuration model.

## Production and evidence route

- Production route: the Home Assistant NFC-entry implementation is active in `ha-starburst`, consumes configured reader state supplied through the provider-owned reader-event interface, and invokes ASTV through the governed Intent Invocation interface.
- Current production fact: AdvNFC begins at the Home Assistant reader-event state and owns the path through canonical ASTV invocation. AdvNFC Reader Agent owns reader acquisition and MQTT publication. During ASTV-257 coexistence, `pi-nfc-02` remains on its unchanged legacy `assistive/nfc/pi-nfc-02/last_uid` topic while replacement/test readers use the candidate `advnfc/<reader>/last_uid` namespace.
- Evidence route: future AdvNFC production evidence must follow the centrally governed Production Evidence Standard.
- Secrets and mutable-state boundary: credentials, secrets, mutable Home Assistant state, and production snapshots remain outside this repository.
- Validation evidence route: Linear records governed work and validation; Git/GitHub records exact candidate and accepted repository states.

## Repository source baseline

The authoritative Home Assistant integration source is only
`custom_components/advnfc/**`; its manifest remains version `1.0.1`.

The authoritative operator-selected Home Assistant configuration baseline is:

- `04_Implementation/haos/source/config/packages/advnfc/advnfc_automations.yaml`
- `04_Implementation/haos/source/config/packages/advnfc/advnfc_scripts.yaml`
- `04_Implementation/haos/source/config/AdvNFC/advnfc_tag_mapping.yaml`

These structural locations preserve the accepted Home Assistant runtime
behaviour. Reader-agent implementation, packaging, tests, deployment material,
and provider-contract authority reside only in `83degrees/AdvNFC-Reader-Agent`.
