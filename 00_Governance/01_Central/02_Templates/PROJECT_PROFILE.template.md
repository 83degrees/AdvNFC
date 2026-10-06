# PROJECT_PROFILE: <Product name>

**Template:** Project Profile
**Version:** v1.4.1
**Status:** Approved
**Approval tag:** `project-profile-template-v1.4.1`
**Approval date:** 2026-10-05

This template is a centrally managed implementation aid for creating a conformant product `PROJECT_PROFILE.md`.

It is not an independent governance authority. Requirements for the Project Profile are defined by `CENTRAL_GOVERNANCE.md`.

## Profile conformance

The required profile content is limited to the sections marked **Required**:
product name, DDR origin code, default Linear team, purpose, scope, ownership/boundaries, approved architecture
location, contracts provided, contracts consumed, product dependencies,
implementation namespace/naming identity, and production/evidence route.
Where the product has deployable content, the deployable-unit inventory is also required.

Sections and fields marked **Optional/recommended** may be included when useful
and may otherwise be omitted or left blank without making the profile
non-conformant.

## Optional/recommended: Document status

- Governance state (optional/recommended): `<current approved | approved target | proposed | historical | unresolved>`
- Product owner (optional/recommended): `<person or accountable role>`
- Last approved through Linear (optional/recommended): `<ISSUE-ID>`
- Exact repository/version (optional/recommended): `<repository and SHA/tag>`

Use the state terms defined in `CENTRAL_GOVERNANCE.md`. Do not describe an
approved target or proposal as current implemented.

## Required: Product identity

- Product name: `<canonical product name>`
- Repository (optional/recommended): `<owner/repository>`
- Primary owner (optional/recommended): `<person or accountable role>`
- DDR origin code: `<two-digit product code>`

## Required: Linear work routing

- Default Linear team: `<Linear team key/identifier>`

This field supplies the project-specific default value used by the central
Linear team-selection rule. Do not repeat or redefine that operating rule in the
Project Profile.

## Required: Purpose

`<What the product exists to do and for whom.>`

## Required: Scope

### In scope

- `<Owned responsibility>`

### Out of scope

- `<Explicit non-responsibility>`

## Required: Ownership and boundaries

| Boundary or capability | Relationship | Owner | Notes (optional/recommended) |
| --- | --- | --- | --- |
| `<boundary>` | `<owned | consumed | shared | external>` | `<owner>` | `<constraints or clarification>` |

Identify product, subsystem, data, runtime, and external-system boundaries that
are material to ownership. A dependency or reused name does not transfer
ownership.

## Required: Approved architecture location

- Approved architecture location: `<authoritative architecture path>`
- Architecture state (optional/recommended): `<current approved | approved target | proposed | unresolved>`
- Material DDRs (optional/recommended): `<DDR-<origin product code>-<local sequence> or None>`

The architecture Markdown is the semantic authority. Diagrams are governed
representations and must conform to the Architecture Diagram Standard.

## Required: Contracts provided

| Contract | Status/version (optional/recommended) | Authoritative provider-owned location (optional/recommended) | Consumers (optional/recommended) | Notes (optional/recommended) |
| --- | --- | --- | --- | --- |
| `<INTERFACE.md>` | `<status/version>` | `<Product>/03_Contracts/<INTERFACE.md>` | `<consumer(s)>` | `<compatibility or limitations>` |

## Required: Contracts consumed

| Contract | Status/version (optional/recommended) | Provider/owner (optional/recommended) | Authoritative location (optional/recommended) | Local use (optional/recommended) |
| --- | --- | --- | --- | --- |
| `<INTERFACE.md>` | `<status/version>` | `<provider>` | `<Provider>/03_Contracts/<INTERFACE.md>` | `<how the governed interface is consumed>` |

Do not create an authoritative duplicate of a consumed contract. Dependencies
use governed interfaces rather than undocumented provider internals.

## Required: Product dependencies

| Dependency | Type (optional/recommended) | Owner (optional/recommended) | Governed interface/evidence (optional/recommended) | Required state (optional/recommended) | Failure boundary (optional/recommended) |
| --- | --- | --- | --- | --- | --- |
| `<dependency>` | `<product | service | data | platform | external>` | `<owner>` | `<contract, evidence route, or N/A>` | `<requirement>` | `<expected behaviour or limitation>` |

## Required: Implementation namespace / naming identity

- Implementation namespace / naming identity: `<canonical namespace, domain, prefix, package, integration identity, or other owned naming boundary>`

Explain how the implementation namespace identifies ownership and legitimate
reuse. List consumed, shared, or external namespaces separately; do not imply
ownership that the product does not possess.

Optional/recommended detail:

| Identity | Classification | Owner | Permitted use | Evidence |
| --- | --- | --- | --- | --- |
| `<domain/prefix/package/service/entity>` | `<owned | consumed | shared | external>` | `<owner>` | `<scope of use>` | `<architecture, contract, repository, or production route>` |

Record naming collisions, legacy aliases, or unresolved ownership explicitly.
Do not normalize a caller capture name, returned field, or foreign namespace
merely for consistency.

## Required: Production and evidence route

- Production route: `<where and how the product is deployed or operated>`
- Evidence route: `<route to current production evidence>`
- Evidence owner (optional/recommended): `<person or role>`
- Provenance and freshness requirement (optional/recommended): `<capture/live source, timestamp expectations, integrity checks>`
- Secrets and mutable-state boundary (optional/recommended): `<where these remain; they must not be stored in governed repositories>`
- Validation evidence route (optional/recommended): `<where exact repository/SHA validation evidence is recorded>`
- Known limitations (optional/recommended): `<missing, stale, excluded, or unresolved evidence>`

Production evidence, Git state, and validation evidence are distinct. A push or
repository state does not prove deployed runtime truth.

## Required when applicable: Deployable units

Include one row for every independently deployable unit. Omit this section only where the product has no deployable content.

| Unit | Deployment type | Authoritative source | Target | Mechanism | Release/update route | Validation route | Rollback/recovery identity |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `<bounded unit>` | `<approved target_type>` | `<repository path>` | `<environment or target>` | `<approved mechanism or tbc>` | `<route or unresolved>` | `<checks/evidence route>` | `<prior known-good identity and recovery route>` |

Use the classifications and canonical structure in `DEPLOYMENT_ARCHITECTURE_STANDARD.md`. A product may have more than one row and more than one mechanism. Do not infer a mechanism where the Standard records `tbc`. A separate deployment manifest is not required.

## Optional/recommended: Current and target state summary

| Area | State | Statement | Authority/evidence |
| --- | --- | --- | --- |
| `<area>` | `<current implemented | current approved | approved target | proposed | historical | unresolved>` | `<concise statement>` | `<authoritative path or evidence route>` |

## Required when applicable: Home Assistant App repository deployment

Include this section when the product is installed or updated as a Home Assistant App through a Git custom repository. Omit it for other products.

- App package path: `04_Implementation/haos/source/apps/<app>/` (or legacy `04_Source/<app>/` only while an explicit migration issue remains open)
- App slug/identity: `<Home Assistant App slug>`
- Repository manifest: `repository.yaml` at product root
- Beta repository source: `https://github.com/<owner>/<repository>#beta`
- Stable repository source: `<accepted stable branch-qualified or unqualified source>`
- Repository visibility model: `<public | private with separately authorised temporary-public deployment windows | credentialed approved route>`
- Beta environment association: `<environment(s) authorised to retain the #beta source>`
- App-private data/configuration boundary: `<location, backup and preservation route>`
- Deployment runbook: `<product runbook based on HOME_ASSISTANT_APP_DEPLOYMENT_RUNBOOK.template.md>`
- Deployment evidence route: `<Linear issue and supporting environment evidence>`
- Prior working candidate / rollback route: `<how identified and restored>`

Do not record credentials in the profile. A temporary-public model must acknowledge that publication cannot be retracted from third-party copies or caches and that every install/update window requires fresh explicit authority under `HOME_ASSISTANT_APP_DEPLOYMENT_STANDARD.md`, as required by Central Governance Section 18.8.

## Optional/recommended: Governance and work control

- Linear project/team: `<project/team>`
- Current governing issues: `<ISSUE-ID(s)>`
- Applicable change classes: `<Change: ...>`
- Repository workflow: `<branch and PR expectations>`
- Human approver(s): `<person or role>`

## Optional/recommended: Unresolved items

- `<Question, owner, decision route, and blocking effect, or None>`
