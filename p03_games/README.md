# P3. Game AI

Lecture notes: 06 - Game Search  
Reuses: —

**Build:** Connect Four with a `Game` interface (`actions`, `result`, `terminal`, `utility`), plus Nim as a tiny test game you can solve by hand.

## Core
- [ ] Minimax
- [ ] Alpha-beta
- [ ] Depth-limited search with an evaluation function
- [ ] Move ordering

## Measure
Nodes searched by minimax vs. alpha-beta vs. alpha-beta with ordering at depths 2–6.

## Check yourself
- Confirm alpha-beta always returns the same move as minimax.
- Why does good ordering get close to O(b^(m/2))?

## Stretch
Add a chance element (random column blocked each turn) and play it with expectimax; round-robin tournament between eval functions.
