from pathlib import Path
import pytest
from p01_agents.Map import Map
from p01_agents.GridWorld import GridWorld, Action, DIRECTION
from p01_agents.Agent import ReflexAgent, ModelBasedAgent, GoalBasedAgent, Agent

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