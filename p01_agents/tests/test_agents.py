from pathlib import Path
import pytest
from p01_agents.Map import Map
from p01_agents.GridWorld import GridWorld, Action, DIRECTION
from p01_agents.Agent import ReflexAgent, ModelBasedAgent, GoalBasedAgent, Agent
from p01_agents.simulation import run_episode

MAPS = Path(__file__).parent / "maps"

def test_reflex_agent_dirty_cell():
    agent = ReflexAgent(seed=0)

    # agent is on dirty cell
    assert agent.choose((True, False)) == Action.CLEAN

def test_reflex_agent_clean_cell():
    agent = ReflexAgent(seed=0)

    # agent moves around randomly, should never trigger a clean action
    for i in range(100):
        assert agent.choose((False, False)) in DIRECTION

def test_reflex_agent_bumped():
    agent = ReflexAgent(seed=0)

    # agent moves around randomly, should never trigger a clean action
    for i in range(100):
        assert agent.choose((False, True)) in DIRECTION

def test_two_reflex_agents_same_seed():
    agent1 = ReflexAgent(seed=0)
    agent2 = ReflexAgent(seed=0)

    agent1_moves = []
    agent2_moves = []
    for i in range(20):
        agent1_moves.append(agent1.choose((False, False)))
        agent2_moves.append(agent2.choose((False, False)))

    assert agent1_moves == agent2_moves

def test_two_reflex_agents_diff_seed():
    agent1 = ReflexAgent(seed=0)
    agent2 = ReflexAgent(seed=1)

    agent1_moves = []
    agent2_moves = []
    for i in range(20):
        agent1_moves.append(agent1.choose((False, False)))
        agent2_moves.append(agent2.choose((False, False)))

    assert agent1_moves != agent2_moves


# ======================================================================
# Model-based agent: updating its memory from percepts
# ======================================================================

# the cell one step from position in the direction of move
def step_from(position, move):
    row, col = position
    d_row, d_col = DIRECTION[move]
    return (row + d_row, col + d_col)

# before its first action the agent has not moved: it is at its own (0, 0)
def test_model_first_call_does_not_move():
    agent = ModelBasedAgent(seed=0)
    agent.choose((False, False))

    assert agent.curr_position == (0, 0)
    assert agent.visited == {(0, 0)}
    assert agent.blocked_cells == set()

# a move that did not bump: the agent is now one step over, and has visited it
def test_model_successful_move():
    agent = ModelBasedAgent(seed=0)
    move = agent.choose((False, False))
    assert move in DIRECTION

    agent.choose((False, False))            # percept: the move worked

    expected = step_from((0, 0), move)
    assert agent.curr_position == expected
    assert expected in agent.visited

# a move that bumped: the agent stays put and remembers the blocked cell
def test_model_bump_records_blocked_cell():
    agent = ModelBasedAgent(seed=0)
    move = agent.choose((False, False))

    agent.choose((False, True))             # percept: the move bumped

    blocked = step_from((0, 0), move)
    assert agent.curr_position == (0, 0)
    assert blocked in agent.blocked_cells
    assert blocked not in agent.visited

# CLEAN does not move the agent, even after an earlier successful move
def test_model_clean_does_not_move():
    agent = ModelBasedAgent(seed=0)
    move = agent.choose((False, False))
    action = agent.choose((True, False))    # moved onto a dirty cell
    assert action == Action.CLEAN

    position = agent.curr_position
    agent.choose((False, False))            # percept after the clean

    assert agent.curr_position == position
    assert position == step_from((0, 0), move)

# the tricky case: a bump, then CLEAN. After the bump the agent's last target
# is the blocked cell; if CLEAN does not reset the target, the next update
# would wrongly "move" the agent into that blocked cell.
def test_model_clean_after_bump_does_not_move():
    agent = ModelBasedAgent(seed=0)
    move = agent.choose((False, False))
    action = agent.choose((True, True))     # bumped, and the current cell is dirty
    assert action == Action.CLEAN

    agent.choose((False, False))            # percept after the clean

    assert agent.curr_position == (0, 0)
    assert step_from((0, 0), move) not in agent.visited

# coordinates are relative to the start, so they can go negative
def test_model_negative_coordinates():
    agent = ModelBasedAgent(seed=0)
    # walk until the agent has gone up or left of its start at least once
    for _ in range(50):
        agent.choose((False, False))
        if any(r < 0 or c < 0 for r, c in agent.visited):
            break
    assert any(r < 0 or c < 0 for r, c in agent.visited)


# ======================================================================
# Model-based agent: choosing where to go (select_move)
# ======================================================================

# the agent is at (0,0); mark three neighbors as visited or blocked by hand,
# so the only new cell is the one in the remaining direction
def test_select_move_prefers_unvisited():
    agent = ModelBasedAgent(seed=0)
    agent.visited.update({(-1, 0), (1, 0)})     # UP and DOWN already visited
    agent.blocked_cells.add((0, -1))            # LEFT is a known wall

    for _ in range(50):
        assert agent.select_move() == Action.RIGHT

# with several new neighbors, it never picks a visited or blocked one
def test_select_move_never_picks_known_cells():
    agent = ModelBasedAgent(seed=0)
    agent.visited.add((-1, 0))                  # UP visited
    agent.blocked_cells.add((0, -1))            # LEFT blocked

    for _ in range(50):
        assert agent.select_move() in (Action.DOWN, Action.RIGHT)

# every neighbor is visited or blocked: falling back must still
# avoid walking into a wall the agent already knows about
def test_select_move_fallback_avoids_known_wall():
    agent = ModelBasedAgent(seed=0)
    agent.visited.update({(-1, 0), (1, 0), (0, 1)})   # UP, DOWN, RIGHT visited
    agent.blocked_cells.add((0, -1))                  # LEFT blocked

    for _ in range(50):
        assert agent.select_move() != Action.LEFT

# the same seed must give the same choices
def test_select_move_same_seed():
    agent1 = ModelBasedAgent(seed=3)
    agent2 = ModelBasedAgent(seed=3)
    assert [agent1.select_move() for _ in range(20)] == \
           [agent2.select_move() for _ in range(20)]


# ======================================================================
# Model-based agent: BFS to the nearest frontier cell (bfs_move)
#
# A frontier cell is next to a visited cell but is neither visited nor
# blocked. The BFS walks only through visited cells and returns the FIRST
# move of the shortest route to the nearest frontier cell.
# ======================================================================

# block the up and down neighbors of every cell in a row of cells
def wall_in_row(cells):
    blocked = set()
    for row, col in cells:
        blocked.update({(row - 1, col), (row + 1, col)})
    return blocked

# visited corridor (0,0) - (0,1) - (0,2); the only way out is past (0,2),
# so the only frontier cell is (0,3) and the first move is RIGHT
def test_bfs_corridor():
    agent = ModelBasedAgent(seed=0)
    agent.visited = {(0, 0), (0, 1), (0, 2)}
    agent.blocked_cells = wall_in_row(agent.visited) | {(0, -1)}

    assert agent.bfs_move() == Action.RIGHT

# frontier (0,-2) is 2 moves away to the left, (0,3) is 3 moves to the right:
# the nearer one wins
def test_bfs_nearest_frontier():
    agent = ModelBasedAgent(seed=0)
    agent.visited = {(0, -1), (0, 0), (0, 1), (0, 2)}
    agent.blocked_cells = wall_in_row(agent.visited)

    assert agent.bfs_move() == Action.LEFT

# the route to the frontier turns a corner: the answer is the first move
# from the agent's position (DOWN), not the last move of the route (RIGHT)
def test_bfs_returns_first_move():
    agent = ModelBasedAgent(seed=0)
    agent.visited = {(0, 0), (1, 0), (2, 0)}
    agent.blocked_cells = {(-1, 0), (0, -1), (0, 1),
                           (1, -1), (1, 1),
                           (2, -1), (3, 0)}
    # only frontier: (2,1), reached by DOWN, DOWN, RIGHT

    assert agent.bfs_move() == Action.DOWN

# the BFS may only walk through visited cells: an unknown cell between
# the agent and a far frontier is itself the nearest frontier
def test_bfs_does_not_walk_through_unknown_cells():
    agent = ModelBasedAgent(seed=0)
    agent.visited = {(0, 0)}
    agent.blocked_cells = {(-1, 0), (1, 0), (0, -1)}

    assert agent.bfs_move() == Action.RIGHT     # (0,1) itself is the frontier

# everything reachable is explored: there is no frontier
def test_bfs_no_frontier():
    agent = ModelBasedAgent(seed=0)
    agent.blocked_cells = {(-1, 0), (1, 0), (0, -1), (0, 1)}

    assert agent.bfs_move() is None

# the BFS only looks at the agent's memory; it must not change it
def test_bfs_does_not_change_memory():
    agent = ModelBasedAgent(seed=0)
    agent.visited = {(0, 0), (0, 1), (0, 2)}
    agent.blocked_cells = wall_in_row(agent.visited) | {(0, -1)}
    visited_before = set(agent.visited)
    blocked_before = set(agent.blocked_cells)

    agent.bfs_move()

    assert agent.visited == visited_before
    assert agent.blocked_cells == blocked_before
    assert agent.curr_position == (0, 0)


# ======================================================================
# Goal-based agent: knows the whole map, BFS to the nearest dirt, repeat
# ======================================================================

def run_goal_agent(world_map):
    world = GridWorld(world_map)
    agent = GoalBasedAgent(world.initial_knowledge())
    return world, run_episode(world, agent)

# 3x3: start (0,0), dirt (2,2): shortest path is 4 moves, then 1 clean
def test_goal_3x3_exact():
    world, result = run_goal_agent(Map.from_file(MAPS / "3x3_map.txt"))
    assert result.steps == 5
    assert result.score == 95
    assert result.cleaned == 1
    assert not result.hit_limit

# 4x4: start (0,1), dirt (2,2) and (3,3):
# 5 moves + clean to (2,2), then 2 moves + clean to (3,3) = 9 steps
def test_goal_4x4_exact():
    world, result = run_goal_agent(Map.from_file(MAPS / "4x4_map.txt"))
    assert result.steps == 9
    assert result.score == 191
    assert result.cleaned == 2
    assert not result.hit_limit

# it knows every wall and edge, so it never bumps
def test_goal_never_bumps():
    for seed in range(20):
        world = GridWorld(Map.generate(10, seed, 0.2, 0.2))
        agent = GoalBasedAgent(world.initial_knowledge())
        percept = world.percept()
        while not world.done:
            percept = world.step(agent.choose(percept))
            dirty, bumped = percept
            assert not bumped

# no randomness: the same map always gives the same result
def test_goal_deterministic():
    world_map = Map.generate(10, 3, 0.2, 0.2)
    _, result1 = run_goal_agent(world_map)
    _, result2 = run_goal_agent(world_map)
    assert result1 == result2
    assert result1.cleaned == result1.total_dirt   # a real, complete result

# on random maps it always cleans everything, and never needs more steps
# than the model-based agent on the same map
def test_goal_beats_model_based():
    for seed in range(20):
        world_map = Map.generate(10, seed, 0.2, 0.2)
        _, goal = run_goal_agent(world_map)
        model = run_episode(GridWorld(world_map), ModelBasedAgent(seed))

        assert goal.cleaned == goal.total_dirt
        assert not goal.hit_limit
        assert goal.steps <= model.steps

# the agent's copy of the dirt is separate from the knowledge package,
# so cleaning must not change the read-only frozenset
def test_goal_does_not_change_knowledge():
    world = GridWorld(Map.from_file(MAPS / "3x3_map.txt"))
    knowledge = world.initial_knowledge()
    run_episode(world, GoalBasedAgent(knowledge))
    assert knowledge.dirt == {(2, 2)}
