# AdvNFC Administration Interface

## Status and identity

- Provider: AdvNFC
- Interface ID: `advnfc.tag_mapping.administration`
- Interface version: `2`
- Status: candidate
- Source issues: `ASTV-324`, `ASTV-325`

This is the provider-owned boundary for reading, validating, and persisting the
AdvNFC tag-mapping model. Consumers use normalized records through this
interface and must not read, write, or depend on the YAML representation of
`advnfc_tag_mapping.yaml`.

## Transport and operations

The interface uses response-only Home Assistant services:

| Operation | Service | Input |
|---|---|---|
| Capabilities | `advnfc.get_administration_capabilities` | none |
| List | `advnfc.list_tag_mappings` | none |
| Get | `advnfc.get_tag_mapping` | `uid` |
| Query | `advnfc.query_tag_mappings` | `action_type`, `intent_id` |
| Validate document | `advnfc.validate_tag_mapping` | `candidate` containing `tag_mapping_schema_version` and complete `mappings` list |
| Validate record | `advnfc.validate_tag_mapping_record` | `mapping` |
| Create | `advnfc.create_tag_mapping` | `expected_revision`, `mapping` |
| Update | `advnfc.update_tag_mapping` | `expected_revision`, complete replacement `mapping` |
| Delete | `advnfc.delete_tag_mapping` | `expected_revision`, `uid` |

Validation calls do not write or activate state. Create, update, and delete
replace persisted state but do not activate or reload it.

## Common identity and normalized record

Every response contains `interface_id`, `interface_version`,
`tag_mapping_schema_version`, and `ok`. Read responses contain the opaque,
deterministic `revision` of the active snapshot. Validation and write responses
contain `active_revision`; successful writes additionally contain the new
`persisted_revision` and `activation_required`.

Consumers must compare revisions only for equality. Their format and derivation
are provider-owned. A write supplies `expected_revision`; a value different
from the currently persisted revision fails with `stale_revision` and does not
write. A successful write returns a new revision for a subsequent write.

Records contain canonical `uid`, `label`, optional `area_override`, and typed `action`. They are projections of the active immutable snapshot, not serialized YAML.

## Capabilities, list, get, and query

Capabilities returns supported action types and operations. List returns `count` and canonical-UID-ordered `mappings`.

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
