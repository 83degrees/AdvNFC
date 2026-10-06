# GITHUB_PAGES_DEPLOYMENT_STANDARD.md

**Standard:** GitHub Pages Deployment Standard
**Version:** v1.0.0
**Status:** Approved
**Approval tag:** `github-pages-deployment-standard-v1.0.0`
**Approval date:** 2026-10-06
**Lifecycle:** Independent

## 1. Purpose, Scope and Authority

This Standard defines the mandatory publication, identity, validation, recovery and evidence model for governed static assets delivered through GitHub Pages.

It is a **product-applicable Standard** maintained authoritatively at:

`/Standards/Product/GITHUB_PAGES_DEPLOYMENT_STANDARD.md`

It is projected unchanged into applicable governed product repositories at:

`00_Governance/01_Central/01_Standards/GITHUB_PAGES_DEPLOYMENT_STANDARD.md`

It applies to a governed deployable unit classified as `static_asset` with deployment mechanism `github_pages` under the Deployment Architecture Standard.

`CENTRAL_GOVERNANCE.md` remains the higher constitutional authority. The Deployment Architecture Standard remains authoritative for deployable-unit classification, canonical source and packaging structure, and platform-required location exceptions. Product architecture and the Project Profile remain authoritative for product-specific source, target, endpoint and environment meaning. This Standard supplies only the mechanism-specific GitHub Pages controls and must not duplicate or override those authorities.

This Standard does not itself authorise publication, Beta deployment, stable promotion, production deployment, rollback or unpublication. It does not bypass issue workflow, human review, validation, Beta or stable authority, deployment authority, rollback authority or other required approval gates.

## 2. Platform Basis

The external platform basis for this model is GitHub's documentation for [configuring a publishing source](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site), [using custom workflows](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages), [managing a custom domain](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site) and [unpublishing a site](https://docs.github.com/en/pages/getting-started-with-github-pages/unpublishing-a-github-pages-site).

GitHub Pages supports publication from a selected branch/folder or from an artifact deployed by GitHub Actions. GitHub ultimately performs Pages deployments through Actions, and Pages content may be internet-accessible even when its repository is private, subject to the applicable GitHub plan and configuration.

These sources describe platform behaviour; this Standard defines the governed controls for using it.

## 3. Product Declaration and Publication Model

The applicable Project Profile or product deployment authority must identify, for each GitHub Pages deployable unit:

- authoritative source location;
- selected publication model: `actions_artifact` or `branch_source`;
- build or publication machinery location;
- source branch and any selected publication branch/folder;
- GitHub repository, Pages site and canonical endpoint;
- Beta and stable environment/endpoints where both exist;
- whether generated output is retained or reproducibly rebuilt;
- custom-domain and HTTPS expectations where applicable;
- publication validation route; and
- rollback or recovery route and prior-known-good identity.

Exactly one publication model is authoritative for a deployed site at a time. A product must not treat branch publication and a custom Actions artifact workflow as interchangeable concurrent authorities.

A change of publication model, source branch/folder, canonical endpoint, custom domain, or environment meaning is a governed deployment change rather than an incidental repository setting edit.

## 4. Authoritative Source and Machinery Boundary

Authoritative static-asset source remains at the canonical source location selected under the Deployment Architecture Standard. Machine-consumed build, packaging and publication machinery belongs under the applicable `04_Implementation/<target>/packaging/github_pages/**` path except for the thin workflow entrypoint that GitHub requires under `.github/workflows/**`.

The workflow entrypoint may define the GitHub-required orchestration, permissions and environment binding. Substantive reusable build or publication logic must not be duplicated there when governed packaging machinery already supplies it.

Generated output is a publication product, not a second authoritative source tree, unless product architecture explicitly designates prebuilt static files as the authoritative deployable source. Generated output must not be committed back into an unrelated source path or treated as an undocumented alternative authority.

The selected build must consume one exact repository state. Dependencies, tool versions, configuration and inputs material to the published bytes must be pinned or otherwise recorded sufficiently to reproduce or independently verify the output.

## 5. Supported Publication Models

### 5.1 Actions Artifact Publication

Use the `actions_artifact` model when the deployable unit requires a build, when generated output should not live on a publication branch, or when the product selects a custom GitHub Actions publication route.

The governed route must:

1. check out the exact authorised source commit rather than a later moving branch state;
2. build from the declared authoritative source using the governed packaging machinery;
3. validate the generated publication tree before upload;
4. create a deterministic content digest or complete file-manifest digest for that tree;
5. upload exactly that validated tree as the Pages artifact;
6. deploy that artifact through the protected `github-pages` environment or an explicitly approved equivalent; and
7. record the workflow run, run attempt, deployment result and endpoint returned by the deployment.

The workflow requires only the minimum permissions needed for checkout, artifact upload, identity-token use and Pages deployment. Pull-request validation may build and inspect an artifact but must not publish to the live Pages environment unless separately authorised.

### 5.2 Branch-Source Publication

Use the `branch_source` model only where the selected branch and permitted root or `/docs` folder are the intentional publication source.

The governed route must record the exact source commit, selected branch and folder, validate the selected tree before publication, and record the resulting Pages workflow/deployment identity. If external build machinery writes generated output to the publication branch, the generating source commit, output commit and validated output-tree digest must remain traceably bound.

A moving branch name by itself is not publication identity. A commit made with `GITHUB_TOKEN` may not trigger a subsequent branch-source Pages build; the route must verify that the expected Pages workflow actually ran and published the recorded state.

## 6. Publication and Release Identity

Every publication must bind all of the following applicable identities:

- governing Linear issue and authorised workflow stage;
- repository and deployable unit;
- exact source commit SHA and selected source branch;
- exact release or deployment cut-off authorised under Central Governance;
- publication model and selected branch/folder or workflow revision;
- build dependency/configuration identity material to the output;
- validated publication-tree digest;
- artifact identity or exact publication-branch commit;
- GitHub Actions workflow run ID and run attempt;
- GitHub Pages deployment/environment identity;
- canonical endpoint and expected visibility; and
- custom-domain/DNS configuration identity where applicable.

For generated sites, source commit identity alone is insufficient because different build inputs or machinery can produce different output. For branch-source sites, workflow success alone is insufficient because it does not identify the selected source tree. The combined evidence must identify the exact published bytes and the repository state from which they were derived.

If the source, output or Pages deployment identity cannot be established without contradiction, publication must not begin or must not be accepted as successful.

## 7. Trigger, Protection and Cut-Off

Automatic publication triggers may operate only within the deployment authority already established by Central Governance and the product's approved workflow. A Git push, merge, tag, scheduled event or manual workflow dispatch is a technical trigger; it is not by itself approval to publish.

The workflow must enforce the approved source ref or immutable cut-off and use environment protection where required to prevent an unreviewed branch, pull request or unrelated workflow from publishing. Concurrency controls must prevent an older or superseded run from becoming the accepted publication after a later authorised candidate.

Where a product follows `WF-01`, Beta and stable publication must remain bound to the exact candidate and promotion-equivalence controls in Central Governance. A Beta publication must not silently replace the stable public endpoint unless that endpoint and action are explicitly the approved Beta environment and deployment route.

## 8. Publication Validation

Before publication, validation must establish as applicable:

- the exact authorised source and build inputs;
- successful generation of the complete intended output tree;
- absence of secrets, credentials, private data, source maps or internal artefacts not approved for the endpoint;
- expected entry documents, asset paths, base URL and links;
- content or functional checks appropriate to the static asset;
- the publication-tree digest; and
- readiness of the configured Pages environment and domain.

After publication, validation must establish against the canonical endpoint:

- the Pages deployment completed successfully and corresponds to the recorded workflow/deployment identity;
- HTTPS and expected visibility behave as approved;
- the expected release marker, content fingerprint or representative content binds the endpoint to the recorded publication;
- critical documents, assets, links and client-side behaviour load successfully;
- no prior or unrelated publication is being served as the accepted result; and
- custom-domain, redirect and certificate behaviour is correct where applicable.

Workflow success without endpoint observation does not prove successful publication. Endpoint availability without exact-content evidence does not prove that the intended candidate was published.

## 9. Custom Domains and Pages Configuration

Where the default GitHub Pages domain is used, no custom-domain controls are required beyond recording and validating the canonical endpoint.

Where a custom domain is used, the governed deployment authority must record the repository Pages setting, domain ownership/verification, relevant DNS records, HTTPS expectation and responsible operator. Domain verification should be established before cutover and its verification record retained where the domain remains in use.

For branch-source publication, a root `CNAME` file may represent the configured custom domain. For custom Actions publication, GitHub may ignore `CNAME`; repository/API settings and DNS state remain the operative configuration. The product must not infer live domain state from a `CNAME` file alone.

DNS or domain changes must be sequenced to avoid an unclaimed-domain or takeover window. A custom-domain or HTTPS failure prevents acceptance where that domain is the canonical endpoint.

## 10. Failure, Rollback and Recovery

Before publication, record a prior known-good publication identity and confirm that it can be reconstructed or replayed. That identity must include the prior source commit and output digest, plus the retained artifact/publication commit and build inputs required by the selected model.

If build, upload, deployment, identity verification, endpoint validation, custom-domain validation or content validation fails:

- do not accept the candidate or claim successful publication;
- prevent a failed or superseded run from becoming the accepted deployment;
- preserve diagnostic evidence without retaining secrets;
- determine whether the endpoint still serves the prior known-good publication, the failed candidate or an indeterminate state;
- with required rollback authority, redeploy or rebuild the exact prior known-good publication and verify its digest and endpoint behaviour; and
- repeat the applicable post-publication checks after recovery.

If the prior publication cannot be reproduced exactly, recovery must fail closed rather than publish an unverified approximation. Where continued exposure of incorrect or unsafe content is more harmful than loss of availability, an authorised operator may unpublish the Pages site while governed recovery proceeds. Unpublication is a deployment action and is not a substitute for restoring a required service.

A branch name, workflow name, run status or endpoint URL alone is not a rollback identity.

## 11. Evidence and Traceability

The governing Linear issue and supporting authoritative evidence must establish, as applicable:

- product, repository and deployable unit;
- publication model, source branch/folder and workflow revision;
- exact source commit and governed release/cut-off identity;
- material build inputs and publication-tree digest;
- artifact or publication-branch commit identity;
- workflow run ID, attempt and Pages deployment/environment result;
- canonical endpoint, expected visibility and observation time;
- pre-publication and endpoint-validation results;
- custom-domain, DNS and HTTPS evidence where applicable;
- prior known-good publication identity;
- rollback, recovery or unpublication authority and result where used; and
- the relationship among Beta, stable and promoted identities where applicable.

Evidence proves only the state it actually observes. Git identity does not prove endpoint content, and endpoint content without source/output identity does not prove governed provenance.

## 12. Security and Fail-Closed Behaviour

GitHub Pages publication is an external disclosure boundary. A product must explicitly establish the intended visibility of the site independently from repository visibility and must review the publication tree for information that is not authorised for that audience.

Publication tooling must fail closed when it cannot establish the exact authorised source, output digest, selected environment, deployment identity or required custom-domain state. It must not fall back to the latest branch head, reuse an unverified artifact, broaden token permissions, publish a pull-request artifact to the stable endpoint, or treat a successful HTTP response as sufficient identity evidence.

Platform limits, retention periods and action versions that are material to reproducibility or rollback must be pinned, recorded or checked at execution time rather than assumed indefinitely.
