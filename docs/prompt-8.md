Continue the existing project.

Implement the core Construction Causality Engine.

This is a critical subsystem.

==================================================
OBJECTIVE
=========

Given an observed problem such as:

"Project A is delayed."

identify evidence-backed candidate causes and causal chains.

==================================================
IMPORTANT
=========

Do NOT let the LLM invent causes.

The causality engine must first generate candidates from:

graph relationships

schedule dependencies

temporal ordering

risks

supplier dependencies

material dependencies

RFIs

submittals

contracts

payments

quality events

resource constraints

historical evidence

==================================================
CAUSAL TYPES
============

Distinguish:

OBSERVED_RELATIONSHIP

EXPLICIT_DEPENDENCY

CONTRACTUAL_DEPENDENCY

TEMPORAL_ASSOCIATION

STATISTICAL_ASSOCIATION

INFERRED_CAUSALITY

HUMAN_CONFIRMED_CAUSALITY

==================================================
CAUSAL CHAIN
============

Create:

CausalChain

CausalNode

CausalEdge

CausalEvidence

CausalScore

==================================================
EXAMPLE
=======

Supplier Z delivery delay

↓

Material M42 shortage

↓

Activity A45 blocked

↓

Building B delayed

↓

Milestone M17 delayed

↓

Project A delayed

==================================================
SCORING
=======

Create a configurable scoring system based on:

temporal evidence

graph dependency strength

schedule criticality

evidence quality

data freshness

historical evidence

business impact

relationship confidence

Do NOT pretend this is mathematically proven causality.

Call it:

"Causal Contribution Score"

unless causal certainty is explicitly established.

==================================================
ROOT CAUSE
==========

Implement:

find_root_cause_candidates()

rank_root_causes()

build_causal_chain()

explain_causal_chain()

==================================================
EVIDENCE
========

Every causal edge must have evidence.

Example:

Supplier Z → Material M42

Source:

Purchase Order PO-9981

Confidence:

0.99

Verified:

true

==================================================
TEST
====

The seeded Project A scenario must identify:

Supplier Z

Material M42

Activity A45

Milestone M17

as a causal chain candidate.

==================================================
ACCEPTANCE
==========

Given Project A delay, the engine returns ranked causal chains with evidence.

No LLM is required for the underlying calculation.
