"""Map: the fixed layout of a grid world (walls, dirt, agent start).

A Map never changes once built. Build one with Map.from_file(path) or
Map.generate(size, seed, wall_density, dirt_density).

Cells: "_" empty, "*" dirt, "#" wall. Positions are (row, col).
"""
import copy
import random
from collections import deque


class Map:
    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------
    def __init__(self, grid, start):
        self.grid = grid      # list of rows, each a list of cells
        self.start = start    # (row, col) where the agent begins

    # ------------------------------------------------------------------
    # Builders (alternative constructors)
    # ------------------------------------------------------------------

    # load a map from a text file: _ empty, * dirt, # wall, O agent start
    @classmethod
    def from_file(cls, mapFile):
        with open(mapFile, encoding="utf-8") as mpf:
            lines = mpf.read().rstrip().splitlines()

        # convert map file into a matrix
        sym = ["_", "*", "#", "O"]
        grid = []
        agent_count = 0
        agent_pos = None
        for i, line in enumerate(lines):
            row = []
            line = line.rstrip()
            for j, char in enumerate(line):
                if char in sym:
                    if char == "O":
                        agent_count += 1
                        agent_pos = (i, j)
                    row.append(char)
                else:
                    raise ValueError(f"Invalid cell found at ({i},{j}): {char}.")
            grid.append(row)

        # the following checks if map is valid
        cls.isEmptyMapFile(grid)
        cls.isSquareMatrix(grid)
        if len(grid) == 1:
            raise ValueError(f"map is too small, must be at least 2x2 matrix")

        if agent_count == 0 or agent_count > 1:
            raise ValueError(f"There are {agent_count} agents, only 1 agent per map.")

        # checks if map is connected
        if not cls.is_connected(grid, agent_pos):
            raise ValueError("This map is disconnected")

        # replace agent position with "_"
        agent_row, agent_col = agent_pos
        grid[agent_row][agent_col] = "_"

        return cls(grid, agent_pos)

    # build a random connected map from a seed
    @classmethod
    def generate(cls, size, seed, wall_density, dirt_density, max_tries=100):
        # validate inputs
        if size < 2:
            raise ValueError("map size is too small, must be at least 2x2 matrix")

        if wall_density < 0:
            raise ValueError("wall density cannot be negative")

        if dirt_density <= 0:
            raise ValueError("dirt density cannot be less than 0")

        # convert densities to exact cell counts
        total_cells = size * size
        wall_count = round(total_cells * wall_density)
        dirt_count = round(total_cells * dirt_density)

        # at least one dirt in each map
        if dirt_count < 1:
            dirt_count = 1

        # walls + dirt + the start cell must fit in the grid
        if wall_count + dirt_count + 1 > total_cells:
            raise ValueError("walls and dirt surpasses grid space")

        # one generator for every attempt, so retries stay reproducible
        rng = random.Random(seed)

        for attempts in range(max_tries):
            # build a nxn grid filled with _
            grid = []
            for i in range(size):
                grid.append([])
                for j in range(size):
                    grid[i].append("_")

            # build a list of every cell position
            coords = []
            for row in range(size):
                for col in range(size):
                    coords.append((row, col))

            # shuffle coord list
            rng.shuffle(coords)

            # first wall_count positions -> turn to walls
            for row, col in coords[:wall_count]:
                grid[row][col] = "#"

            # next dirt_count positions -> turn to dirt
            for row, col in coords[wall_count:wall_count + dirt_count]:
                grid[row][col] = "*"

            # agent position: the next free cell after walls and dirt
            agent_pos = coords[wall_count + dirt_count]

            # keep the map only if it is connected; otherwise try again
            if cls.is_connected(grid, agent_pos):
                return cls(grid, agent_pos)

        raise ValueError(f"no connected map after {max_tries} attempts (size={size}, walls={wall_density})")

    # ------------------------------------------------------------------
    # Validation checks (raise ValueError, or return True/False)
    # ------------------------------------------------------------------

    # makes sure the map file is not empty
    @staticmethod
    def isEmptyMapFile(grid):
        if len(grid) == 0:
            raise ValueError(f"Map is empty")

    # makes sure map is nxn
    @staticmethod
    def isSquareMatrix(grid):
        # number of rows; every row must have this many cells
        col_size = len(grid)

        for i, row in enumerate(grid):
            if len(row) != col_size:
                raise ValueError(f"map must be square: row {i} is {len(row)}, expected {col_size}")

    # True if every non-wall cell can be reached from agent_pos
    @classmethod
    def is_connected(cls, grid, agent_pos):
        reached_cells = cls.reachable_cells(grid, agent_pos)
        if len(reached_cells) != (len(grid)**2) - cls.countWalls(grid):
            return False

        return True

    # ------------------------------------------------------------------
    # Grid helpers
    # ------------------------------------------------------------------

    # BFS from start: returns the set of every cell the agent can reach
    @staticmethod
    def reachable_cells(grid, start):
        queue = deque([start])
        visited = {start}
        while len(queue) > 0:
            cell = queue.popleft()
            row, col = cell
            for direction_row, direction_col in [(-1, 0), (1, 0), (0, -1), (0, 1)]: # up, down, left, right
                next_row, next_col = row + direction_row, col + direction_col
                # skip if neighbor is not in grid row-wise
                if next_row < 0 or next_row > len(grid) - 1:
                    continue

                # skip if neighbor is not in grid column wise
                if next_col < 0 or next_col > len(grid) - 1:
                    continue

                if grid[next_row][next_col] == "#":
                    continue

                next_cell = next_row, next_col
                if next_cell not in visited:
                    visited.add(next_cell)
                    queue.append(next_cell)

        return visited

    # helper to count number of walls
    @staticmethod
    def countWalls(grid):
        numWalls = 0
        for row in grid:
            for cell in row:
                if cell == "#":
                    numWalls+=1

        return numWalls

    # ------------------------------------------------------------------
    # Display
    # ------------------------------------------------------------------

    # print the map with the agent shown as O (read only: grid is not changed)
    def displayMap(self):
        agent_row, agent_col = self.start
        displayCopy = copy.deepcopy(self.grid)
        displayCopy[agent_row][agent_col] = "O"

        for row in displayCopy:
            print(*row)
