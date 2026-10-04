# DDR-04-001 — Model AdvNFC tags as UID-to-typed-action mappings

## Status

`Proposed`

## Decision

AdvNFC tag mappings use the stored UID as the tag identity and map it to a
closed, versioned tag record containing human-facing metadata and one typed
action. Schema v1 supports only the `astv_intent` action type. Runtime lookup
preserves the typed action until a dedicated AdvNFC action selector routes it to
the provider-owned ASTV Intent Invocation interface.

The complete document is validated before atomic activation as an immutable
snapshot. A failed reload retains the previous valid snapshot.

## Context

The original mapping collapsed each UID directly to an ASTV `intent_id`, which
coupled lookup to immediate ASTV invocation and left no governed seam for later
action types or managed configuration. AdvNFC also needs deterministic
whole-document validation and safe reload behavior before a management surface
can be introduced.

## Alternatives considered

- Keep the direct UID-to-intent mapping. This preserves simplicity but cannot
  express action type or support safe future extension.
- Introduce an independent `tag_id`. This duplicates the UID identity without a
  schema-v1 requirement.
- Add native Home Assistant actions in v1. This widens the first schema and
  routing change before its validation and management foundations are proven.
- Validate ASTV intent existence by reading the ASTV catalogue. This would
  couple AdvNFC to provider-internal storage instead of a governed interface.

## Rationale

A closed typed-action record creates one explicit routing seam while keeping v1
narrow. UID identity remains stable, ASTV ownership stays behind its governed
boundary, and atomic validated snapshots prevent partial or invalid mappings
from becoming active.

## Consequences / trade-offs

- Every stored tag requires a non-blank label and typed action.
- Existing mappings require a one-time whole-file migration.
- Unknown fields and action types fail closed.
- New action types require later governed schema, architecture and runtime work.
- ASTV referential existence validation remains deferred until ASTV exposes a
  suitable provider-owned lookup/read boundary.
- The loader becomes a small AdvNFC Home Assistant integration rather than a
  direct YAML include.

## Source Linear issue

`ASTV-299`

## Supersedes

`Not applicable`
