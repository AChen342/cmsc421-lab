# P6. Logic engine and Wumpus agent

Lecture notes: 10b - Logic Part I - Representing Things, 12 - Logic Part II - Reasoning about Things  
Reuses: P1 grid

**Build:** A propositional logic module: sentence parser, CNF conversion and a `KB` with `tell` / `ask`.

## Core
- [ ] Truth-table entailment
- [ ] DPLL
- [ ] Resolution
- [ ] Forward and backward chaining for Horn KBs
- [ ] Wumpus World agent (P1's grid) that asks the KB which squares are safe

## Measure
Time for truth-table vs. DPLL entailment as the KB grows from 10 to 40 symbols.

## Check yourself
- Prove Colonel West is a criminal by hand with forward chaining, then with your code.
- Why is resolution refutation-complete but not complete for generating every consequence?

## Stretch
Lifted FOL inference with unification for the Colonel West KB.
