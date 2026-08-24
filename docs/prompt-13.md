Continue the project.

Implement a scenario simulation engine.

==================================================
EXAMPLES
========

"What happens if Supplier Z fails for 15 days?"

"What happens if Activity A45 is delayed 20 days?"

"What happens if Contract C234 is terminated?"

"What happens if Material M42 becomes unavailable?"

==================================================
SCENARIO MODEL
==============

Create:

Scenario

ScenarioEvent

ScenarioNode

ScenarioEdge

ScenarioImpact

ScenarioResult

==================================================
IMPORTANT
=========

Never modify production project data.

Scenarios operate on a copy/simulation context.

==================================================
PROCESS
=======

Scenario

↓

Graph propagation

↓

Schedule analysis

↓

Risk analysis

↓

Impact analysis

↓

Recommendations

==================================================
OUTPUT
======

Show:

baseline

scenario

difference

affected activities

affected buildings

affected milestones

affected projects

risk changes

==================================================
ACCEPTANCE
==========

A 15-day Supplier Z failure can be simulated without modifying production data.

The system returns a traceable impact chain.
