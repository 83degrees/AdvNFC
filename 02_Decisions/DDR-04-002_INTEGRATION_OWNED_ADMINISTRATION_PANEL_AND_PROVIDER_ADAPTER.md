# DDR-04-002 — Integration-Owned Administration Panel and Provider Adapter

## Status

`Proposed`

## Decision

AdvNFC will deliver its tag-mapping administration UI as a non-iframe Home
Assistant custom panel bundled with the existing `advnfc` HACS custom
integration. The panel will use Home Assistant's authenticated frontend
WebSocket connection to invoke the provider's response-only services. It will
not introduce a Home Assistant App, shared server, browser-direct MQTT, direct
YAML access or a separate deployment route.

One client-side provider adapter will own capability negotiation, response
extraction, native transport and authorization error mapping, bounded timeout
state, read/manage presentation separation, active/persisted revision display
and concurrency reconciliation. Before create, update or delete it will read
status and supply the current `persisted_revision` as `expected_revision`. On
`stale_revision` it will refresh status and active mappings, expose a conflict,
and never retry or overwrite automatically.

Save and activation will remain separate user actions. A successful save will
remain visibly `activation_required` and will not reload the provider. Explicit
reload will use the provider's existing unguarded v3 activation operation,
followed by a status read that verifies equality of active and persisted
revisions. A reload failure or ambiguous timeout will retain and reconcile the
previous active state rather than claim success or retry automatically.

ASTV intent selection will be an optional read-only adapter dependency. It will
negotiate the ASTV administration interface and active-list capability, follow
revision-bound pagination, and use active `intent_id` plus `title` records.
ASTV absence or incompatibility will not disable independent AdvNFC
administration or structurally valid manual intent entry.

Frontend files will remain in the HACS integration tree. The registered module
URL will carry a digest of the installed bytes for cache invalidation. HACS
update/removal and the required Home Assistant restart remain the lifecycle
mechanism. Repeated integration setup will not duplicate the sidebar entry.

## Context

AdvNFC administration interface v3 already exposes capability discovery,
normalized active reads, status, guarded persisted mutations and failure-safe
explicit reload. ASTV-355 needs a responsive list/editor, but ASTV-354 first
establishes a supported Home Assistant presentation and transport boundary
without confusing active state with the separately persisted candidate.

Home Assistant custom panels reuse the authenticated frontend session and
sidebar. Response-only services require `return_response: true`; service-bus
authorization and service-schema rejection may fail before an AdvNFC handler
can return its structured envelope. The client therefore needs an explicit
transport/provider outcome boundary.

Unlike ASTV's draft model, AdvNFC mutations are guarded by
`persisted_revision`, while list/get expose the active snapshot. Reload accepts
no expected revision. These provider-owned semantics cannot be borrowed from a
shared UI abstraction without an AdvNFC-specific adapter.

## Alternatives considered

### Reuse the ASTV adapter directly

Rejected. ASTV uses `editable_revision`, a provider-owned durable draft and a
guarded activation operation. AdvNFC uses `persisted_revision`, active-only
reads and an unguarded reload. Treating them as identical would corrupt
concurrency and activation meaning.

### Separate Home Assistant App or shared administration server

Rejected. It adds a deployable unit, authentication boundary and operational
lifecycle when the existing integration and Home Assistant frontend already
provide the required local surface.

### Lovelace card only

Rejected. A card can demonstrate calls but does not provide the discoverable,
integration-owned sidebar workspace approved for AdvNFC administration.

### Admin-only panel

Rejected. The provider exposes non-secret capability, status and normalized
active reads to ordinary service-call contexts. Hiding the entire panel would
collapse the read/manage distinction; provider-side admin registration remains
the state-change boundary.

### Automatic retry after stale revision, reload failure or timeout

Rejected. Retry can overwrite a concurrent persisted change or repeat an
operation whose server outcome is unknown. Reconciliation and a new explicit
user action are required.

### Browser-direct YAML or MQTT access

Rejected. Either path bypasses the provider contract, Home Assistant
authorization, atomic persistence and failure-safe activation boundary.

### Require ASTV for every edit

Rejected. AdvNFC owns structural reference validation and remains independently
administrable. Live target discovery is useful but optional.

## Rationale

An integration-owned panel is the smallest boundary that preserves native Home
Assistant authentication, HACS delivery and product independence. A dedicated
AdvNFC adapter concentrates the v3 contract semantics the later editor must not
duplicate or confuse with ASTV. Digest-addressed assets give deterministic
cache invalidation while restart-based cleanup matches the custom-integration
lifecycle already governed for AdvNFC.

## Consequences / trade-offs

- The panel is present for read-only users; UI affordance checks improve
  clarity but never replace provider authorization.
- A Home Assistant restart is required after HACS update or removal before
  process routes and module identity are rebuilt.
- A timed-out mutation or reload is indeterminate until status and active data
  are reread.
- Concurrent changes can require manual reapplication; there is no automatic
  merge or retry.
- The adapter depends on AdvNFC interface major 3 and schema 1, and negotiates
  optional operations before use.
- ASTV target discovery can be unavailable without preventing manual valid
  `intent_id` entry or unrelated AdvNFC work.
- Mobile layout must account for Home Assistant safe-area insets and narrow
  iPhone viewports without a separate mobile application.
- Schema v1 remains unchanged: Name maps to `label`, `action.type` remains
  required `astv_intent`, `area_override` remains optional, and Description,
  unassigned records and physical reader capture remain excluded.

## Source Linear issue

`ASTV-354`

## Supersedes

`Not applicable`
