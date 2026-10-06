# CENTRAL_GOVERNANCE.md

**Governance version:** 11.10.0
**Status:** Approved
**Approval tag:** `governance-v11.10.0`
**Approval date:** 2026-10-06

**Authority of appendices:**  
All appendices form an integral part of this governance book and carry the same authority as the main body unless an appendix explicitly states otherwise. Agents must apply applicable appendix requirements together with the relevant body sections and must not treat appendices as optional or supplementary guidance.

---

# Contents

## Part I — Governance Foundations

1. Objective  
2. Governance Model  
3. Standard Repository Model  

## Part II — Work Management and Execution

4. Linear as the Workflow Authority  
5. Change Classes  
6. Sub-Issues and Issue Decomposition  
7. Execution Routes  

## Part III — Durable Product Knowledge

8. Knowledge Retention  
9. Design Decision Records  
10. Contract Ownership and Compatibility  

## Part IV — Git, Review and Change Acceptance

11. Git Working Model and Linear Alignment  
12. Branch and Pull Request Rules  
13. Code Review  
14. Non-Code Review  

## Part V — Validation and Completion

15. Validation Model  
16. Validation Failure Handling  
17. Non-Code Completion  
18. Code Completion and Beta  

## Part VI — Stable Product Release

19. Stable Release  
20. Release Modes  

## Part VII — Assurance and Governance Operations

21. Audit Model  
22. Central Governance Change, Release and Distribution Lifecycle  
23. Validation Tooling Lifecycle  
24. Production Evidence Authority  
25. Agent Execution Efficiency  
26. Monitoring and Continuous Improvement  

## Appendices

- Appendix A — Authoritative Workflow Gate Matrix
- Appendix B — Authoritative Change-Class Control Matrix
- Appendix C — Governance Change Approval Checklist
- Appendix D — Monitoring Register
- Appendix E — Authoritative Repository Structure and Artefact Placement

---

## Part I — Governance Foundations

### 1. Objective

Central Governance provides the minimum effective controls needed to protect product integrity, architecture, contracts, durable decisions, recoverability and auditability, while making normal development and maintenance straightforward to execute.

The operating model favours:

- one authoritative source for each kind of truth;
- convention over repeated configuration;
- proportionate controls based on change type and risk;
- lightweight handling of non-code artefacts;
- Git-native history, provenance and rollback;
- clear human approval points;
- automation where it removes repetitive work;
- reuse of valid evidence rather than unnecessary revalidation;
- low execution, runtime and agent-context overhead.

Execution method is interchangeable.

Governance controls apply to the change and its risk, not to whether the work is performed by an agent or manually by the user.

The same required control gates therefore apply regardless of execution method, while the actor and mechanics used to perform the work may differ.

Governance must not become more burdensome than the risks it is intended to control.

#### 1.1 Governed Execution Path

For normal governed work, use the following navigation sequence to identify the applicable authority without treating this map as a separate source of control:

1. **Establish authority and product context** — use Sections 2–3 and the applicable Project Profile, architecture, contracts and evidence sources.
2. **Classify the work and select the workflow** — use Sections 4–5 together with Appendix A for workflow gates and Appendix B for change-class-specific controls.
3. **Define the executable scope and route** — use Sections 6–7 for issue decomposition and execution route.
4. **Identify durable product-knowledge obligations early** — use Sections 8–10 for architecture, DDR and contract obligations that may need to be satisfied during the same logical work.
5. **Execute through Git and human review** — use Sections 11–14 where the normal Git/review route applies.
6. **Validate and complete the issue** — use Sections 15–18, including any applicable durable-knowledge obligations identified above.
7. **Promote a stable product release only where separately applicable** — use Sections 19–20; stable release is not implied by issue completion.
8. **Apply assurance and Governance-operations controls where relevant** — use Sections 21–26 for audit, central Governance lifecycle/distribution, validation tooling, production evidence, execution efficiency and continuous improvement.

This routing map is navigation only. It does not create, weaken, duplicate or replace any requirement in the cited sections or appendices. Where a cited section or appendix applies, that source remains authoritative for the control itself.

---

### 2. Governance Model

#### 2.1 One Central Governance Book

There is one authoritative central governance book:

`CENTRAL_GOVERNANCE.md`

The central governance repository owns and approves this artefact.

Once approved, the exact approved file is deployed unchanged into each product repository as part of the centrally managed governance projection defined in Appendix E.2.

Product repositories must not locally modify the deployed central governance book.

Any change to central governance must first be made and approved in the central governance repository and then distributed as a new approved version.

There shall be:

- no project-specific rendering of the central governance book;
- no generated project governance book;
- no local tailoring of the deployed central governance copy;
- no duplicate substantive validation merely because the approved book has been distributed into another repository.

#### 2.2 Central Governance Repository

The central governance model is maintained in its own independent Git/GitHub repository.

Its authoritative central artefacts include:

- `/CENTRAL_GOVERNANCE.md`
- `/Standards/Product/ARCHITECTURE_DIAGRAM_STANDARD.md`
- `/Standards/Product/DDR_STANDARD.md`
- `/Standards/Product/DEPLOYMENT_ARCHITECTURE_STANDARD.md`
- `/Standards/Product/GITHUB_PAGES_DEPLOYMENT_STANDARD.md`
- `/Standards/Product/HOME_ASSISTANT_APP_DEPLOYMENT_STANDARD.md`
- `/Standards/Product/PRODUCTION_EVIDENCE_STANDARD.md`
- `/Standards/Product/HOME_ASSISTANT_INTEGRATION_DEPLOYMENT_STANDARD.md`
- `/Standards/Central/GOVERNANCE_LIFECYCLE_STANDARD.md`
- `/Standards/Central/GOVERNANCE_DISTRIBUTION_STANDARD.md`
- `/Templates/PROJECT_PROFILE.template.md`
- `/Templates/HOME_ASSISTANT_APP_DEPLOYMENT_RUNBOOK.template.md`
- `/Templates/DIAGRAM_CONVENTION_LEARNING.md`
- `/Templates/DDR.template.md`
- `/Templates/AUDIT_REVIEW_LOG.template.md`
- `/Templates/product_root_agents.template.md`

Central governance artefacts required locally by product agents are deployed through the centrally managed governance projection defined in Appendix E.2.

The repository's `main` branch represents the accepted integrated governance state.

The central governance repository is not required to use the standard product-repository folder structure.

GitHub hosts the repository and may technically enforce branch, pull-request and merge controls.

`CENTRAL_GOVERNANCE.md` remains authoritative for what those controls mean and when they apply.

GitHub configuration does not replace or independently redefine central governance.

#### Centrally Governed Standards

Governance may define centrally governed standards for subjects that require specialised consistent rules but are expected to evolve as a distinct governed discipline.

A centrally governed standard:

- is authoritative within its defined scope;
- is maintained in the central Governance repository;
- has one fixed authoritative filename and path;
- must not contradict `CENTRAL_GOVERNANCE.md`; and
- follows the applicability and lifecycle-delegation rules defined in Section 22.7 together with the detailed Governance Lifecycle Standard where release/provenance mechanics apply.

Centrally governed Standards have one of two applicability categories:

- **Product-applicable** — the Standard is required as product-local working authority and is projected unchanged to every product to which it applies;
- **Central-only** — the Standard is not part of the product projection and is loaded from its authoritative central path only when central Governance operations or a rulebook-routed mechanism-specific task makes it applicable.

Repository structure makes applicability visible. Central-only Standards are stored under:

`/Standards/Central/`

Product-applicable Standards are stored under:

`/Standards/Product/`

The centrally governed standards are:

| Standard | Applicability | Authoritative central path | Deployed product path |
|---|---|---|---|
| `ARCHITECTURE_DIAGRAM_STANDARD.md` | Product-applicable | `/Standards/Product/ARCHITECTURE_DIAGRAM_STANDARD.md` | `00_Governance/01_Central/01_Standards/ARCHITECTURE_DIAGRAM_STANDARD.md` |
| `DDR_STANDARD.md` | Product-applicable | `/Standards/Product/DDR_STANDARD.md` | `00_Governance/01_Central/01_Standards/DDR_STANDARD.md` |
| `DEPLOYMENT_ARCHITECTURE_STANDARD.md` | Product-applicable | `/Standards/Product/DEPLOYMENT_ARCHITECTURE_STANDARD.md` | `00_Governance/01_Central/01_Standards/DEPLOYMENT_ARCHITECTURE_STANDARD.md` |
| `GITHUB_PAGES_DEPLOYMENT_STANDARD.md` | Product-applicable | `/Standards/Product/GITHUB_PAGES_DEPLOYMENT_STANDARD.md` | `00_Governance/01_Central/01_Standards/GITHUB_PAGES_DEPLOYMENT_STANDARD.md` |
| `HOME_ASSISTANT_APP_DEPLOYMENT_STANDARD.md` | Product-applicable | `/Standards/Product/HOME_ASSISTANT_APP_DEPLOYMENT_STANDARD.md` | `00_Governance/01_Central/01_Standards/HOME_ASSISTANT_APP_DEPLOYMENT_STANDARD.md` |
| `PRODUCTION_EVIDENCE_STANDARD.md` | Product-applicable | `/Standards/Product/PRODUCTION_EVIDENCE_STANDARD.md` | `00_Governance/01_Central/01_Standards/PRODUCTION_EVIDENCE_STANDARD.md` |
| `HOME_ASSISTANT_INTEGRATION_DEPLOYMENT_STANDARD.md` | Product-applicable | `/Standards/Product/HOME_ASSISTANT_INTEGRATION_DEPLOYMENT_STANDARD.md` | `00_Governance/01_Central/01_Standards/HOME_ASSISTANT_INTEGRATION_DEPLOYMENT_STANDARD.md` |
| `GOVERNANCE_LIFECYCLE_STANDARD.md` | Central-only | `/Standards/Central/GOVERNANCE_LIFECYCLE_STANDARD.md` | — |
| `GOVERNANCE_DISTRIBUTION_STANDARD.md` | Central-only | `/Standards/Central/GOVERNANCE_DISTRIBUTION_STANDARD.md` | — |

Where `CENTRAL_GOVERNANCE.md` and a centrally governed standard conflict, `CENTRAL_GOVERNANCE.md` prevails and the conflict must be surfaced for resolution.

#### 2.3 Root `AGENTS.md`

Every product repository contains a small, stable root:

`AGENTS.md`

Its purpose is to route the agent to applicable Governance and product-context authority without becoming a second Governance rulebook.

Before working in the repository, the loader directs the agent to establish:

- `00_Governance/01_Central/CENTRAL_GOVERNANCE.md` as the constitutional Governance authority; and
- `00_Governance/PROJECT_PROFILE.md` as the product-context authority.

The agent then uses the governed execution path to identify and read the sections, appendices, Standards and other current authority applicable to the task. The agent must retain sufficient awareness of Central Governance to route safely, but must not load unrelated Governance material solely because it exists.

The root `AGENTS.md` is centrally managed and projected verbatim from the inert central source:

`/Templates/product_root_agents.template.md`

The central source is deliberately not named `AGENTS.md` and is not an active instruction surface within the Governance repository. The active filename `AGENTS.md` is introduced only at the governed product-root projection target.

Product repositories must not locally modify the projected root loader.

The root loader remains common across governed products. Product-specific operating rules, product identity and product-specific authority belong in their applicable authoritative product artefacts rather than in `AGENTS.md`.

When task scope makes a specialised centrally governed Standard applicable, the governed execution path identifies that Standard for loading. The root loader itself must not duplicate those task-specific routing rules.

The root `AGENTS.md` must not become an additional Governance rulebook or a location for project-specific operating rules.

#### 2.4 Project Profile

Every product repository contains:

`00_Governance/PROJECT_PROFILE.md`

The Project Profile defines what the product is.

It contains at minimum:

- project name;
- DDR origin code;
- default Linear team;
- purpose;
- scope;
- explicit boundaries and out-of-scope responsibilities;
- authoritative architecture artefact;
- external contracts consumed;
- relevant external dependencies or evidence sources where necessary.

The DDR origin code is the product's immutable code used when allocating DDR identifiers. It identifies the product in which a DDR originates and does not represent current DDR ownership.

The Project Profile must not repeat common governance, workflow, validation, DDR, repository or operating rules already defined centrally.

Project-specific governance overrides are not permitted as standing rules.

If a project exposes a genuine need for a different rule, that need is raised through the governance-improvement process.

#### 2.4.1 Project Profile Change Classification

Changes to `PROJECT_PROFILE.md` are classified according to their semantic effect rather than through a dedicated profile change class.

Examples:

| Semantic effect | Typical change class | Important condition |
|---|---|---|
| Substantive change to product scope, responsibility or architectural boundary | `Change: Architecture` | Normally carries this class because the underlying architectural subject changes |
| Correction or descriptive update | `Change: Documentation` | Applies only where architecture or another governed authority is not altered |
| Change to the declaration that a product consumes an existing external contract | Not automatically `Change: Contract` | The provider-owned contract itself has not necessarily changed |
| Another governed subject is actually changed | Applicable underlying change class | Apply the class only where its underlying governed subject is changed |

File location or filename does not override semantic classification.

#### 2.5 Authority by Subject

Different authoritative sources answer different questions.

| Subject | Authoritative source |
|---|---|
| Governance rules and operating model | `CENTRAL_GOVERNANCE.md` |
| Product identity, scope and declared external dependencies | `PROJECT_PROFILE.md` |
| Approved product architecture | Approved `*_ARCHITECTURE.md` |
| Architecture diagram construction and shared presentation conventions | `ARCHITECTURE_DIAGRAM_STANDARD.md` |
| DDR construction, numbering, status and supersession specification | `DDR_STANDARD.md` |
| Cross-product deployable-unit classification, source/packaging structure and deployment architecture | `DEPLOYMENT_ARCHITECTURE_STANDARD.md` |
| GitHub Pages publication, validation, recovery and evidence for governed static assets | `GITHUB_PAGES_DEPLOYMENT_STANDARD.md` |
| App-repository deployment, publication, validation, data preservation and rollback for governed Home Assistant Apps | `HOME_ASSISTANT_APP_DEPLOYMENT_STANDARD.md` |
| HACS deployment, Beta identity, stable release, validation and rollback for governed Home Assistant custom integrations | `HOME_ASSISTANT_INTEGRATION_DEPLOYMENT_STANDARD.md` |
| Production-evidence acquisition, freshness, retention, integrity and reuse practice | `PRODUCTION_EVIDENCE_STANDARD.md` |
| Central Governance release/provenance lifecycle mechanics | `GOVERNANCE_LIFECYCLE_STANDARD.md` |
| Central Governance downstream distribution protocol | `GOVERNANCE_DISTRIBUTION_STANDARD.md` |
| Cross-product interface | Provider-owned authoritative contract |
| Significant durable design rationale | Applicable DDR |
| Current implemented/runtime state | Approved current production evidence |
| Operational work state | Linear |
| Repository/version history and exact repository states | Git/GitHub |

These sources do not form a simple universal priority hierarchy.

For example:

- production evidence establishes what currently runs;
- architecture establishes what is approved;
- Git establishes exact repository history;
- Linear establishes operational workflow state.

Where relevant authoritative sources appear inconsistent, the discrepancy must be surfaced and resolved through the applicable governed workflow.

Agents must not silently choose one source and reinterpret another.

Approved `*_ARCHITECTURE.md` documentation remains authoritative for product architecture, architectural meaning, boundaries and product-specific semantics.

`ARCHITECTURE_DIAGRAM_STANDARD.md` governs common diagram representation. It does not define product architecture.

For diagram work, the authority order is:

1. `CENTRAL_GOVERNANCE.md`;
2. `ARCHITECTURE_DIAGRAM_STANDARD.md`;
3. applicable approved `*_ARCHITECTURE.md` and governed contracts;
4. `DIAGRAM_CONVENTION_LEARNING.md`;
5. incidental existing presentation where no higher authority defines the matter.

`DIAGRAM_CONVENTION_LEARNING.md` must never override a higher-authority source.

A convention recorded in the learning file may be used as a local working default only where it does not conflict with:

1. `CENTRAL_GOVERNANCE.md`;
2. `ARCHITECTURE_DIAGRAM_STANDARD.md`;
3. approved product architecture;
4. applicable contracts; or
5. an explicit user instruction.

Higher-authority sources always prevail.

#### 2.5.1 State Labelling

Where an authoritative artefact contains information representing different lifecycle states, those states must be clearly distinguishable.

In particular, distinguish where applicable:

- current implemented state;
- current approved architecture;
- approved target state;
- proposed or exploratory design;
- historical state;
- unresolved or uncertain state.

Proposed or exploratory design must not be described as current implementation or current approved architecture.

#### 2.6 Governance Improvement Feedback

Agents must monitor the operation of the governance model during normal work.

Governance-improvement observations and recommendations are advisory only. They do not become governance unless explicitly accepted by the user and incorporated into the applicable authoritative central Governance artefact through its defined approval lifecycle.

The constitutional feedback loop remains:

`observe → evidence → recommend → user review → applicable central change if accepted`

Detailed observation, recommendation, review and promotion mechanics are consolidated in Section 26.1.

#### 2.7 Project AAR Register

Each product repository maintains:

`00_Governance/AAR_REGISTER.md`

The register captures governance and operating-model observations arising from real project work.

It must not become:

- a product defect backlog;
- an execution log;
- a substitute for Linear;
- a repository for ordinary task notes.

AAR entries should contain at minimum:

- date;
- source issue/task;
- observation;
- practical impact;
- recommendation;
- status;
- central follow-up reference where applicable.

Statuses are:

- `Open`
- `Promoted`
- `Rejected`
- `Superseded`

Entries are append-only except for status and follow-up/reference fields.

Recurring review and promotion mechanics for open observations are defined in Section 26.2.

#### 2.8 In-Flight User Authority

The user remains the final authority over the project governance model.

The user may explicitly authorise an in-flight override for a specific work item.

An override may:

- resolve ambiguity;
- provide task-specific direction;
- authorise an exception to a normal governance rule;
- permit current work to proceed where strict application would otherwise block it.

Where an override is given, the agent must:

1. record the override and its scope against the current work item or PR;
2. proceed according to the authority provided;
3. not treat the override as a permanent rule;
4. not reuse it automatically on later work;
5. record an AAR observation where it exposes a recurring governance gap or defect.

An in-flight override changes authority for that work item only.

Only an accepted and formally incorporated central change alters governance for future work.

This authority remains subject to genuinely non-waivable external legal, safety or platform constraints.

---

### 3. Standard Repository Model

Every product repository follows the same centrally governed repository model unless central governance itself is changed.

Repository structure favours convention over configuration.

Agents should infer expected handling of an artefact substantially from its location.

Top-level folders should use meaningful subfolders where this improves organisation. Large flat collections of unrelated files should be avoided.

Detailed standard repository paths, folder purposes, placement rules and materialisation mechanics are defined in **Appendix E — Authoritative Repository Structure and Artefact Placement**. Appendix E is consulted when detailed placement is material; ordinary work need not load the full placement catalogue where the relevant existing location is already established.

#### 3.1 Central and Product Ownership Boundary

Everything under:

`00_Governance/01_Central/**`

is centrally managed content.

Two exact managed paths outside that subtree are also centrally owned:

- product-root `AGENTS.md`;
- `.github/workflows/central-gov-hook.yml`.

Product-local work must not create, edit, rename, move or delete anything within `00_Governance/01_Central/**`, and must not locally modify either exact centrally managed out-of-subtree path.

The central Governance repository remains the source of truth for all centrally projected content. The canonical source for product-root `AGENTS.md` is `/Templates/product_root_agents.template.md`. The canonical source for `.github/workflows/central-gov-hook.yml` is `/Templates/central_gov_hook.yml`.

The product hook is deliberately thin. It triggers on every pull request and runs the centrally managed read-only routing checker projected at `00_Governance/01_Central/03_Tooling/central_gov_checks.py`. The authoritative source remains `/tooling/central_gov_checks.py` in the Governance repository; distribution projects the exact approved checker into each governed product so the control works for both public and private repositories without requiring runtime access to the private Governance repository. Product-specific parameters are not embedded in the hook. Applicable checks are inferred centrally from deterministic governed repository structure.

These exact out-of-subtree exceptions do not authorise central ownership of other product-root or `.github/**` content.

`PROJECT_PROFILE.md` and `AAR_REGISTER.md` are product-owned artefacts and remain outside the centrally managed subtree.

Templates within `01_Central/02_Templates/` are centrally managed implementation aids. Their presence in a product repository does not make them independent governance authorities.

`ARCHITECTURE_DIAGRAM_STANDARD.md`, `DDR_STANDARD.md`, `DEPLOYMENT_ARCHITECTURE_STANDARD.md` and `PRODUCTION_EVIDENCE_STANDARD.md` are exact deployed copies of their centrally approved standards and must not contain product-specific amendments.

Product-specific architectural meaning belongs in the applicable approved architecture documentation. Product-specific durable design rationale belongs in the applicable product DDRs. Product/environment evidence routes belong in the applicable Project Profile or environment authority.

Routine architecture, validation output, audit evidence or product work must not accumulate in `00_Governance/01_Central/`.

Repository location does not change the substantive authority relationships defined elsewhere in this Governance book. In particular, approved `*_ARCHITECTURE.md` remains authoritative for product architecture; diagrams support but do not replace that record; provider-owned contracts remain authoritative for their interfaces; centrally governed Standards retain only their defined scope; and centrally managed templates remain non-authoritative implementation aids.

#### 3.2 Repository Organisation Principle

New recurring top-level artefact classes are raised through the AAR/governance-improvement process rather than introduced independently by individual products.

The canonical top-level structure and detailed placement rules remain authoritative through Appendix E.

A product may place a platform-required repository manifest at the product root only where this Governance book explicitly recognises that exact manifest as an exception. The manifest remains metadata; it must not become a second location for authoritative runtime implementation.

#### 3.3 Secrets and Credentials

Credentials, passwords, tokens, private keys and other secret runtime values must not be committed to governed repositories or deliberately retained in validation, audit or production-evidence artefacts.

Repository artefacts should reference the applicable external secret mechanism where required.

Authorised evidence capture must exclude secrets where reasonably possible.

If an accidental capture contains secret material, it must not be committed or retained as normal governed evidence.

Create a safe replacement capture rather than editing the unsafe capture into an apparently original state.

The immutability requirement for retained evidence applies once evidence has been accepted for retention; it does not require preservation of an unsafe accidental capture.

---

## Part II — Work Management and Execution

### 4. Linear as the Workflow Authority

Linear is the authoritative source for the operational state of work.

The workflow is actor-neutral.

Appendix A is authoritative for the gates that permit movement between workflow states.

#### 4.1 Workflow Profiles

A workflow profile defines the Linear workflow that an issue must follow.

Each governed change class has a default workflow profile defined in Section 5.1.

Two workflow profiles are currently defined:

| Workflow profile | Definition | Linear workflow |
|---|---|---|
| `WF-01` | Code workflow profile. Applies to issues whose selected workflow requires controlled progression through Beta before completion. | `Backlog → Ready → In Progress → Ready for Review → Ready for Validation → Beta → Done` |
| `WF-02` | Non-Code workflow profile. Applies to issues whose selected workflow does not require a Beta stage before completion. | `Backlog → Ready → In Progress → Ready for Review → Ready for Validation → Done` |

Two workflow profiles are currently defined because genuine product runtime implementation changes require a Beta stage before completion, while non-runtime and central Governance tooling changes do not solely by virtue of being executable.

The workflow-profile model is intentionally structured so that profile definitions, change-class mappings and precedence can be changed or extended later without redesigning the underlying change-class model.

Where a governed operational work item has no applicable change class, it follows workflow profile `WF-02`.

If an applicable change class is subsequently assigned, the workflow-profile selection rules in Section 5 apply from that point.

Appendix A is authoritative for the gates applicable to each workflow profile and the transitions those gates control.

#### 4.2 Backlog

`Backlog` means the issue is known but is not yet prepared for execution.

It may still require clarification, acceptance criteria, dependency identification, design decisions, change-class identification or prioritisation.

#### 4.3 Ready

`Ready` means the issue is sufficiently prepared to start without redesigning or materially reinterpreting the task.

An issue may enter `Ready` only when **Appendix A G0** is satisfied.

`Ready` means eligible for execution.

It does not itself trigger automatic delegation.

#### 4.4 In Progress

`In Progress` means work is actively being performed.

Manual and delegated work use the same state.

#### 4.5 Ready for Review

`Ready for Review` means:

- the proposed change is complete;
- the reviewable artefact or PR is available;
- substantive execution has paused;
- human review is required.

#### 4.6 Ready for Validation

`Ready for Validation` means:

- applicable human acceptance has been obtained and remains valid;
- accepted substance is ready for applicable validation;
- no further design/content review is expected unless the accepted substance changes;
- only applicable technical, runtime, integrity or evidence validation remains.

#### 4.7 Beta

`Beta` applies where the selected workflow profile requires a Beta stage.

It means:

- review is complete;
- applicable pre-beta validation has passed;
- the accepted runtime candidate has been integrated into the product's persistent `beta` branch;
- the exact resulting Beta candidate identity has been recorded;
- the user has authorised beta deployment or release where required;
- that exact candidate has been deployed or released to the applicable Beta runtime/environment;
- required product-specific preflight or configuration validation has passed;
- deployed/released candidate identity has been sufficiently verified;
- real-world Beta operation is underway.

`Beta` does not mean the candidate has already been promoted to stable `main`.

#### 4.8 Done

`Done` means all completion requirements applicable to the issue have been satisfied against the final implemented state.

The applicable completion gate is defined in Appendix A.

Applicable change-class-specific completion controls are defined in Appendix B.

`Done` must not be treated as an implementation-complete, merge-complete or deployment-complete shortcut.

Stable release is separate from individual issue completion.

#### 4.9 Blocked

`Blocked` is an exception state.

It is used only where work genuinely cannot proceed because of an unresolved dependency, access problem, external constraint or required user decision.

An agent must not declare work blocked merely because the first tool or evidence route failed.

#### 4.10 Changes Requested

`Changes Requested` is a rework state.

Before a PR has been integrated into the applicable target branch, the same issue, branch and PR should normally remain in use.

After a runtime candidate has been integrated into `beta`, a Beta failure remains on the same Linear issue. Corrective implementation normally uses a new corrective branch based on the current failed-Beta `beta` state and a new PR targeting `beta`.

A failed Beta does not require or authorise promotion of that candidate to `main`.

Where correction changes previously accepted content or behaviour, the work returns through human review.

Where correction is purely technical and leaves accepted substance unchanged, it may return directly to validation where Appendix A permits.

#### 4.11 Workflow Integrity

Linear status must reflect the real operational state.

Comments and narrative updates do not substitute for required state transitions.

GitHub may hold detailed implementation/review discussion, but Linear remains workflow authority.

A displayed `Done` state is not sufficient evidence of valid closure where the required closure evidence is absent or contradictory.

If an agent encounters an issue already marked `Done` without evidence that applicable review, validation, acceptance criteria, post-change revalidation and required human acceptance were satisfied, the agent must surface the inconsistency rather than treating the status alone as proof of completion.

#### 4.11.1 Post-Validation State Changes

If a merge, deployment, synchronization, environment update or other state-changing action occurs after validation, any acceptance criterion or validation conclusion affected by that action must be revalidated before closure.

Revalidation is proportionate to the changed state. Unaffected evidence may be reused where Section 15.4 and Appendix A.6 permit.

A state-changing action must not be treated as administrative merely because the substantive design was already accepted.

#### 4.12 Sole Work Tracker

Linear is the sole product and governance work tracker and workflow authority.

GitHub Issues or other repository issue trackers must not be introduced as a parallel backlog, work queue or workflow record.

This applies to:

- product changes;
- central governance changes;
- governed rollout work;
- releases where a tracked release issue is required;
- audit or assurance work requiring an operational work item.

GitHub remains the version-control and review surface for branches, commits, pull requests and release/version history.

GitHub Releases and pull requests are not alternative product work trackers.

#### 4.13 Linear Team Selection

Where current governed work has an applicable `PROJECT_PROFILE.md`, the default Linear team for a newly created issue is the `Default Linear team` declared in that profile.

Use a different Linear team only when the user explicitly specifies one.

The Project Profile supplies the project-specific team value only. It must not restate or locally redefine this team-selection rule.

#### 4.14 Linear Assignee Selection

When an agent creates a Linear issue on behalf of the user, the default assignee is the authenticated Linear user.

Where the Linear integration supports the portable alias `assignee: "me"`, use that alias rather than hard-coding a user UUID.

Use a different assignee only when the user explicitly specifies one or the governed workflow explicitly requires another assignee or an unassigned issue.

This rule governs issue ownership only. It does not alter workflow state, delegation, change-class selection, project or team selection, or execution authority.

---

### 5. Change Classes

Every governed change issue identifies the type or types of change using controlled Linear labels.

Change classes determine applicable change-class-specific controls and each change class defines a default workflow profile.

The selected workflow profile determines the workflow and applicable transition gates.

Change classes do not replace workflow state.

Operational activities such as a release or formal audit that do not themselves change governed product content are not required to invent an artificial change class.

Appendix A defines workflow transition gates and workflow-profile gate applicability.

Appendix B defines change-class-specific controls.

#### 5.1 Standard Change Classes

| Change class | Definition | Default workflow profile |
|---|---|---|
| `Change: Code` | Changes executable or deployable product implementation, including runtime-controlling configuration. | `WF-01` |
| `Change: Architecture` | Changes approved structure, responsibilities, boundaries, components, interactions or architectural behaviour. | `WF-02` |
| `Change: Contract` | Creates or changes an authoritative product-provided interface/contract, including inputs, outputs, schemas, guarantees or compatibility expectations. | `WF-02` |
| `Change: Governance` | Changes rules, controls, authority, repository conventions, workflow or governance process. | `WF-02` |
| `Change: Governance Tooling` | Changes executable automation, release/deployment tooling, validation tooling or workflow implementation whose governed purpose is to operate or assure the central Governance system and which is not deployable product runtime implementation. | `WF-02` |
| `Change: DDR` | Creates, updates or supersedes a Design Decision Record. | `WF-02` |
| `Change: Documentation` | Changes durable explanatory or operational documentation not governed as architecture, contract, governance, DDR or diagram. | `WF-02` |
| `Change: Diagram` | Creates or changes a governed diagram or visual architecture artefact. | `WF-02` |

A single issue or file may require multiple classes.

There is no generic `Mixed` class.

Executable central Governance tooling is not assigned `Change: Code` solely because it is executable. Where the same issue also changes genuine deployable product runtime implementation, both `Change: Governance Tooling` and `Change: Code` apply and Section 5.2 selects `WF-01`.

#### 5.2 Multiple Change Classes

Applicable controls are cumulative.

The issue satisfies controls required by every relevant change class unless a control is explicitly incompatible or inapplicable.

**Where any change class assigned to an issue has a default workflow profile of `WF-01`, then this workflow profile takes precedence over all other default workflow profiles, with the result that the issue must follow workflow profile `WF-01`.**

#### 5.3 Assignment

Change classes should be assigned before `Ready`.

If scope changes during execution, labels must be updated before the affected gate is reached.

Classes must not be omitted to avoid controls.

#### 5.4 Change-Class Simplicity

The set remains deliberately small.

New classes require a genuinely distinct control need and arise through central governance review informed by AAR evidence.

---

### 6. Sub-Issues and Issue Decomposition

A single Linear issue may contain multiple change classes where they form one cohesive logical change.

Work is not split merely because it affects different artefact classes.

#### 6.1 When to Use Sub-Issues

Use a sub-issue where part of the work:

- has distinct acceptance criteria;
- can be executed independently;
- requires materially different sequencing/dependencies;
- requires separate ownership/delegation;
- is independently reviewable;
- will likely complete at a different time;
- would otherwise make the parent difficult to control.

#### 6.2 Parent/Sub-Issue Relationship

The parent describes the overall outcome.

Each sub-issue defines its executable scope and change classes.

Dependencies are explicit where sequencing matters.

The parent completes only when sub-issues required for its outcome have completed.

#### 6.3 Cohesion Principle

Split by independent work outcome, not file type.

Issue decomposition should reduce complexity rather than create administration.

#### 6.4 Multi-Repository Work

A single cohesive Linear work item may affect more than one repository.

The issue must not be split merely because several repositories are affected.

Where the normal Git route applies:

- each changed repository normally has its own issue branch;
- each changed repository normally has its own linked PR;
- all repository changes remain traceable to the same governing Linear issue.

An explicitly approved lightweight exception may apply where permitted by Section 12.7.

All repository-specific obligations required for the outcome must be complete before the applicable issue gate is passed.

#### 6.5 Scoped Change Principle

Work only within the approved issue scope and make the smallest change reasonably required to satisfy it.

Do not opportunistically:

- reformat;
- relayout;
- rename;
- relocate;
- refactor;
- restructure;
- or otherwise modify unrelated material.

Newly discovered work outside scope should be recorded separately unless the user explicitly expands the current issue scope.

---

### 7. Execution Routes

Governed work may be performed manually or delegated.

Invocation determines how work starts, not how it is governed afterward.

All routes converge on the same applicable workflow, gates, evidence and completion rules.

`Ready` means eligible for execution; it is not itself an execution trigger.

Work starts only through an explicit user/manual instruction, an explicitly invoked supported delegation route, or an automatic delegation rule previously enabled by explicit user decision.

#### 7.1 Manual User Execution

The user may perform work directly.

Manual work is not required to imitate agent-specific mechanics that do not contribute to a control objective.

#### 7.2 Local Codex Execution

The user may explicitly instruct Codex Desktop using `This computer`, or another supported local Codex surface, to pick up or resume a Linear issue.

The agent should establish current issue context, confirm repository and change classes, reflect `In Progress`, perform the authorised phase and update workflow state normally.

Local Codex execution is distinct from Codex Cloud execution. Both remain subject to the same applicable Governance.

#### 7.3 Codex Cloud Execution and Linear Delegation

Codex Cloud is a supported phase-based remote executor. It performs work in an isolated configured cloud environment; it is not an implicit workflow orchestrator.

The Linear-to-Codex route is a supported way to invoke Codex Cloud from the governed issue. For initial implementation at G1, the normal current trigger is explicit delegation of the issue to Codex (`Delegate = Codex`) after execution has been authorised. Entering `Ready`, or any other Linear state, does not itself invoke Codex Cloud.

`Execution: Codex Cloud` is a passive execution-route marker. It records that the issue is intended to use Codex Cloud after separate authorisation, but applying the label does not start work or satisfy G1.

The governed issue supplies the scope, repository, workflow profile, Git route and acceptance criteria. Any additional initial handoff must identify the current implementation phase and require Codex to stop at the next human or action-specific gate.

##### 7.3.1 Workflow State, Authority and Invocation

The following are separate:

- **workflow state** records where the issue is in its governed lifecycle;
- **human or action-specific authority** permits a protected decision or action where Governance requires it; and
- **Codex invocation** starts or resumes a Cloud execution phase through delegation or a supported explicit `@Codex` instruction.

A state change, including entry into `Changes Requested`, `Ready for Validation` or `Beta`, must not be treated as an automatic Codex Cloud trigger. When Cloud execution reaches a gate requiring human judgement or separate action-specific authority, it must stop. Completion of one Cloud phase does not authorise the next protected phase.

After the required decision or authority is recorded, any further Cloud work requires a fresh explicit invocation on the same Linear issue. The existing issue, branch, pull request and Cloud task context remain the normal continuity mechanism where Governance permits; unnecessary replacement work must not be created.

Automatic invocation or resumption based on state changes is a separate orchestration capability and remains disabled unless enabled under Section 7.4.

##### 7.3.2 Continuation Handoff Contract

A Codex Cloud continuation instruction must identify the governed issue and current phase, preserve the applicable issue/branch/PR route, state the authorised work, and identify the next gate at which Codex must stop.

The following are normative invocation patterns; equivalent wording may be used where it preserves the same boundaries:

- **Initial implementation — G1:** set `Delegate = Codex` after execution is authorised. Where an additional instruction is supplied: `Perform the authorised implementation phase for this issue and stop at the next required human or action-specific gate.`
- **Review rework — `Changes Requested`:** `@Codex Resume this issue. Address the human review comments on the existing PR, keep the same issue/branch/PR where Governance permits, re-run affected checks, and return the issue to Ready for Review when the revised change is complete. Do not proceed beyond human review.`
- **Post-acceptance validation — `Ready for Validation`:** `@Codex Resume this issue at Ready for Validation. Validate the exact human-accepted state against the issue acceptance criteria and applicable Governance. Do not make substantive changes. Record the validation evidence. If a substantive correction is required, move the issue to Changes Requested and stop; otherwise advance only as far as the next authorised governance gate.`
- **WF-01 Beta or deployment continuation:** resume Codex only after the applicable Beta or deployment authority has been explicitly provided. The instruction must identify the accepted candidate and the authorised action, and must not imply stable-promotion authority.
- **Stable promotion or another protected action:** the continuation prompt does not substitute for the explicit authority Governance requires. Once that authority exists, a fresh instruction may direct Codex to perform only the authorised action and subsequent governed evidence or closure work.

##### 7.3.3 Cloud Environment Responsibility

A Codex Cloud environment provides execution context, including repository access, required runtime/tooling/dependencies, legitimately required environment variables or secrets, and legitimately required network access.

The environment must be compatible with the repository's governed and tested dependency baseline. Central Governance does not prescribe one product-specific runtime version or setup through a generic cloud image.

The environment does not determine or override Linear workflow, change classification, issue scope, Git branch route, review or validation requirements, or human-acceptance requirements. Separate cloud environments must not be used to encode `main` versus `beta` routing.

#### 7.4 Future Automatic Delegation

The model supports future automatic delegation from qualifying states such as:

- `Ready`
- `Changes Requested`

Automatic delegation is disabled initially.

It may only be enabled by explicit user decision.

It must never bypass human approval or other governance gates.

#### 7.5 Rework and Resume

Before integration into the applicable target branch, rework normally resumes the same issue, branch and PR.

After a candidate integrated into `beta` fails Beta, the same Linear issue continues but corrective Git work normally uses a new corrective branch from the failed-Beta `beta` state and a new PR targeting `beta`.

`main` remains unchanged by the failed candidate.

#### 7.6 Execution-Route Neutrality

Equivalent risk receives equivalent governance regardless of actor.

Governance distinguishes the control that must be satisfied from the actor or mechanism used to satisfy it.

Manual execution, local Codex and Codex Cloud therefore converge on the same applicable Linear lifecycle, Git traceability, human review, validation, Beta controls, completion evidence and human-acceptance boundaries.

#### 7.7 Workflow-to-Git Route Binding

Where the selected workflow profile determines the required PR target, that consequence must be made explicit rather than left for an executor or reviewer to infer.

For `WF-01` runtime-changing product work:

- G0 records the selected workflow profile and required reviewed-issue PR target as persistent product `beta`;
- G0 verifies that the required persistent `beta` branch exists before the issue may enter `Ready`;
- G1 execution instructions or handoff state the target/base branch explicitly;
- the established Git route must match the G0 routing decision; and
- G2 independently verifies the actual PR base branch before substantive review begins.

An executor, including local Codex or Codex Cloud, must not silently default a `WF-01` issue PR to `main` or infer the target from repository defaults or the selected execution environment.

If the required persistent `beta` branch is absent, runtime-changing `WF-01` work is not ready to start. The absence must be resolved as governed prerequisite work or through an applicable explicit user override; it must not first be discovered by attempting to retarget a completed PR.

---

## Part III — Durable Product Knowledge

### 8. Knowledge Retention

Durable product knowledge is captured during normal work rather than reconstructed later.

#### 8.1 Completion Check

Before completion determine whether the change:

1. altered product architecture;
2. created, changed or superseded a decision meeting the DDR threshold;
3. created or changed a provider-owned contract;
4. changed another authoritative durable artefact.

Where yes, the corresponding authoritative artefact must be updated.

This is a lightweight completion check, not a broad documentation audit.

#### 8.2 Architecture

Known architectural changes update the authoritative `*_ARCHITECTURE.md` during the same logical work.

Architecture changes must be grounded in:

- the current authoritative architecture;
- materially applicable contracts;
- production evidence where current implementation state is relevant;
- materially applicable DDRs.

Historical context should be consulted only where materially necessary to understand or justify the change.

Architecture must not be invented or altered merely for implementation, documentation or diagramming convenience.

Where production evidence and approved architecture differ, the discrepancy must be surfaced and resolved rather than silently normalised.

#### 8.3 Decisions

Decisions meeting the DDR threshold are captured during normal work.

Audit-based DDR recovery is a backstop.

#### 8.4 Contracts

Provider-owned contract changes update the provider's authoritative contract during the same logical work.

Declared consumers are assessed for compatibility.

#### 8.5 Supporting Artefacts

Supporting durable artefacts are updated only where genuinely affected.

---

### 9. Design Decision Records

DDRs preserve significant durable design decisions and their rationale.

They do not record every implementation choice.

#### 9.1 Threshold

A DDR is normally required where a decision:

- establishes or materially changes architectural direction;
- chooses among meaningful alternatives with lasting consequences;
- establishes a future constraint;
- creates an important cross-product design principle;
- deliberately accepts a material trade-off;
- supersedes an earlier durable decision;
- would otherwise be difficult to reconstruct safely later.

A DDR is not normally required for routine implementation/configuration choices, obvious corrections or purely presentational decisions.

#### 9.2 Relationship to Architecture

Architecture states what is approved now.

A DDR explains why an important decision was made.

Current architecture must be understandable without reconstructing it from historical DDRs.

#### 9.3 Location and Ownership

Each DDR is owned by one product.

`Owner` means the product currently accountable for maintaining the DDR.

The authoritative DDR is stored in the current owning product's:

`02_Decisions/`

Detailed identifier, numbering, allocation and ownership mechanics are defined in the centrally governed `DDR_STANDARD.md`.

#### 9.4 DDR Standard and Template

Detailed mandatory DDR content, statuses, numbering, allocation, ownership, immutability and supersession mechanics are defined in:

`00_Governance/01_Central/01_Standards/DDR_STANDARD.md`

The central authoritative source is:

`/Standards/Product/DDR_STANDARD.md`

When a DDR is created, edited, reviewed or superseded, the applicable agent must apply the active DDR Standard together with this section and other applicable governance controls.

For a new DDR, the centrally managed implementation aid is:

`00_Governance/01_Central/02_Templates/DDR.template.md`

The template is non-authoritative and must not override either `CENTRAL_GOVERNANCE.md` or `DDR_STANDARD.md`.

#### 9.5 Recovered Decisions

A retrospective DDR may be created where audit discovers a missing durable decision and sufficient evidence remains.

This is recovery, not the preferred normal process.

---

### 10. Contract Ownership and Compatibility

Authoritative cross-product contracts are provider-owned.

Consumers do not maintain authoritative duplicates.

#### 10.1 Provider Authority

The provider stores the authoritative contract in its `03_Contracts/` area.

#### 10.2 Consumer Declaration

Consumers identify external contracts they consume in `PROJECT_PROFILE.md`.

#### 10.3 Contract Change Assessment

Before approving a provider-owned contract change:

1. identify all declared consumers;
2. assess the change as compatible or potentially breaking for each;
3. determine whether implementation/expectation is affected;
4. identify required consumer follow-up;
5. resolve material compatibility risk required for approval.

Full consumer testing is not automatic.

Validation depth is proportionate to actual contract delta and credible risk.

A provider-owned contract is not approved in isolation from its declared consumers.

#### 10.4 Cross-Product Dependency Boundary

Cross-product dependencies must use an explicit governed interface or contract.

A consumer must not depend on another product's undocumented internal implementation as though it were a supported interface.

This includes reliance on internal:

- entities;
- files;
- data structures;
- helper conventions;
- implementation details;
- runtime behaviour not represented by the governed interface.

Where an exceptional temporary dependency on an undocumented internal is genuinely necessary, it requires an explicit task-specific user override under Section 2.8.

Such an override:

- applies only to the stated work item;
- must be recorded;
- must not establish the internal as a supported interface;
- must trigger an AAR observation where the dependency is expected to persist or recur.

---

## Part IV — Git, Review and Change Acceptance

### 11. Git Working Model and Linear Alignment

Git records version history.

Linear records operational state.

The table below shows which Git concepts normally become relevant at each Linear state and where those concepts are defined.

| Linear state | Git/GitHub activity | Relevant definition |
|---|---|---|
| `Backlog` | Normally no Git activity | — |
| `Ready` | Normally no Git activity yet | — |
| `In Progress` | Create/use issue branch; make changes; commit; push as needed | 11.2 Branch, 11.3 Commit, 11.4 Push |
| `Ready for Review` | Branch pushed; linked PR open and reviewable | 11.4 Push, 11.5 Pull Request |
| `Changes Requested` — pre-merge | Continue same branch/PR; commit and push corrections | 11.2–11.6 |
| `Changes Requested` — after failed Beta | Same Linear issue; corrective branch/PR normally based on failed-Beta `beta` state and targeted back to `beta`; `main` unchanged | 11.1 `main`, 11.2 `beta` and Branch, 11.5 Pull Request, 11.6 Review Changes |
| `Ready for Validation` | Reviewed PR represents accepted proposed change; for WF-01 runtime work, candidate is ready for controlled integration into `beta` and Beta-entry preparation | 11.2 `beta` and Branch, 11.5 Pull Request, 11.7 Merge and Promotion |
| `Beta` | Accepted candidate is integrated into `beta`; exact Beta candidate is deployed/released and required preflight validation has passed; runtime Beta operation is underway | 11.2 `beta` and Branch, 11.7 Merge and Promotion |
| `Done` | Required issue-level Git actions complete; for WF-01 runtime work, Beta-passed content has been promoted to `main` with required equivalence evidence | 11.1 `main`, 11.7 Merge and Promotion |
| `Blocked` | Preserve current Git state for later resumption | 11.2 Branch, 11.3 Commit, 11.5 Pull Request |

The table is a workflow guide.

Sections 11.1–11.8 define the individual Git concepts.

#### 11.1 `main`

`main` represents accepted integrated product state.

For product runtime-affecting content governed through `WF-01`, `main` contains only content that has successfully completed the applicable Beta gate and been promoted with required tested-content equivalence evidence.

Non-runtime work following `WF-02` may merge to `main` after its applicable review, validation and completion controls without acquiring a Beta result solely because it shares the repository.

Stable SemVer tags identify explicitly released stable states; issue-level promotion to `main` remains separate from creating a stable product release.

#### 11.2 `beta` and Branch

A product using `WF-01` maintains a persistent `beta` integration branch for accepted runtime candidates awaiting or undergoing Beta validation.

`beta` is not a stable branch and does not replace `main` as the accepted integrated product state. It exists to isolate unproven runtime-affecting content from `main` until Beta succeeds.

The default runtime-candidate model is serialized:

`one product → one unresolved runtime Beta candidate`

A second runtime-affecting candidate must not be integrated into `beta` while another candidate remains unresolved unless an explicit governed exception defines how candidate identity, environment state and validation evidence remain unambiguous.

After successful promotion or explicit abandonment/reversion of the candidate, `beta` is deterministically realigned with the accepted `main` baseline before another runtime candidate is integrated.

Issue branches remain separate lines of work.

Normal model:

`one independently reviewable Linear work item → one issue branch`

A corrective branch may be required after a candidate integrated into `beta` fails. Corrective work normally branches from the failed-Beta `beta` state so the correction is assessed against the candidate that actually failed.

#### 11.3 Commit

A commit records an identifiable Git state.

Multiple commits may occur during implementation/rework.

A commit alone does not publish, request review, merge or release work.

#### 11.4 Push

Push sends commits to GitHub.

Implementation may contain multiple:

`change → commit → push`

cycles.

#### 11.5 Pull Request

A pull request proposes incorporation of a branch into the target branch appropriate to the selected workflow.

For normal `WF-01` runtime-changing work, the reviewed issue PR targets persistent `beta` before Beta operation. For work that does not require Beta, the normal target remains `main`. Promotion of Beta-passed content from `beta` to `main` is governed separately by Section 11.7 and does not create a second substantive human-review requirement where the accepted/tested content is unchanged.

Before substantive review begins at G2, the actual PR base must be independently verified against the workflow-to-Git route recorded for the issue. A PR that does not target the branch required by its selected workflow fails G2 and must not be treated as review-ready.

Governed product repositories receive the centrally managed `.github/workflows/central-gov-hook.yml` hook and an exact centrally projected copy of the read-only routing checker at `00_Governance/01_Central/03_Tooling/central_gov_checks.py`. On every pull request the hook checks out the exact candidate and executes that projected checker locally. The authoritative checker source remains `/tooling/central_gov_checks.py` in the Governance repository; product-local work must not edit the projected copy. For the mechanical routing control, a PR that changes any path under canonical `04_Implementation/**`, the approved HACS-native root `custom_components/**` exception, or transitionally supported legacy `04_Source/**` is treated as runtime-affecting and therefore requires both an existing persistent `beta` branch and an actual PR base of `beta`. A non-runtime PR may target `main` without being blocked solely by this routing check. Where product-root `repository.yaml` identifies a Home Assistant App repository, the checker also confirms that recursively discoverable App configuration exists beneath canonical `04_Implementation/haos/source/apps/**` or transitionally supported legacy `04_Source/**`, and that no duplicate root-level App package is introduced.

This path-based check is an enforcement mechanism for the standard repository model, not a substitute for correct semantic classification. Runtime-affecting implementation placed outside the recognised canonical, approved-exception or transition paths remains a repository-model violation and must not be treated as non-runtime merely because the routing check did not classify its path as runtime implementation.

The centrally managed check supplies independent mechanical evidence for G2. Where repository-plan or platform limits do not make the check a technically mandatory merge status, Governance still treats a failing or absent required check as a failed G2 condition; the work must not proceed to substantive review or merge as though the route were valid.

It provides the principal GitHub review surface and may contain:

- diffs;
- comments;
- requested changes;
- approvals;
- automated checks;
- merge history.

Opening a PR does not mean the change has been accepted or merged.

#### 11.6 Review Changes

Before integration into the applicable target branch, requested changes normally use the applicable Appendix A rework and review gates while continuing on the existing issue branch and PR.

After a candidate integrated into `beta` fails Beta, the same Linear issue continues through the applicable Appendix A rework gates using a new corrective branch/PR normally based on and targeted to `beta`.

The Linear issue remains the same unless the correction has become an independently governable piece of work requiring issue decomposition under Section 6.

#### 11.7 Merge and Promotion

The standard issue-PR merge method is:

**Squash merge**

Where the applicable workflow profile requires Beta, the reviewed issue branch is squash-merged into persistent `beta` after human acceptance and applicable pre-Beta validation. The resulting `beta` commit/state becomes the Beta candidate and its exact identity must be recorded.

Where the applicable workflow profile does not require Beta, the issue PR normally squash-merges to `main` after review and applicable validation, immediately before `Done`.

After a `WF-01` candidate successfully completes Beta, the same tested runtime-affecting content is promoted from `beta` to `main` before the issue reaches `Done`.

Promotion does not require a second substantive human review where the accepted and Beta-tested content is unchanged. It does require integrity evidence sufficient to prove that the runtime-affecting content incorporated into `main` is equivalent to the content that passed Beta.

Prefer a fast-forward or other promotion mechanism that preserves exact candidate identity where practical. Where Git ancestry or intervening non-runtime `main` changes require a different commit identity, equivalence may be established using tree, file/content hashes, artifact identity or another immutable comparison appropriate to the affected runtime content.

Any runtime-affecting difference introduced during promotion invalidates the prior Beta result and requires a new Beta candidate before that difference may enter `main`.

After successful promotion, `beta` must be realigned to the accepted `main` state before another runtime candidate is integrated.

#### 11.8 Tag and Release

A Git tag identifies an exact commit using a durable name.

Stable product releases use SemVer tags such as:

`v1.2.0`

Central governance approval uses a governance-specific approval tag such as:

`governance-v2.0.0`

Tags resolve to exact Git commits.

Beta uses exact commit SHAs and does not require a beta tag.

---

### 12. Branch and Pull Request Rules

Default:

`one independently reviewable Linear work item → one dedicated branch → one linked PR`

#### 12.1 Dedicated Work Branches

An issue branch normally remains associated with the issue through implementation, review, requested changes and validation until integration into the applicable target branch.

Long-lived branches containing unrelated issues should be avoided.

The persistent product `beta` branch defined in Section 11.2 is an explicit integration-branch exception to the temporary issue-branch model; it is not an issue branch and must not accumulate multiple unresolved runtime candidates by default.

#### 12.2 Pull Requests

The PR should be linked to the Linear issue.

The relationship among issue, branch, proposed change, review and completion should remain clear.

#### 12.3 Rework Before Merge

Review or validation rework before merge normally continues on the same branch and PR.

#### 12.4 Rework After Beta Integration

If a candidate integrated into `beta` fails Beta, corrective work remains on the same Linear issue but normally uses a new corrective branch from the failed-Beta `beta` state and a new PR targeting `beta`.

The earlier issue PR and failed Beta candidate remain immutable historical evidence. `main` remains unchanged by the failed candidate.

If the failed change is explicitly abandoned rather than corrected, the applicable Beta runtime/environment is restored as required and persistent `beta` is realigned to the accepted `main` baseline before another runtime candidate is integrated.

#### 12.5 Scope

Git structure follows work decomposition rather than repository folder or file type.

#### 12.6 Actor Neutrality

Manual and automated execution use the same Git traceability standard.

#### 12.7 Lightweight Non-Code Route

A clearly presentational/editorial non-code change may bypass the normal dedicated branch/PR route only with explicit user approval for that work item.

Eligibility requires that the change:

- does not alter substantive meaning, intent, behaviour, responsibility, boundary, interface, decision or governance rule;
- does not alter an authoritative position;
- does not create downstream compatibility/dependency impact;
- cannot reasonably alter runtime behaviour or governed interpretation;
- can confidently be assessed as presentational/editorial;
- retains sufficient traceability through Git history.

Examples may include:

- spelling/grammar;
- formatting;
- whitespace;
- alignment;
- non-semantic wording polish;
- diagram positioning where relationships and labels remain unchanged.

If reasonable interpretation could change, use the normal governed route.

The agent may recommend the lightweight route but may not self-authorise it.

Appendix A.4 defines its relationship to normal gates.

#### 12.8 Exceptional Direct Changes

Other direct changes to the protected target branch are not normal governed work.

A specific in-flight user override may authorise one, but it does not create a standing alternative workflow.

#### 12.9 Post-Merge Branch Cleanup

Issue branches are temporary work branches.

After an issue pull request is merged, its head branch is deleted automatically under the normal governed operating model.

The persistent product `beta` branch is not an issue-PR head branch and is explicitly retained as governed integration infrastructure.

Other post-merge issue-branch retention is outside the normal model.

At the time this rule was established, the governed repositories were private repositories using GitHub Free and protected branches/rulesets were not available as an operational mechanism for preserving a merged branch from automatic deletion.

If a future migration, release, rollback or other governed use case genuinely requires a branch to survive merge:

1. the need must be raised as separate governed work before merge;
2. the work must define an implementable technical retention control for the repository and GitHub plan then in force;
3. Linear or PR documentation alone must not be relied upon to preserve the branch;
4. the exception must be approved before the merge that would otherwise trigger deletion.

No branch may be deleted where unresolved, unmerged, review-active, rollback-required or otherwise explicitly retained governed work remains.

Squash-merge commit identity differences are not, by themselves, evidence that substantive branch content is missing from `main`; substantive content must be assessed where cleanup safety is in doubt.

---

### 13. Code Review

Code requires human review at the applicable Appendix A human-acceptance gate before validation may proceed.

GitHub is the detailed code-review surface.

Linear remains workflow authority.

#### 13.1 Entry

A code issue enters `Ready for Review` when:

- implementation is complete;
- branch is pushed;
- linked PR exists;
- change is meaningfully reviewable;
- substantive execution has paused.

#### 13.2 Human Review

The user may examine:

- diff;
- inline comments;
- questions;
- approval;
- requested changes.

Detailed review feedback remains attached to the PR rather than duplicated into Linear.

#### 13.3 Accepted Review

Acceptance satisfies the substantive human-review requirement for the applicable Appendix A gate.

It does not mean validation, Beta or stable release has completed.

#### 13.4 Changes Requested

Required changes proceed through the applicable Appendix A rework gate.

Before merge, the same issue/branch/PR normally continue.

#### 13.5 Review Authority

Human approval is initially mandatory for code.

Automated or agent review may support but not replace it unless central governance is later changed.

---

### 14. Non-Code Review

Non-code review is proportionate to artefact and risk.

It must not inherit code-review ceremony automatically.

#### 14.1 Entry

A non-code issue enters `Ready for Review` when:

- proposed change is meaningfully reviewable;
- artefact is available;
- applicable review surface exists;
- substantive execution has paused.

#### 14.2 Text-Based Artefacts

Architecture, contracts, DDRs, governance and durable documentation normally use a linked PR where the standard Git route applies.

Review establishes whether the artefact is acceptable in substance.

#### 14.3 Diagrams and Visual Artefacts

A textual or XML diff alone is insufficient where visual result matters.

The user must be able to review the final visual artefact.

Manual user edits during review may remain within the same issue/branch/PR.

A new issue is not required merely because the user performs final visual adjustment.

After visual acceptance, exact accepted state is used for final applicable integrity/provenance validation.

Earlier hashes or renders do not remain final evidence if the artefact changes afterward.

Governed architecture diagrams must be reviewed against the active `ARCHITECTURE_DIAGRAM_STANDARD.md` when the conformance trigger in Section 14.3.1 applies.

The canonical conformance trigger is therefore:

- a newly created governed architecture diagram;
- a substantive change in an area governed by the standard; or
- work explicitly brought into scope for a conformance update.

A purely presentational or editorial change does not by itself require previously grandfathered content elsewhere in the diagram to be brought into current-standard conformance.

Human visual review remains required where visual meaning matters.

Compliance with the diagram standard does not replace review of the product-specific architectural meaning represented by the diagram.

##### 14.3.1 Existing Diagram Conformance

Approval or deployment of a new Architecture Diagram Standard does not automatically require existing governed diagrams to be modified.

The active standard applies when a diagram is:

- newly created;
- substantively changed in an area governed by the standard; or
- explicitly brought into scope for a conformance update.

A standard change must not create an automatic repository-wide diagram remediation obligation unless the approved standard change explicitly requires migration because continued use of the previous representation would create a material governance or architectural risk.

#### 14.4 Presentational Versus Substantive

A change is presentational only where it changes how information is displayed, not what it means.

Presentational examples include:

- layout;
- spacing;
- alignment;
- typography;
- annotation positioning;
- spelling/grammar;
- non-semantic polish;
- diagram object placement without semantic change.

A change is substantive where it can alter reasonable interpretation, including responsibilities, boundaries, contracts, governance, decisions, diagram relationships or meaning-bearing labels.

If reasonable interpretation could change, treat the change as substantive.

#### 14.5 Review Authority

Automation may assist but does not replace required human judgement over architecture, contracts, governance, durable decisions or final visual acceptance.

---

## Part V — Validation and Completion

### 15. Validation Model

Validation provides evidence that a governed change or repository state satisfies applicable controls.

It is proportionate to:

- change class;
- risk;
- affected dependencies;
- reusable evidence;
- exact state being assessed.

The default is not to run every available validator.

Appendix A is authoritative for workflow transition gates and workflow-profile gate applicability.

Appendix B is authoritative for change-class-specific controls.

#### 15.1 Universal Integrity and Selection

Every governed change receives one lightweight universal selection/integrity assessment.

Its purpose is to:

- confirm issue/change classification is sufficient;
- identify applicable class-specific and dependency-triggered controls;
- confirm exact state being assessed is identifiable;
- consider durable-knowledge obligations;
- detect obvious repository/change-integrity problems.

It is not a universal substantive validation suite.

#### 15.2 Change-Class-Specific Validation

Substantive validation is driven by applicable change class and identified risk.

A class does not inherit unrelated validation merely because another validator exists.

#### 15.3 Dependency-Triggered Validation

Validation follows the credible affected dependency chain only as far as impact can reasonably propagate.

Traversal requires a specific affected dependency or risk.

“Related to” is not sufficient justification.

Appendix A.5 defines the dependency stop rule.

#### 15.4 Reusable Evidence

Evidence may be reused where relevant immutable state remains unchanged.

Useful identifiers include:

- Git SHA;
- file hash;
- stable release tag.

Unchanged state should not be revalidated solely to reproduce the same evidence.

Appendix A.6 defines the evidence reuse rule.

#### 15.5 Final-Acceptance Validation

Where review can alter an artefact, final validation applies to the exact user-accepted state.

This is especially important for diagrams and manually adjusted governed artefacts.

Validation of a governed architecture diagram may include conformity with the active Architecture Diagram Standard.

Validation of the standard itself and validation of a product diagram are separate controls.

Deployment of a new Architecture Diagram Standard does not by itself require revalidation of unchanged product diagrams.

#### 15.6 Validation Selection

Before substantive validation determine:

1. applicable change classes;
2. universal integrity/selection result;
3. applicable class-specific checks;
4. material dependency impact;
5. reusable valid evidence;
6. need for final-acceptance validation.

Only the resulting set is executed.

#### 15.7 Validation Evidence

Retained evidence should identify:

- what was validated;
- control/risk addressed;
- exact state;
- result;
- reuse validity where relevant.

Routine output is not retained indefinitely merely because it exists.

#### 15.8 Integration and Promotion Preservation

Where applicable validation is performed before integration into `beta` or before a non-Beta squash merge, the resulting commit may rely on that evidence where the governed content is demonstrably identical to the validated and accepted content.

A change in Git commit identity alone does not require substantive revalidation.

Where useful, post-integration integrity confirmation may establish preservation by comparing the relevant accepted content, file hash, artifact identity or equivalent immutable representation.

A successful Beta result may likewise carry through promotion from `beta` to `main` only where the runtime-affecting content incorporated into `main` is demonstrably equivalent to the exact content/state that passed Beta.

Prior validation or Beta evidence does not carry forward where integration or promotion:

- changes the governed/runtime-affecting content;
- changes its effective meaning or behaviour;
- introduces additional unvalidated runtime-affecting content;
- otherwise means the resulting state is no longer equivalent to the accepted or Beta-tested state.

For artefacts requiring final-state validation, including visually accepted diagrams, the merged artefact must remain the exact accepted content even though its enclosing Git commit SHA may differ.

---

### 16. Validation Failure Handling

Validation failure is assessed according to what failed and what correction is required.

Rework follows the applicable Appendix A rework gate.

Whether repeated human review is required depends on whether the accepted substance has changed, as defined by Appendix A and the applicable change-class controls in Appendix B.

#### 16.1 Validation-Tool Failure

A broken validator or tool failure must be distinguished from an artefact/product failure.

Expected negative search results, no-match outcomes and runtime/tool errors are not automatically governed-change failures.

### 17. Non-Code Completion

Non-code completion follows the applicable workflow profile and transition gates defined in Appendix A.

Applicable change-class-specific completion controls are defined in Appendix B.

Sections 17.1–17.5 describe the operating model and evidence expectations for non-code completion; they do not independently authorise workflow transitions.

#### 17.1 Merge Timing

Normal non-code PR merge occurs after human acceptance and applicable validation, immediately before `Done`.

#### 17.2 Final Accepted State

The merged state must preserve the exact final accepted governed content.

Where applicable, final integrity/provenance evidence refers to that accepted content and its resulting repository state.

Section 15.8 governs preservation of pre-merge evidence across squash merge.

#### 17.3 Presentational Changes

Presentational work uses the lightest applicable path.

The lightweight Git route remains subject to explicit user approval under Section 12.7 and Appendix A.4.

#### 17.4 No Stable Release Requirement

Non-code issue completion does not by itself require a product stable-release step.

#### 17.5 Final Closure Evidence

Before a governed issue enters `Done`, closure evidence must record enough information to establish:

- the result of each acceptance criterion against the final implemented state;
- required review status;
- applicable validation result;
- any post-change revalidation performed;
- unresolved findings status;
- required human acceptance;
- completion of required post-merge, deployment, synchronization or environment-update work.

The authoritative issue closure record is maintained in Linear.

Supporting review, validation, Git, deployment or other evidence may remain in its authoritative native location and must be linked or referenced from the Linear closure record where required to establish closure.

Human acceptance and transition authority are governed by Appendix A.

Any separately required action-specific authorisation remains mandatory.

### 18. Code Completion and Beta

Code completion follows the applicable workflow profile and transition gates defined in Appendix A.

Where the selected workflow profile requires Beta, the code issue reaches `Done` only after applicable review, validation and successful Beta operation.

Stable release is separate.

Applicable change-class-specific controls are defined in Appendix B.

#### 18.1 Entry to Beta

Entry to `Beta` occurs only when the applicable Appendix A Beta-entry gate and Appendix B code controls have been satisfied.

For normal `WF-01` runtime work this requires, at minimum, that the accepted candidate has been integrated into persistent `beta`, its exact candidate identity has been recorded, the exact candidate has been deployed/released to the applicable Beta runtime/environment with required authority, required product-specific preflight/configuration validation has passed, and deployed/released state has been sufficiently verified.

The resulting deployed/released candidate state is the state against which Beta operation is assessed.

#### 18.2 Beta Candidate Integrity

Beta result applies only to the exact deployed/released runtime-affecting state represented by the recorded Beta candidate identity.

A later runtime-affecting change does not inherit that result.

Runtime traces or behavioural evidence prove only what they actually observe; where candidate identity is material, deployment/release provenance and runtime evidence must be combined as necessary rather than treating behaviour evidence alone as proof of repository SHA or artifact identity.

#### 18.3 Beta Operation

Beta testing focuses on behaviour and risks introduced by the change.

Duration and depth are proportionate to risk.

A test having executed is not, by itself, proof that an acceptance criterion passed. Beta evidence must establish the criterion actually being relied upon.

#### 18.4 Successful Beta and Promotion

Successful Beta satisfies the Beta-operation requirement but does not by itself complete the issue.

Before transition from `Beta` to `Done`, the same Beta-tested runtime-affecting content must be promoted from `beta` to `main` and required promotion-equivalence evidence must be established under Sections 11.7 and 15.8.

No second substantive human review is required solely for unchanged promotion of already accepted and Beta-tested content.

The implementation issue is complete when the applicable Appendix A completion gate is satisfied. No stable product release is automatically created unless an applicable mechanism-specific Standard expressly defines release creation as part of the authorised stable-promotion action.

#### 18.5 Failed Beta

A failed Beta requires rework through the applicable Appendix A rework gate.

The failed candidate remains part of Git history and may remain on `beta` while corrective work is performed.

Corrective implementation normally uses a new branch from the failed-Beta `beta` state and a new PR targeting `beta` under the same Linear issue unless issue decomposition is genuinely required.

The failed candidate is not promoted to `main`.

Where appropriate, the Beta runtime/environment may be rolled back to the accepted `main` state or another approved rollback target with explicit user authorisation where required.

#### 18.6 Agent-Assisted Beta Deployment

Initial Beta deployment/release is agent-assisted rather than fully automatic unless a separately approved product mechanism provides an authorised automated route.

The agent performs mutation/deployment mechanics only after explicit user authorisation where Governance requires it.

Deployment/release must:

- target the exact recorded Beta candidate identity;
- sufficiently verify deployed/released state;
- preserve rollback capability.

Product-specific mechanics and evidence routes belong to the applicable product/environment authority rather than being hard-coded in Central Governance.

#### 18.7 Beta Branch Protection, Concurrency and Resolution

While an unresolved runtime Beta candidate exists:

- `main` remains the accepted integrated state and must not receive the unresolved candidate;
- a second runtime-affecting candidate must not be integrated into `beta` by default;
- corrective work for a failed candidate may proceed against `beta` through the same Linear issue;
- non-runtime work may proceed only where it does not alter the Beta-tested runtime content, invalidate candidate evidence, interfere with correction/rollback, or make candidate identity ambiguous.

A Beta candidate is resolved only when either:

1. it successfully completes Beta and the tested runtime-affecting content is promoted to `main` with required equivalence evidence; or
2. it is explicitly abandoned/reverted and the Beta runtime/environment and persistent `beta` branch are restored/realigned to an accepted known baseline as required.

After resolution, persistent `beta` must be deterministically realigned with accepted `main` before the next runtime candidate is integrated.

A product-specific concurrency exception requires explicit governed authority and must preserve unambiguous candidate identity, environment state, rollback and validation evidence.

#### 18.8 Home Assistant App Custom-Repository Deployment

A governed Home Assistant App classified as `haos_app` with deployment mechanism `app_repository` and installed or updated through the Home Assistant App store from a Git custom repository must use the product-applicable Home Assistant App Deployment Standard projected at:

`00_Governance/01_Central/01_Standards/HOME_ASSISTANT_APP_DEPLOYMENT_STANDARD.md`

That Standard is the detailed authority for App package placement, root `repository.yaml`, recursive App discovery, branch-qualified repository sources, exact candidate identity, private-repository constraints, temporary-public deployment controls, preflight, deployment evidence, App-private data preservation, failure handling, rollback and reusable product guidance.

The Standard does not replace applicable workflow gates or independently authorise publication, Beta deployment, stable promotion, production deployment or rollback.

#### 18.9 Home Assistant Custom-Integration Deployment

A governed Home Assistant custom integration whose approved deployment mechanism is HACS must use the product-applicable Home Assistant Integration Deployment Standard projected at:

`00_Governance/01_Central/01_Standards/HOME_ASSISTANT_INTEGRATION_DEPLOYMENT_STANDARD.md`

That Standard is the detailed authority for HACS installation/update, immutable lightweight-tag Beta identity, operator handoff, post-deployment validation, stable release and instance-specific rollback. Manual copying into `/config/custom_components` is exception-only and must not be the routine production deployment mechanism.

The Standard does not replace applicable workflow gates or independently authorise Beta deployment, stable promotion, production deployment or rollback.

---

## Part VI — Stable Product Release

### 19. Stable Release

A stable release promotes an integrated product state whose runtime-affecting content has valid beta/stable coverage into an explicitly versioned stable state.

It is product-level activity separate from individual issue completion.

#### 19.1 Stable Authority

Stable promotion requires explicit user authorisation.

Successful beta does not itself authorise stable promotion or generally create a release. Where an applicable mechanism-specific Standard expressly binds automatic stable-release creation to the authorised promotion of Beta-covered runtime content and the selected stable release SHA satisfies Sections 19.3 and 19.4, no second release-creation authorisation is required.

#### 19.2 Semantic Versioning

Stable releases use:

`vMAJOR.MINOR.PATCH`

| Version component | Use when |
|---|---|
| `MAJOR` | Breaking or deliberately incompatible product or consumer-facing contract change |
| `MINOR` | Backward-compatible new capability or materially expanded behaviour |
| `PATCH` | Backward-compatible fix, correction, documentation-only release, or internal change with no new external capability |

Version significance reflects released product behaviour/state, not implementation effort.

#### 19.3 Beta and Stable Coverage

A stable release SHA must have valid runtime coverage for all runtime-affecting content included in that release.

Runtime content already contained in an earlier stable release is considered to retain established runtime coverage while that content remains unchanged.

Runtime-affecting content introduced or altered after that established coverage must obtain applicable Beta coverage before stable promotion.

The release SHA may therefore represent:

- an exact successfully Beta-tested commit where issue-level promotion preserved that commit identity;
- a promoted `main` commit whose runtime-affecting content is demonstrably equivalent to the exact Beta-tested content under Sections 11.7 and 15.8; or
- a later descendant where changes introduced after the applicable Beta/stable coverage are demonstrably non-runtime-affecting and have passed their applicable controls.

Any runtime-affecting change introduced after the applicable Beta result requires a new Beta candidate.

A non-runtime-affecting change does not require Beta redeployment or runtime revalidation merely to reproduce coverage for unchanged runtime content.

#### 19.4 Release Cut-Off

The selected stable SHA is the release cut-off.

Later commits on `main` are not part of that release.

#### 19.5 Stable Tag and GitHub Release

Every stable release receives:

- a SemVer Git tag;
- a corresponding GitHub Release.

Beta SHAs do not generally require GitHub Releases or beta tags. The Home Assistant Integration Deployment Standard requires an immutable lightweight Beta tag as the HACS-facing install identity but does not create a GitHub prerelease.

The GitHub Release should concisely identify:

- version/tag;
- exact SHA;
- material changes;
- deployment considerations;
- known material limitations;
- previous stable rollback target.

#### 19.6 Agent-Assisted Stable Deployment

Initial stable deployment is agent-assisted and requires explicit user authorisation.

The agent deploys the exact tagged version to user-selected environments and verifies deployed state.

The model supports deployment to:

- `ha-starburst`;
- `ha-glenrosa`.

#### 19.7 Rollback

Rollback is agent-assisted and requires explicit user authorisation.

Each environment may be rolled back independently to a selected previous stable tag.

#### 19.8 Release Integrity

A stable release must remain traceable to:

- SemVer tag;
- exact released SHA;
- applicable beta/stable coverage;
- GitHub Release;
- deployment state;
- relevant supporting evidence.

---

### 20. Release Modes

Stable releases use either **Simple Release** or **Managed Release**.

#### Release Mode Comparison

| Attribute | Simple Release | Managed Release |
|---|---|---|
| Default / when used | Default where all Section 20.1 conditions are satisfied | Used where release activity itself requires material operational coordination |
| Separate Linear release issue | Not required | Required; a dedicated Linear work item manages the release |
| Cross-product coordination | None | May include multiple coordinated products/releases |
| Sequencing / migration preparation | No unusual sequencing and no migration/environment preparation | May include dependency-sensitive sequencing or migration/environment preparation |
| Release-specific validation | No material release-specific validation | May include special release validation |
| Rollback preparation | No special rollback preparation requiring managed control | May include special rollback preparation |
| Execution lifecycle tracking | Promotion action rather than a parallel backlog item | May include several distinct execution steps requiring lifecycle tracking |
| Release record / tracking | Git tag and GitHub Release; no separate Linear release issue | Git tag and GitHub Release plus the dedicated Linear release work item |
| Escalation | May convert to Managed if unexpected complexity appears | Already managed |

#### 20.1 Simple Release

Simple Release is the default where:

- the intended stable SHA is known;
- all runtime-affecting content has valid beta/stable coverage;
- subsequent un-beta-tested changes, if any, are demonstrably non-runtime-affecting and have passed their applicable controls;
- promotion is straightforward;
- established agent-assisted deployment is sufficient;
- no unusual sequencing exists;
- no cross-product coordination exists;
- no migration/environment preparation is required;
- no material release-specific validation is required.

#### 20.2 Managed Release

Use a Managed Release where release activity itself requires material operational coordination, including:

- multiple coordinated products/releases;
- dependency-sensitive sequencing;
- migration/environment preparation;
- special release validation;
- special rollback preparation;
- several distinct execution steps requiring lifecycle tracking;
- explicit user decision that managed control is warranted.

#### 20.3 Escalation

A Simple Release may be converted to Managed if unexpected complexity appears.

#### 20.4 Release Completion

Release completion requires:

- explicit promotion;
- correct tag;
- GitHub Release;
- intended deployment completed;
- deployed state verified;
- applicable release checks passed;
- rollback target identified.

---

## Part VII — Assurance and Governance Operations

### 21. Audit Model

Audit is a periodic assurance backstop.

It does not replace normal knowledge capture.

#### 21.1 Scope and Bounded Execution

Each audit defines explicit scope and must not silently expand.

Where the size, risk or execution method of an engagement warrants it, the audit may define bounded execution controls appropriate to the engagement.

Examples include:

- maximum batch size;
- review checkpoints;
- pause-for-user-review or approval points;
- staged population release;
- other bounded execution controls.

These controls belong to the applicable audit work instruction or engagement definition rather than becoming permanent central values.

The applicable audit work instruction or engagement definition defines the actual values.

Central governance deliberately does not prescribe a universal batch size.

Where a batch or checkpoint control is defined, the agent must follow it and must not silently continue beyond the authorised boundary.

#### 21.2 Engagement Folder

Each formal audit/AAR has its own `07_Audit/` subfolder.

#### 21.3 Review Log

The Review Log is the authoritative audit population and progress record.

It must uniquely identify every in-scope item and contain sufficient state to determine, without relying on agent memory:

- whether every item in the defined population was reviewed;
- the review outcome for each item;
- whether a finding or follow-up resulted;
- whether the applicable audit checkpoint was completed.

It contains at minimum:

- source issue/item identifier;
- product/project;
- review status;
- review result;
- finding reference where applicable;
- completion/checkpoint state.

Audit completeness is determined from the Review Log, not agent memory or scattered comments.

When creating a Review Log, the centrally managed implementation aid is:

`00_Governance/01_Central/02_Templates/AUDIT_REVIEW_LOG.template.md`

The template is non-authoritative and must not override this section or any engagement-specific governed instruction.

#### 21.4 Reviewed Versus Archive Ready

A review label means an issue was included and reviewed.

`Reviewed` means the item was examined within the defined audit scope.

It does not mean the issue is archive-ready.

`Reviewed` and `Archive Ready` are distinct concepts.

An issue may be marked `Archive Ready` only where:

- the issue is `Done`;
- there is no unresolved audit finding that requires the issue to remain operationally active;
- required follow-up has either completed or is separately governed and traceable;
- applicable durable-knowledge obligations have been satisfied.

Archival is an administrative action following `Archive Ready`.

Archiving does not:

- change the audit result;
- remove historical Linear traceability;
- alter Git history;
- replace required durable documentation.

#### 21.5 Findings

Audits use the following findings taxonomy:

- `Documentation Update`
- `DDR`
- `Investigation / Integrity`
- `Already Captured / No Finding`

The taxonomy may be refined centrally if operating evidence shows a need.

Substantive findings are resolved through normal governed Linear/Git work.

The audit itself records the finding and its disposition; it does not silently make untracked substantive fixes.

#### 21.6 Audit Completion

An audit engagement completes only when:

- defined population is fully accounted for;
- Review Log is complete;
- findings are resolved or explicitly retained/deferred;
- final engagement state is recorded;
- required labels/checkpoints are applied.

Audit completion does not trigger unrelated broad revalidation.

---

### 22. Central Governance Change, Release and Distribution Lifecycle

Approved central Governance is maintained in the central Governance Git/GitHub repository.

Central Governance artefacts required locally by product agents or by centrally governed repository controls are distributed to the authorised centrally managed projection destinations. These consist of:

- `00_Governance/01_Central/**`;
- exact product-root `AGENTS.md`; and
- exact `.github/workflows/central-gov-hook.yml`.

Content at those managed destinations remains centrally owned and must not be locally altered by product work.

This section is the constitutional authority and routing surface for permanent central Governance changes. Detailed release/provenance mechanics are defined in the central-only Governance Lifecycle Standard; downstream product deployment mechanics are defined in the central-only Governance Distribution Standard.

The normal authority handoff is:

`governed change → human approval and validation → exact accepted merge → release/provenance lifecycle → downstream distribution only where projected content changed → terminal evidence → Done`

Neither Standard may approve Governance content, widen its own authority or override this rulebook.

#### 22.1 Source and Ownership

The authoritative source of every central Governance artefact is its approved location in the central Governance repository.

The central Governance repository owns the centrally managed product projection and the operational artefacts used to define release and distribution populations.

The authoritative source for product-root `AGENTS.md` is the inert `/Templates/product_root_agents.template.md`; it becomes an active loader only when projected to the product root.

The authoritative source for `.github/workflows/central-gov-hook.yml` is `/Templates/central_gov_hook.yml`. The authoritative source for the projected routing checker is `/tooling/central_gov_checks.py`, distributed unchanged to `00_Governance/01_Central/03_Tooling/central_gov_checks.py`. The hook and checker are both centrally owned; their product copies are execution surfaces, not product-owned implementations.

Product repositories must not locally modify centrally projected Governance content. Distribution of approved central content is deployment, not a transfer of authority to the product repository.

#### 22.2 Central Governance Changes Require Linear

A permanent change to the central Governance model must originate from and remain governed by a Linear work item.

A central Governance change follows the workflow profile selected under Sections 4.1 and 5 and the applicable gates and controls in Appendices A and B.

Governance-book-specific approval requirements for changes to `CENTRAL_GOVERNANCE.md` are additionally defined in Appendix C.

The Linear issue carries `Change: Governance` and any additional applicable change classes.

GitHub provides the detailed change and review surface. Linear remains workflow authority.

A permanent Governance change must not be made solely through an untracked GitHub branch, pull request, direct commit or repository edit.

#### 22.3 Relationship to In-Flight User Overrides

A task-specific user override under Section 2.8 does not constitute a permanent central Governance change.

Such an override may govern the stated work item without first changing `CENTRAL_GOVERNANCE.md`.

If the override identifies a rule that should apply to future work, that permanent change must subsequently follow the normal Linear-governed central Governance change route.

#### 22.4 Governance Change Impact Assessment

Before approval, a central Governance change must proportionately assess:

- affected products;
- compatibility with the changed Governance;
- transition action;
- staged-distribution safety;
- temporary mixed-version risk; and
- rollback or restoration considerations.

#### 22.5 Human Approval and Merge Boundary

Before central Governance content is merged, the applicable pre-merge requirements in Appendix C must be satisfied where `CENTRAL_GOVERNANCE.md` is changed, together with all other applicable workflow and change-class controls.

Human approval applies to the substantive proposed Governance content and binds to the exact accepted review state.

After substantive human approval and applicable validation, squash merge of that exact accepted Governance pull request to `main` is the substantive approval boundary.

The merge does not itself complete the governing issue. It authorises and initiates the deterministic post-approval lifecycle defined below.

#### 22.6 Post-Approval Release, Provenance and Distribution Routing

Every approved Governance artefact requiring independent release identity must have immutable, verifiable release/provenance identity.

An explicitly projection-owned artefact may instead derive its approval identity from the exact approved Governance source event where this rulebook and the Governance Lifecycle Standard define that model. The product-root loader source is such a projection-owned artefact and does not require embedded independent release metadata merely to be projected.

Detailed source-event binding, artefact discovery, release metadata verification, approval-tag creation/reuse/verification, projection-owned source-event identity, release-set derivation, Linear provenance recording, idempotency and lifecycle recovery are authoritative in:

`/Standards/Central/GOVERNANCE_LIFECYCLE_STANDARD.md`

That Standard is central-only and is loaded only when central Governance artefact change/release/provenance work, relevant Governance Tooling, or lifecycle failure/recovery makes it applicable.

Once required central release/provenance has been established, downstream product distribution is invoked only where one or more projected artefacts changed. Detailed downstream deployment mechanics are authoritative in:

`/Standards/Central/GOVERNANCE_DISTRIBUTION_STANDARD.md`

Distribution copies exact already-approved Governance into the authorised centrally managed projection destinations. It is deployment, not substantive re-approval, and does not require a second human Governance approval.

The Distribution Standard consumes the release/provenance identity established by the Lifecycle Standard and must not independently recreate or redefine that identity.

Where no projected artefact changed, downstream product distribution is not required solely to generate `no_change` results.

#### 22.7 Centrally Governed Standard Applicability and Lifecycle Delegation

A centrally governed Standard is subordinate to this rulebook and authoritative only within its defined scope.

Changes to a centrally governed Standard follow the applicable workflow profile, Appendix A transition gates and Appendix B change-class controls. The governing issue must identify the Standard and include `Change: Governance`; other applicable change classes may also apply.

Repository structure defines Standard applicability:

- `/Standards/Product/` — product-applicable and projected unchanged to products to which it applies;
- `/Standards/Central/` — central-only and not part of product projection while it remains central-only; applicable work loads it from its authoritative central path where this rulebook routes that subject to it.

A Standard may be released independently of a new `CENTRAL_GOVERNANCE.md` version where the rulebook itself is unchanged.

Detailed independent Standard discovery, release identity, approval-tag provenance, historical transitional provenance and rerun mechanics are delegated to the Governance Lifecycle Standard.

A change in Standard applicability requires an explicit governed authority change; moving a file must not silently change applicability or release identity.

Where this rulebook and a centrally governed Standard conflict, `CENTRAL_GOVERNANCE.md` prevails and the conflict must be surfaced for resolution.

#### 22.8 Governance Content-Change Completion Boundary

The governing central-Governance issue reaches `Done` only when all requirements applicable to the approved source event are complete.

At minimum this means:

1. the exact accepted Governance content has been merged;
2. every required changed independently released Governance artefact has valid verified release/provenance identity and every changed projection-owned artefact has valid exact source-event provenance;
3. where projected artefacts changed, the complete projected release set has been derived and recorded against the governing Linear issue;
4. where projected artefacts changed, downstream distribution has been executed for the governed product population; and
5. where distribution occurs, every targeted product has reached an acceptable terminal rollout state under the Governance Distribution Standard.

Acceptable terminal rollout states are:

- `merged`;
- `no_change`;
- explicitly `deferred`; or
- explicitly `excluded`.

A blocked, failed, contradictory or still-open required release/provenance/deployment step keeps the governing issue incomplete.

A separate rollout or remediation issue is required only where deferred, exceptional or subsequent work has become independently governable. Such a follow-up does not reopen substantive approval of unchanged already-approved Governance.

#### 22.9 Drift

A locally altered, misplaced, mismatched, incomplete or untraceable artefact within `00_Governance/01_Central/**`, product-root `AGENTS.md`, or `.github/workflows/central-gov-hook.yml` that differs from its applicable centrally approved projection is a Governance-integrity issue.

Restore the applicable approved central artefact rather than preserve or normalise local divergence.

Product-local work must not resolve such drift by editing centrally managed content.

---

### 23. Validation Tooling Lifecycle

Validation tooling has a defined purpose, authority and lifecycle.

Existence of a script does not make it mandatory.

#### 23.1 Authority

It must be possible to determine:

- risk/control addressed;
- triggering classes/dependencies;
- whether validator is authoritative;
- evidence produced.

#### 23.2 New Validators

Add new tooling only for a defined control need.

Define:

- risk;
- trigger;
- inputs;
- pass/fail;
- overlap with existing tooling.

#### 23.3 Changed Validators

Changes to validation tooling are assessed separately from the product state they validate.

Tool changes do not automatically trigger broad product revalidation.

Executable validation/release/deployment/workflow tooling whose governed purpose is to operate or assure the central Governance system uses `Change: Governance Tooling` rather than `Change: Code` solely because it is executable. It requires the Appendix B Governance Tooling controls and does not require product runtime Beta unless the same issue also contains genuine deployable product runtime implementation.

#### 23.4 Superseded Validators

Superseded/transitional validators are retired, removed or clearly marked non-authoritative.

Conflicting overlapping validators require authority resolution rather than automatic execution of both.

#### 23.5 Runtime Assumptions

Environment assumptions such as OS, PowerShell version, locale, date parsing, file layout and dependency versions should be explicit where relevant.

Regression checks tied to those assumptions run when those assumptions or tooling change, not automatically after unrelated changes.

#### 23.6 Execution Route for Mandatory Automated Suites

Where an authoritative governed source makes execution of a maintained automated regression or test suite necessary to evidence acceptance of current governed work, the owning product must maintain a reproducible, version-controlled execution route for that suite.

The existence of a test suite, script, workflow or CI configuration does not by itself make execution mandatory. The requirement applies only when the suite is an applicable governed acceptance dependency for the work being assessed.

Governance requires the outcome, not a particular platform. A compliant execution route may be a repository CI workflow, checked-in runner or script, reproducible container or development-environment definition, or another deterministic version-controlled method that permits the required suite to be invoked without reconstructing an undocumented ad-hoc environment.

The route must identify, as applicable:

- runtime and dependency requirements;
- invocation or entry point;
- required fixtures, configuration and environment assumptions;
- expected pass/fail evidence; and
- the exact repository state to which resulting evidence applies.

Such execution-route tooling is normally product-owned validation tooling under this section. It is Governance Tooling only where its governed purpose is to operate on or assure the central Governance system itself.

If a suite is an applicable required acceptance dependency but cannot be executed because its required route is absent or broken, that acceptance dependency has not been evidenced and validation must not be claimed complete. The missing or broken route should normally be handled as separately governed corrective work rather than silently reconstructed within unrelated work, unless the suite is demonstrably not applicable or the user provides a specific in-flight override under Section 2.8.

Maintaining an execution route does not require unnecessary reruns. Valid existing evidence remains reusable against unchanged immutable state where Section 15.4 and Appendix A.6 permit, and Section 25 efficiency principles continue to apply.

---

### 24. Production Evidence Authority

Where current implemented/runtime state is material to governed work, sufficiently reliable and sufficiently current production evidence must be obtained through an approved evidence route.

Detailed production-evidence acquisition, freshness, retained-evidence handling, provenance, integrity and reuse practice is governed by the active product-applicable:

`00_Governance/01_Central/01_Standards/PRODUCTION_EVIDENCE_STANDARD.md`

The central authoritative source is:

`/Standards/Product/PRODUCTION_EVIDENCE_STANDARD.md`

The applicable Project Profile or other explicit environment authority identifies the actual product/environment production and evidence route. Central Governance and the Production Evidence Standard do not hard-code environment-specific connector or endpoint identities.

When production evidence is material, agents apply this section, the active Production Evidence Standard and the applicable Project Profile/environment authority together.

#### 24.1 Evidence Availability

Before declaring required production evidence unavailable or work blocked, use the approved route and other applicable approved evidence capabilities in accordance with the Production Evidence Standard.

A failed first route does not by itself establish that required evidence is unavailable or that work is blocked.

#### 24.2 Freshness Requirement

Where freshness affects a governed decision, sufficiently current evidence is required.

Detailed assessment of live versus retained evidence, contextual freshness, provenance and limitations is governed by the Production Evidence Standard.

#### 24.3 Production Versus Architecture

Production evidence establishes what is implemented or currently observed within its evidenced scope.

Approved architecture establishes what is approved.

A discrepancy is surfaced rather than silently resolved or normalised.

#### 24.4 Production Mutation Boundary

Production evidence access is read-only by default.

Availability of a write-capable tool does not authorise mutation.

For ordinary implementation work, a live-state mutation, service call, reload, restart or configuration change requires:

- the mutation to fall within the governing Linear issue scope;
- applicable governance gates to have passed;
- required explicit user authorisation.

For beta or stable deployment, authority may instead arise directly from the applicable beta/release rule together with the required explicit user deployment authorisation.

This permits a Simple Release without inventing a separate Linear release issue.

The Production Evidence Standard does not create or broaden mutation authority.

Broader technical permissions do not create broader governance authority.

---

### 25. Agent Execution Efficiency

Agents use the minimum context, evidence and dependency scope needed to complete work safely.

#### 25.1 Working Set

Once relevant governance, profile, architecture, contracts, issue context, repository structure, tool routes and evidence are established, they form the current working set.

Unchanged artefacts should not be repeatedly reread unless:

- they may have changed;
- a new phase requires fresh verification;
- context is genuinely insufficient;
- a gate requires latest-state verification.

#### 25.2 Bounded Dependency Traversal

Follow dependencies only as far as necessary for objective, acceptance criteria, change classes, identified risk or applicable gates.

Stop when further traversal cannot reasonably affect the decision or evidence.

#### 25.3 Tool Discovery

Use established tool routes where already known.

Do not repeatedly rediscover the same connector, MCP route, schema, repository or evidence source without reason.

#### 25.4 Historical Context

Use Git, Linear and audit history where materially helpful.

Do not automatically traverse extensive history where current authoritative state is sufficient.

#### 25.5 Expected Negative Outcomes

Distinguish:

- expected no-match;
- genuine execution error;
- validation failure;
- unavailable capability.

No result is not automatically an error.

#### 25.6 Existing Evidence

Reuse valid established evidence, including evidence tied to unchanged immutable state.

Refresh where freshness/state genuinely matters.

#### 25.7 Execution Logging

Use platform-native execution history, Git, Linear and retained validation/audit evidence where sufficient.

Do not create a detailed parallel agent self-log by default.

#### 25.8 Efficiency Does Not Bypass Control

Efficiency never bypasses genuinely applicable:

- human review;
- validation;
- fresh production evidence;
- knowledge retention;
- contract compatibility;
- beta;
- other required gates.

---

### 26. Monitoring and Continuous Improvement

Central Governance maintains a monitoring register for operating-model hypotheses, risks and improvement questions that require evidence from real use before becoming governance.

Monitoring items are not controls and must not be treated as mandatory requirements.

The current monitoring population is recorded in the central Governance repository at:

`/MONITORING_REGISTER.md`

The register records operational monitoring state only. It is not a source of Governance rules and is not part of the centrally managed product projection.

Applicable monitoring evidence-source and disposition rules are defined in Appendix D.

A monitoring item only alters governance if it is formally promoted through the governance-improvement process and approved centrally.

#### 26.1 Governance Improvement Review and Promotion

If an agent identifies that central governance is:

- ambiguous;
- incomplete;
- internally inconsistent;
- unnecessarily burdensome;
- causing repeated execution inefficiency;
- failing to cover a recurring risk;
- encouraging workarounds;
- retaining a stale or duplicative control,

the agent should record the observation and provide a concise recommendation.

The recommendation should identify:

- the rule, omission or operating-model issue;
- the practical effect encountered;
- available evidence or examples;
- the proposed central change;
- known risks or trade-offs.

The recommendation is advisory only.

It does not become governance unless explicitly accepted by the user and incorporated into the applicable authoritative central governance artefact through its defined approval lifecycle.

This may be `CENTRAL_GOVERNANCE.md` or a separately governed central standard where that standard is the authoritative artefact for the subject.

The feedback loop is:

`observe → evidence → recommend → user review → applicable central change if accepted`

#### 26.2 Project AAR Review and Promotion

Open observations in product `00_Governance/AAR_REGISTER.md` files are periodically reviewed for possible central promotion.

Review of an AAR observation does not change the register's authority or make the observation Governance. Promotion occurs only where the observation is accepted through the governance-improvement process and incorporated into the applicable authoritative central Governance artefact through its normal approval lifecycle.

The AAR register remains product-owned operational learning state and must retain the purpose, boundaries, required fields, statuses and append-only rules defined in Section 2.7.

#### 26.3 Diagram Convention Learning and Review

Agents may add or refine `DIAGRAM_CONVENTION_LEARNING.md` incidentally during normal governed work only where that work involves creation, editing or review of a governed architecture diagram.

This restriction governs incidental learning capture. It does not prevent periodic review, disposition or maintenance of existing learning entries under this section.

An entry should be recorded only where a convention is:

- recurring;
- clearly deliberate; or
- explicitly reinforced during the work.

Agents must not create arbitrary new conventions merely for diagramming convenience.

A single accidental or isolated presentation detail should not normally be recorded.

Entries should remain lightweight.

Each entry should record, at minimum:

- the observed convention; and
- sufficient provenance to understand where it was learned, normally the originating Linear issue or equivalent work reference.

Example:

```markdown
## Gateway sizing

- Observed convention: ASTV routing gateways use 50 × 50 diamonds.
- First observed: ASTV-78
```

Additions or refinements made solely to `DIAGRAM_CONVENTION_LEARNING.md` as incidental learning:

- travel with the branch, PR or other normal change surface of the diagram work that produced the observation;
- do not require a separate Linear issue;
- do not add a change class;
- do not introduce an additional review or validation gate;
- do not prevent the originating work item from completing; and
- do not constitute approval of the convention as governance or architecture.

Periodic disposition or maintenance may update or remove learning entries without requiring concurrent creation, editing or review of a governed architecture diagram. Such changes travel with the governance, assurance or other governed work surface through which the periodic review is being performed.

Previously recorded learning may be reused as a provisional local working default where it does not conflict with a higher authority.

Use of a learned convention does not make that convention approved.

Rejection or removal of a learned convention does not retrospectively make earlier diagrams governance failures merely because they used that convention while it remained provisional.

Product `DIAGRAM_CONVENTION_LEARNING.md` files must be reviewed periodically and proportionately.

No fixed review cadence is required.

A review may occur through governance review, assurance activity, accumulation of meaningful learning, or another suitable checkpoint.

The review may update `DIAGRAM_CONVENTION_LEARNING.md` directly to record the resulting disposition of existing entries. This maintenance does not require concurrent diagram editing and is governed by the work surface through which the review is performed.

Each learned convention may be:

- **Promoted** — incorporated into the applicable centrally governed standard through its normal approval lifecycle;
- **Retained locally** — remains useful product-local learning;
- **Rejected** — removed because it is undesirable, accidental or unsupported; or
- **Superseded** — replaced by a newer local convention or central rule.

Promotion must be a deliberate human decision.

Similar conventions appearing independently across multiple products are strong candidates for centralisation, but similarity alone does not automatically promote them.

Periodic review of learning files is intended to improve central standards over time without turning incidental agent learning into a separate governance workflow.

---

## Appendices

### Appendix A — Authoritative Workflow Gate Matrix

This appendix is the **single authoritative source for workflow transition gates and workflow-profile gate applicability**.

The workflow profile applicable to an issue is determined under Sections 4.1 and 5.

The applicable change-class-specific controls for each gate or workflow point are defined in **Appendix B — Authoritative Change-Class Control Matrix**.

`Change: Governance Tooling` uses `WF-02` unless the same issue also carries a `WF-01` class such as genuine product `Change: Code`, in which case Section 5.2 precedence applies.

The actor performing the work does not change the applicable workflow profile or gate.

#### A.1 Preparation and Review Gates

| Gate | Transition / point | `WF-01` | `WF-02` | Universal requirement |
|---|---|---:|---:|---|
| **G0 — Ready Gate** | `Backlog → Ready` | Yes | Yes | Objective, acceptance criteria, repository, applicable change classes and material dependencies sufficiently defined; no unresolved prerequisite decision. For `WF-01`, selected workflow and required reviewed-issue PR target are explicitly recorded and required persistent `beta` existence is verified. |
| **G1 — Start Gate** | `Ready → In Progress` | Yes | Yes | An authorised execution trigger has occurred; execution route selected; normal Git route established where applicable. Where workflow determines a target branch, execution/handoff explicitly states that base and the established route matches the G0 decision. |
| **G2 — Review-Readiness Gate** | `In Progress → Ready for Review` | Yes | Yes | Proposed change complete and reviewable; applicable PR/review surface available; substantive execution paused. Actual PR base is independently verified against the selected workflow/recorded route, and any applicable centrally managed routing check passes. |
| **G3 — Human Acceptance Gate** | Human acceptance while in `Ready for Review` | Yes | Yes | Required human review completed and accepted |
| **G4 — Validation Entry Gate** | `Ready for Review → Ready for Validation` | Yes | Yes | Applicable human acceptance has been obtained and remains valid; accepted substance is ready for applicable validation |

Human acceptance obtained at **G3** remains valid through validation and completion while the accepted substance remains unchanged.

Fresh human acceptance is required where:

- the previously accepted substance changes; or
- a separate action-specific authorisation is expressly required by Governance.

Action-specific authorisation, including beta deployment or stable release/deployment authorisation where applicable, does not constitute a second acceptance of unchanged substantive content.

#### A.2 Validation and Completion Gates

| Gate / point | Transition / point | `WF-01` | `WF-02` | Universal requirement |
|---|---|---:|---:|---|
| **Validation activity** | During `Ready for Validation` | Yes | Yes | Applicable validation is performed against the accepted substance and current relevant state; valid reusable evidence is considered; affected requirements are revalidated following relevant state-changing actions |
| **G5 — Beta Entry Gate** | `Ready for Validation → Beta` | Yes | No | Applicable pre-Beta validation passed; accepted candidate integrated into persistent `beta`; exact Beta candidate identity recorded; exact candidate deployed/released to the applicable Beta runtime/environment with required authority; required product preflight/configuration validation passed; deployed/released state sufficiently verified |
| **G6 — Beta Completion Gate** | `Beta → Done` | Yes | No | Beta acceptance passed against the exact candidate; same tested runtime-affecting content promoted to `main`; promotion equivalence and required completion obligations satisfied; persistent `beta` realigned as required |
| **G7 — Completion Gate** | `Ready for Validation → Done` | No | Yes | Applicable validation passed and completion obligations satisfied against the final implemented state |

#### A.3 Rework and Exception Gates

| Gate | Transition | Universal requirement |
|---|---|---|
| **G8 — Rework Gate** | Review/validation/Beta → `Changes Requested` | Required correction identified and recorded |
| **G9 — Technical Correction Return** | `Changes Requested → Ready for Validation` without repeated review | Permitted only where accepted substance has not changed |
| **G10 — Blocker Exit Gate** | `Blocked → prior active state` | Genuine blocker resolved or required user guidance/override supplied and recorded; resume the preserved work state through the applicable execution/Git route |

#### A.4 Lightweight Non-Code Exception

A clearly presentational/editorial non-code change may use the lightweight Git route only where:

1. it meets the eligibility criteria in Section 12.7; and
2. the user explicitly approves that route for the specific work item.

The exception may simplify Git/PR mechanics.

It does not:

- authorise semantic change;
- remove applicable classification;
- bypass required human judgement;
- convert a substantive change into a presentational one.

#### A.5 Dependency Stop Rule

Any gate that triggers dependency assessment follows this rule:

> Validate only the credible affected dependency chain, and stop when downstream impact is no longer reasonably possible.

Relationship alone does not justify additional validation.

#### A.6 Evidence Reuse Rule

Where evidence already proves an applicable requirement against the exact unchanged immutable state, it may be reused unless freshness itself is material to the control.

Section 15.8 additionally governs preservation of pre-integration validation evidence and Beta evidence across integration or promotion where Git commit identity changes without changing the governed or Beta-tested content.

---

### Appendix B — Authoritative Change-Class Control Matrix

This appendix is the **single authoritative source for change-class-specific controls**.

Where an issue has multiple change classes, applicable controls are cumulative unless explicitly incompatible or inapplicable.

The workflow profile determines which workflow gates apply. The assigned change classes determine the additional controls that must be satisfied at those gates or workflow points.

#### B.1 Preparation and Review Controls

| Gate | Code | Architecture | Contract | Governance | Governance Tooling | DDR | Documentation | Diagram |
|---|---|---|---|---|---|---|---|---|
| **G0** | Product runtime code scope/objective identifiable; for `WF-01`, required PR target recorded and persistent `beta` existence confirmed | Architectural concern/boundary identifiable | Provider/consumer relationship identifiable | Governance scope identifiable | Central Governance tooling purpose/control objective and non-product-runtime boundary identifiable | DDR need identifiable where already known | Durable-document scope identifiable | Diagram/visual scope identifiable |
| **G1** | For `WF-01`, executor/handoff names the required `beta` base explicitly and the established route matches G0 | — | — | — | — | — | — | — |
| **G2** | Linked PR pushed; implementation ready for human review; for `WF-01`, actual PR base independently matches required persistent `beta` and applicable routing check passes | Authoritative architecture change reviewable | Contract delta and declared-consumer impact identifiable | Governance change reviewable; Appendix C preparation applies only where `CENTRAL_GOVERNANCE.md` is being changed; separately governed Standards follow Section 22.7 and the Governance Lifecycle Standard | Linked PR pushed; tooling implementation and affected Governance control/release behaviour reviewable | DDR change reviewable | Durable documentation reviewable | Final or near-final visual artefact available for human visual review |
| **G3** | Human code approval | Human acceptance of architectural substance | Human acceptance plus proportionate consumer compatibility assessment | Human acceptance of governance change | Human technical acceptance of tooling behaviour and fit with the governing control objective | Human acceptance of durable decision record | Human acceptance of the final intended documentation state | Human visual acceptance of final intended state; Architecture Diagram Standard conformity reviewed where applicable |
| **G4** | Applicable tests/technical checks identified | Applicable architecture consistency and authority checks identified | Compatibility validation requirements identified | Governance structure/integrity checks identified | Applicable unit/integration/fixture and release/provenance checks identified | Identifier, ownership and supersession checks identified | Applicable integrity/document checks identified | Applicable integrity/provenance and standard-conformity checks identified |

#### B.2 Validation and Completion Controls

| Gate / point | Code | Architecture | Contract | Governance | Governance Tooling | DDR | Documentation | Diagram |
|---|---|---|---|---|---|---|---|---|
| **Validation activity** | Applicable product tests/technical checks pass; candidate suitable for controlled Beta integration/deployment | Applicable architecture consistency and authority checks pass | Compatibility risk resolved; consumer validation only where justified | Governance structure/integrity checks pass; Appendix C requirements apply only where `CENTRAL_GOVERNANCE.md` is being changed; separately governed Standards satisfy Section 22.7 and the Governance Lifecycle Standard | Applicable unit/integration/fixture checks pass; governing control objective, failure behaviour, release/provenance integrity and rerun behaviour validated where relevant; product runtime Beta is not required solely for Governance Tooling | Identifier, ownership and supersession consistency pass | Only applicable integrity/document checks | Exact final accepted bytes/content used for integrity/provenance checks; Architecture Diagram Standard conformity confirmed where applicable |
| **G5** | Accepted issue PR squash-merged to persistent `beta`; exact Beta candidate identity recorded; required beta deployment/release authorised; exact candidate deployed/released to applicable Beta runtime/environment; required product preflight/configuration validation passes; deployed/released state sufficiently verified | If part of same issue, architecture obligations already satisfied before Beta | If part of same issue, compatibility obligations already satisfied before Beta | If part of same issue, governance obligations already satisfied before Beta | Applies only where the same issue also selects WF-01 through another class; Governance Tooling obligations already satisfied before Beta | If part of same issue, DDR obligations already satisfied before Beta | If part of same issue, durable-document obligations already satisfied where required | If part of same issue, final accepted diagram obligations already satisfied |
| **G6** | Beta succeeds against exact candidate; same tested runtime-affecting content promoted to `main`; promotion equivalence verified; persistent `beta` realigned as required; result remains traceable | — | — | — | — | — | — | — |
| **G7** | — | Accepted architecture state merged | Accepted contract state merged | Accepted governance state merged; Appendix C post-merge requirements apply only to `CENTRAL_GOVERNANCE.md` changes; separately governed Standards complete under Section 22.7 and the Governance Lifecycle Standard; distribution follows Section 22 where within scope | Accepted tooling implementation merged; required technical checks pass; any affected post-merge release/provenance state is validated; no product runtime Beta is required unless another applicable class selected WF-01 | DDR state merged | Accepted durable documentation merged | Exact visually accepted content merged |

#### B.3 Rework and Exception Controls

| Gate | Code | Architecture | Contract | Governance | Governance Tooling | DDR | Documentation | Diagram |
|---|---|---|---|---|---|---|---|---|
| **G8** | Pre-integration correction normally continues same issue branch/PR. Failed Beta correction uses same Linear issue but new corrective branch/PR normally based on and targeted to `beta`; failed candidate does not enter `main` | Substantive correction returns through human review | Contract meaning/compatibility correction returns through human review | Governance-substance correction returns through human review | Tooling behaviour/control-semantics correction returns through human review | Decision-substance correction returns through human review | Substantive correction returns through human review where required | Semantic/visual-meaning correction returns through human visual review |
| **G9** | Technical-only correction may bypass repeated review only where product code behaviour remains unchanged | Metadata/provenance-only correction | Metadata/provenance-only correction | Technical packaging/approval-metadata correction where governance substance is unchanged | Technical-only correction may bypass repeated review only where accepted tooling behaviour and governing control semantics remain unchanged | Metadata/provenance-only correction where decision is unchanged | Non-substantive technical correction | Integrity/provenance regeneration against unchanged accepted content |
| **G10** | — | — | — | — | — | — | — | — |

---

### Appendix C — Governance Change Approval Checklist

This appendix is mandatory whenever `CENTRAL_GOVERNANCE.md` is changed.

For the `Change: Governance` class, Appendix C requirements apply only where `CENTRAL_GOVERNANCE.md` itself is being changed.

A change confined to a separately governed Standard follows Section 22.7 and the Governance Lifecycle Standard and does not, by itself, trigger Appendix C or a new `CENTRAL_GOVERNANCE.md` release.

#### C.1 Governance Semantic Versioning

Governance versions use:

`vMAJOR.MINOR.PATCH`

Classify the change by its effect rather than by the file or section changed.

| Version component | Governance change |
|---|---|
| `PATCH` | Backward-compatible correction or clarification that does not create a new obligation or materially alter authority |
| `MINOR` | Backward-compatible new rule, control or capability, or material expansion of an existing one |
| `MAJOR` | Incompatible rule change, removal or material weakening of an existing protection, changed authority boundary, or change requiring coordinated migration |

Urgency does not determine the version increment.

#### C.2 Linear and GitHub Preconditions

Before a permanent central governance change may be approved:

- [ ] a governing Linear issue exists;
- [ ] the issue carries `Change: Governance`;
- [ ] any additional applicable change classes are present;
- [ ] the issue has satisfied the applicable `Ready` and review gates;
- [ ] the change has been made through the central governance repository;
- [ ] the normal dedicated branch and linked pull-request route has been used unless a specific authorised exception applies;
- [ ] substantive human review has been completed;
- [ ] Linear accurately reflects the current workflow state.

A GitHub pull request without a governing Linear work item is not sufficient authority for a permanent central governance change.

#### C.3 Governance Impact Assessment

Before governance content may be merged:

- [ ] affected products have been identified;
- [ ] compatibility with the changed governance has been assessed;
- [ ] transition implications have been assessed;
- [ ] staged-distribution safety has been considered;
- [ ] temporary mixed-version risk has been considered;
- [ ] rollback/restoration implications have been considered.

#### C.4 Pre-Merge Approval Requirements

Before governance content may be merged:

- [ ] change followed applicable governance workflow;
- [ ] change classes are correct;
- [ ] substantive human governance review is complete;
- [ ] governance SemVer classification is correct;
- [ ] intended version is correct;
- [ ] intended approval tag is defined;
- [ ] intended approval date is defined;
- [ ] applicable Appendix A pre-merge gates have passed.

#### C.5 Post-Merge Approval-Release Requirements

After merge and before the governance version is available for distribution:

- [ ] exact accepted governance content has been merged;
- [ ] resulting commit has been identified;
- [ ] approval tag has been created against that exact commit;
- [ ] tag resolves to the expected commit;
- [ ] governance version/tag/date metadata is correct;
- [ ] distributable `CENTRAL_GOVERNANCE.md` is the exact approved artefact.

Product distribution performs integrity validation only and does not repeat substantive governance approval.

---

### Appendix D — Monitoring Register

Monitoring items are hypotheses or operating-model questions, not mandatory controls.

#### D.1 Operational Register

The current monitoring population and item state are maintained in the central Governance repository at:

`/MONITORING_REGISTER.md`

The register is operational state only. It does not create or amend Governance rules, and routine maintenance of the monitored population does not by itself change `CENTRAL_GOVERNANCE.md`.

The register is not part of the centrally managed product projection. Ordinary product agents do not need to load it merely to apply Governance.

Where register content appears to conflict with this governance book, this governance book prevails and the conflict must be surfaced.

#### D.2 Evidence Sources

Prefer evidence already produced through normal operation:

- Linear history;
- Git/GitHub;
- native agent telemetry;
- validation evidence;
- audit findings;
- release records;
- AAR registers;
- user intervention.

A separate heavyweight telemetry system must not be introduced without evidence of need.

#### D.3 Disposition

Monitoring items may be:

- `Retained`
- `Closed — No Change`
- `Promoted`
- `Superseded`

Only a `Promoted` item that then follows normal central governance review and approval becomes a governance rule.

---

### Appendix E — Authoritative Repository Structure and Artefact Placement

This appendix is the authoritative detailed repository-reference surface for the standard product-repository model governed by Section 3.

It defines canonical paths, folder purposes, placement rules and materialisation mechanics. Section 3 remains authoritative for the constitutional repository model, central-versus-product ownership boundary, convention-over-configuration principle, new recurring top-level artefact-class control, and secrets/credentials boundary.

#### E.1 Canonical Top-Level Structure

Top-level folders use:

`##_Name`

The baseline is:

```text
<Product>/
│
├── .github/
│   └── workflows/
│       └── central-gov-hook.yml
├── AGENTS.md
├── repository.yaml                  # Home Assistant App repositories only
├── 00_Governance/
├── 01_Architecture/
├── 02_Decisions/
├── 03_Contracts/
├── 04_Implementation/
├── 05_Tests/
├── 06_Validation/
├── 07_Audit/
└── 08_Deployment/
```

`AGENTS.md` and `.github/workflows/central-gov-hook.yml` are the exact centrally managed paths outside `00_Governance/01_Central/**`. Their central sources and ownership are defined in Sections 3.1 and 22.1.

Root `repository.yaml` is present only for a Home Assistant App custom repository that requires it. It is the approved platform-manifest exception routed by Section 18.8 and detailed in the Deployment Architecture and Home Assistant App Deployment Standards; it remains product-owned metadata and does not authorise root-level runtime implementation.

The presence of the centrally managed hook does not make other `.github/**` content centrally owned; product repositories may retain other product-owned GitHub configuration subject to normal governance.

A standard structural location need not physically exist in Git until it contains required content.

Empty standard folders must not be materialised solely through placeholder files such as `.gitkeep` or dummy `README.md` files unless a specific operational requirement requires the physical directory to exist.

#### E.2 `00_Governance/`

Contains centrally deployed governance artefacts and product-owned governance/context artefacts.

The standard structure is:

```text
00_Governance/
├── 01_Central/
│   ├── CENTRAL_GOVERNANCE.md
│   ├── 01_Standards/
│   │   ├── ARCHITECTURE_DIAGRAM_STANDARD.md
│   │   ├── DDR_STANDARD.md
│   │   ├── DEPLOYMENT_ARCHITECTURE_STANDARD.md
│   │   ├── GITHUB_PAGES_DEPLOYMENT_STANDARD.md
│   │   ├── HOME_ASSISTANT_APP_DEPLOYMENT_STANDARD.md
│   │   ├── HOME_ASSISTANT_INTEGRATION_DEPLOYMENT_STANDARD.md
│   │   └── PRODUCTION_EVIDENCE_STANDARD.md
│   ├── 02_Templates/
│   │   ├── PROJECT_PROFILE.template.md
│   │   ├── HOME_ASSISTANT_APP_DEPLOYMENT_RUNBOOK.template.md
│   │   ├── DIAGRAM_CONVENTION_LEARNING.md
│   │   ├── DDR.template.md
│   │   └── AUDIT_REVIEW_LOG.template.md
│   └── 03_Tooling/
│       └── central_gov_checks.py
├── PROJECT_PROFILE.md
└── AAR_REGISTER.md
```

The ownership and mutation boundary for `00_Governance/01_Central/**` is defined in Section 3.1 and applies to this structure. The separately managed product-root `AGENTS.md` and `.github/workflows/central-gov-hook.yml` are governed by the same central-ownership principle through their explicit exceptions in Sections 3.1 and 22.1.

#### E.3 `01_Architecture/`

Contains authoritative and supporting architecture artefacts.

The authoritative architecture document uses:

`*_ARCHITECTURE.md`

For example:

```text
01_Architecture/
├── <PRODUCT>_ARCHITECTURE.md
└── Diagrams/
    ├── <governed diagram files>
    └── DIAGRAM_CONVENTION_LEARNING.md
```

Architecture diagrams support the authoritative architecture record but do not replace it.

Product-local recurring diagram presentation conventions may be captured in `DIAGRAM_CONVENTION_LEARNING.md`.

`DIAGRAM_CONVENTION_LEARNING.md` is the standard location for product-local diagram convention learning.

It must not be used to restate central standards, architecture, contracts or governance.

The learning file contains provisional product-local observations and working defaults only. Incidental capture, reuse, maintenance, review and disposition mechanics are defined in Section 26.3.

#### E.4 `02_Decisions/`

Contains Design Decision Records.

Routine issue notes, temporary design discussion and implementation history do not belong here.

#### E.5 `03_Contracts/`

Contains authoritative interfaces/contracts provided by this product.

Consumers reference the provider-owned contract from their `PROJECT_PROFILE.md`; they do not maintain authoritative duplicates.

#### E.6 `04_Implementation/`

Contains authoritative deployable payload and the machine-consumed packaging or distribution machinery that builds, prepares or exposes it.

The canonical structure is target-platform first:

```text
04_Implementation/
├── haos/
│   ├── source/
│   │   ├── config/
│   │   └── apps/
│   └── packaging/
│       ├── hacs/
│       └── apps/
└── rpi_os/
    ├── source/
    │   ├── opt/
    │   ├── lib/
    │   └── usr/
    └── packaging/
        └── deb/
```

Each target separates deployable source from mechanism-specific packaging. Source paths mirror the relevant deployment root where the target permits it. The detailed deployable-unit model, path meaning, platform exceptions and transition controls are defined in `DEPLOYMENT_ARCHITECTURE_STANDARD.md`.

Platform-required root descriptors may exist only where this Governance book or the Deployment Architecture Standard recognises the exact exception. They remain thin metadata or entrypoints and must not become duplicate authoritative payload.

Legacy `04_Source/**` remains a supported transition location only for products awaiting their explicit repository migration issue. Migration must preserve runtime behaviour and deployment semantics and must not be performed opportunistically as part of unrelated work.

#### E.7 `05_Tests/`

Contains tests of product behaviour.

Examples include:

- unit tests;
- integration tests;
- behavioural tests;
- fixtures;
- test helpers;
- implementation test scripts.

Purpose:

> Determine whether the product behaves as intended.

#### E.8 `06_Validation/`

Contains validation tooling and retained validation evidence concerning governed repository/change integrity.

Where useful:

```text
06_Validation/
├── Tools/
└── Evidence/
```

Purpose:

> Determine whether the governed change or repository state satisfies applicable controls.

Validation must not become a duplicate testing framework.

#### E.9 `07_Audit/`

Reserved for formal audit and review engagements.

Each engagement has its own subfolder.

Routine PR history, normal Linear issue notes and temporary development output do not belong here.

#### E.10 `08_Deployment/`

Contains human-facing and operational deployment material.

Examples include:

- installation and rollout runbooks;
- cutover plans;
- rollback procedures;
- migration instructions;
- environment-specific deployment guidance;
- retained deployment or validation evidence.

Executable or machine-consumed build, packaging and release-generation machinery belongs under `04_Implementation/<target>/packaging/<mechanism>/**`, not here. This folder must not contain duplicate authoritative source.
