# PROJECT_PROFILE: AdvNFC

## Profile conformance

This profile contains the required product-profile subjects and is established under the approved Central Governance authority.

## Document status

- Governance state: candidate under ASTV-240
- Product bootstrap state: repository authority being established; no AdvNFC runtime is deployed by this issue

## Product identity

- Product name: AdvNFC
- Repository: `83degrees/AdvNFC`
- DDR origin code: `04`

## Linear work routing

- Default Linear team: `ASTV`
- Product work container: `AdvNFC`
- Routing note: AdvNFC currently uses the existing ASTV Linear team because no dedicated AdvNFC team exists in the workspace. This does not transfer product ownership to ASTV.

## Purpose

AdvNFC is the Home Assistant NFC interaction and intent-production product. It consumes configured NFC-reader events, filters invalid reader transitions, resolves scanned UIDs through its governed tag mapping, and submits the resulting canonical intent invocation to a downstream intent consumer through a governed interface.

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
- Ownership of Home Assistant, MQTT infrastructure, NFC reader hardware, or their transport protocols.
- ASTV execution engines or external Google Home / Google Assistant / Matter behavior.

## Ownership and boundaries

| Boundary or capability | Relationship | Owner | Notes |
| --- | --- | --- | --- |
| NFC interaction-to-intent-production pipeline | owned | AdvNFC | Includes reader-event consumption, filtering, UID normalization, tag lookup/validation, mapping, and invocation construction. |
| AdvNFC tag mapping | owned | AdvNFC | Maps normalized UID values to AdvNFC tag records containing the canonical downstream intent reference and optional caller area override. |
| ASTV Intent Invocation interface | consumed | ASTV | Provider-owned contract defines `intent_id`, optional `input_area_override`, optional `trigger_entity`, and failure semantics. |
| Home Assistant runtime | external | Home Assistant | AdvNFC consumes configured entities and actions; runtime truth remains external to this repository. |
| MQTT and NFC reader delivery | external | MQTT / reader infrastructure | AdvNFC consumes configured reader-sensor state changes and does not own transport or hardware. |

## Approved architecture location

- Approved architecture location: `01_Architecture/ADVNFC_ARCHITECTURE.md`
- Governed diagram: `01_Architecture/Diagrams/ADVNFC_ARCHITECTURE.drawio`
- Architecture state: candidate target architecture under ASTV-240; not yet deployed
- Material DDRs: none at bootstrap

The Markdown file is the semantic architecture authority. The diagram is its governed representation.

## Contracts provided

AdvNFC provides no cross-product contract at bootstrap.

## Contracts consumed

| Contract | Status/version | Provider/owner | Authoritative location | Local use |
| --- | --- | --- | --- | --- |
| `ASTV_INTENT_INVOCATION_INTERFACE.md` | v1.0.0 candidate/current with ASTV-241 acceptance | ASTV | `ASTV/03_Contracts/ASTV_INTENT_INVOCATION_INTERFACE.md` | Canonical downstream intent invocation from AdvNFC into `script.astv_intent_gateway`. |

The provider-owned ASTV contract is the sole operational authority for the cross-product request. AdvNFC must not maintain an authoritative duplicate.

## Product dependencies

| Dependency | Type | Owner | Governed interface/evidence | Required state | Failure boundary |
| --- | --- | --- | --- | --- | --- |
| Home Assistant | platform | Home Assistant | Future verified production evidence | Configured reader entities and required script/action surfaces available | No usable reader event reaches AdvNFC or downstream invocation cannot be issued. |
| MQTT and NFC reader infrastructure | external | Infrastructure owner | Future production evidence | Reader state changes delivered to configured Home Assistant entities | No input event reaches AdvNFC. |
| ASTV | product/service | ASTV | `ASTV_INTENT_INVOCATION_INTERFACE.md` | Contracted `script.astv_intent_gateway` entry point available | Invocation fails/stops at the provider-defined ASTV boundary. |
| AdvNFC tag mapping | data | AdvNFC | Future `advnfc_tag_mapping.yaml` source baseline | Mapping file present and loadable | Unknown or invalid tag stops visibly before ASTV invocation. |

## Implementation namespace / naming identity

- Implementation namespace / naming identity: `advnfc_`

AdvNFC owns the `advnfc_` prefix for its Home Assistant scripts, automations, data files, and package naming.

Planned initial implementation identities are:

- `automation.advnfc_tag_listener`
- `script.advnfc_uid_gateway`
- `script.advnfc_find_tag_record`
- `advnfc_tag_mapping.yaml`
- `packages/advnfc`

These names identify target AdvNFC ownership. They do not claim that production ownership has moved before the separately governed extraction and cutover work completes.

## Production and evidence route

- Production route: not established by ASTV-240. Initial deployment and cutover are governed by later AdvNFC carve-out issues.
- Current production fact: the active NFC-entry implementation remains within ASTV until the governed extraction and production cutover complete.
- Evidence route: future AdvNFC production evidence must follow the centrally governed Production Evidence Standard.
- Secrets and mutable-state boundary: credentials, secrets, mutable Home Assistant state, and production snapshots remain outside this repository.
- Validation evidence route: Linear records governed work and validation; Git/GitHub records exact candidate and accepted repository states.

## Repository source baseline

No AdvNFC runtime source baseline is established by ASTV-240. Runtime source is introduced by the separately governed extraction issue after product authority and the ASTV invocation contract are accepted.
