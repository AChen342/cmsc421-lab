import random
from .GridWorld import Action, DIRECTION

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

    def choose(self, percept):
        raise NotImplementedError()

# goal-based agent
class GoalBasedAgent(Agent):
    def __init__(self, knowledge):
        super().__init__()
        self.knowledge = knowledge

    def choose(self, percept):
        raise NotImplementedError()