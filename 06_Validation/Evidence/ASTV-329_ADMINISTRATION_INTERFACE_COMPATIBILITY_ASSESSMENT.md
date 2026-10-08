# ASTV-329 — AdvNFC administration-interface compatibility assessment

## Assessment result

AdvNFC administration interface v3 is substantially compatible with the approved Product Administration Interface Standard v1.0.0. Its provider-owned CRUD, validation, revision, persisted-versus-active, activation, and reverse-reference query design are conformant independent implementations; they do not need refactoring for visual or structural uniformity.

Two genuine gaps prevent a conformance claim:

1. the provider contract does not publish a deterministic mapping from its existing error codes to the Standard's common categories; and
2. the implementation does not enforce a distinct manage-authority boundary even though Home Assistant provides an admin-service wrapper.

The contract remains explicitly `candidate`. That is a readiness constraint, not a third runtime incompatibility. No runtime code is changed by this assessment.

## Authority and evidence baseline

The governed execution path was loaded from `AGENTS.md`. The constitutional authority is Central Governance v11.14.0, and `00_Governance/PROJECT_PROFILE.md` is the product-context authority. Central Governance identifies provider-owned contracts as authority for concrete interfaces and the Product Administration Interface Standard as authority for common interoperability.

| Artefact | Evidence identity |
| --- | --- |
| `AGENTS.md` | `c40aa2207fcc6ac146ae26243d3a3d2326850817` |
| `00_Governance/01_Central/CENTRAL_GOVERNANCE.md` | v11.14.0; `c429a4adba986148e897f39a53a713a29c5e17a0` |
| `00_Governance/PROJECT_PROFILE.md` | `87c64aafbf65ad266e3e5d274b7c07f1972c72c7` |
| `PRODUCT_ADMINISTRATION_INTERFACE_STANDARD.md` | approved v1.0.0; `51a94d75fc166b980a182d184b4985299d044ccf` |
| `ADVNFC_ADMINISTRATION_READ_INTERFACE.md` | candidate v3; `66e02693768f3fa02c36ca7e6ed2117dfebbc398` |
| `ADVNFC_ARCHITECTURE.md` | `cd240d2ded50df218ea4b0ce3f1dbd10b253d411` |
| `custom_components/advnfc/__init__.py` | `e4d46f0c1ac6376210364ac95e3265f77d5d5d7f` |
| `custom_components/advnfc/mapping.py` | `5849bf75a1287b0a0c55b2732fc9481455c68a08` |
| `custom_components/advnfc/services.yaml` | `5bb2796df18436a01540a67623e11eaf911046a4` |
| `05_Tests/test_advnfc_administration.py` | `f215c58ea041bb80fbd1e924c779213ac222596e` |

ASTV-327 is Done and records approval and projection of the Standard into AdvNFC. For the authorization finding, Home Assistant core `homeassistant/helpers/service.py`, blob `47ab34d1c063449e27725fdf284097cab0cd896b`, lines 962–1020 enforces administrative user context and exposes `async_register_admin_service`.

## Clause-by-clause matrix

| Standard clause | Contract and implementation evidence | Assessment | Consumer/remediation impact |
| --- | --- | --- | --- |
| §2 Applicability | Contract lines 3–9 identify v3 as `candidate`. Standard §14.2 preserves current codes and requires separate conformance work. | **Readiness constraint** | Do not claim conformance before remediation and contract review. |
| §3 Provider boundary | Contract lines 8–14 prohibit dependence on `advnfc_tag_mapping.yaml`; architecture lines 144–182 assign the boundary to AdvNFC. | **Compliant** | No common manager, storage format, or code structure is required. |
| §4 Mandatory baseline | Contract lines 16–36 list capabilities/status. `mapping.py` 386–414 emits identity, schema version, `ok`, action types, and operations; 564–589 adds state. | **Compliant** | No operation rename or shared transport required. |
| §5 Discovery | `mapping.py` 19–35 defines interface v3, schema v1, types, and operations; 408–414 returns them. | **Compliant** | Operations unambiguously advertise mutation and activation. |
| §5 Identity separation | Contract 38–53 distinguishes interface, schema, and opaque revisions. `mapping.py` 220–228 derives the revision; 386–391 exposes identities. | **Compliant** | Consumers compare revisions only for equality. |
| §6 Structured outcomes | Contract 125–139 defines `ok`, stable code/message, and branching rule. `mapping.py` 394–402 and 578–592 implement it. | **Compliant** | Provider-specific codes may remain stable. |
| §6 Common categories | Contract 125–135 lists provider codes but has no deterministic mapping to the common categories. | **Gap G1** | Add mapping without replacing wire codes: ASTV-337. |
| §6 Negative results | Contract 62–67 specifies successful empty query and `not_found`; `mapping.py` 427–487 implements it. | **Compliant** | No change. |
| §7 Status/state identity | Contract 55–61 and 91–123 specifies state. `mapping.py` 564–589 and 636–718 exposes revisions, activation need, state, counts, and last error while retaining active state. | **Compliant** | Interface availability is also observable through HA service discovery. |
| §8 Authorization | Contract has no policy. `__init__.py` 155–225 registers reads, validation, mutation, and activation uniformly with `hass.services.async_register`; no provider check exists. HA supports an admin-service wrapper. | **Gap G2** | Runtime/contract remediation: ASTV-338. Non-admin callers may be affected. |
| §9 Validation | Contract 32–36 and 72–89 says validation does not write. `mapping.py` 594–625 validates without persistence; tests 139–159 cover it. | **Compliant** | No change. |
| §9 Mutation atomicity | Contract defines complete replacement and full-candidate validation. `mapping.py` 727–822 validates the complete candidate; 341–364 uses fsync plus `os.replace`. | **Compliant** | YAML remains provider-owned. |
| §9 Concurrency | Contract 44–49; `mapping.py` 737–754 checks `expected_revision` under the write lock. Tests 263–272 cover rejection. | **Compliant** | No change. |
| §10 Save/activation | Contract 91–123 defines the transaction. `mapping.py` 680–718 activates under the lock; 817–822 saves without changing active state. Tests 160–262 cover save, activation, failure, and retry. | **Compliant** | No uniform implementation refactor justified. |
| §10 Restoration | Contract 105–108 states no hidden rollback/history store. | **Compliant** | No change. |
| §11 References/queries | Contract 62–70 states structural validation only and no ASTV catalogue lookup. `mapping.py` 450–487 implements reverse query; architecture 180–182 preserves isolation. | **Compliant** | Intended independent behavior, not a missing live check. |
| §12 Optional provider isolation | No administration operation promises live ASTV validation; stored references and local administration remain available without ASTV. | **Compliant / not triggered** | ASTV-337 should document why `dependency_unavailable` is not currently emitted. |
| §13 Compatibility | Contract 136–139 requires a version change and impact assessment for breaking changes. | **Compliant** | ASTV-337 is additive; ASTV-338 must assess non-admin callers. |
| §14.2 Existing AdvNFC profile | Standard 237–243 records the reviewed v3 design and preserves provider codes. | **Compliant migration path** | Confirms G1 is compatibility documentation, not error rewriting. |
| §15 Conformance claim | Project Profile lists candidate v3 and architecture points to the provider contract. | **Readiness constraint** | Locations are correct; claim waits for remediation and approval. |

## Backward compatibility and consumer impact

No declared consumer requires a breaking change to CRUD, normalized records, schema v1, revision equality, persisted/active status, or activation. The Project Profile identifies only future management consumers. The interface remains independently administrable and does not acquire a compulsory manager or live ASTV dependency.

ASTV-337 is additive contract work: existing consumers continue branching on provider codes while a deterministic compatibility table supplies the common category. No interface-major change is indicated.

ASTV-338 may newly reject calls from non-admin Home Assistant user contexts. System-context calls remain compatible with Home Assistant's admin-service wrapper. Before Beta, the remediation must inventory actual callers and decide whether candidate status and the absence of supported consumers permit additive enforcement or require a new interface major/transition.

## Remediation disposition

| Finding | Linear remediation | Route |
| --- | --- | --- |
| G1 — missing common error-category mapping | ASTV-337 | `Change: Contract`, WF-02 |
| G2 — missing read/manage authorization enforcement | ASTV-338 | `Change: Code` + `Change: Contract`, WF-01 |

No other remediation is justified. Provider-owned service names, YAML persistence, record shape, revision derivation, write locking, explicit reload activation, and structural-only ASTV reference validation are permitted independent choices.

## Acceptance-criteria result

| Criterion | Result |
| --- | --- |
| Matrix cites exact contract and implementation evidence. | **Satisfied** — sections, line ranges, and immutable blobs recorded. |
| Genuine gaps distinguished from permitted implementation. | **Satisfied** — G1/G2 isolated; compatible choices retained. |
| Remediation and backward-compatibility impacts identified. | **Satisfied** — ASTV-337 and ASTV-338 created. |
| Approved documentation and governance evidence captured. | **Satisfied** — authority, Standard identity, ASTV-327, contract, architecture, implementation, tests, and platform authorization evidence recorded. |

## Validation note

This is a static documentation assessment against immutable source identities. Existing tests were inspected as implementation evidence but were not rerun because ASTV-329 changes no runtime behavior. Final document review, repository integrity checks, and merge remain subject to WF-02 gates.
