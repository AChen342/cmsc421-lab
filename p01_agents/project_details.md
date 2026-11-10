# P1: Agent simulator — project details

Three vacuum agents (simple reflex, model-based, goal-based) clean a grid world.
Compare them by score over 100 random 10x10 maps.

Pieces:
- `Map` (`Map.py`): the fixed layout. **Done and tested** (`tests/test_map.py`).
- `GridWorld`: the simulation (agent position, dirt left, steps, score). **To design.**
- Agents: the three agent types. **To build after GridWorld.**

Conventions:
- Positions are `(row, col)`; `(0, 0)` is the top-left. Index the grid as `grid[row][col]`.
- Cells: `_` empty, `*` dirt, `#` wall. The agent is never stored in the grid.

---

## Map (done)

What a Map holds:
- `grid`: an n x n list of rows, each a list of cells (`_`, `*`, `#`)
- `start`: the agent's starting `(row, col)`, always an empty cell
- A Map is never changed after it is built.

Rules every Map follows:
- Square, at least 2x2.
- Exactly one start position, on an empty cell.
- Connected: every non-wall cell can be reached from the start (BFS flood fill).
  Full connectivity (not just "all dirt reachable") was chosen so every map size
  means the same thing and so dirt could later reappear anywhere.

### Loading from a file: `Map.from_file(path)`
File format, one character per cell:
- `_` empty, `*` dirt, `#` wall, `O` agent start (stored as empty, position saved in `start`)

Accepted:
- Windows (`\r\n`) or Unix (`\n`) line endings
- Trailing spaces on a row and trailing blank lines at the end of the file (ignored)

Rejected with `ValueError` (checked in this order):
- Any other character, including a leading space (reported with its position)
- Empty file, or only blank lines
- Not square (rows of different lengths, or rows != columns)
- 1x1 map
- Not exactly one `O`
- Disconnected

A missing file raises `FileNotFoundError`.

### Random maps: `Map.generate(size, seed, wall_density, dirt_density, max_tries=100)`
- Uses its own `random.Random(seed)`: same seed -> same walls, dirt and start.
- Densities become exact counts: `round(n*n * density)`.
- Placement: shuffle every cell position, then the first `wall_count` become walls,
  the next `dirt_count` become dirt, and the next one is the start.
- Retries with the same generator until the map is connected, up to `max_tries`,
  then raises `ValueError`.

Input rules (raise `ValueError`):
- `size >= 2`
- `wall_density >= 0`
- `dirt_density > 0`; at least 1 dirt cell is always placed
- walls + dirt + 1 (start) must fit in n*n

Wall density limit (enforced in `main.py`): **0 to 0.25**.
Measured with 400 seeds per setting (single attempt -> connected):

| walls | 5x5 | 10x10 | 20x20 |
|---|---|---|---|
| 0.10 | 99% | 95% | 87% |
| 0.15 | 88% | 80% | 61% |
| 0.20 | 73% | 59% | 26% |
| 0.25 | 60% | 34% | 6% |
| 0.30 | 27% | 13% | 0% |
| 0.35 | 18% | 2% | 0% |
| 0.40 | 10% | 0% | 0% |

Bigger maps tolerate fewer walls, because every open cell must be reachable.
With 100 tries, 10x10 is reliable up to about 0.30.

### Command line (`main.py`)
- `--map PATH` loads a file; cannot be combined with the random options.
- Otherwise random: `--size` (default 10), `--seed` (42), `--walls` (0.2), `--dirt` (0.2).
- Errors are reported with `parser.error`, not tracebacks.

---

## GridWorld (to design)

Decided so far:
- World authority: agents propose actions; the world applies them and owns the true state.
- Actions: up, down, left, right, clean.
- Every action costs 1 step (successful move, bump, clean, or cleaning a clean cell).
- Episode ends when all dirt is gone, or after 4 * n^2 steps.
- Score = 100 x dirt cleaned - 1 x steps.
- Percept given to every agent after each step:
  - is my current cell dirty?
  - did my last move bump into a wall?

Open questions (answer before coding):
1. What it holds: the Map, the agent's current position, a set of remaining dirt
   positions (so the Map is never changed), the step count, the score?
2. How actions are represented (strings, constants, Enum), and what happens with an unknown action.
3. Exact `step(action)` rules:
   - move: inside the grid and not a wall -> move; otherwise stay and set bumped
   - clean: remove the current cell from the dirt set if it is there
4. The percept's form (tuple? dict?).
5. What `step` does if called after the episode has ended.
6. Score computed on the fly, or tracked as the episode runs?
7. How the goal-based agent receives the dirt and wall positions at the start
   without being able to read or change the world's true state.

---

## Agents

### Simple reflex agent
- No memory.
- If the current cell is dirty, clean it; otherwise move in a random direction.
- Cannot know when it is done; the world ends the episode.

### Model-based reflex agent
- Tracks its own position in local coordinates, starting at (0, 0).
  - Successful move: update its position.
  - Bump: stay put and record a wall at the cell it tried to enter.
- Remembers visited cells, walls found and cells cleaned.
- Action selection:
  - If the current cell is dirty, clean it.
  - Prefer an unvisited neighbor that is not a known wall.
  - Otherwise BFS over its own memory to the nearest known-but-unvisited cell (the frontier).
  - Frontier empty -> exploration done; it knows it has finished.

### Goal-based agent
- Knows at the start: its position, every dirt position, every wall.
- Action selection: BFS shortest path to the nearest dirt, follow it, clean, repeat.
- Greedy nearest-dirt is not always the shortest total tour (that is the TSP, project P4).

---

## Experiment
- 100 random 10x10 maps, same seeds for every agent.
- Record per map and agent: dirt cleaned, total dirt, steps, whether the step limit was hit, score.

## Check yourself (write-up)
- PEAS for this world; classify it (observable, deterministic, episodic, static, discrete, single-agent).
  The answer differs per agent: the goal-based agent sees everything, the others do not.
- What changes if dirt reappears?
