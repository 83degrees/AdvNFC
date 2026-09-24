# AdvNFC reader-agent Debian packaging

## Selected model

ASTV-255 uses a staged distribution model:

1. build a versioned Debian `.deb` package from governed repository content;
2. publish the package as a governed GitHub Release artefact;
3. install or upgrade the package explicitly on a reader node;
4. keep node-local configuration and secrets outside the package under `/etc/advnfc/`;
5. consider an APT repository only when the number/frequency of managed reader nodes makes it worthwhile.

The package is the governed software unit. `/etc/advnfc/` is the node-local configuration boundary.

## Build

From the repository root:

```bash
04_Source/reader_agent/packaging/build_deb.sh 0.1.0
```

The package is written to `dist/` by default and embeds both package version and Git commit identity in:

`/opt/advnfc/reader_agent/VERSION`

## Fresh install

```bash
sudo apt install ./advnfc-reader-agent_<version>_<arch>.deb
sudo advnfc-reader-agent-init
sudoedit /etc/advnfc/reader-agent.env
sudo advnfc-reader-agent-check
sudo systemctl start advnfc-reader-agent.service
```

The package enables the service but deliberately does not start a fresh install before node-local configuration is present.

## Upgrade

```bash
sudo apt install ./advnfc-reader-agent_<new-version>_<arch>.deb
sudo advnfc-reader-agent-check
```

The package never owns `/etc/advnfc/reader-agent.env`, so upgrades do not overwrite credentials or node-local values. If the service was already active, package post-install restarts it after files are replaced.

## Rollback

Keep the prior governed package artefact. Roll back explicitly:

```bash
sudo apt install --allow-downgrades ./advnfc-reader-agent_<old-version>_<arch>.deb
sudo advnfc-reader-agent-check
```

## Uninstall

```bash
sudo apt remove advnfc-reader-agent
```

Removal stops/disables the service but preserves `/etc/advnfc/`. Node-local configuration is intentionally not deleted by the package.

## Readiness check

`advnfc-reader-agent-check` fails if any mandatory readiness condition is missing:

- package version metadata;
- `nfc-list`, `mosquitto_pub`, `lsusb`, and `timeout`;
- dedicated `advnfc` service account;
- node-local environment file with a non-placeholder MQTT password;
- ACS ACR122U USB ID `072f:2200`;
- successful `nfc-list` communication with a reader.

Service enabled/active state is reported separately so the check can be used before first start.

## Security and node identity

No credentials are included in the package or release artefact. Reader identity continues to default to `hostname -s`; node-specific overrides remain in the external environment file.

The package creates a dedicated `advnfc` system account and an ACR122U udev rule granting that group access to USB device `072f:2200`. This removes the previous dependency on a host-specific login account such as `pi01`.

## Distribution evolution

A GitHub Release artefact is the initial distribution mechanism because it provides versioned provenance without the operational overhead of an APT repository. An APT feed remains a future optimisation, not a prerequisite for repeatable test/deployment cycles.
