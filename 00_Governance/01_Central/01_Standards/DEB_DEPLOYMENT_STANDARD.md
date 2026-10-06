# DEB_DEPLOYMENT_STANDARD.md

**Standard:** Debian Package Deployment Standard
**Version:** v1.0.0
**Status:** Approved
**Approval tag:** `deb-deployment-standard-v1.0.0`
**Approval date:** 2026-10-06
**Lifecycle:** Independent

## 1. Purpose, Scope and Authority

This Standard defines the mandatory build, release, distribution, installation, upgrade, validation, rollback and evidence model for governed software delivered as a Debian binary package.

It is a **product-applicable Standard** maintained authoritatively at:

`/Standards/Product/DEB_DEPLOYMENT_STANDARD.md`

It is projected unchanged into applicable governed product repositories at:

`00_Governance/01_Central/01_Standards/DEB_DEPLOYMENT_STANDARD.md`

It applies to a governed deployable unit classified as `rpi_os_software` with deployment mechanism `deb` under the Deployment Architecture Standard.

`CENTRAL_GOVERNANCE.md` remains the higher constitutional authority. The Deployment Architecture Standard remains authoritative for deployable-unit classification, canonical source and packaging structure, and platform-required location exceptions. Product architecture and the Project Profile remain authoritative for product-specific component, target, service, configuration and data meaning. This Standard supplies only the mechanism-specific Debian package controls and must not duplicate or override those authorities.

This Standard does not itself authorise package publication, installation, Beta deployment, stable promotion, production deployment, downgrade, rollback or recovery. It does not bypass issue workflow, human review, validation, Beta or stable authority, deployment authority, rollback authority or other required approval gates.

## 2. Platform Basis

The external platform basis for this model is the Debian Policy Manual sections covering [binary packages](https://www.debian.org/doc/debian-policy/ch-binary.html), [control fields](https://www.debian.org/doc/debian-policy/ch-controlfields.html), [package relationships](https://www.debian.org/doc/debian-policy/ch-relationships.html), [maintainer scripts and installation procedure](https://www.debian.org/doc/debian-policy/ch-maintainerscripts.html) and [configuration-file handling](https://www.debian.org/doc/debian-policy/ap-pkg-conffiles.html).

Debian binary packages contain both installed payload and package metadata. Their control data records package identity, version, architecture and relationships; package-maintainer scripts may participate in installation, upgrade and removal; and declared conffiles receive package-manager configuration-preservation behaviour.

These sources describe platform behaviour. This Standard defines the governed controls for using that behaviour.

## 3. Product Declaration and Package Model

The applicable Project Profile or authoritative product deployment artefact must identify, for each Debian-package deployable unit:

- authoritative package-owned source location;
- packaging and build machinery location;
- Debian source package name and produced binary package name or names;
- target distribution, release, hardware architecture and other material platform constraints;
- package repository and channel/suite/component where used, or the separately approved direct-package route;
- install and upgrade procedure;
- services, timers, sockets or other managed units affected by package operations;
- package-owned configuration and state, if any;
- external node-local configuration and runtime data on which the package relies but does not own;
- validation route; and
- rollback, downgrade or recovery route and prior known-good package identity.

The declaration must distinguish a source package from each binary package it produces. A package repository channel, suite, component, branch, filename or `latest` reference is a selection aid, not a sufficient immutable package identity where its referenced content can move.

## 4. Authoritative Source, Packaging and Evidence Boundary

Package-owned target filesystem content remains in the canonical Raspberry Pi OS source tree selected under the Deployment Architecture Standard. Machine-consumed package metadata, build scripts and release machinery belong under the applicable `04_Implementation/rpi_os/packaging/deb/**` path.

Only filesystem content owned by the package belongs in `04_Implementation/rpi_os/source/**`. Node-local configuration, mutable application data, credentials, caches, logs and other runtime state that the package does not own remain outside that authoritative source tree. The presence of such content on a target does not transfer ownership to the package. For example, `/etc/advnfc/**` remains external where product architecture declares that the package does not own it.

The package may declare, read, validate, migrate or preserve external configuration or data only where product authority defines that interaction. A maintainer script, service unit or installation instruction must not silently expand package ownership, overwrite external state or convert a node-local path into authoritative packaged source.

Human-facing installation, upgrade, rollback and recovery procedures, together with retained deployment evidence, belong under `08_Deployment/**` or another governed evidence location. Generated `.deb`, `.dsc`, `.changes`, `.buildinfo`, repository metadata and checksums are build or release outputs; they are not a second authoritative source tree.

## 5. Package and Release Identity

Every built binary package must have an unambiguous identity comprising, as applicable:

- source repository and exact source commit SHA;
- governed release or build cut-off;
- source package name and source version;
- binary package name;
- complete Debian version, including epoch and Debian revision where present;
- target architecture, or `all` where valid;
- package format and material build-tool identity;
- cryptographic digest of the exact `.deb` bytes, using SHA-256 or a stronger approved digest;
- repository snapshot, publication record or immutable artifact identity where distributed through a package repository; and
- signing key or attestation identity where signing or attestation is part of the approved route.

Package versions must follow Debian version semantics, be monotonically selectable in the intended upgrade route and distinguish materially different package contents. Rebuilding different bytes under the same package name, version and architecture is prohibited for an accepted or published package identity.

The filename is descriptive only. Acceptance, installation and rollback must use package control metadata together with an immutable digest or repository snapshot/publication identity sufficient to identify the exact package bytes.

## 6. Build Provenance and Reproducibility

The build must consume the exact authorised source commit and governed packaging machinery. Material source inputs, patches, dependencies, toolchain versions, target architecture, build options and environment assumptions must be pinned, captured or otherwise made independently verifiable.

The preferred route is a reproducible build in which an independent rebuild of the same declared inputs produces the same package bytes. Where full byte-for-byte reproducibility is not yet practical, the route must retain sufficient build provenance to verify independently:

- the exact source and packaging revision;
- the controlled builder and build invocation;
- the material dependency and toolchain set;
- the produced package metadata and file manifest;
- the digest of every released package; and
- the relationship between the source SHA and released package.

Where generated `.buildinfo`, `.changes`, `.dsc`, software-bill-of-materials, signature or attestation records form part of the approved route, they must be retained and bound to the same build. A successful build job, mutable branch or unverified artifact upload alone does not establish provenance.

If the source, builder inputs or output identity cannot be established without contradiction, the package must not be released or installed as the governed candidate.

## 7. Package Metadata, Compatibility and Dependencies

Before release, the built package must be inspected rather than relying only on source templates. Its control metadata must accurately declare at least the package name, version, architecture, maintainer, description and dependency relationships required by Debian tooling and the product's approved route.

The package must declare runtime dependencies and version constraints needed for correct operation. Build dependencies must be sufficient to reproduce or independently verify the build. `Pre-Depends`, `Breaks`, `Conflicts`, `Replaces`, `Provides` and multi-architecture semantics must be used only where their Debian meanings and upgrade effects have been deliberately assessed.

Target compatibility must cover the intended Debian or Raspberry Pi OS release, CPU architecture, ABI, init/service manager and other material platform assumptions. `Architecture: all` must not be used for content whose installed behaviour or dependencies are architecture-specific.

Package-maintainer scripts and triggers must be non-interactive unless the approved route explicitly supplies a governed interaction mechanism, must be idempotent where Debian package operations may repeat them, and must fail with a non-zero status when a required operation cannot be completed safely. They must not download or execute unpinned replacement payload as an undeclared second installation mechanism.

## 8. Distribution and Installation Route

The normal package-repository route must establish:

- the approved repository, suite/channel and component;
- authenticated repository configuration and signing-key trust;
- immutable binding from repository metadata to the exact package digest;
- publication evidence showing that the intended package version and architecture are available; and
- repository metadata freshness and client selection behaviour sufficient to prevent installation of a stale, superseded or unintended candidate.

A direct-package route may be used only where separately approved for the product or deployment event. It must authenticate or otherwise securely acquire the exact `.deb`, verify its recorded digest before installation, record the transfer source and avoid substituting a similarly named local or downloaded file.

Before installation or upgrade, the executor must:

1. establish deployment authority and the exact target node or node set;
2. record the currently installed package identity and prior known-good recovery identity;
3. verify platform compatibility, required dependencies, repository or artifact identity and available storage;
4. protect or back up configuration and data where the approved recovery route requires it;
5. preview or otherwise identify the package-manager transaction and reject unintended removals, downgrades or dependency substitutions; and
6. install the exact authorised package version through the approved non-interactive or governed-interaction route.

Package-manager state must be allowed to complete cleanly. An interrupted or partially configured transaction is not a successful deployment and must enter governed recovery.

## 9. Upgrade, Configuration and Service Handling

The package must define expected behaviour for first installation, upgrade, downgrade where supported, removal and purge where those operations are within product scope.

Package-owned configuration that operators may edit must use appropriate Debian conffile or other explicitly governed preservation and migration behaviour. External node-local configuration and runtime data must remain preserved by default. Upgrade logic may validate or migrate such state only under the declared ownership boundary, with a recoverable prior state where migration is not safely reversible.

An upgrade must not silently reset credentials, endpoints, calibration, device identity, accumulated data or other node-local state. Destructive or incompatible data migration requires explicit product authority, backup/recovery preparation and the applicable human approval.

Where the package installs or changes a service, timer, socket or similar unit, the package model and deployment procedure must state whether the unit is enabled, started, stopped, restarted or reloaded during install and upgrade. Service actions must be ordered so that incompatible binaries, configuration and data are not exposed as an accepted running state.

Automatic restart may be used only where interruption and state-transition effects are acceptable for the approved deployment stage. A package transaction completing successfully does not prove that the affected service started or functions correctly.

## 10. Post-Installation Validation

Validation must be performed against the installed target and must establish as applicable:

- package-manager status is fully installed and configured;
- installed package name, complete version and architecture match the authorised candidate;
- the installed package can be bound to the recorded `.deb` digest or immutable repository publication identity;
- package-owned files, permissions and relevant digests or package-manager verification results match expectations;
- external configuration and data remain present, correctly owned and semantically usable;
- affected services are in the expected enabled and runtime state;
- logs and package-manager records show no unresolved installation or migration failure;
- a basic functional or health check exercises the material runtime behaviour; and
- the observed target and time are recorded.

The exact validation depth is proportionate to the deployable unit and risk, but it must include both package identity and basic runtime function where the package supplies a running service. A successful `dpkg` or `apt` exit code alone is insufficient.

Where a `WF-01` product change is being deployed, Beta and stable validation remain bound to the exact candidate and promotion-equivalence requirements in Central Governance. This Standard does not convert package installation into stable-promotion authority.

## 11. Failure, Rollback and Recovery

Before deployment, record a prior known-good package identity and confirm that its exact package bytes or immutable repository snapshot remain obtainable. Record the compatible configuration/data recovery point and any required dependency versions.

If build, publication, dependency resolution, installation, configuration, service handling, identity verification or functional validation fails:

- do not accept the candidate or claim successful deployment;
- preserve package-manager, service and diagnostic evidence without retaining secrets;
- determine whether the target is running the prior version, the candidate, a partially configured transaction or an indeterminate mixed state;
- stop or isolate unsafe runtime behaviour where required by product authority;
- use the required rollback authority to reinstall or downgrade to the exact prior known-good package and compatible dependencies, or use the approved recovery procedure when downgrade is unsupported;
- restore configuration or data only from the declared compatible recovery point; and
- repeat package-identity, managed-file, service and functional validation after recovery.

Rollback must not select `latest`, a moving repository channel, a branch name or an unverified filename. If the exact prior package or compatible state cannot be established, recovery must fail closed and be escalated rather than install an approximation.

Where a maintainer-script or data migration has irreversible effects, the deployment plan must identify the recovery route before installation. A package downgrade alone must not be represented as complete rollback when configuration, data, dependency or service state remains incompatible.

## 12. Evidence and Traceability

The governing Linear issue and supporting authoritative evidence must establish, as applicable:

- product, repository, deployable unit and target node or node set;
- governing workflow stage and deployment authority;
- exact source commit and release/build cut-off;
- source and binary package names, complete version and architecture;
- build invocation, builder, material inputs and provenance records;
- exact `.deb` digest and any signature or attestation identity;
- package repository publication/snapshot identity or approved direct-package transfer identity;
- pre-install installed state and prior known-good recovery identity;
- package-manager transaction and resulting installed identity;
- package-owned file and external-state preservation checks;
- service and functional validation results with observation time;
- rollback, downgrade or recovery authority and result where used; and
- the relationship among Beta, stable and promoted package identities where applicable.

The evidence chain must make the relationship `exact source SHA → exact built package bytes → exact installed target state` independently reviewable. Source identity alone does not prove package bytes, and package bytes alone do not prove installed or running target state.

## 13. Security and Fail-Closed Behaviour

Package build, repository and target credentials must remain outside source and retained evidence. Signing keys, repository credentials and deployment privileges must be scoped to the minimum approved operation and separated where the product's risk model requires it.

Build and deployment tooling must fail closed when it cannot establish the exact authorised source, package metadata, digest, target architecture, dependency transaction, repository trust, installed identity or required prior known-good recovery identity. It must not fall back to a moving branch, `latest` artifact, unsigned alternate repository, cached file with an unverified digest, broader target set or undeclared installation script.

Package-maintainer scripts must not suppress failures that leave required files, services, configuration or migrations incomplete. Evidence may redact secrets, but redaction must not remove the identities needed to prove which source, package and installed target state were used.
