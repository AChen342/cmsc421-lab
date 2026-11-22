from .map import Map
from enum import Enum
from collections import namedtuple
import copy

class Action(Enum):
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4
    CLEAN = 5

DIRECTION = {
    Action.UP : (-1, 0),
    Action.DOWN: (1, 0),
    Action.LEFT: (0, -1),
    Action.RIGHT: (0, 1)
}

Knowledge = namedtuple("Knowledge", ["start", "dirt", "walls", "size"])

class GridWorld:
    def __init__(self, world_map : Map):
        self.world_map = world_map
        self.agent_position = world_map.start
        self.steps = 0
        self.dirty_cells = set()
        self.cleaned = 0

        # the episode ends after 4 * n^2 steps
        size = len(world_map.grid)
        self.step_limit = 4 * size * size

        for row in range(len(world_map.grid)):
            for col in range(len(world_map.grid[row])):
                if world_map.grid[row][col] == "*":
                    self.dirty_cells.add((row, col))

    @property
    def score(self):
        return 100 * self.cleaned - self.steps

    @property
    def done(self):
        return len(self.dirty_cells) == 0 or self.steps >= self.step_limit

    def step(self, action : Action):
        if self.done:
            raise RuntimeError("episode is over")

        bumped = False

        if not isinstance(action, Action):
            raise ValueError("invalid action")
        
        if action in DIRECTION:
            size = len(self.world_map.grid)
            dir_row, dir_col = DIRECTION[action]
            agent_row, agent_col = self.agent_position
            
            # calculates target cell's row and col
            target_row, target_col = dir_row + agent_row, dir_col + agent_col
            target = target_row, target_col

            # checks if target cell is within grid space
            inside = 0 <= target_row < size and 0 <= target_col < size

            # checks if agent can move to that cell
            # cannot if wall or out of bounds
            blocked = not inside or self.world_map.grid[target_row][target_col] == "#"

            # set bumped to True if blocked, move agent if not
            if blocked:
                bumped = True
            else:
                self.agent_position = target

        elif action == Action.CLEAN:
            if self.agent_position in self.dirty_cells:
                self.dirty_cells.remove(self.agent_position)
                self.cleaned += 1
        
        # checks if cell is dirty
        dirty = self.agent_position in self.dirty_cells

        self.steps += 1

        return dirty, bumped

    def percept(self):
        return self.agent_position in self.dirty_cells, False

    def initial_knowledge(self):
        wall_positions = set()
        dirt_positions = set()
        grid = self.world_map.grid

        # collect every wall and dirt position from the (unchanging) Map
        for i, row in enumerate(grid):
            for j, cell in enumerate(row):
                if cell == "#":
                    wall_positions.add((i, j))

                if cell == "*":
                    dirt_positions.add((i, j))

        return Knowledge(start=self.world_map.start, dirt=frozenset(dirt_positions),
                         walls=frozenset(wall_positions), size=len(grid))

    def render(self):
        current_state = copy.deepcopy(self.world_map.grid)

        # check dirt cells
        for i, row in enumerate(current_state):
            for j, cell in enumerate(row):
                if cell == "*" and not (i, j) in self.dirty_cells:
                    current_state[i][j] = "_"

        # place agent
        agent_row, agent_col = self.agent_position
        current_state[agent_row][agent_col] = "O"

        return "\n".join(" ".join(row) for row in current_state)