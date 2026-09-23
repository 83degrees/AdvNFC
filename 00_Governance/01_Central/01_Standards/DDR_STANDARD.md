# DDR_STANDARD.md

**Standard:** Design Decision Record Standard  
**Version:** v1.0.1  
**Status:** Approved  
**Approval tag:** `ddr-standard-v1.0.1`  
**Approval date:** 2026-09-03

## 1. Purpose and Authority

This standard defines the detailed construction, numbering, status and supersession rules for Design Decision Records (DDRs).

`CENTRAL_GOVERNANCE.md` remains authoritative for when a DDR is required, the governance significance of a DDR, its relationship to architecture and other authorities, and the lifecycle controls that apply to governed work.

Where this standard conflicts with `CENTRAL_GOVERNANCE.md`, `CENTRAL_GOVERNANCE.md` prevails and the conflict must be surfaced for resolution.

`Templates/DDR.template.md` is a centrally managed implementation aid. It is not an independent governance authority and must not override this standard or `CENTRAL_GOVERNANCE.md`.

## 2. DDR Purpose

A DDR records a significant durable design decision and why it was made.

It is not a task log or general implementation journal.

## 3. Federated Numbering

DDRs use:

`DDR-<origin product code>-<local sequence>`

For example:

`DDR-03-001`

Each product's DDR origin code is defined in its `00_Governance/PROJECT_PROFILE.md`.

The origin product code identifies the product in which the DDR was first created and is immutable once used in a DDR identifier.

`Owner` is the product currently accountable for the DDR. The origin product code records provenance and does not necessarily identify the current Owner.

A DDR identifier is immutable once created. DDR ownership may subsequently transfer to another product without changing the identifier. Detailed ownership-transfer mechanics are intentionally deferred.

## 4. Allocation

When a new DDR is required:

1. read the product's DDR origin code from `00_Governance/PROJECT_PROFILE.md`;
2. inspect the DDR identifiers already allocated by that product;
3. determine the next local sequence;
4. create the DDR in the owning product's `02_Decisions/` folder.

The next local sequence is derived from the product's existing DDR identifiers.

A mutable "next DDR number" counter must not be maintained in the Project Profile or elsewhere solely for allocation.

There is no central DDR allocation authority, registry or reservation process.

## 5. Required DDR Content

Each DDR contains at minimum:

- identifier and title;
- status;
- decision;
- context;
- material alternatives considered where relevant;
- rationale;
- consequences/trade-offs;
- source Linear issue;
- superseded DDR where applicable.

## 6. Status

Allowed DDR statuses are:

- `Proposed` — decision is undergoing governed development/review;
- `Accepted` — governing work has completed and the decision record is authoritative historical evidence;
- `Superseded` — a later accepted DDR replaces the durable decision.

When a replacement DDR becomes accepted, the superseded DDR must be updated accordingly.

## 7. Supersession

When superseded:

- the old DDR remains preserved;
- the old DDR is marked `Superseded`;
- the new DDR identifies what it supersedes.

Historical decisions are not deleted merely because they are no longer current.

## 8. Approved DDR Immutability

Once accepted, a DDR must not be substantively rewritten.

A changed durable decision requires a new DDR that supersedes the earlier record.

Only traceable non-substantive corrections that leave the decision, rationale, alternatives and consequences unchanged may be made to an accepted DDR.

## 9. Architecture Relationship

Architecture must describe the current approved design without requiring agents to reconstruct it from DDR history.

DDRs preserve significant rationale, not the complete current architecture.
