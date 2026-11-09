# cmsc421-lab

Projects for reviewing UMD CMSC421 (Intro to AI, Spring 2026; Russell & Norvig AIMA 4th ed.).
The full plan lives in Obsidian: `UMD/Spring 2026/CMSC421/Projects/CMSC421 Project Plan.md`.

## Setup

```powershell
py -3.12 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pytest
```

Run a project as a module from the repo root, e.g. `python -m p02_search.main`.

## Layout

- `core/` – shared code reused across projects (grid world, frontiers, plotting)
- `p01_agents/` – P1: Agent simulator (notes 01, 02)
- `p02_search/` – P2: Search lab (notes 03, 04, 05)
- `p03_games/` – P3: Game AI (notes 06)
- `p04_local_search/` – P4: Local search on TSP (notes 07)
- `p05_csp/` – P5: CSP engine (notes 08, 10)
- `p06_logic/` – P6: Logic engine and Wumpus agent (notes 10b, 12)
- `p07_prolog_kb/` – P7: Knowledge base in Prolog (notes 11)
- `p08_planning/` – P8: Planner (notes 13-14, 15, 16)
- `p09_bayes_nets/` – P9: Bayes net library (notes 20, 21, 22)
- `p10_sampling_filters/` – P10: Sampling, HMMs and robot localization (notes 23, 24)
- `p11_ml/` – P11: Machine learning from scratch (notes 25, 26)
- `p12_rl/` – P12: Reinforcement learning (notes 27-28)
- `p13_capstone/` – P13: Capstone: agents, utilities and games (notes 29, 31)

Each project folder has a README checklist, a `tests/` folder and a `results/` folder for plots.
