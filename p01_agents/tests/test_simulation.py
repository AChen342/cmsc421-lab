from pathlib import Path
import pytest
from p01_agents.Map import Map
from p01_agents.GridWorld import GridWorld
from p01_agents.Agent import ReflexAgent, ModelBasedAgent, GoalBasedAgent
from p01_agents.simulation import run_episode

MAPS = Path(__file__).parent / "maps"

def test_simulation_4x4():
    world = GridWorld(Map.from_file(MAPS / "4x4_map.txt"))
    agent = ReflexAgent(seed=1)

    result = run_episode(world, agent)

    assert result.steps == world.steps
    assert result.cleaned == world.cleaned
    assert result.score == world.score
    assert world.done
    assert result.cleaned == 2
    assert result.total_dirt == 2
    assert not result.hit_limit

# seed 0 never reaches either dirt cell on the 4x4 map, so the episode
# only ends when it runs out of steps (4 * 4 * 4 = 64)
def test_simulation_hits_step_limit():
    world = GridWorld(Map.from_file(MAPS / "4x4_map.txt"))
    agent = ReflexAgent(seed=0)

    result = run_episode(world, agent)

    assert result.steps == 64
    assert result.cleaned == 0
    assert result.total_dirt == 2
    assert result.hit_limit
    assert world.done

# the same map and the same seed must give the same result every time.
# A GridWorld cannot be reused after its episode ends, so each run
# gets a fresh GridWorld built from the same Map.
def test_simulation_same_seed_same_result():
    world_map = Map.from_file(MAPS / "4x4_map.txt")

    result1 = run_episode(GridWorld(world_map), ReflexAgent(seed=1))
    result2 = run_episode(GridWorld(world_map), ReflexAgent(seed=1))

    assert result1 == result2
    assert result1.cleaned == 2   # a real result, not two Nones that happen to be equal


# ======================================================================
# on_step callback
# ======================================================================

# on_step is called once before the first action and once after every step,
# so recording the agent's position gives its full path
def test_on_step_records_path():
    world = GridWorld(Map.from_file(MAPS / "4x4_map.txt"))
    path = []

    result = run_episode(world, ReflexAgent(seed=1),
                         on_step=lambda w: path.append(w.agent_position))

    assert len(path) == result.steps + 1
    assert path[0] == (0, 1)               # the 4x4 map's start
    assert path[-1] == world.agent_position

# consecutive positions are either the same cell (bump or clean)
# or one cell apart (a move): the agent never jumps or walks through a wall
def test_on_step_path_is_valid():
    world_map = Map.from_file(MAPS / "4x4_map.txt")
    path = []

    run_episode(GridWorld(world_map), ReflexAgent(seed=0),
                on_step=lambda w: path.append(w.agent_position))

    assert len(path) > 1   # otherwise the loop below checks nothing
    for (r1, c1), (r2, c2) in zip(path, path[1:]):
        assert abs(r1 - r2) + abs(c1 - c2) <= 1
        assert world_map.grid[r2][c2] != "#"

# without on_step, nothing changes: same result as before
def test_on_step_does_not_change_result():
    world_map = Map.from_file(MAPS / "4x4_map.txt")

    plain = run_episode(GridWorld(world_map), ReflexAgent(seed=1))
    watched = run_episode(GridWorld(world_map), ReflexAgent(seed=1),
                          on_step=lambda w: None)

    assert plain == watched
