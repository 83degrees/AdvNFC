# AdvNFC Administration Interface

## Status and identity

- Provider: AdvNFC
- Interface ID: `advnfc.tag_mapping.administration`
- Interface version: `3`
- Status: candidate
- Source issues: `ASTV-324`, `ASTV-325`, `ASTV-326`, `ASTV-337`, `ASTV-338`

This is the provider-owned boundary for reading, validating, persisting, and
activating the AdvNFC tag-mapping model. Consumers use normalized records
through this interface and must not read, write, or depend on the YAML
representation of `advnfc_tag_mapping.yaml`.

## Transport and operations

The interface uses response-only Home Assistant services:

| Operation | Service | Input |
|---|---|---|
| Capabilities | `advnfc.get_administration_capabilities` | none |
| Status | `advnfc.get_administration_status` | none |
| List | `advnfc.list_tag_mappings` | none |
| Get | `advnfc.get_tag_mapping` | `uid` |
| Query | `advnfc.query_tag_mappings` | `action_type`, `intent_id` |
| Validate document | `advnfc.validate_tag_mapping` | `candidate` containing `tag_mapping_schema_version` and complete `mappings` list |
| Validate record | `advnfc.validate_tag_mapping_record` | `mapping` |
| Create | `advnfc.create_tag_mapping` | `expected_revision`, `mapping` |
| Update | `advnfc.update_tag_mapping` | `expected_revision`, complete replacement `mapping` |
| Delete | `advnfc.delete_tag_mapping` | `expected_revision`, `uid` |
| Activate/reload | `advnfc.reload_tag_mapping` | none |

Validation calls do not write or activate state. Create, update, and delete
replace persisted state but do not activate it. Reload is the sole
provider-owned managed activation operation.

## Authorization policy

AdvNFC distinguishes read authority from manage authority at its Home Assistant
service boundary:

| Authority | Operations |
|---|---|
| Runtime/read | `find_tag_record`, capabilities, status, list, get, and query |
| Manage | validate document, validate record, create, update, delete, and activate/reload |

Runtime/read operations retain the ordinary Home Assistant service-call
authorization path. Authenticated Home Assistant users who can call services
may use the advertised administration reads; trusted Home Assistant
system-context calls with no `user_id` remain supported. `find_tag_record` is a
runtime lookup rather than an administration mutation and remains callable
through the ordinary service path.

Manage operations are registered through Home Assistant's supported
admin-service mechanism. A user-context call must resolve to a Home Assistant
administrator. Unknown-user and non-administrator calls are rejected by Home
Assistant before the AdvNFC handler runs, so they do not inspect the area
registry, read or validate the persisted mapping, mutate it, or activate it.
Trusted Home Assistant system-context calls with no `user_id` remain permitted
by that mechanism.

An authorization rejection is a platform-raised service-call failure, not a
normal AdvNFC response payload. Its common Product Administration Interface
category is `permission_denied`; it therefore does not add or replace an
AdvNFC `error.code` in interface v3. Consumers must handle the Home Assistant
authorization failure separately from a returned `ok: false` provider outcome.

This enforcement may newly reject an undocumented caller that invokes a manage
operation with a non-administrator user context. No current consumer is
declared for the candidate interface, and the repository contains no automation
that invokes `reload_tag_mapping`; the deployment runbook is its only local
caller reference. A future manager must use an administrator user context or an
approved trusted Home Assistant system context. Because no supported v3
consumer behavior is withdrawn and the response wire contract is unchanged,
this enforcement does not require an interface-major transition.

## Common identity and normalized record

Every response contains `interface_id`, `interface_version`,
`tag_mapping_schema_version`, and `ok`. Manager-facing responses expose
`active_revision`, `persisted_revision`, and `activation_required`. Read/query
responses retain `revision` as an alias of the active revision for
compatibility. Revisions are opaque and deterministic.

Consumers must compare revisions only for equality. Their format and derivation
are provider-owned. A write supplies `expected_revision`; a value different
from the currently persisted revision fails with `stale_revision` and does not
write. A successful write returns a new revision for a subsequent write.

Records contain canonical `uid`, `label`, optional `area_override`, and typed
`action`. They are projections of the active immutable snapshot, not serialized
YAML.

## Capabilities, status, list, get, and query

Capabilities returns supported action types, operations, and the currently
known active/persisted state. Status validates the authoritative persisted
candidate and returns `state: active` when its revision equals the active
snapshot, or `state: activation_required` when they differ. It also returns
`active_count`, `persisted_count`, and `last_activation_error`. An invalid or
unreadable persisted candidate returns `persisted_invalid` or
`persisted_unavailable` while continuing to identify the retained active
revision. List returns `count` and canonical-UID-ordered `mappings`.

Get trims and uppercases UID input. A known UID returns `mapping`; a valid missing UID returns `not_found`; a value that does not normalize to non-blank alphanumeric form returns `invalid_query`.

Query version 1 accepts `action_type: astv_intent` and a structurally valid `intent_id`; both are trimmed and lowercased. It returns normalized `query`, `count`, and `mappings`. No matches is successful with an empty collection. Unsupported types or malformed targets return `invalid_query`.

AdvNFC validates identifier structure and active mapping equality only. It does not read the ASTV catalogue or guarantee downstream intent existence.

## Validation and mutation semantics

Complete-candidate validation accepts the schema version and a full list of
normalized administration records. Record validation accepts one proposed
record. Both apply the complete closed schema-v1 rules without writing.

Create fails when the normalized UID exists. Update and delete fail when it
does not exist. Every accepted mutation validates the complete resulting
schema-v1 candidate before one atomic replacement of the authoritative
persisted file.

Successful mutations deliberately leave the active immutable snapshot
unchanged. Runtime routing and active read/query results therefore remain
unchanged until a separate provider-owned activation operation succeeds.
`activation_required` makes the persisted/active separation explicit.

A rejected candidate, stale revision, missing/existing-record conflict, or
failed atomic replacement leaves both persisted and active state unchanged.

## Activation and end-to-end transaction semantics

`advnfc.reload_tag_mapping` reads and validates the complete authoritative
persisted document under the same provider-owned lock used for writes. Only a
fully valid snapshot is swapped into active state. Success returns
`operation: activate`, `state: active`, equal active and persisted revisions,
`activation_required: false`, and the active mapping count.

Activation failure is a response, not a partial state change. It returns
`ok: false`, the retained `active_revision`, `activation_required: true`, a
stable error code, and `state: persisted_invalid` or
`persisted_unavailable`. The previously active valid snapshot continues to
serve runtime routing and read/query calls. No hidden rollback or history store
is created.

The complete manager transaction model is:

1. validation failure returns `invalid_candidate`; nothing is persisted or
   activated;
2. stale-write rejection returns `stale_revision`; nothing is persisted or
   activated;
3. save success returns a new persisted revision and leaves the old active
   revision in service with `activation_required: true`;
4. activation success makes that complete persisted revision active atomically;
5. activation failure retains the prior active snapshot and exposes the failure
   through status. After the persisted candidate or its dependencies are
   corrected, the consumer retries the same reload operation; a successful
   retry clears `last_activation_error`.

A consumer must refresh status after another actor may have written or
activated state. A save response is not evidence of activation, and an
activation response is not a substitute for checking the intended active
revision.

## Error semantics and compatibility

Errors retain the common identity and return:

```yaml
ok: false
query: {}
error:
  code: invalid_query | invalid_candidate | duplicate_uid | not_found | already_exists | stale_revision | persisted_state_unavailable | atomic_write_failed
  message: <diagnostic>
```

Consumers branch on `error.code`, not `message`. Compatible additions may add
optional fields. Removing or changing an operation, field, action type, error
code, normalization meaning, revision semantics, or atomicity guarantee
requires an interface-version change and governed consumer-impact assessment.

### Common error-category compatibility mapping

Interface v3 predates the Product Administration Interface Standard and retains
the provider-specific `error.code` values above as its wire contract. It does
not add a common-category response field. A consumer that needs the Standard's
common taxonomy derives it deterministically from the failed operation and the
provider code, in this order:

1. A failed `activate` operation maps to `activation_failed`, whether its
   retained provider code is `invalid_candidate`, `duplicate_uid`, or
   `persisted_state_unavailable`. The provider code continues to identify the
   root cause while `activation_failed` identifies the failed transaction and
   retained prior active state.
2. Every other failed operation uses the following mapping.

| Provider `error.code` | Common category | Applies to | Compatibility meaning |
|---|---|---|---|
| `invalid_query` | `invalid_request` | Get and query | The input is malformed or violates the supported operation contract. An unadvertised `action_type` is an invalid parameter to the advertised query operation; it is not an unsupported operation. |
| `invalid_candidate` | `invalid_request` | Status, validation, create, update, and delete | The submitted or persisted record, document, UID, schema, or complete resulting candidate violates the AdvNFC contract. The activation override above applies when this code is returned by `activate`. |
| `duplicate_uid` | `invalid_request` | Status and validation | The submitted or persisted complete candidate violates UID uniqueness. The activation override above applies when this code is returned by `activate`. |
| `not_found` | `not_found` | Get, update, and delete | The requested active or persisted AdvNFC mapping does not exist. A query with no matches remains a successful empty result. |
| `already_exists` | `invalid_request` | Create | The create request violates the requirement that its canonical UID not already exist. |
| `stale_revision` | `stale_revision` | Create, update, and delete | The guarded mutation does not match the current persisted revision and does not write. |
| `persisted_state_unavailable` | `dependency_unavailable` | Status, create, update, and delete | The advertised operation depends on the provider's persisted-state/platform capability, which cannot currently be read or validated. The activation override above applies when this code is returned by `activate`. |
| `atomic_write_failed` | `dependency_unavailable` | Create, update, and delete | The provider's atomic persistence/platform capability failed before the authoritative file was replaced. |

The mapping is exhaustive for interface v3's current provider codes. Operation
context is part of the mapping because the same retained root-cause code can
describe ordinary input validation or failure of the distinct activation
transaction. Consumers must not infer the common category from diagnostic
message text.

The remaining Standard categories have these current dispositions:

- `permission_denied` is represented by Home Assistant's platform-raised
  authorization failure for a denied manage operation. It is not an emitted
  AdvNFC response payload or provider `error.code`; the provider handler does
  not run for the rejected call.
- `unsupported_operation` is not currently produced as an AdvNFC error code.
  Consumers discover support through the capabilities operation and must not
  invoke absent operations. An unsupported query `action_type` is
  `invalid_query` / `invalid_request`, while an unknown Home Assistant service
  is outside this response contract.
- `dependency_unavailable` is produced only through the compatibility mapping
  for `persisted_state_unavailable` and `atomic_write_failed`. AdvNFC performs
  structural ASTV-reference validation and no administration operation depends
  on live ASTV availability, so ASTV unavailability does not produce this
  category.
- `activation_failed` is produced through the operation-context mapping above;
  the wire response retains the root provider code and the prior valid active
  snapshot.

This compatibility profile is additive documentation only. Existing response
fields, provider codes, interface version, operation behavior, and consumer
branching remain unchanged. Declared consumers are future AdvNFC management
consumers, so there is no existing declared consumer migration. New consumers
may normalize outcomes with this table while continuing to branch on the
provider code when AdvNFC-specific detail is required. The interface remains
`candidate`; this mapping does not by itself approve the contract or complete
the contract's governed approval path.
