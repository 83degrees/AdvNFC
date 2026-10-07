# AdvNFC HACS Deployment Runbook

## Scope and authority

This runbook applies the governed route:

`haos_integration -> hacs -> HOME_ASSISTANT_INTEGRATION_DEPLOYMENT_STANDARD.md`

The authoritative integration source is `custom_components/advnfc/**`; its
stable version is the `version` in `manifest.json`, currently `1.2.0`. This
runbook does not authorise Beta deployment, stable promotion, production
deployment, or rollback. Once explicit stable-promotion authority exists,
stable tag and GitHub Release creation follow through the approved HACS
mechanism.

HACS is the sole future GitHub Release consumer for this repository.
Historical `reader-agent-*` Git tags remain as migration provenance, but they
are not AdvNFC integration versions and must not acquire new GitHub Release
objects.

## Beta preparation and handoff

After the accepted issue PR is integrated into persistent `beta`, record its
full candidate SHA and derive the immutable lightweight tag
`vX.Y.Z-beta.<short-sha>` from the manifest version. Confirm the tag is unused,
create it at the exact candidate SHA, validate the tagged root `hacs.json`, push
it without creating a GitHub prerelease, and independently verify the remote
tag resolves to the recorded SHA. Tag creation and push require the applicable
Beta/deployment authority.

The operator handoff records the immutable Beta tag, full SHA, tag-to-SHA and
HACS metadata validation, prior installed version, target `ha-starburst`
instance, and the verified instance-specific HACS update entity. The supported
action is:

```yaml
action: update.install
target:
  entity_id: update.advnfc_update
data:
  version: "<immutable-beta-tag>"
```

Verify the actual update entity on `ha-starburst`; do not infer it from this
example. Target the immutable tag, never `main`, `beta`, or a raw SHA. Restart
Home Assistant after the update, confirm the expected tag is installed, confirm
AdvNFC loads without errors, and verify `sensor.advnfc_tag_mapping` plus one
controlled `advnfc.find_tag_record` lookup.

The separately operator-managed top-level `advnfc:` activation and AdvNFC
configuration payload remain governed by the HAOS configuration runbook. HACS
does not own them.

## Stable release

After successful Beta, promotion to `main`, required equivalence evidence, and
explicit stable-promotion authority, dispatch
`.github/workflows/hacs-release.yml` with the selected stable SHA, accepted
Beta tag, and the promotion-equivalence evidence reference when the integrated
SHA differs. The workflow invokes
`04_Implementation/haos/packaging/hacs/hacs_release.py`, validates repository
metadata and identity, fails on contradictory tags or missing evidence, and
creates the immutable `vX.Y.Z` tag and GitHub Release. It does not deploy to
Home Assistant or grant stable-promotion authority.

## Failure, rollback, and evidence

On install, identity, load, restart, or functional-check failure, stop
progression and preserve non-secret diagnostics. With rollback authority,
restore through HACS the exact version installed immediately before the attempt
and repeat restart, load, sensor, and lookup checks. Moving branches are not
rollback identities.

Record target instance, prior version, requested tag/version, exact Git SHA,
update entity, install result, restart result, load result, functional check,
promotion equivalence, stable release identity, and any rollback result in the
governing issue or linked authoritative evidence.
