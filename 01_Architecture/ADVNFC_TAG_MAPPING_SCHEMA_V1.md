# AdvNFC Tag Mapping Schema v1

## Status and authority

This document defines the version-1 stored and normalized runtime shapes for the
AdvNFC-owned `advnfc_tag_mapping.yaml` document. It is authoritative for that
schema and is implemented by the AdvNFC tag-mapping loader.

## Closed stored document

The document root contains exactly:

```yaml
tag_mapping_schema_version: 1
tags: {}
```

`tag_mapping_schema_version` is the integer `1`. `tags` is a mapping and may be
empty. Unknown root fields and duplicate YAML keys are invalid.

## Stored UID and tag record

Each key under `tags` is the authoritative UID identity. It must be a non-blank
alphanumeric string already stored in canonical uppercase form. Runtime input is
trimmed and uppercased before exact lookup.

Each tag record contains exactly:

| Field | Required | Meaning |
|---|---:|---|
| `label` | Yes | Non-blank human-facing metadata; need not be unique. |
| `area_override` | No | Non-blank Home Assistant area ID that must resolve when the document is validated. |
| `action` | Yes | Closed typed-action record. |

No separate tag ID, description, notes, timestamps, history, audit metadata or
enabled flag exists in schema v1.

## Typed action

The action record contains exactly `type` and `intent_id`. Schema v1 supports
only:

```yaml
action:
  type: astv_intent
  intent_id: classic_fm
```

`intent_id` is trimmed, lowercased and required to match lowercase underscore
identifier form. AdvNFC does not check whether it exists in the ASTV Intent
Catalogue because ASTV does not yet provide a governed provider-owned lookup
boundary. AdvNFC must not read ASTV-owned catalogue storage directly.

## Validation and activation

The complete candidate document is validated on initial load and explicit
reload. Validation rejects:

- unknown or missing fields;
- a schema version other than integer `1`;
- duplicate YAML keys or UIDs;
- non-canonical stored UIDs;
- missing or blank required values;
- unsupported action types;
- structurally invalid intent IDs; and
- area overrides that do not resolve through the Home Assistant area registry.

One invalid record rejects the entire candidate. A successful validation
atomically replaces the active immutable snapshot. A failed reload leaves the
previous active snapshot unchanged.

## Normalized runtime record

`advnfc.find_tag_record` normalizes the supplied UID and returns `{}` for an
unknown UID. A known UID returns:

```yaml
uid: 7AB06354E000
label: Dad - Classic FM
area_override: martin_bedroom  # omitted when not configured
action:
  type: astv_intent
  intent_id: classic_fm
```

The action remains typed until `script.advnfc_select_tag_action` selects the v1
route. Only the selected `intent_id`, optional `input_area_override`, and
originating `trigger_entity` cross the provider-owned ASTV Intent Invocation
boundary.
