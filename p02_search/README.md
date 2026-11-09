# P2. Search lab

Lecture notes: 03 - Uninformed Search, 04 - Heuristic Search, 05 - Practical Issues - Time and Memory  
Reuses: P1 grid

**Build:** One `search(problem, frontier)` function where the frontier type alone decides the algorithm ("one queue to rule them all").

## Core
- [ ] DFS, BFS, IDS, UCS
- [ ] Greedy best-first and A*
- [ ] IDA* and weighted A*
- [ ] Grid pathfinding (P1's grid) and the 8-puzzle with misplaced-tiles and Manhattan heuristics

## Measure
Nodes expanded, peak frontier size, runtime and path cost per algorithm across 50 random 8-puzzles. Plot nodes expanded vs. solution depth.

## Check yourself
- Show on your data that Manhattan dominates misplaced tiles.
- Build a small graph where an inconsistent heuristic makes A* graph search return a suboptimal path.

## Stretch
ARA* (anytime weighted A*) printing a better solution each time the weight drops; animate the frontier in pygame.
