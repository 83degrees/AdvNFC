# PRODUCTION_EVIDENCE_STANDARD.md

**Standard:** Production Evidence Standard  
**Version:** v1.0.0  
**Status:** Approved  
**Approval tag:** `production-evidence-standard-v1.0.0`  
**Approval date:** 2026-09-04

## 1. Purpose and Authority

This standard defines the detailed rules for acquiring, assessing, retaining, qualifying and reusing production evidence where current implemented/runtime state is material to governed work.

`CENTRAL_GOVERNANCE.md` remains authoritative for:

- the authority of production evidence as evidence of current implemented/runtime state;
- the authority of approved architecture as the approved product-design state;
- the requirement to surface discrepancies between production and approved architecture;
- when sufficiently reliable/current production evidence is required;
- the read-only-by-default production-evidence boundary;
- production-mutation authority, including issue scope, applicable gates and explicit user authorisation;
- beta/stable deployment authority; and
- the relationship among Governance, this Standard and the applicable Project Profile/environment authority.

This Standard does not authorise production mutation.

Availability of a write-capable tool, connector or route does not create authority to alter production.

The applicable `00_Governance/PROJECT_PROFILE.md` identifies the product/environment production and evidence route. This Standard governs how approved evidence routes are used and how evidence obtained through them is handled; it does not hard-code environment-specific endpoint, connector or tool identities.

Where this Standard conflicts with `CENTRAL_GOVERNANCE.md`, `CENTRAL_GOVERNANCE.md` prevails and the conflict must be surfaced for resolution.

## 2. Proportionality

Production-evidence handling must be proportionate to the current work scope, evidence need and credible risk.

Gather and retain only the evidence reasonably required to support the governed decision or validation objective.

This Standard does not create universal requirements for:

- a formal evidence manifest for every work item;
- hashing every capture;
- fixed freshness windows applicable to all evidence;
- permanent retention of routine tool output;
- heavyweight chain-of-custody processes; or
- duplicate evidence where existing evidence remains valid.

A stronger provenance, integrity or retention control is used only where the evidence purpose, risk or applicable governed work justifies it.

## 3. Approved Evidence Routes and Source Selection

Where production evidence is required, use an evidence route approved by the applicable Project Profile/environment authority or another explicit governing authority for the work.

When more than one approved route is available, select the route that provides sufficient evidence for the current purpose with the least unnecessary access, mutation risk, duplication and context overhead.

Prefer direct current evidence where current state is material and direct access is appropriate.

Approved retained evidence may be used where direct access is unavailable, inappropriate or unnecessary and the retained evidence remains sufficiently suitable and current for the decision.

Another approved evidence source may be used where it is sufficient for the current purpose and its authority, provenance and limitations are understood.

A failed first route does not by itself establish that production evidence is unavailable or that the work is blocked.

## 4. Capability Discovery Before Declaring Evidence Unavailable

Before declaring a required evidence capability unavailable or work blocked, check the evidence routes and capabilities reasonably available for the current product/environment and task.

As applicable, this includes:

- the applicable Project Profile;
- known approved environment-specific evidence routes;
- available connected/deferred tools or connectors;
- retained approved evidence; and
- another explicitly approved evidence source.

Do not repeatedly rediscover already established routes without reason.

Stop discovery once sufficient evidence can be obtained or further discovery cannot reasonably change the availability conclusion.

## 5. Live and Retained Evidence

Live evidence represents the state observed through the approved route at the time of observation.

Retained evidence represents the state recorded at its capture time and within its recorded scope.

Neither live nor retained evidence should be treated as broader than what was actually observed or captured.

Where a decision depends on current state, assess whether the evidence is sufficiently current for that decision.

Freshness is contextual. Do not apply an arbitrary universal age limit where the relevant state is unchanged or where a different freshness requirement has not been established by the work, risk or environment authority.

Evidence known or reasonably suspected to be stale for the material decision must not be presented as current evidence without qualification.

## 6. Provenance, Scope and Limitations

Before relying materially on retained production evidence, establish the provenance and limitations reasonably necessary for the current use.

Relevant information may include:

- source;
- environment;
- capture or observation time;
- capture/observation method;
- scope;
- inclusions and exclusions;
- completeness;
- integrity information where proportionate; and
- known limitations.

Not every evidence item requires every field to be recorded independently. Existing trustworthy metadata, tool output, capture records or governed context may satisfy the requirement.

Do not infer unsupported provenance merely to make evidence appear complete.

Where a limitation is material to the conclusion, surface it with the evidence-dependent conclusion.

## 7. Retained-Evidence Immutability

A production snapshot or capture accepted for retention as governed evidence is immutable read-only evidence.

Do not:

- edit the retained capture;
- rename or restructure its contents merely to make it easier to use;
- regenerate it in place;
- retrospectively correct it;
- use it as a working directory; or
- treat a later interpretation, annotation or derived conclusion as though it formed part of the original capture.

Analysis, indexes, manifests or interpretations may be created separately where useful, but they must remain distinguishable from the original retained evidence.

If a retained capture is deficient, record the deficiency or create a new authorised capture where required.

Do not alter the original retained evidence to remove or conceal the deficiency.

An unsafe accidental capture containing credentials, secrets or other material prohibited from retention is not required to be preserved as governed evidence. Apply the applicable Central Governance secrets/credentials boundary and create a safe replacement capture where required.

## 8. Integrity Information

Use integrity identifiers such as hashes, immutable source identifiers or exact capture references where they materially improve confidence that evidence is the same state previously assessed or retained.

Integrity information is especially useful where:

- retained evidence may be reused later;
- exact capture identity matters;
- several similar captures exist;
- a manifest/index is used to identify captured files; or
- a downstream conclusion depends on unchanged evidence bytes/state.

Do not require hashing merely because a hash can be produced.

Integrity information proves identity or preservation within its scope; it does not by itself prove completeness, correctness, freshness or runtime truth beyond that scope.

## 9. Deficient and Superseded Evidence

A deficient capture remains evidence of what was actually captured, subject to its limitation.

Do not retrospectively reconstruct missing provenance, content or context and present it as part of the original capture.

Where the deficiency materially prevents the required conclusion, obtain a new authorised capture or another sufficient approved evidence source.

A later capture may supersede an earlier capture for a current-state decision without deleting or rewriting the earlier retained evidence where that earlier evidence remains legitimately retained.

The newer evidence must not be treated as having existed at the earlier capture time.

## 10. Evidence Reuse and Invalidation

Reuse existing evidence where it remains sufficiently relevant, reliable and current for the same governed purpose.

Evidence tied to unchanged immutable state should not be reacquired or revalidated solely to reproduce the same conclusion.

Reconsider reuse where:

- the relevant production state may have changed;
- freshness materially affects the decision;
- the original scope did not cover the present question;
- provenance or integrity is insufficient for the present risk;
- a known limitation affects the conclusion; or
- the governing work/gate explicitly requires latest-state verification.

Reuse only the conclusions supported by the unchanged evidence. Do not extend an earlier evidence result to new state, scope or meaning without justification.

## 11. Evidence and Interpretation

Production evidence and interpretation of that evidence are distinct.

Raw/live output, snapshots and captures record observed state within their scope.

An analysis, summary, architecture comparison, audit finding or later annotation is an interpretation or derived artefact unless it is itself the original evidence source.

Derived interpretation must not be represented as though it were part of the original capture.

Where interpretation is retained, keep sufficient traceability to the evidence on which it materially relies.

## 12. Non-Mutating Evidence Preference

Where practical and sufficient for the current purpose, prefer local, static, read-only or otherwise non-mutating inspection before controlled runtime mutation.

This is an evidence-handling preference, not a prohibition on authorised implementation or deployment actions.

Where live mutation is required, authority comes only from the applicable Central Governance implementation/beta/release rule together with required user authorisation; this Standard does not supply that authority.

## 13. Tooling Boundary

Connectors, snapshot/capture scripts, hashing/manifest tools, transport/retry behaviour and technical validation implementation are tooling mechanics beneath Governance and this Standard.

Tooling may implement these evidence rules but must not redefine evidence authority, production-mutation authority or product/environment route ownership.

A tooling change does not by itself change this Standard unless the normative evidence-handling rule changes.

## 14. Product/Environment Route Changes

Actual production/evidence route identity belongs in the applicable Project Profile/environment authority.

Changing an endpoint, connector, tool identity or route implementation does not require this Standard to change where the normative evidence-handling requirements remain unchanged.

Where route changes affect product scope, architecture, another governed authority or evidence semantics, apply the corresponding change classification and controls rather than treating the route update as purely operational.
