# AdvNFC Home Assistant Configuration Deployment Runbook

## Purpose and authority

This runbook applies the approved route:

`haos_config -> operator_selected -> HOME_ASSISTANT_CONFIG_DEPLOYMENT_STANDARD.md`

It covers only AdvNFC's Home Assistant package, tag mapping, and required
top-level activation on `ha-starburst`. It does not authorise deployment and
does not apply to the HACS-managed integration. The operator selects the
practical transport for each authorised deployment.

## Deterministic path map

| Governed source or required target step | Deterministic `ha-starburst` target |
| --- | --- |
| `04_Implementation/haos/source/config/packages/advnfc/advnfc_automations.yaml` | `/config/packages/advnfc/advnfc_automations.yaml` |
| `04_Implementation/haos/source/config/packages/advnfc/advnfc_scripts.yaml` | `/config/packages/advnfc/advnfc_scripts.yaml` |
| `04_Implementation/haos/source/config/AdvNFC/advnfc_tag_mapping.yaml` | `/config/AdvNFC/advnfc_tag_mapping.yaml` |
| top-level `advnfc:` activation | `/config/configuration.yaml` |

The activation is an operator-managed target configuration step, not a second
repository payload. The scripts package must not contain an `advnfc:`
activation key. Only the accepted files and activation change explicitly
authorised for a deployment are applied.

## Controlled deployment

Before transfer, record deployment authority, authorised operator, exact
accepted commit SHA, selected source and target paths, `ha-starburst`
environment, transport, Home Assistant configuration-check route, and rollback
route. Record source hashes where practical. Capture the immediate prior bytes
and state for every affected target, including `configuration.yaml` when its
activation changes, and store that capture separately from the target paths.

Transfer the accepted bytes without editing, reformatting, line-ending or
encoding conversion, merge resolution, or generation. Prefer target-side
hashes or a byte comparison. Otherwise record the strongest available
read-back, size, manifest, and inspection evidence and state the remaining
manual-provenance limitation honestly.

Run the Home Assistant-supported configuration check on `ha-starburst` after
transfer. Record route, time, result, warnings, and evidence binding the result
to the deployed state. Restart Home Assistant only after the check succeeds and
the action is authorised. Verify the AdvNFC integration loads, the mapping
sensor reports `loaded` with schema version `1`, and a controlled UID lookup
returns the expected normalized record.

Fail closed when authority, candidate, target, prior state, transferred bytes,
configuration validation, or required evidence is missing, ambiguous, failed,
or contradictory. To roll back, restore every affected target and prior
activation state, verify restored bytes, repeat the configuration check, and
record the final target status.

## Deployment evidence record

```text
Governing issue and deployment authority:
Authorised operator and time:
Accepted commit SHA:
Selected source paths and source hashes:
Target instance/environment: ha-starburst
Exact target paths and activation state:
Transport actually used:
Immediate prior-state identities and rollback locations:
Target-byte verification and remaining limitation:
Home Assistant configuration-check route, time, and result:
Restart authority and result, if applicable:
Integration load and functional-check result:
Overall outcome:
Rollback and revalidation result, if invoked:
Unresolved conditions:
```
