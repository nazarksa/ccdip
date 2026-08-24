Continue the existing project.

Implement a hybrid GraphRAG architecture.

==================================================
RETRIEVAL
=========

Combine:

vector retrieval

keyword retrieval

metadata filtering

graph traversal

temporal filtering

evidence retrieval

==================================================
QUESTION
========

For:

"Why is Project A delayed?"

retrieve:

project status

activities

critical path

supplier relationships

materials

risks

RFIs

contracts

documents

causal chains

evidence

==================================================
ARCHITECTURE
============

Query

↓

intent

↓

entity extraction

↓

permission validation

↓

graph retrieval

↓

SQL retrieval

↓

vector retrieval

↓

evidence consolidation

↓

context construction

==================================================
IMPORTANT
=========

Do not send huge unfiltered context to the LLM.

Bound retrieval.

Respect tenant/project permissions.

==================================================
OUTPUT
======

Return structured evidence:

claims

sources

graph paths

documents

confidence

==================================================
TEST
====

Create tests for:

Project A delay

Supplier Z

Material M42

Activity A45

Milestone M17

==================================================
ACCEPTANCE
==========

The retrieval system can produce grounded context for the future AI agent.
