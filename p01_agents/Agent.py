import random, copy
from collections import deque
from .GridWorld import Action, DIRECTION, Knowledge

#-----------------------------------------------------
# Base class for Agents
#-----------------------------------------------------
class Agent:
    def __init__(self, seed=None):
        self.rng = random.Random(seed)

    def choose(self, percept):
        raise NotImplementedError()

    def random_move(self):
        return self.rng.choice(list(DIRECTION))
    
    def neighbor(self, position, move):
        row, col = position
        d_row, d_col = DIRECTION[move]

        return (row + d_row, col + d_col)


#-----------------------------------------------------
# subclass of Agents
#-----------------------------------------------------

# reflex agent
class ReflexAgent(Agent):
    def __init__(self, seed=None):
        super().__init__(seed)

    def choose(self, percept) -> Action:
        dirty, bumped = percept

        if dirty:
            return Action.CLEAN

        return self.random_move()

# model-based agent
class ModelBasedAgent(Agent):
    def __init__(self, seed=None):
        super().__init__(seed)
        self.blocked_cells = set() # keeps track of walls and grid edges
        self.curr_position = (0, 0)
        self.target_position = (0, 0)
        self.visited = {(0, 0)}

    # bfs fallback after all cells around current position have been visited
    # uses bfs to search for the nearest unvisited cell and gives us the first
    # move towards that unvisited cell
    def bfs_move(self):
        queue = deque([(self.curr_position, None)])
        seen = {self.curr_position} # if the current cell has been visited

        while len(queue) > 0:
            cell, first_move = queue.popleft()
            
            for move in DIRECTION:
                target = self.neighbor(cell, move)
                
                # finding first frontier cell
                if target in self.blocked_cells or target in seen:
                    continue

                # saves the first move towards the neighbor cell
                first = move if first_move is None else first_move
                if target not in self.visited:
                    return first

                seen.add(target)
                queue.append((target, first))

        return None

    # select the next neighbor to move to
    def select_move(self):
        moves = [] # contains all valid moves

        # finds all valid neighbors
        for move in DIRECTION:
            target = self.neighbor(self.curr_position, move)

            if target in self.blocked_cells:
                continue

            if target in self.visited:
                continue

            moves.append(move)

        # if no possible neighbors to move to use bfs fallback move
        if len(moves) == 0:
            bfs = self.bfs_move()

            # if returns Action.CLEAN if all cells have been visited
            return bfs if bfs is not None else Action.CLEAN
        else:
            # randomly choose a move from the valid moveset
            return self.rng.choice(list(moves))

    def choose(self, percept):
        dirty, bumped = percept

        # add walls/grid edges to blocked cells
        if bumped:
            self.blocked_cells.add(self.target_position)
        else:
            # if not blocked, then move to that position
            self.curr_position = self.target_position
            self.visited.add(self.curr_position)

        # clean cell if dirty
        if dirty:
            self.target_position = self.curr_position
            return Action.CLEAN

        # move agent
        move = self.select_move()
        self.target_position = self.neighbor(self.curr_position, move)

        return move

# goal-based agent
class GoalBasedAgent(Agent):
    def __init__(self, knowledge: Knowledge):
        super().__init__()
        self.curr_position = knowledge.start
        self.target_position = knowledge.start
        self.dirt_positions = set(knowledge.dirt)
        self.wall_positions = knowledge.walls
        self.map_size = knowledge.size


    def move_bfs(self):
        queue = deque([(self.curr_position, None)])
        visited = {self.curr_position}

        while len(queue) > 0:
            cell, first_move = queue.popleft()

            for move in DIRECTION:
                target = self.neighbor(cell, move)
                target_row, target_col = target

                ## agent should never bump because it knows all wall positions
                ## and grid edges

                # out of bounds up/down
                if target_row < 0 or target_row >= self.map_size:
                    continue

                # out of bounds right/left
                if target_col < 0 or target_col >= self.map_size:
                    continue

                # cell contains wall block or has been visited
                if target in self.wall_positions or target in visited:
                    continue

                first = move if first_move is None else first_move
                if target in self.dirt_positions:
                    return first

                visited.add(target)
                queue.append((target, first))
        return None

    def choose(self, percept):
        dirty, bumped = percept
        self.curr_position = self.target_position
        
        if dirty:
            self.dirt_positions.discard(self.curr_position)
            self.target_position = self.curr_position
            return Action.CLEAN

        move = self.move_bfs()

        if move is None:
            return Action.CLEAN
        else:
            self.target_position = self.neighbor(self.curr_position, move)
            return move