# AdvNFC Reader-Agent Debian Deployment Runbook

## Scope and package model

This runbook applies the governed route:

`rpi_os_software -> deb -> DEB_DEPLOYMENT_STANDARD.md`

The Debian source and binary package names are `advnfc-reader-agent`; the
current package declares `Architecture: all` and targets Raspberry Pi OS/Debian
with systemd, libnfc, Mosquitto client tooling, Python 3/PyYAML, udev, and the
other dependencies declared in its built control metadata. The initial
approved distribution route is a versioned `.deb` plus SHA-256 digest attached
to a `reader-agent-v<version>` GitHub Release. No APT repository is implied.

Package-owned payload is authoritative beneath
`04_Implementation/rpi_os/source/**`, mirroring `/opt/advnfc/**`,
`/lib/systemd/system/**`, `/lib/udev/rules.d/**`, `/usr/local/sbin/**`, and
`/usr/share/advnfc/**`. Build and generated Debian metadata logic is at
`04_Implementation/rpi_os/packaging/deb/build_deb.sh`. Profiles, secrets, the
active selector, credentials, and other `/etc/advnfc/**` state remain node-local
and outside package ownership.

## Build and candidate identity

Build only from the exact authorised source commit:

```bash
04_Implementation/rpi_os/packaging/deb/build_deb.sh 0.1.0
```

The build fails unless an exact 40-character source Git SHA is available. It
produces `dist/advnfc-reader-agent_<version>_all.deb` and a matching
`.deb.sha256` record, and embeds package version plus source SHA in
`/opt/advnfc/reader_agent/VERSION`.

Before release, inspect the built package control metadata and file manifest;
record the exact source SHA, build invocation and environment, binary package
name, complete Debian version, architecture, `.deb` SHA-256, and GitHub Release
identity. Different bytes must never be published under the same package name,
version, and architecture.

## Install or upgrade

Deployment requires explicit authority for the exact target and package. Before
changing the node, record its installed package version/architecture, service
state, external `/etc/advnfc/**` state, and exact prior known-good `.deb` plus
digest. Verify the candidate digest and inspect the package-manager transaction
for unintended removals or substitutions.

Fresh install:

```bash
sudo apt install ./advnfc-reader-agent_<version>_all.deb
sudo advnfc-reader-agent-init
sudoedit /etc/advnfc/secrets/<credential_ref>.env
sudo advnfc-profile validate <profile>
sudo advnfc-profile switch <profile>
sudo advnfc-reader-agent-check
```

Upgrade:

```bash
sudo apt install ./advnfc-reader-agent_<new-version>_all.deb
sudo advnfc-reader-agent-check
```

A fresh install enables but does not start the service before a valid local
profile and secret exist. An upgrade restarts only an already-active service.
Package operations preserve `/etc/advnfc/**`.

## Validation

After installation, record `dpkg-query` identity and confirm the complete
version and `all` architecture match the authorised candidate. Confirm the
embedded `VERSION` source SHA, package-owned files and permissions, unchanged
external profiles/secrets/selector, expected service enablement and runtime
state, and absence of unresolved package or service errors. Run
`advnfc-reader-agent-check`; it validates the profile/secret boundary, ACR122U
USB identity and permissions, direct `nfc-list` access as `advnfc`, dependency
availability, and service diagnostics. Perform a controlled reader functional
check appropriate to the authorised environment.

## Rollback, removal, and evidence

On build, identity, installation, service, or functional failure, stop
progression and establish whether the node is on the prior version, candidate,
or a partial state. With rollback authority, reinstall the exact retained prior
package after verifying its recorded digest:

```bash
sudo apt install --allow-downgrades ./advnfc-reader-agent_<old-version>_all.deb
sudo advnfc-reader-agent-check
```

Removal uses `sudo apt remove advnfc-reader-agent`; it stops and disables the
service while preserving `/etc/advnfc/**`. Record target node, authority, source
SHA, package identity and digest, prior state, package-manager transaction,
external-state preservation, service and functional validation, and any
rollback result. A successful package-manager exit alone is not acceptance.

The `pi-nfc-02` production reader remains subject to its explicit deployment
constraints; this repository migration does not authorise or perform an update
on that node.
