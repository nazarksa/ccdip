Continue the existing project.

Implement enterprise authentication and authorization.

==================================================
AUTHENTICATION
==============

Implement a secure authentication architecture compatible with OAuth2/OIDC.

For local development you may provide local username/password authentication.

Design for future Azure Entra ID integration.

==================================================
AUTHORIZATION
=============

Implement:

User
Role
Permission

Support:

organization-level access

program-level access

project-level access

document-level permissions

==================================================
TENANCY
=======

Every request must establish:

tenant_id
user_id
roles
permissions

Backend authorization must enforce tenant isolation.

Frontend filtering is NOT security.

==================================================
ROLES
=====

Create development roles:

SUPER_ADMIN
ORG_ADMIN
PROGRAM_MANAGER
PROJECT_MANAGER
PROJECT_ENGINEER
SCHEDULE_MANAGER
CONTRACT_MANAGER
RISK_MANAGER
EXECUTIVE
VIEWER

==================================================
AUDIT
=====

Create audit logging.

Record:

who
what
when
entity
before
after
request_id

==================================================
SECURITY
========

Implement:

password hashing

JWT handling

secure cookies or bearer tokens as appropriate

rate limiting foundation

input validation

security headers

CORS configuration

secret handling

file validation foundation

==================================================
TESTING
=======

Test:

unauthenticated access

authorized access

unauthorized access

cross-project access

cross-tenant access

role permissions

==================================================
ACCEPTANCE
==========

A user cannot access another tenant's project even if they know its UUID.

A user cannot access projects they are not authorized to see.

All sensitive operations are auditable.
