Continue the existing project.

Implement the deterministic construction schedule intelligence engine.

DO NOT use an LLM for schedule calculations.

==================================================
SUPPORT
=======

Activities

Milestones

WBS

Calendars

Durations

Dependencies

FS

SS

FF

SF

Lag

Lead

Baseline dates

Actual dates

Forecast dates

Float

==================================================
ALGORITHMS
==========

Implement:

topological sorting

forward pass

backward pass

earliest start

earliest finish

latest start

latest finish

total float

free float

critical path

schedule variance

milestone variance

==================================================
IMPORT
======

Create an adapter architecture for:

CSV

Excel

future Primavera P6/XER

Do not attempt to implement every P6 feature yet.

==================================================
OUTPUT
======

Given a project schedule, calculate:

critical activities

critical path

delayed activities

float consumption

milestone slippage

forecast finish

baseline variance

==================================================
TEST
====

Create deterministic schedule fixtures.

Test known critical paths.

Test lag.

Test dependency types.

Test delayed predecessors.

Test zero-float propagation.

==================================================
ACCEPTANCE
==========

The engine can determine whether Activity A45 is critical and whether a predecessor delay can affect Milestone M17.

No AI should be required to obtain these calculations.
