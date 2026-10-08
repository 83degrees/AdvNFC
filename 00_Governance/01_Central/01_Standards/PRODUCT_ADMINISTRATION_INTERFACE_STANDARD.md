# PRODUCT_ADMINISTRATION_INTERFACE_STANDARD.md

**Standard:** Product Administration Interface Standard
**Version:** v1.0.0
**Status:** Approved
**Approval tag:** `product-administration-interface-standard-v1.0.0`
**Approval date:** 2026-10-08
**Lifecycle:** Independent

## 1. Purpose, Scope and Authority

This Standard defines the common external administration-interface principles for independently managed products that choose to expose local or cross-product administration capabilities.

It is a **product-applicable Standard** maintained authoritatively at:

`/Standards/Product/PRODUCT_ADMINISTRATION_INTERFACE_STANDARD.md`

It is projected unchanged into governed product repositories at:

`00_Governance/01_Central/01_Standards/PRODUCT_ADMINISTRATION_INTERFACE_STANDARD.md`

`CENTRAL_GOVERNANCE.md` remains the higher constitutional authority. Each provider-owned contract remains authoritative for that provider's concrete operations, transport, records, schemas and compatibility promises. Product architecture and the applicable Project Profile remain authoritative for product responsibilities and boundaries.

This Standard governs external interoperability invariants. It does not define or require a common manager, user interface, storage format, YAML representation, service framework, code structure, integration implementation, deployment mechanism or shared database.

## 2. Normative Language and Applicability

The key words **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT** and **MAY** are normative.

A product remains independently administrable. Installing, removing or making another optional product unavailable MUST NOT remove the provider's independent administration path or corrupt unrelated provider state.

A new administration interface claiming conformance to this Standard MUST satisfy the mandatory baseline in this Standard from its first supported version.

An interface that predates this Standard is not silently redefined. It MAY adopt the Standard through backward-compatible additions or a documented compatibility profile. It MUST NOT claim conformance until its provider-owned contract identifies how the mandatory baseline and common error categories are exposed. Any required provider or consumer remediation is separate governed work.

## 3. Provider Ownership and Interface Boundary

The provider owns:

- its administration interface and provider-owned contract;
- its capability and operation vocabulary;
- its data and schema meaning;
- its persistence, activation and revision mechanisms;
- authorization enforcement at its boundary; and
- provider-specific diagnostics and implementation details.

A consumer MUST use published provider capabilities and normalized interface records. It MUST NOT depend on undocumented internal storage, filenames, schema serialization, process structure or UI implementation.

A conforming interface MAY use Home Assistant actions or services, HTTP, IPC or another documented transport. Transport differences do not weaken the semantic requirements in this Standard.

## 4. Mandatory Baseline

Every conforming interface MUST expose:

1. capability and operation discovery;
2. interface identity and version information;
3. applicable schema identity and version information;
4. structured success and error outcomes; and
5. administration status.

Record list, get, query, create, update and delete operations are optional. Candidate validation, staging, activation and cross-product query operations are optional. Every optional operation MUST be advertised before a consumer relies on it.

Discovery and status MAY be separate operations or one operation when the combined response satisfies both contracts. Their concrete operation names are provider-owned.

## 5. Discovery, Identity and Version Negotiation

Capability discovery MUST return or unambiguously provide:

- a provider-unique `interface_id`;
- an `interface_version` with an identifiable major version;
- supported operation or capability identifiers;
- each schema identity and schema version material to consumer input or output; and
- whether the interface is read-only or supports managed mutation and activation.

Interface, schema and revision identities are independent:

- `interface_version` versions the external administration contract;
- each schema version identifies the applicable data vocabulary or normalized record shape; and
- a revision identifies one provider state for equality or concurrency purposes.

A provider MUST NOT reuse a revision as an interface or schema version. Consumers MUST treat provider revisions as opaque unless the provider-owned contract explicitly promises more.

An interface version MAY be an integer major version or a semantic version. A consumer MUST select behavior from discovered versions and capabilities rather than infer it from product version, storage format or operation presence alone.

Capability identifiers MUST be stable within an interface major version. A provider MAY add optional capabilities compatibly. Absence of an optional capability means unsupported, not failed.

## 6. Common Outcome and Error Semantics

Every new conforming operation MUST expose a structured outcome equivalent to:

```yaml
ok: true | false
```

A failed outcome MUST expose a stable machine-readable error category and a diagnostic message equivalent to:

```yaml
ok: false
error:
  code: <common category or documented provider code>
  message: <diagnostic>
```

Consumers MUST branch on machine-readable codes and MUST NOT branch on diagnostic message text.

The common error categories are:

| Category | Meaning |
| --- | --- |
| `invalid_request` | Input is malformed, incomplete or violates the operation contract. |
| `not_found` | The requested provider-owned record or resource does not exist. |
| `permission_denied` | The caller lacks the required read or manage authority. |
| `unsupported_operation` | The requested capability or operation is not advertised or supported for the negotiated interface. |
| `stale_revision` | A guarded mutation does not match current persisted state. |
| `dependency_unavailable` | An advertised result depends on another provider or platform capability that is currently unavailable. |
| `activation_failed` | A persisted candidate could not become active and the previous valid active state was retained. |

A provider MAY define more specific codes. New interfaces SHOULD expose the common category as `error.code` and MAY expose a provider-specific refinement separately. A pre-existing interface MAY retain its stable wire code and publish a deterministic mapping to the common category. Compatibility adoption MUST NOT silently replace a code on which existing consumers rely.

Expected negative results MUST remain distinguishable from execution failure. For example, a successful query with no matches SHOULD return an empty result, while lookup of a required named record MAY return `not_found`.

A failed operation MUST NOT be represented as partial success. If an operation deliberately supports partial results, that behavior and each per-item outcome MUST be explicit in the provider-owned contract and advertised capability.

## 7. Administration Status and State Identity

Administration status MUST report enough normalized information for a consumer to determine:

- whether the provider is available for administration;
- whether mutation is supported;
- whether activation is applicable;
- whether persisted and active state differ;
- whether activation is required; and
- the last material activation failure, where one remains relevant.

A mutable provider with separately persisted and active state MUST expose distinct `persisted_revision` and `active_revision`, or semantically equivalent opaque identities, plus an explicit activation-required indicator.

A read-only provider or a provider for which persistence and activation are inseparable MAY report activation as not applicable. It MUST NOT imply that an unapplied persisted candidate is active.

Status MUST distinguish a provider's unavailable persisted state, invalid persisted candidate and retained valid active state where those conditions can occur. Diagnostic details MAY be provider-specific.

## 8. Read and Manage Authorization

Providers MUST distinguish read authority from manage authority wherever the platform or provider supports that distinction.

Read authority covers discovery, status and advertised read/query operations. Manage authority covers validation inputs that reveal protected configuration, persistence, mutation, staging, activation and other state-changing administration operations.

A provider MUST enforce authorization at its own boundary. A consumer or common manager MUST NOT be trusted as the sole enforcement point.

Authorization failure MUST use `permission_denied` or a documented compatible mapping. Responses MUST NOT expose secrets, credentials, repository tokens or protected internal paths merely to support administration.

This Standard does not mandate one authentication mechanism or credential store.

## 9. Optional Validation, Mutation and Concurrency

Where candidate or record validation is advertised, it MUST be side-effect free: validation MUST NOT persist, activate or partially mutate provider state.

Where mutation is advertised:

- the provider-owned contract MUST state whether operations replace complete records, apply patches or replace a complete candidate;
- an accepted mutation MUST be atomic at the promised boundary;
- rejection MUST leave the promised persisted and active states unchanged; and
- concurrent-write protection MUST use an opaque expected revision or an equally explicit provider-owned mechanism where concurrent writers can exist.

A stale guarded mutation MUST fail with `stale_revision` or a documented compatible mapping and MUST NOT write.

CRUD is not a mandatory capability. A provider MAY expose validation and activation while an external provider-owned client manages storage, provided ownership and transaction boundaries are explicit.

## 10. Persistence, Staging and Activation

For a mutable provider with separate save and activation phases:

- saving or staging MUST NOT be represented as activation;
- a successful save MUST identify the resulting persisted revision;
- status MUST indicate that activation is required while persisted and active revisions differ;
- activation MUST validate the complete candidate needed by the provider before changing active state;
- successful activation MUST switch the promised active boundary atomically; and
- activation failure MUST retain the previous valid active state and return `activation_failed` or a documented compatible mapping.

A provider MAY combine persistence and activation only when its contract explicitly promises one atomic operation with no separately observable staged state.

Rollback of provider state, filesystem history and backup retention are not implied by activation failure safety. The provider-owned contract MUST identify who owns restoration when those capabilities exist.

## 11. Cross-Product References and Queries

The product that stores a reference owns that reference and its validation at the boundary it promises.

A provider MUST NOT write reverse-reference state into another product merely to support discovery. Reverse relationships are obtained by querying the product that owns the referencing records, when that product advertises a suitable query capability.

A reference MAY identify another provider's stable published identity. It MUST NOT depend on the referenced provider's undocumented storage or implementation.

Structural validation of a reference and live validation of the referenced target are separate capabilities. A provider MUST state which it performs. Structural acceptance MUST NOT be represented as proof that the optional referenced product or target is currently available.

Cross-product queries are optional and MUST be discovered. A consumer MUST NOT assume that all installed products implement them.

## 12. Optional-Provider Failure Isolation

An unavailable optional provider MUST disable only features that depend on that provider.

The consumer or referencing provider MUST:

- report `dependency_unavailable` or a documented compatible mapping when the missing dependency prevents the requested operation;
- preserve unrelated administration and runtime functions;
- preserve stored references unless provider-owned policy explicitly authorizes their removal;
- avoid destructive cleanup solely because the optional provider is temporarily unavailable; and
- permit recovery when the provider returns without requiring an unrelated product migration.

A provider MUST distinguish unsupported capability from temporary dependency unavailability.

## 13. Compatibility and Evolution

Backward-compatible changes include adding optional fields, capabilities, operations, error detail or supported schema versions when existing meanings and required fields remain intact. Such additions do not require a new interface major version, although the provider MAY advance a minor version.

A breaking change includes removing or renaming a promised operation or required field, changing a field's type or meaning, weakening atomicity or retained-active-state guarantees, changing revision comparison semantics, or replacing a stable error code without a compatibility mapping.

A breaking change MUST:

1. use a new interface major version;
2. include an explicit consumer-impact assessment;
3. provide an agreed transition for affected consumers;
4. preserve existing supported versions for that transition where reasonably required; and
5. avoid interpreting a consumer's use of an older discovered version as consent to the new behavior.

Consumers MUST negotiate from discovery and tolerate unknown optional fields and capabilities. They MUST NOT invoke an undiscovered optional operation.

A stored-schema version change is not by itself an administration-interface break. It becomes an interface break only when the external administration contract changes incompatibly.

## 14. Existing Interface Compatibility Assessment

### 14.1 MediaCat administration interface v1.0.0

The reviewed MediaCat contract already provides capability discovery, an independent administration-interface version, a stored-schema version, side-effect-free validation, transactional complete-registry reload and retention of the prior active registry on reload failure.

Its current contract intentionally leaves file writes, atomic file replacement, history and restoration with MediaCat Manager. It does not currently expose the complete common `ok` outcome, error taxonomy, general administration-status model or active/persisted revision model defined for new conforming interfaces.

This Standard does not change MediaCat behavior or transfer storage ownership. Compatibility adoption may be additive, including a documented common-category mapping and additional discovery/status fields. Any incompatible remediation requires separate governed provider and consumer work.

### 14.2 AdvNFC administration interface v3

The reviewed AdvNFC candidate contract already provides interface and schema identity, capability and operation discovery, normalized reads and queries, side-effect-free validation, atomic guarded persisted mutation, opaque revisions, explicit persisted-versus-active status and failure-safe activation.

Its existing provider codes include more specific categories such as `invalid_query`, `invalid_candidate`, `persisted_state_unavailable` and `atomic_write_failed`. These remain provider-owned compatibility promises. Adoption of this Standard may add a common-category mapping without silently replacing them.

This assessment records AdvNFC's reviewed provider state and does not reclassify the candidate contract as approved or change its runtime behavior. Any remaining conformance or compatibility work belongs to a separate governed issue.

## 15. Governance, Adoption and Completion

A product claiming conformance MUST record the provider-owned contract and applicable interface version in its normal authoritative product artefacts.

Per-product compatibility review, provider implementation, consumer implementation and migration are not performed by approval of this Standard. They require separately governed issues with the applicable change classes and workflow.

This Standard follows the independent centrally governed Standard lifecycle. Its approval and projection do not by themselves merge, release, distribute or activate any product runtime change.
