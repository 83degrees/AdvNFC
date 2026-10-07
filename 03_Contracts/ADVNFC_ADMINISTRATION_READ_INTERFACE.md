# AdvNFC Administration Interface

## Status and identity

- Provider: AdvNFC
- Interface ID: `advnfc.tag_mapping.administration`
- Interface version: `3`
- Status: candidate
- Source issues: `ASTV-324`, `ASTV-325`, `ASTV-326`

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
