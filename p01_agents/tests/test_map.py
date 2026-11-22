from pathlib import Path
import pytest
from p01_agents.map import Map

MAPS = Path(__file__).parent / "maps"

# 3x3_map.txt (and its variants) after loading: the O becomes "_"
GRID_3X3 = [["_", "_", "_"],
            ["_", "#", "_"],
            ["_", "_", "*"]]


def count(grid, symbol):
    """Number of cells in grid equal to symbol."""
    return sum(cell == symbol for row in grid for cell in row)


# ======================================================================
# Grid helpers: count_walls, reachable_cells
# ======================================================================

def test_count_walls():
    grid = [["_", "_", "_"],
            ["_", "#", "#"],
            ["_", "_", "#"]]
    assert Map.count_walls(grid) == 3

def test_reachable_cells_all_open():
    grid = [["_", "_", "_"],
            ["_", "#", "#"],
            ["_", "_", "#"]]
    reached_cells = Map.reachable_cells(grid, (0, 0))

    assert reached_cells == {(0,0), (0, 1), (0, 2), (1, 0), (2, 0), (2, 1)}
    assert len(reached_cells) == 6

# (2,2) is boxed in by walls and the grid edge, so it must not be reached
def test_reachable_cells_boxed_corner():
    grid = [["_", "_", "_"],
            ["_", "#", "#"],
            ["_", "#", "_"]]
    reached_cells = Map.reachable_cells(grid, (0, 0))

    assert reached_cells == {(0,0), (0, 1), (0, 2), (1, 0), (2, 0)}
    assert len(reached_cells) == 5


# ======================================================================
# from_file: valid maps
# ======================================================================

def test_load_smallest():
    m = Map.from_file(MAPS / "smallest_map.txt")
    assert m.start == (0, 0)
    assert m.grid == [["_", "_"],
                      ["_", "_"]]

def test_load_3x3():
    m = Map.from_file(MAPS / "3x3_map.txt")
    assert m.start == (0, 0)
    assert m.grid == GRID_3X3

def test_load_4x4():
    m = Map.from_file(MAPS / "4x4_map.txt")
    assert m.start == (0, 1)
    assert m.grid == [["_", "_", "_", "_"],
                      ["#", "#", "#", "_"],
                      ["#", "_", "*", "_"],
                      ["#", "_", "_", "*"]]

# should be a valid map, the trailing blanks will be dropped
def test_trailing_blank_lines():
    m = Map.from_file(MAPS / "trailing_blank_lines_map.txt")
    assert m.start == (0, 0)
    assert m.grid == GRID_3X3

# same map as 3x3_map.txt, but with \n line endings instead of \r\n
def test_unix_line_endings(tmp_path):
    f = tmp_path / "unix.txt"
    f.write_bytes(b"O__\n_#_\n__*\n")

    m = Map.from_file(f)
    assert m.start == (0, 0)
    assert m.grid == GRID_3X3


# ======================================================================
# from_file: invalid maps
# ======================================================================

def test_missing_file():
    with pytest.raises(FileNotFoundError):
        Map.from_file(MAPS / "1milx1mil_map.txt")

def test_empty_map():
    with pytest.raises(ValueError, match="Map is empty"):
        Map.from_file(MAPS / "empty_map.txt")

def test_only_blanks():
    with pytest.raises(ValueError, match="Map is empty"):
        Map.from_file(MAPS / "only_blanks_map.txt")

def test_load_1x1():
    with pytest.raises(ValueError, match="map is too small"):
        Map.from_file(MAPS / "1x1_map.txt")

def test_not_square():
    with pytest.raises(ValueError, match="map must be square"):
        Map.from_file(MAPS / "not_square_map.txt")

def test_ragged_map():
    with pytest.raises(ValueError, match="map must be square"):
        Map.from_file(MAPS / "ragged_map.txt")

def test_leading_blank_lines():
    with pytest.raises(ValueError, match="map must be square"):
        Map.from_file(MAPS / "leading_blank_lines_map.txt")

# if there is a leading space in the map, then the loader
# should throw an invalid cell message so that map maker can
# fix it.
def test_leading_space():
    with pytest.raises(ValueError, match="Invalid cell found at"):
        Map.from_file(MAPS / "leading_space_map.txt")

def test_unknown_char():
    with pytest.raises(ValueError, match="Invalid cell found at"):
        Map.from_file(MAPS / "unknown_char_map.txt")

def test_no_agent():
    with pytest.raises(ValueError, match="There are 0 agents"):
        Map.from_file(MAPS / "no_agent_map.txt")

def test_two_agents():
    with pytest.raises(ValueError, match="There are 2 agents"):
        Map.from_file(MAPS / "two_agents_map.txt")

def test_disconnected_map():
    with pytest.raises(ValueError, match="disconnected"):
        Map.from_file(MAPS / "disconnected_map.txt")

# not square AND two agents: the square error must be reported first
def test_too_many_issues():
    with pytest.raises(ValueError, match="map must be square"):
        Map.from_file(MAPS / "too_many_issues_map.txt")


# ======================================================================
# display_map
# ======================================================================

# display_map() should not modify the original map, read only access
def test_display_map():
    m = Map.from_file(MAPS / "3x3_map.txt")
    m.display_map()
    assert m.start == (0, 0)
    assert m.grid == GRID_3X3


# ======================================================================
# generate: shape and placement
# ======================================================================

def test_generate():
    m = Map.generate(5, 42, 0.2, 0.2)
    assert len(m.grid) == 5
    assert all(len(row) == 5 for row in m.grid)

# each row must be its own list: changing one cell must not
# change the same column in any other row
def test_cell_reference():
    m = Map.generate(5, 42, 0.2, 0.2)
    before = [row[4] for row in m.grid[1:]]

    m.grid[0][4] = "X"

    after = [row[4] for row in m.grid[1:]]
    assert after == before

# for dirt and wall densities of 0.2 on 5x5, there should be
# 5 walls and 5 dirt
def test_dirt_and_wall_count():
    m = Map.generate(5, 42, 0.2, 0.2)
    assert count(m.grid, "*") == 5
    assert count(m.grid, "#") == 5

def test_agent_start():
    m = Map.generate(5, 42, 0.2, 0.2)
    row, col = m.start
    assert m.grid[row][col] == "_"

# with dirt_density = 0.05 that gives us a dirt count of 0.45,
# which is less than one, which forces generate() to make dirt_count = 1
def test_forced_dirt_count():
    m = Map.generate(3, 0, 0.2, 0.05)
    assert count(m.grid, "*") == 1


# ======================================================================
# generate: reproducibility
# ======================================================================

def test_same_seed_generation():
    m = Map.generate(5, 42, 0.2, 0.2)
    m2 = Map.generate(5, 42, 0.2, 0.2)

    # m and m2 should create the same map
    assert m.grid == m2.grid
    assert m.start == m2.start

def test_different_seed_generation():
    m = Map.generate(5, 42, 0.2, 0.2)
    m2 = Map.generate(5, 43, 0.2, 0.2)
    assert m.grid != m2.grid


# ======================================================================
# generate: connectivity and retries
# ======================================================================

# seed 7's first attempt is disconnected, so this exercises a retry
def test_retry_seed_7():
    m = Map.generate(5, 7, 0.2, 0.2)
    assert m.is_connected(m.grid, m.start)
    assert count(m.grid, "#") == 5
    assert count(m.grid, "*") == 5

def test_many_seeds():
    for i in range(50):
        m = Map.generate(5, i, 0.2, 0.2)
        assert count(m.grid, "*") == 5
        assert count(m.grid, "#") == 5
        assert m.is_connected(m.grid, m.start)

def test_max_tries_timeout():
    with pytest.raises(ValueError, match="no connected map"):
        Map.generate(5, 7, 0.2, 0.2, max_tries=0)


# ======================================================================
# generate: invalid arguments
# ======================================================================

def test_map_size_0x0():
    with pytest.raises(ValueError, match="map size is too small"):
        Map.generate(0, 7, 0.2, 0.2)

def test_map_size_1x1():
    with pytest.raises(ValueError, match="map size is too small"):
        Map.generate(1, 7, 0.2, 0.2)

def test_negative_wall_density():
    with pytest.raises(ValueError, match="wall density cannot be negative"):
        Map.generate(5, 7, -0.2, 0.2)

def test_negative_dirt_density():
    with pytest.raises(ValueError, match="dirt density cannot be less than 0"):
        Map.generate(5, 7, 0.2, -0.1)

def test_dirt_density_zero():
    with pytest.raises(ValueError, match="dirt density cannot be less than 0"):
        Map.generate(5, 7, 0.2, 0)

def test_no_grid_space():
    with pytest.raises(ValueError, match="grid space"):
        Map.generate(2, 0, 0.25, 0.7)
