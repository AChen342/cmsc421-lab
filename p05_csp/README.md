# P5. CSP engine

Lecture notes: 08 - Constraint Satisfaction Problems, 10 - Search Summary and Symbols  
Reuses: —

**Build:** A `CSP` class (variables, domains, constraints) and a solver with pluggable pieces.

## Core
- [ ] Backtracking
- [ ] Forward checking
- [ ] AC-3
- [ ] MRV and LCV ordering
- [ ] Min-conflicts
- [ ] Solve map coloring, Sudoku, N-queens, SEND+MORE=MONEY and the Zebra puzzle

## Measure
Backtracks per Sudoku with each add-on turned on in turn. Time min-conflicts on N-queens for N = 10 up to 1,000,000.

## Check yourself
- Run AC-3 by hand on a 3-variable example and check it against your code.
- Why are tree-structured CSPs solvable in O(nd²)?

## Stretch
Solve the same scheduling problem as a CSP and as an integer program with PuLP ("one problem, four formulations").
