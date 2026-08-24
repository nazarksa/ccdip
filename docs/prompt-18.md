Continue the existing project.

Prepare the system for production deployment.

==================================================
AZURE
=====

Design deployment for:

Azure Container Apps or AKS

Azure Database for PostgreSQL

Azure Cache for Redis

Azure Blob Storage

Azure OpenAI

Azure Key Vault

Azure Monitor

Application Insights

Neo4j Aura or appropriately managed Neo4j

==================================================
SECURITY
========

Secrets must be stored in Key Vault or equivalent.

No secrets in repository.

Implement:

network security

TLS

managed identities where practical

RBAC

logging

audit

tenant isolation

==================================================
OBSERVABILITY
=============

Implement:

structured logs

metrics

tracing

health checks

AI latency

AI token usage

AI cost

graph query latency

database latency

worker metrics

==================================================
CI/CD
=====

Pipeline must include:

lint

type checking

tests

security scan

container build

migration validation

frontend build

deployment

==================================================
BACKUP
======

Document:

PostgreSQL backup

Neo4j backup

object storage backup

disaster recovery

restore procedures

==================================================
OPERATIONS
==========

Document:

deployment

rollback

migration

monitoring

incident response

scaling

AI cost control

==================================================
FINAL REVIEW
============

Review the entire repository.

Identify:

dead code

security issues

performance issues

architecture inconsistencies

missing tests

missing authorization

hardcoded values

fake functionality

unfinished functionality

Fix what can be fixed.

Document what remains.

==================================================
FINAL ACCEPTANCE
================

A fresh developer should be able to:

clone repository

configure environment

start locally

run migrations

seed data

run tests

start backend

start frontend

log in

open Project A

ask:

"Why is Project A delayed?"

see:

causal chain

evidence

graph

downstream impact

recommendations

then run:

"What happens if Supplier Z fails for 15 days?"

and receive a traceable scenario analysis.

The system must behave as an enterprise construction intelligence platform rather than a chatbot demo.
