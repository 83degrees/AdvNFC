# HOME_ASSISTANT_APP_DEPLOYMENT_STANDARD.md

**Standard:** Home Assistant App Deployment Standard
**Version:** v1.0.0
**Status:** Approved
**Approval tag:** `home-assistant-app-deployment-standard-v1.0.0`
**Approval date:** 2026-10-05
**Lifecycle:** Independent

## 1. Purpose, Scope and Authority

This Standard defines the mandatory deployment, Beta, publication, validation, data-preservation and rollback model for governed Home Assistant Apps installed or updated through the Home Assistant App store from a Git custom repository.

It is a **product-applicable Standard** maintained authoritatively at:

`/Standards/Product/HOME_ASSISTANT_APP_DEPLOYMENT_STANDARD.md`

It is projected unchanged into applicable governed product repositories at:

`00_Governance/01_Central/01_Standards/HOME_ASSISTANT_APP_DEPLOYMENT_STANDARD.md`

It applies to a governed deployable unit classified as `haos_app` with deployment mechanism `app_repository` under the Deployment Architecture Standard.

`CENTRAL_GOVERNANCE.md` remains the higher constitutional authority. The Deployment Architecture Standard remains authoritative for deployable-unit classification, canonical structure and platform-required location exceptions. This Standard supplies the mechanism-specific App-repository procedure and must not override either authority.

This Standard does not itself authorise publication, Beta deployment, stable promotion, production deployment or rollback. It does not bypass issue workflow, human review, validation, Beta-entry authority, deployment authority, stable-promotion authority, rollback authority or exact-candidate evidence.

## 2. Platform Basis

The external platform basis for this model is the Home Assistant developer documentation for [App repositories](https://developers.home-assistant.io/docs/apps/repository/) and [App configuration](https://developers.home-assistant.io/docs/apps/configuration/), together with Supervisor source commit `bdcba61fc7c1500e96d2e319d07546f7b896e067`: `supervisor/validate.py` defines the optional `#branch` repository syntax, `supervisor/store/git.py` passes the parsed branch to the clone operation, and `supervisor/store/data.py` recursively discovers App configuration.

These sources describe platform behaviour; this Standard defines the controls for using it.

## 3. Repository and App-Package Model

Home Assistant requires a repository configuration file named `repository.yaml` at the repository root. Supervisor recursively discovers App `config.yaml` files in the repository.

A governed product therefore keeps the authoritative App package under:

`04_Implementation/haos/source/apps/<app>/**`

and may place only the required `repository.yaml` metadata at the product root. A product awaiting its controlled structure migration may retain the App package under legacy:

`04_Source/<app>/**`

until its migration issue completes.

Root `repository.yaml` is an approved platform-manifest exception under Central Governance Section 3.2, Appendix E and the Deployment Architecture Standard. It does not authorise root-level runtime implementation or a duplicate App package.

## 4. Repository Source and Deployment Identity

The Home Assistant repository source is part of deployment identity. A branch-qualified source of the form:

`https://github.com/<owner>/<repository>#<branch>`

selects that branch for Supervisor's Git clone/update route.

Governed Beta normally uses `#beta` and remains associated only with the intended Beta environment. Stable installation/update uses the accepted stable branch or release state selected by the product's approved deployment design.

Changing the repository source, branch qualification or App identity is a deployment change and must not be treated as a harmless UI edit.

For `WF-01`, the selected repository source, branch, App version and Git candidate identity must together identify the exact accepted candidate.

## 5. Private Repository Constraint and Publication Meaning

Where the Home Assistant instance intentionally stores no GitHub repository credential, Supervisor can clone or update a private GitHub repository only while anonymous access is possible. If temporary public visibility is selected to enable that access, the visibility change is a security-sensitive external publication event.

Returning the repository to private visibility does not retract content already fetched, cached, cloned, mirrored or observed. Authorisation of a temporary-public window therefore includes explicit acknowledgement that third-party copies may persist permanently. The operation must never be described as fully reversible.

Temporary public visibility is a narrow deployment mechanism, not a release shortcut or standing publication policy. Each install or update that requires anonymous access requires a new authorised public window unless a separately approved product mechanism removes that requirement.

## 6. Public-Window Preconditions

Before a private product repository is made public, the operator must establish and record against the governing Linear issue:

- explicit user authorisation for the exact repository, candidate, target environment and deployment purpose;
- the planned start and end conditions of the public window;
- review of the complete current tree and reachable Git history for secrets, credentials, personal data, sensitive operational evidence and other content unsuitable for publication;
- confirmation that no private dependency or submodule will be exposed, broken or made unusable by anonymous cloning;
- confirmation that publication is compatible with applicable product licensing, third-party content and dependency terms;
- the exact repository source, selected branch, candidate SHA and App version to be deployed;
- an identified rollback target and a plan for preserving App-private data; and
- an operator responsible for restoring and verifying private visibility.

Failure of any precondition prevents the public transition. Secret scanning or repository tooling may support the review, but a narrow current-tree scan alone is not evidence that full Git history is safe to publish.

## 7. Install or Update Window

During the authorised public window:

1. make only the authorised repository public;
2. verify public visibility and record the observation time;
3. add, repair or refresh only the recorded Home Assistant repository source and branch;
4. install or update only the recorded App candidate;
5. verify that Supervisor selected the expected repository, branch and App version;
6. obtain sufficient deployed-content or running-version evidence to bind the running App to the recorded Git candidate; and
7. restore private visibility promptly after the authorised operation, then independently verify and record that private access has been restored.

The public window must not remain open for convenience. If privacy restoration fails or cannot be verified, stop further deployment activity, record the exposure, notify the user promptly and treat the repository as publicly exposed until restoration is proven.

Any suspected credential or sensitive-data exposure follows the applicable incident/rotation route; merely making the repository private is insufficient remediation.

## 8. Preflight, Evidence and Data Preservation

The minimum install/update preflight confirms:

- the target is the intended Home Assistant environment and is suitable for Beta or stable use as applicable;
- the recorded repository source and branch resolve to the intended candidate;
- root `repository.yaml` and the recursively discovered App `config.yaml` are valid;
- the App version corresponds to the candidate being deployed;
- required images, build inputs, dependencies and submodules are anonymously obtainable during the selected route;
- current App configuration and App-private data have a usable backup or preservation route; and
- the prior working candidate and repository source are known.

Deployment evidence records, at minimum, the governing Linear issue, target environment, repository source, selected branch, App slug/version, Git candidate identity, preflight result, install/update result, sufficient running-version or deployed-content verification, visibility-transition timestamps/results where applicable, and rollback outcome if used.

Because Supervisor repository identity is derived from the repository source, removing/re-adding a source or changing its branch qualification may alter repository/App association. Before such a change, preserve App configuration and App-private data, determine whether the installed App would become detached or require reinstallation, and avoid destructive removal until restoration has been proven.

## 9. Failure and Rollback

If clone, refresh, install, update, start-up or candidate verification fails:

- do not promote or claim success for the candidate;
- restore private visibility first where a public window remains open, unless keeping it open is explicitly re-authorised for a bounded recovery action;
- preserve diagnostic evidence without retaining secrets;
- prefer repair or rollback that preserves the existing Supervisor repository/App identity and App-private data;
- roll back to the recorded prior working candidate/source with required user authority; and
- reverify repository visibility, installed version, running state and data preservation after recovery.

Removing a repository source or reinstalling the App is not a default rollback where it could change identity or discard App-private data.

## 10. Reusable Product Guidance

Home Assistant App products record their repository source, Beta/stable branch routing, App identity, visibility model, data-preservation boundary and deployment-evidence route in `PROJECT_PROFILE.md` or the product's applicable deployment authority.

The centrally managed `HOME_ASSISTANT_APP_DEPLOYMENT_RUNBOOK.template.md` is the reusable operator aid for this route. It implements this Standard but does not independently authorise publication, deployment, rollback or promotion.
