# ASTV-299 Home Assistant Beta Deployment

## Scope

This runbook deploys the ASTV-299 AdvNFC schema-v1 mapping loader, registered
capability sensor, lookup action, and typed-action routing to `ha-starburst`.
Deploy the exact accepted candidate from the persistent `beta` branch.

## Backup and rollback unit

Before deployment, retain the live copies of:

- `/config/packages/advnfc/advnfc_scripts.yaml`
- `/config/AdvNFC/advnfc_tag_mapping.yaml`
- the existing top-level AdvNFC activation state in
  `/config/configuration.yaml`

The custom component directory, scripts, mapping, and configuration activation
are one deployment and rollback unit.

## Install

Copy these governed source paths to the corresponding Home Assistant paths:

| Governed source | Home Assistant destination |
| --- | --- |
| `04_Source/config/custom_components/advnfc/` | `/config/custom_components/advnfc/` |
| `04_Source/config/packages/advnfc/advnfc_scripts.yaml` | `/config/packages/advnfc/advnfc_scripts.yaml` |
| `04_Source/config/AdvNFC/advnfc_tag_mapping.yaml` | `/config/AdvNFC/advnfc_tag_mapping.yaml` |

Activate the custom integration explicitly in the top level of
`/config/configuration.yaml`:

```yaml
advnfc:
```

The scripts package must not contain a separate `advnfc:` activation key.

Run Home Assistant's configuration check and restart Home Assistant. A script
reload is insufficient when custom-integration Python changes.

## Runtime verification

Verify all of the following:

1. The AdvNFC integration version is `1.0.1` and it is loaded without an
   AdvNFC setup error.
2. `sensor.advnfc_tag_mapping` appears under the AdvNFC integration's entity
   list and in Developer Tools.
3. The sensor state is `loaded`, with `schema_version: 1` and
   `mapping_count: 9`.
4. `advnfc.find_tag_record` returns the normalized record for
   `7AB06354E000`, including `action.type: astv_intent` and
   `action.intent_id: classic_fm`.
5. A controlled UID Gateway invocation produces the existing visible success
   notification and invokes the expected ASTV intent.

## Rollback

Restore the retained scripts and mapping together, restore the previous
`configuration.yaml` activation state, and remove
`/config/custom_components/advnfc/` if it did not exist before ASTV-299. Run
the Home Assistant configuration check and restart Home Assistant. Confirm the
prior AdvNFC runtime path is restored before closing the rollback action.
