# ARCHITECTURE_DIAGRAM_STANDARD.md

**Standard:** Architecture Diagram Standard  
**Version:** v1.0.5  
**Status:** Approved  
**Approval tag:** `diagram-standard-v1.0.5`  
**Approval date:** 2026-09-03

## Contents

1. Purpose and Authority  
   1.1 Purpose  
   1.2 Scope  
   1.3 Authority and Related Artefacts  

2. Core Diagram Principles  
   2.1 Architectural Accuracy  
   2.2 Existing Diagram Preservation  
   2.3 Architectural Relationships  
   2.4 External Boundaries  
   2.5 Layout and Readability  

3. Diagram Grammar  
   3.1 Control-Flow Gateways  
   3.2 Function Calls  
   3.3 Function Returns  
   3.4 Connector Variable Labels  
   3.5 Interface Naming  
   3.6 Decision and Routing Labels  
   3.7 Connector Routing  

4. Product-Local Convention Learning  
   4.1 Local Convention Learning  
   4.2 Authority Limits  
   4.3 Promotion to the Central Standard  

5. Editing, Review and Integrity  
   5.1 Editing the Source Diagram  
   5.2 Diagram Review  
   5.3 Final-State Integrity  

---

# 1. Purpose and Authority

## 1.1 Purpose

This standard defines common construction and representation rules for governed architecture diagrams.

It provides a shared visual grammar across products without defining the architecture of those products.

## 1.2 Scope

This standard applies when a governed architecture diagram is:

- created;
- substantively edited in an area covered by this standard;
- reviewed for a governed architecture change; or
- explicitly brought into scope for conformance.

It does not require existing unchanged diagrams to be retrospectively redrawn merely because the standard changes.

This standard governs representation. It must not be used to invent, alter or infer architecture for diagramming convenience.

## 1.3 Authority and Related Artefacts

Product architecture, boundaries, responsibilities and product-specific semantics remain governed by the applicable approved `*_ARCHITECTURE.md` and governed contracts.

Where this standard conflicts with `CENTRAL_GOVERNANCE.md`, `CENTRAL_GOVERNANCE.md` prevails and the conflict must be surfaced.

Product-local recurring diagram practices may be captured in:

`01_Architecture/Diagrams/DIAGRAM_CONVENTION_LEARNING.md`

That file contains provisional local learning and is subordinate to this standard, approved architecture, governed contracts and `CENTRAL_GOVERNANCE.md`.

---

# 2. Core Diagram Principles

## 2.1 Architectural Accuracy

A governed architecture diagram must prioritise architectural accuracy.

It must:

- show actual architectural relationships;
- preserve meaningful product and subsystem boundaries;
- distinguish calls, returns, data sources and external interactions where represented; and
- avoid visual structure that implies relationships which do not exist.

Architecture determines the space required for representation. The existing canvas must not constrain or reshape the architecture.

## 2.2 Existing Diagram Preservation

When modifying an existing approved diagram, make the smallest diagram change required by the governed work.

Do not move, resize, rename, delete, restyle, reroute or otherwise clean up unrelated existing objects unless explicitly within scope.

Preserve deliberate whitespace and established layout.

Expand the available canvas where necessary rather than compressing architecture purely to fit the existing drawing.

## 2.3 Architectural Relationships

A connector must represent an actual architectural relationship.

Do not connect components merely because they happen to execute sequentially or appear near one another.

Supporting elements should be positioned so their relationship to the component that actually uses them remains clear.

Data sources must not be represented as independent execution branches unless they actually participate in execution flow.

## 2.4 External Boundaries

External products, systems and subsystems must be visibly distinguishable from components owned by the product whose architecture is being documented.

An external subsystem may be represented at boundary level without exposing its internal implementation.

Do not display another product's internal component chain merely to make the local diagram appear complete.

Show only the external interaction necessary to explain the architecture in scope.

The applicable product architecture and governed contract determine the meaning of the boundary.

## 2.5 Layout and Readability

Diagram layout must favour clarity over symmetry.

Avoid unnecessary visual complexity.

Use sufficient whitespace to make architectural relationships readable.

Supporting elements should remain visually associated with the component or relationship they support.

Visual arrangement of architecturally defined phases may remain product-local.

The existence, names, boundaries and architectural meaning of phases must come from the approved product architecture.

Other local spacing, positioning and arrangement conventions may remain product-local where they do not contradict this standard or distort architectural meaning.

---

# 3. Diagram Grammar

## 3.1 Control-Flow Gateways

Use a diamond only for a genuine control-flow gateway.

### Exclusive Split

One incoming flow with mutually exclusive outgoing outcomes.

### Exclusive Merge

Multiple mutually exclusive incoming flows converging into one outgoing flow.

A merge represents convergence only. It must not imply a function, transformer or consolidator where none exists.

### Parallel or Synchronising Gateway

Use only where genuine parallel completion or synchronisation exists.

Represent a parallel gateway with a visible `+`.

Do not introduce a parallel gateway merely because a component invokes several independent functions.

### Presentation

Gateways should remain visually subordinate to the components whose flow they control.

Specific gateway dimensions or placement conventions may remain product-local unless adopted centrally.

## 3.2 Function Calls

One invocation must be represented by **one solid directional call connector**.

The connector represents the invocation as a whole.

Do not create one call connector for each variable passed in that invocation.

## 3.3 Function Returns

Where a meaningful result is returned, represent the return using a **separate dashed directional connector**.

Call and return must not be represented by a double-headed connector.

Do not invent a return connector where the architecture has no return.

Call and return paths must remain visually distinguishable.

## 3.4 Connector Variable Labels

Each represented variable passed or returned across an interface must have its **own bordered connector-native label**.

A connector-native label is a label attached to the connector using the editable diagram format's native connector-labelling capability rather than a detached free-standing shape.

Therefore:

- one invocation remains one call connector;
- one return remains one return connector;
- multiple variables use multiple individual labels on that connector;
- do not create a separate connector for every variable;
- do not combine multiple variables into one bordered payload label; and
- do not substitute detached free-standing shapes for connector labels.

Labels must remain visibly associated with the connector they describe.

Exact local label positioning may remain a product convention where the relationship remains unambiguous.

## 3.5 Interface Naming

Where an interface value is shown, use its exact governed architectural or implementation-facing name.

Do not rename values merely to make diagram terminology appear consistent.

A caller's capture-variable name and a returned field or payload name may legitimately differ.

The diagram must preserve such distinctions across product, provider, adapter or subsystem boundaries.

## 3.6 Decision and Routing Labels

Decision outcomes must be native labels on the outgoing connector to which they apply.

The relationship between outcome and route must remain unambiguous.

Do not use detached outcome labels.

## 3.7 Connector Routing

Prefer simple routing that makes relationships easy to follow.

Avoid unnecessary:

- crossings;
- bends;
- waypoints;
- diagonal routing;
- long return loops; and
- decorative paths.

Routing clarity takes precedence over geometric symmetry.

A connector must not visually imply attachment to an object it merely passes near or crosses.

Exact spacing, routing patterns and local positioning may remain product conventions where they do not impair architectural clarity.

---

# 4. Product-Local Convention Learning

## 4.1 Local Convention Learning

This standard does not prescribe every useful presentation convention that may develop within an individual product.

Product-local recurring practices may be captured in:

`01_Architecture/Diagrams/DIAGRAM_CONVENTION_LEARNING.md`

Where a learned convention is useful and does not conflict with a higher authority, it may be reused as a local working default.

Examples may include:

- component or gateway sizing;
- product-specific box-content presentation;
- visual arrangement of architecturally defined phases;
- local spacing or positioning patterns;
- colour use not defined centrally; and
- other recurring visual practices not yet adopted centrally.

## 4.2 Authority Limits

Learned conventions are provisional.

They must not:

- contradict this standard;
- contradict `CENTRAL_GOVERNANCE.md`;
- redefine approved product architecture;
- create or alter architectural phases, boundaries or responsibilities;
- alter a governed contract or boundary;
- redefine a centrally governed convention; or
- be treated as approved central rules.

Use of a learned convention does not make it approved.

## 4.3 Promotion to the Central Standard

Local learning may subsequently be promoted into this standard through the centrally governed standard lifecycle.

Promotion requires deliberate human approval.

Similarity between conventions across products is evidence that centralisation may be useful, but does not itself create a central rule.

---

# 5. Editing, Review and Integrity

## 5.1 Editing the Source Diagram

The governed editable diagram file is the source used for change and review.

Only one editor may write or save the governed diagram file at a time.

Before agent editing:

1. any concurrent human changes must be saved;
2. no other editor may remain capable of writing or saving the same governed diagram file during the agent edit; and
3. the agent must read the latest saved diagram.

After editing, the changed source must be saved before review.

Rendered PNG, PDF or similar output is supporting representation and does not replace the governed editable source unless governance explicitly defines otherwise.

## 5.2 Diagram Review

Review must consider both:

### Architectural Meaning

Whether the diagram accurately represents the approved architecture.

### Standard Conformance

Whether changed content complies with this standard.

Standard conformance does not establish that the underlying architecture is correct.

Human visual review remains required where visual meaning, routing, layout or boundary representation matters.

## 5.3 Final-State Integrity

Validation must apply to the exact final accepted diagram content.

If the diagram changes after visual review or validation, earlier integrity evidence does not automatically establish the final content.

Where only Git commit identity changes while the accepted diagram content remains demonstrably identical, governance merge-preservation rules may carry earlier evidence forward.

The final governed diagram must remain the exact visually accepted content.
