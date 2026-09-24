# AdvNFC Reader-Agent Profile Schema

## Schema version 1

A profile is a YAML mapping stored as `<name>.yaml`.

Required fields:

```yaml
schema_version: 1
name: starburst
mqtt:
  host: ha-starburst.little-dory.ts.net
  port: 1883
  username: ha_mqtt
  credential_ref: starburst_mqtt
  topic_pattern: advnfc/{reader}/last_uid
reader: {}
```

`name` must match the filename. `mqtt.topic_pattern` is constrained to the governed ASTV-257 interface `advnfc/{reader}/last_uid`; profiles do not redefine MQTT protocol semantics.

`reader.override` is optional. When omitted, the reader identity remains `hostname -s`.

## Secrets

`credential_ref` resolves to:

`/etc/advnfc/secrets/<credential_ref>.env`

That file contains the node-local secret:

```text
MQTT_PASS=...
```

Secret files are never committed to Git. The package ships only placeholder examples.

## Runtime layout

```text
/etc/advnfc/
  active-profile.yaml -> profiles/<name>.yaml
  profiles/
    <name>.yaml
  secrets/
    <credential_ref>.env
```

The active selector is a stable symlink. Package upgrades do not own or overwrite these node-local files.

## User operations

```text
advnfc-profile list
advnfc-profile status
advnfc-profile validate [name]
sudo advnfc-profile switch <name>
```

`switch` validates the requested profile and referenced secret before changing the selector. It then stops the service, switches the selector atomically, starts the service, verifies activation, and restores the previous profile if activation fails.

Status and diagnostics expose the profile name and non-secret effective configuration only; they never print `MQTT_PASS`.
