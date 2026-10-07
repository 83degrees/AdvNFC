# AdvNFC Administration Read Interface

## Status and identity

- Provider: AdvNFC
- Interface ID: `advnfc.tag_mapping.administration`
- Interface version: `1`
- Status: candidate
- Source issue: `ASTV-324`

This is the provider-owned boundary for reading the active AdvNFC tag-mapping model. Consumers must use this interface and must not read `advnfc_tag_mapping.yaml` or depend on its YAML representation.

## Transport and operations

The interface uses response-only Home Assistant services:

| Operation | Service | Input |
|---|---|---|
| Capabilities | `advnfc.get_administration_capabilities` | none |
| List | `advnfc.list_tag_mappings` | none |
| Get | `advnfc.get_tag_mapping` | `uid` |
| Query | `advnfc.query_tag_mappings` | `action_type`, `intent_id` |

Calls are read-only and do not write, activate, or reload the mapping.

## Common identity and normalized record

Every response contains `interface_id`, `interface_version`, `tag_mapping_schema_version`, and `ok`. The interface version identifies this consumer contract; the schema version identifies the active mapping model.

Records contain canonical `uid`, `label`, optional `area_override`, and typed `action`. They are projections of the active immutable snapshot, not serialized YAML.

## Capabilities, list, get, and query

Capabilities returns supported action types and operations. List returns `count` and canonical-UID-ordered `mappings`.

Get trims and uppercases UID input. A known UID returns `mapping`; a valid missing UID returns `not_found`; a value that does not normalize to non-blank alphanumeric form returns `invalid_query`.

Query version 1 accepts `action_type: astv_intent` and a structurally valid `intent_id`; both are trimmed and lowercased. It returns normalized `query`, `count`, and `mappings`. No matches is successful with an empty collection. Unsupported types or malformed targets return `invalid_query`.

AdvNFC validates identifier structure and active mapping equality only. It does not read the ASTV catalogue or guarantee downstream intent existence.

## Error semantics and compatibility

Errors retain the common identity and return:

```yaml
ok: false
query: {}
error:
  code: invalid_query | not_found
  message: <diagnostic>
```

Consumers branch on `error.code`, not `message`. Compatible additions may add optional fields. Removing or changing an operation, field, action type, error code, or normalization meaning requires an interface-version change and governed consumer-impact assessment.
