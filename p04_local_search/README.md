# P4. Local search on TSP

Lecture notes: 07 - Local Search  
Reuses: P2 A*

**Build:** Rebuild course Project 1 (TSP) without looking at your old code.

## Core
- [ ] Random-restart hill climbing with 2-opt moves
- [ ] Simulated annealing
- [ ] Genetic algorithm (order crossover + swap mutation)
- [ ] Exact A* with an MST heuristic for small n

## Measure
Tour cost vs. runtime for n = 10, 50, 200 random cities. For n ≤ 10, each method's gap from the A* optimum.

## Check yourself
- What does temperature do early vs. late in SA?
- When does hill climbing get stuck, and why does a restart help?

## Stretch
WalkSAT on random 3-SAT; plot % solved vs. clause/variable ratio and find the hard region near 4.26.
