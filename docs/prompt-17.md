Continue the existing project.

Now perform comprehensive testing.

==================================================
TEST TYPES
==========

Implement:

unit tests

integration tests

API tests

database tests

Neo4j tests

schedule tests

causality tests

impact tests

risk tests

scenario tests

AI tool tests

LangGraph workflow tests

frontend tests

end-to-end tests

==================================================
CAUSALITY TEST
==============

Given:

Supplier Z

↓

Material M42

↓

Activity A45

↓

Building B

↓

Milestone M17

↓

Project A

the system must identify this as a valid causal candidate when the evidence supports it.

==================================================
AI EVALUATION
=============

Create a golden question dataset.

Questions:

Why is Project A delayed?

What is the primary cause?

What projects are affected?

What happens if Supplier Z fails?

Which supplier is a single point of failure?

Evaluate:

retrieval correctness

evidence correctness

tool correctness

groundedness

causal correctness

citation correctness

==================================================
SECURITY
========

Test:

SQL injection

Cypher injection

prompt injection

document injection

cross-tenant access

unauthorized projects

unauthorized documents

secret leakage

tool abuse

file upload vulnerabilities

==================================================
PERFORMANCE
===========

Test:

large graph traversal

large schedule

document retrieval

AI latency

database latency

API concurrency

==================================================
ACCEPTANCE
==========

Do not claim production readiness until major tests pass.

Fix defects rather than hiding them.
