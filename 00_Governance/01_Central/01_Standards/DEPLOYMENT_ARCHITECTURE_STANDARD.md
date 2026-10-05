# DEPLOYMENT_ARCHITECTURE_STANDARD.md

**Standard:** Deployment Architecture Standard
**Version:** v1.0.0
**Status:** Approved
**Approval tag:** `deployment-architecture-standard-v1.0.0`
**Approval date:** 2026-10-05

## 1. Purpose, Scope and Authority

This Standard defines the cross-product model for identifying deployable units, classifying their deployment type, locating their authoritative source and packaging machinery, and binding each unit to an approved deployment mechanism.

It is a **product-applicable Standard** maintained at:

`/Standards/Product/DEPLOYMENT_ARCHITECTURE_STANDARD.md`

and projected unchanged to:

`00_Governance/01_Central/01_Standards/DEPLOYMENT_ARCHITECTURE_STANDARD.md`

`CENTRAL_GOVERNANCE.md` remains the higher constitutional authority. Product architecture remains authoritative for product-specific components, responsibilities and boundaries. The applicable mechanism-specific deployment Standard, where one exists, governs the detailed delivery procedure for that mechanism.

This Standard defines deployment architecture. It does not approve a product deployment, replace an applicable workflow gate, or invent a delivery mechanism that has not been designed and approved.

## 2. Deployable Units

A governed product repository may contain one or more independently deployable units.

A deployable unit is a bounded part of authoritative product source with its own:

- deployment type;
- authoritative source location;
- deployment target;
- approved deployment mechanism;
- release or update path;
- validation expectations; and
- rollback or recovery expectations.

The repository itself must not be assumed to have one deployment method. Units that share a repository may use different mechanisms, identities, targets and rollback boundaries.

Each product records its deployable units and the product-specific values above in `PROJECT_PROFILE.md` or in an applicable authoritative deployment artefact referenced by the profile. A separate deployment manifest is not required by this Standard.

## 3. Deployment Type and Mechanism

A **deployment type** classifies what is deployed. Type names use the target-platform taxonomy:

`<target>_<type>`

A **deployment mechanism** identifies how that unit is delivered. Type and mechanism are separate concepts and must not be treated as interchangeable.

The current governed mapping is:

| Deployment type | Approved mechanism | Detailed authority |
|---|---|---|
| `haos_integration` | `hacs` | Dedicated HACS deployment Standard when approved |
| `haos_app` | `app_repository` | `CENTRAL_GOVERNANCE.md` Section 18.8 until the dedicated App deployment Standard is approved |
| `haos_config` | `tbc` | No approved general mechanism |
| `haos_managed_data` | `tbc` | No approved general mechanism |
| `static_asset` | `github_pages` | Dedicated mechanism Standard when approved |
| `rpi_os_software` | `deb` | Dedicated Debian deployment Standard when approved |

`tbc` is an explicit unresolved state. It must remain `tbc` until a mechanism has been designed, evidenced and approved through governed work. Relationship, convenience or an existing ad hoc copy route must not be used to infer a general mechanism. In particular, no generic HAOS managed-data synchronization mechanism is approved by this Standard.

## 4. Canonical Implementation Structure

The canonical product implementation root is:

`04_Implementation/`

Its first level identifies the target platform. Each target then separates deployable payload from packaging and distribution machinery:

```text
04_Implementation/
└── <target>/
    ├── source/
    └── packaging/
        └── <mechanism>/
```

`source/**` contains authoritative deployable payload and mirrors the applicable target deployment root where the platform permits it.

`packaging/<mechanism>/**` contains machine-consumed or executable build, package, release or distribution machinery for that mechanism. Packaging is organised by delivery mechanism rather than by product component.

Empty structural paths must not be materialised merely to depict the model.

## 5. HAOS Structure

The canonical Home Assistant OS structure is:

```text
04_Implementation/
└── haos/
    ├── source/
    │   ├── config/
    │   │   ├── custom_components/
    │   │   ├── packages/
    │   │   ├── <product data or runtime paths>/
    │   │   └── www/
    │   └── apps/
    └── packaging/
        ├── hacs/
        └── apps/
```

`haos/source/config/**` represents content rooted at Home Assistant `/config/**`.

`haos/source/apps/**` contains authoritative Home Assistant App source. A product using the App custom-repository route places each App package, including its App `config.yaml`, beneath this path unless it remains on the controlled legacy transition path in Section 11.

`haos/packaging/hacs/**` is reserved for HACS-specific packaging and release-support machinery. `haos/packaging/apps/**` is reserved for Home Assistant App repository, build and release-support machinery.

The presence of a packaging directory does not itself approve the mechanism or satisfy its detailed deployment controls.

## 6. Raspberry Pi OS Structure

The canonical Raspberry Pi OS structure is:

```text
04_Implementation/
└── rpi_os/
    ├── source/
    │   ├── opt/
    │   ├── lib/
    │   └── usr/
    └── packaging/
        └── deb/
```

The path beneath `04_Implementation/rpi_os/source/` maps directly to the package-owned target filesystem path.

Runtime or node-local state that is intentionally outside package ownership is not represented as package-owned source merely because it exists on the target. For example, `/etc/advnfc/**` remains outside this tree where the Debian package does not own it.

## 7. Packaging and Operational Deployment Material

The boundary is:

> `04_Implementation/<target>/packaging/<mechanism>/**` builds, packages, prepares or exposes a deployable unit; `08_Deployment/**` explains or records how that unit is deployed, operated, validated or recovered.

Packaging includes machine-consumed build scripts, package metadata, packaging definitions and release-generation tooling.

`08_Deployment/**` contains human-facing or operational material such as installation and rollout runbooks, cutover plans, rollback procedures, migration instructions, environment guidance and retained deployment evidence.

Human-facing documentation must not be placed in `packaging/**` merely because it concerns deployment. Executable packaging machinery must not be placed in `08_Deployment/**`.

## 8. Platform-Required Location Exceptions

Where a target platform or approved deployment mechanism requires an exact repository location, that requirement may override the preferred physical layout only for the required artefact.

Platform-required repository-root descriptors or entrypoints must remain thin. They must not become a second authoritative implementation tree or duplicate payload.

Recognised examples include:

- root `repository.yaml` for a Home Assistant App custom repository;
- HACS-required root metadata such as `hacs.json`, where applicable; and
- GitHub workflow entrypoints under `.github/workflows/**` where GitHub requires them.

An exception for one path does not create a general permission to place implementation at repository root.

## 9. Interim HACS Source Exception

HACS requires a custom integration's authoritative source at:

`custom_components/<domain>/`

For a HACS-managed integration:

- root `custom_components/<domain>/**` is the authoritative integration source;
- `04_Implementation/haos/source/config/custom_components/<domain>/README.md` provides a pointer to that authoritative root source so the governed deployment map remains navigable;
- integration code must not be duplicated beneath `04_Implementation/**`; and
- the deployment-map path must not use a symlink unless separate governed validation approves that model.

This is an interim explicit exception, not a precedent for unrelated root-level source.

## 10. Deployment Identity, Validation and Recovery

Every deployable unit must have a reproducible identity appropriate to its mechanism. The identity must be sufficient to establish what was deployed and to bind validation evidence to that exact state.

Validation is proportionate to the unit, mechanism and risk. It must cover the material build, delivery, configuration and post-deployment behaviours relied upon for acceptance.

Rollback or recovery targets the deployable unit and its prior known-good identity. Repository branch names alone are not rollback identities where their referenced content can move.

Mechanism-specific Standards may impose stronger identity, validation, evidence, data-preservation or rollback requirements.

## 11. Controlled Migration

Existing governed products using `04_Source/**` migrate through one explicit governed repository-migration issue per affected repository.

Until that issue completes, existing authoritative content may remain under legacy `04_Source/**`. The legacy path is transitional, not the target for new structural design.

Each migration must:

- preserve runtime behaviour;
- preserve deployment semantics;
- move authoritative source into the applicable target-first structure except for approved platform-location exceptions;
- apply the interim HACS pointer exception where relevant;
- update product deployment and runbook documentation;
- validate that release, deployment and rollback paths still work; and
- avoid combining unrelated product changes with the structural migration.

Migration must not be performed opportunistically and must not become an uncontrolled portfolio-wide rewrite.

## 12. Deferred Mechanism Design

Detailed HACS, Home Assistant App, HAOS configuration, HAOS managed-data, GitHub Pages and Debian procedures belong in their mechanism-specific governed work and Standards.

This Standard supplies the shared architecture and classification model only. A mechanism-specific Standard may refine procedures for its mechanism but must not contradict this Standard or `CENTRAL_GOVERNANCE.md`.
