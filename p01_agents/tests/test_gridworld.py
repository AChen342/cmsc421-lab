from pathlib import Path
import pytest
from p01_agents.map import Map
from p01_agents.gridworld import GridWorld, Action

MAPS = Path(__file__).parent / "maps"

def test_move_off_top_edge_bumps():
    world = GridWorld(Map.from_file(MAPS / "3x3_map.txt"))
    dirty, bumped = world.step(Action.UP)

    assert bumped
    assert not dirty
    assert world.agent_position == (0, 0)
    assert world.steps == 1

def test_move_down():
    world = GridWorld(Map.from_file(MAPS / "3x3_map.txt"))
    dirty, bumped = world.step(Action.DOWN)

    assert not bumped
    assert not dirty
    assert world.agent_position == (1, 0)
    assert world.steps == 1

def test_move_into_wall_bumps():
    world = GridWorld(Map.from_file(MAPS / "3x3_map.txt"))
    world.step(Action.RIGHT) # move right
    dirty, bumped = world.step(Action.DOWN) # move down

    assert bumped
    assert not dirty
    assert world.agent_position == (0, 1)
    assert world.steps == 2

def test_path_to_dirt_is_dirty():
    world = GridWorld(Map.from_file(MAPS / "3x3_map.txt"))
    world.step(Action.DOWN)
    world.step(Action.DOWN)
    world.step(Action.RIGHT)
    dirty, bumped = world.step(Action.RIGHT)

    assert not bumped
    assert dirty
    assert world.agent_position == (2, 2)
    assert world.steps == 4

def test_move_off_right_edge_bumps():
    world = GridWorld(Map.from_file(MAPS / "3x3_map.txt"))
    world.step(Action.RIGHT)
    world.step(Action.RIGHT)
    dirty, bumped = world.step(Action.RIGHT)

    assert bumped
    assert not dirty
    assert world.agent_position == (0, 2)
    assert world.steps == 3

def test_clean_on_clean_cell():
    world = GridWorld(Map.from_file(MAPS / "3x3_map.txt"))
    dirty, bumped = world.step(Action.CLEAN)

    assert not bumped
    assert not dirty
    assert world.agent_position == (0, 0)
    assert world.steps == 1
    assert len(world.dirty_cells) == 1
    assert world.cleaned == 0

def test_clean_on_dirty_cell():
    world = GridWorld(Map.from_file(MAPS / "3x3_map.txt"))
    world.step(Action.DOWN)
    world.step(Action.DOWN)
    world.step(Action.RIGHT)
    world.step(Action.RIGHT)
    dirty, bumped = world.step(Action.CLEAN)

    assert not bumped
    assert not dirty
    assert world.agent_position == (2, 2)
    assert world.steps == 5
    assert world.cleaned == 1
    assert (2, 2) not in world.dirty_cells
    assert world.world_map.grid[2][2] == "*"

def test_invalid_action():
    world = GridWorld(Map.from_file(MAPS / "3x3_map.txt"))
    with pytest.raises(ValueError, match="invalid action"):
        world.step("jump")

    assert world.steps == 0

def test_score_after_clean():
    world = GridWorld(Map.from_file(MAPS / "3x3_map.txt"))
    world.step(Action.DOWN)
    world.step(Action.DOWN)
    world.step(Action.RIGHT)
    world.step(Action.RIGHT)
    world.step(Action.CLEAN)

    assert world.score == 95

def test_done_after_last_dirt_cleaned():
    world = GridWorld(Map.from_file(MAPS / "3x3_map.txt"))

    assert not world.done
    world.step(Action.DOWN)
    world.step(Action.DOWN)
    world.step(Action.RIGHT)
    world.step(Action.RIGHT)
    world.step(Action.CLEAN)

    assert world.done

def test_step_after_done():
    world = GridWorld(Map.from_file(MAPS / "3x3_map.txt"))
    world.step(Action.DOWN)
    world.step(Action.DOWN)
    world.step(Action.RIGHT)
    world.step(Action.RIGHT)
    world.step(Action.CLEAN)

    # step after done is true
    with pytest.raises(RuntimeError, match="episode is over"):
        world.step(Action.LEFT)

    assert world.steps == 5

# 3x3 map: limit is 4 * 3 * 3 = 36 steps. UP from the start (0,0) always bumps,
# so no dirt is ever cleaned and only the step limit can end the episode.
def test_step_limit_3x3():
    world = GridWorld(Map.from_file(MAPS / "3x3_map.txt"))
    for _ in range(35):
        world.step(Action.UP)
    assert not world.done

    world.step(Action.UP)
    assert world.done
    assert world.steps == 36

    # the episode is over: another step is rejected and costs nothing
    with pytest.raises(RuntimeError, match="episode is over"):
        world.step(Action.UP)
    assert world.steps == 36

# 4x4 map: limit is 4 * 4 * 4 = 64. Guards against a hard-coded limit.
def test_step_limit_4x4():
    world = GridWorld(Map.from_file(MAPS / "4x4_map.txt"))
    while not world.done:
        world.step(Action.UP)   # start is (0,1) on the top row, so UP always bumps
    assert world.steps == 64
    assert world.cleaned == 0

def test_knowledge_package_3x3():
    world = GridWorld(Map.from_file(MAPS / "3x3_map.txt"))
    knowledge = world.initial_knowledge()

    assert knowledge.start == (0,0)
    assert knowledge.dirt == {(2, 2)}
    assert knowledge.walls == {(1, 1)}
    assert knowledge.size == 3

def test_knowledge_package_after_episode_3x3():
    world = GridWorld(Map.from_file(MAPS / "3x3_map.txt"))
    world.step(Action.DOWN)
    world.step(Action.DOWN)
    world.step(Action.RIGHT)
    world.step(Action.RIGHT)
    world.step(Action.CLEAN)

    # cleaning the dirty cells does not change the initial knowledge package
    assert world.initial_knowledge().dirt == {(2,2)}

def test_knowledge_package_readonly_3x3():
    world = GridWorld(Map.from_file(MAPS / "3x3_map.txt"))
    knowledge = world.initial_knowledge()

    with pytest.raises(AttributeError):
        knowledge.dirt.add((0, 0))
        knowledge.walls.add((0, 0))

def test_percept():
    world = GridWorld(Map.from_file(MAPS / "3x3_map.txt"))

    # at the start: (0,0) is clean, and looking costs nothing
    assert world.percept() == (False, False)
    assert world.steps == 0

    # move onto the dirt at (2,2)
    for action in [Action.DOWN, Action.DOWN, Action.RIGHT, Action.RIGHT]:
        world.step(action)
    assert world.percept() == (True, False)
    assert world.steps == 4      # percept() did not count a step

    # bump into the bottom edge while standing on the dirt:
    # step() reports the bump, percept() never does
    assert world.step(Action.DOWN) == (True, True)
    assert world.percept() == (True, False)

    # after cleaning, the cell is reported clean
    world.step(Action.CLEAN)
    assert world.percept() == (False, False)
    assert world.steps == 6


# ======================================================================
# render
# ======================================================================

def test_render_start():
    world = GridWorld(Map.from_file(MAPS / "3x3_map.txt"))
    assert world.render() == "O _ _\n_ # _\n_ _ *"

# the agent is drawn over the dirt it is standing on
def test_render_agent_on_dirt():
    world = GridWorld(Map.from_file(MAPS / "3x3_map.txt"))
    for action in [Action.DOWN, Action.DOWN, Action.RIGHT, Action.RIGHT]:
        world.step(action)
    assert world.render() == "_ _ _\n_ # _\n_ _ O"

# 4x4 map: dirt at (2,2) and (3,3), so the episode continues after one clean.
# Once the agent steps off a cleaned cell, that cell is drawn as "_".
def test_render_cleaned_cell():
    world = GridWorld(Map.from_file(MAPS / "4x4_map.txt"))
    assert world.render() == "_ O _ _\n# # # _\n# _ * _\n# _ _ *"

    # (0,1) -> (0,3) -> (2,3) -> (2,2), clean, then step back to (2,3)
    for action in [Action.RIGHT, Action.RIGHT, Action.DOWN, Action.DOWN,
                   Action.LEFT, Action.CLEAN, Action.RIGHT]:
        world.step(action)
    assert world.render() == "_ _ _ _\n# # # _\n# _ _ O\n# _ _ *"

# render() only reads: the Map must still show the dirt the world has cleaned
def test_render_does_not_change_map():
    world = GridWorld(Map.from_file(MAPS / "3x3_map.txt"))
    for action in [Action.DOWN, Action.DOWN, Action.RIGHT, Action.RIGHT, Action.CLEAN]:
        world.step(action)
    world.render()
    assert world.world_map.grid == [["_", "_", "_"],
                                    ["_", "#", "_"],
                                    ["_", "_", "*"]]
