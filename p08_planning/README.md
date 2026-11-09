# P8. Planner

Lecture notes: 13-14 - AI Planning, 15 - PDDL, GraphPlan and SATPlan, 16 - Exam 2 Review - Logic, KR and Planning  
Reuses: P2 A*, P6 DPLL

**Build:** A STRIPS representation (preconditions, add list, delete list) and a parser for a small PDDL subset.

## Core
- [ ] Forward (progression) planning with P2's A* and an ignore-delete-lists heuristic
- [ ] Backward (regression) planning
- [ ] Domains: blocks world, Gripper, Towers of Hanoi

## Measure
Plan length and nodes expanded for forward vs. backward planning on blocks world with 3–8 blocks.

## Check yourself
- Run the Sussman anomaly and explain why solving goals one at a time fails.
- Work the "STRIPS with no delete lists" exam question from note 16.

## Stretch
Planning graph with mutexes and GraphPlan; or SATPlan for a 3-block problem using your P6 DPLL. Check domain files with Fast Downward.
