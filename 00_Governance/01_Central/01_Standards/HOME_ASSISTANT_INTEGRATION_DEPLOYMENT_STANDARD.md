# HOME_ASSISTANT_INTEGRATION_DEPLOYMENT_STANDARD.md

**Standard:** Home Assistant Integration Deployment Standard
**Version:** v1.0.1
**Status:** Approved
**Approval tag:** `home-assistant-integration-deployment-standard-v1.0.1`
**Approval date:** 2026-10-05
**Lifecycle:** Independent

## 1. Purpose, Scope and Authority

This Standard defines the mandatory deployment, Beta, stable-release, validation and rollback model for governed Home Assistant custom integrations distributed through the Home Assistant Community Store (HACS).

It is a **product-applicable Standard** maintained authoritatively at:

`/Standards/Product/HOME_ASSISTANT_INTEGRATION_DEPLOYMENT_STANDARD.md`

It is projected unchanged into applicable governed product repositories at:

`00_Governance/01_Central/01_Standards/HOME_ASSISTANT_INTEGRATION_DEPLOYMENT_STANDARD.md`

It applies to a governed deployable unit classified as `haos_integration` with deployment mechanism `hacs` under the Deployment Architecture Standard.

`CENTRAL_GOVERNANCE.md` remains the higher constitutional authority. The Deployment Architecture Standard remains authoritative for deployable-unit classification, canonical structure and platform-required location exceptions. This Standard supplies the mechanism-specific HACS procedure and must not override either authority.

This Standard does not itself authorise Beta deployment, stable promotion, production deployment or rollback. Those actions retain the authority required by Central Governance.

## 2. Platform Basis and Verified Constraint

The external platform basis for this Standard is:

- Home Assistant's `update.install` action, including its optional provider-supported `version` field: <https://www.home-assistant.io/actions/update.install/>;
- Home Assistant's custom-integration `manifest.json` version requirement: <https://developers.home-assistant.io/docs/creating_integration_manifest/#version>; and
- HACS repository installation behaviour at source commit `adb7d83e33d24325535fb43b8226572405143757`, including resolution of a requested non-default version through a Git tag: <https://github.com/hacs/integration/blob/adb7d83e33d24325535fb43b8226572405143757/custom_components/hacs/repositories/base.py>.

Current HACS behaviour does not reliably install an arbitrary commit SHA supplied as the `version` value when a repository uses releases. HACS also checks version-specific repository metadata before downloading an explicitly requested ref. A governed Beta candidate therefore uses an immutable lightweight Git tag that resolves to the exact candidate commit, and the tagged tree must contain the HACS metadata required to validate that requested version. The tag is the HACS-facing install identity; the full commit SHA remains the underlying immutable Git identity.

If future HACS behaviour invalidates this constraint or route, governed work must reassess and update this Standard before adopting a replacement mechanism.

## 3. Standard Installation and Update Mechanism

HACS is the standard installation and update mechanism for governed Home Assistant custom integrations.

Routine production deployment must not depend on SMB, direct file copying or another manual synchronization route into `/config/custom_components`.

Manual copying is permitted only for:

- development;
- diagnostics;
- recovery; or
- an explicitly justified deployment exception recorded against the governing work.

An exception does not silently become the product's normal deployment mechanism.

## 4. Repository and Configuration Model

The governed HACS repository remains minimal and HACS-native.

It provides:

- authoritative integration source at root `custom_components/<domain>/` under the Deployment Architecture Standard's HACS source exception;
- the Home Assistant integration metadata required by the platform;
- version-addressable `hacs.json` metadata sufficient for HACS to validate an explicitly requested Beta tag; and
- only the other HACS metadata and release automation required for supported installation, immutable-tag Beta deployment and stable release handling.

Integration source must not be duplicated beneath `04_Implementation/**`.

Project-controlled HACS packaging, validation and release-support machinery belongs under:

`04_Implementation/haos/packaging/hacs/`

Platform-required files remain at their required locations. This includes GitHub workflow entrypoints under `.github/workflows/**` and HACS-required root metadata where applicable. A thin platform entrypoint may invoke authoritative project-controlled logic beneath the canonical packaging path.

Where the integration and Home Assistant platform support it, normal configuration uses Home Assistant UI/config-entry setup. Routine installation or configuration must not require edits to `configuration.yaml`.

YAML configuration is permitted only where the integration genuinely requires it or where a specific justified exception is recorded.

## 5. Version and Deployment Identity

The integration's authoritative stable version is the `version` declared in:

`custom_components/<domain>/manifest.json`

A separate `VERSION` file or duplicate version source must not be introduced.

Stable releases use:

`vX.Y.Z`

The stable tag version must equal the `manifest.json` version apart from the optional leading `v` in the Git tag.

A Beta candidate uses an immutable lightweight Git tag. The preferred form is:

`vX.Y.Z-beta.<short-sha>`

The Beta tag must:

- resolve to the exact persistent-`beta` candidate commit;
- retain the full candidate SHA as its underlying recorded commit identity;
- never be moved, overwritten or reused; and
- not create a GitHub prerelease.

The candidate may already declare its intended stable version in `manifest.json`. A Beta-specific manifest version is not required because the immutable Beta tag identifies the HACS deployment candidate.

## 6. Beta Candidate Preparation

While persistent `beta` represents the next deployable test candidate, every governed merge to `beta` produces the next Beta candidate commit.

Before Beta deployment:

1. identify and record the exact full candidate commit SHA on persistent `beta`;
2. derive the Beta tag from the intended stable version and candidate short SHA unless an equally unambiguous approved name is required;
3. confirm that the proposed tag does not already exist;
4. create the lightweight Beta tag at the exact candidate SHA;
5. verify that the tagged tree contains valid version-addressable `hacs.json` metadata for the HACS requested-version route;
6. push the tag without creating a GitHub prerelease; and
7. independently verify that the remote tag resolves to the recorded candidate SHA.

An existing conflicting tag is an identity failure. It must not be moved or replaced.

Tag creation and push form part of Beta-entry preparation and require the applicable Beta/deployment authority under Central Governance.

## 7. Beta Operator Handoff and Installation

Beta deployment remains an operator action in Home Assistant unless a separately approved automated route exists.

At transition into Beta, the operator handoff must include:

- exact immutable Beta tag;
- exact full candidate commit SHA to which the tag resolves;
- confirmation that HACS can validate the tagged repository metadata;
- target Home Assistant instance;
- verified HACS-created update entity;
- the exact `update.install` action;
- required restart or reload step; and
- post-deployment validation steps.

The supported action is:

```yaml
action: update.install
target:
  entity_id: update.<integration>_update
data:
  version: "<beta-tag>"
```

The update entity is instance-specific and must be verified on the target instance. The action must target the immutable Beta tag, not `main`, `beta` or a raw commit SHA.

## 8. Post-Deployment Validation

A governed HACS install or update is incomplete until the operator performs lightweight post-deployment validation.

At minimum, validation must:

1. confirm that the expected Beta tag or stable version is installed;
2. restart or reload Home Assistant where required;
3. confirm that the integration loads without errors; and
4. perform one basic functional check appropriate to the integration.

For Beta, the recorded tag-to-SHA verification and installed-tag observation together bind the runtime result to the candidate commit.

Validation automation or notification is not required by this version of the Standard.

## 9. Beta Acceptance, Promotion and Stable Release

Beta acceptance applies only to the exact candidate identified by the immutable Beta tag and its verified full commit SHA.

After Beta acceptance and explicit stable-promotion authority:

1. promote the same tested runtime-affecting content to `main` under Central Governance;
2. establish the selected integrated stable release SHA under Central Governance Sections 19.3 and 19.4;
3. where promotion preserves the Beta candidate commit identity, require the selected stable release SHA to equal the exact Beta-tested candidate SHA;
4. where promotion produces a different integrated `main` SHA, accept that SHA only where the promotion-equivalence evidence required by Sections 11.7 and 15.8 proves that its runtime-affecting integration content is equivalent to the accepted Beta candidate and any additional release content has valid coverage;
5. read the stable version from `custom_components/<domain>/manifest.json` at the selected stable release SHA;
6. automatically create the corresponding stable tag and GitHub Release at that selected stable release SHA; and
7. record the relationship among the immutable Beta tag, exact Beta candidate SHA, selected stable release SHA and promotion-equivalence evidence.

The Beta tag remains immutable and bound to the exact tested candidate. The stable tag identifies the selected integrated stable release cut-off. The two tags resolve to the same commit where promotion preserves identity; they may resolve to different commits only through the governed promotion-equivalence route above.

The automatic stable-release step is part of this approved mechanism after stable-promotion authority exists. It does not independently authorise promotion or production deployment.

Release automation must fail closed if:

- the stable tag/version and `manifest.json` version do not align;
- the stable tag does not resolve to the selected integrated stable release SHA;
- the Beta and stable tags resolve to different commits without valid required promotion-equivalence evidence;
- the stable tag already exists with contradictory identity; or
- required Beta-acceptance or promotion evidence is absent.

## 10. Stable Deployment Handoff

Production installation or update uses the normal HACS stable update flow after promotion and successful stable-release creation.

The production handoff must include:

- stable release version;
- target Home Assistant instance;
- HACS-managed integration/update entity;
- required restart or reload step;
- post-deployment validation steps; and
- exact version installed on that instance immediately before deployment.

Normal stable deployment does not require the operator to enter a commit SHA manually.

Stable-release creation does not itself authorise or prove production deployment.

## 11. Failure and Rollback

If installation, reload/restart, integration loading, identity verification or the functional check fails:

- do not accept, promote or claim successful deployment of the candidate;
- preserve diagnostic evidence without retaining secrets;
- identify the exact version installed on the affected instance immediately before the failed deployment;
- restore that exact prior version with required rollback authority; and
- repeat the applicable restart/reload, load-error and functional checks after restoration.

Rollback is instance-specific and version-based. The prior version may be a stable release or an immutable Beta tag. Its tag must resolve to the exact commit previously installed.

Moving branches such as `main` or `beta` are not rollback identities.

## 12. Evidence and Traceability

The governing Linear issue and supporting authoritative evidence must establish, as applicable:

- product and integration domain;
- target Home Assistant instance;
- exact Beta tag and full candidate SHA;
- remote tag-to-SHA verification;
- prior installed version;
- HACS update entity and requested version;
- install/update result;
- restart or reload result;
- integration load result;
- basic functional-check result;
- Beta acceptance result;
- promotion-equivalence result;
- stable manifest version, tag, SHA and GitHub Release; and
- rollback target and result where rollback occurs.

Evidence proves only the state it actually observes. A displayed HACS version does not replace Git tag-to-commit verification, and Git identity alone does not prove successful runtime operation.

## 13. Deferred Capabilities

The following are not required by this version of the Standard:

- automatic post-deployment validation;
- automatic validation notifications;
- a Home Assistant helper, script or button for Beta deployment; and
- a different persistent-`beta` operating model.

Any future change to these capabilities follows normal governed work and must preserve unambiguous candidate identity, validation and rollback.
