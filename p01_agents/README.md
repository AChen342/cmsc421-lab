# P1. Agent simulator

Lecture notes: 01 - Introduction to AI, 02 - Intelligent Agents  
Reuses: —

**Build:** A `GridWorld` environment (walls, dirt, an agent) and an `Agent` interface with `percept → action`. Put `GridWorld` in `core/` since later projects reuse it.

## Core
- [ ] Simple reflex vacuum agent
- [ ] Model-based reflex agent that remembers visited cells
- [ ] Goal-based agent that plans to the nearest dirt

## Measure
Score (dirt cleaned minus moves) for each agent over 100 random 10×10 maps.

## Check yourself
- Write PEAS for your world and classify it on each environment property (observable, deterministic, episodic, static, discrete, single-agent).
- What changes if dirt reappears?

## Stretch
Make the world partially observable (agent sees only adjacent cells).
