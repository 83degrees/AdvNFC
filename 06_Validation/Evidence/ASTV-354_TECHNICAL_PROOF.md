# ASTV-354 Technical Proof Record

## Scope

This record describes the review candidate for ASTV-354. It is repository and
automated-test evidence only. It does not claim production deployment, Beta
acceptance, a live mapping mutation, provider activation or release.

The proof covers:

- integration-owned custom-panel and static-route registration;
- authenticated Home Assistant frontend WebSocket `call_service` with
  `return_response: true` for `SupportsResponse.ONLY` services;
- response extraction, native authorization/error preservation and bounded
  timeout state;
- read visibility with client affordance gating plus provider-side admin
  enforcement for manage operations;
- AdvNFC v3 capability, operation and schema-v1 negotiation;
- status-first `persisted_revision` use and no-retry stale-write
  reconciliation;
- persistence-only Save versus explicit separate reload and post-reload status
  verification;
- provider-code normalization through the published compatibility mapping;
- optional ASTV active-intent discovery, revision-consistent pagination and
  unavailable/incompatible fallbacks;
- digest-addressed frontend asset caching and duplicate-panel prevention
  inside the HACS integration tree; and
- responsive layout including narrow viewport and safe-area handling.

The visible panel exposes read-only proof buttons. It intentionally cannot
create, update, delete or reload tag mappings and does not implement the
ASTV-355 list/editor workflow.

## Platform basis

The design reuses the accepted ASTV-350 Home Assistant proof, which checked the
panel and WebSocket path against Home Assistant Core 2026.9.4 and compatible
2026.10 APIs:

- `panel_custom.async_register_panel` for a non-iframe module panel,
  read/admin visibility and safe-area handling;
- `StaticPathConfig` plus `async_register_static_paths` for integration-bundled
  frontend assets; and
- WebSocket `call_service` with `return_response: true`, whose result contains
  the provider payload under `response`.

The AdvNFC proof exercises those exact supported shapes against local test
doubles and specializes only the provider contract semantics. HACS remains
governed by `HOME_ASSISTANT_INTEGRATION_DEPLOYMENT_STANDARD.md`. The frontend
module is an ordinary file inside the installed integration; no new deployment
mechanism is introduced. Module content changes alter the registered digest URL
after update and restart. Removal cleanup likewise completes through HACS
removal and restart, not through a second runtime cleanup path.

## Reproduction

From the repository root:

```powershell
python -m pytest 05_Tests
node --test 05_Tests/test_advnfc_admin_frontend.mjs
node --check custom_components/advnfc/frontend/advnfc-administration-panel.mjs
python 00_Governance/01_Central/03_Tooling/central_gov_checks.py `
  --repository 83degrees/AdvNFC `
  --head gsheldon/astv-354-design-advnfc-ha-administration-ui-and-provider-adapter `
  --base beta `
  --beta-exists true `
  --changed-files-file <newline-delimited-changed-files> `
  --repository-root .
```

The Python suite proves panel/static registration metadata, idempotent sidebar
registration and preserved provider authorization. The Node suite proves the
exact authenticated WebSocket envelope, v3/schema negotiation, permission and
timeout mapping, persisted-revision guarding, no-retry stale reconciliation,
Save/reload separation, activation verification, error normalization, and
optional ASTV pagination/fallback behavior.

Review-candidate results on 2026-10-21:

- Python repository suite: 68 passed;
- focused frontend Node suite: 12 passed;
- frontend module syntax check: passed;
- HACS repository metadata validation: passed for candidate version `1.5.0`;
- Central Governance routing check: passed for WF-01 target `beta`; and
- Git whitespace/error check: passed.

## Runtime proof boundary

No live Home Assistant mutation, activation or deployment is authorized by
ASTV-354. At later governed validation/Beta gates, the exact accepted candidate
still requires HACS installation on the authorized target, restart,
panel/sidebar observation, desktop and iPhone observation, read/non-admin and
admin behavior checks, cache-busted asset observation, integration regression,
and rollback evidence required by the issue and HACS deployment standard.
