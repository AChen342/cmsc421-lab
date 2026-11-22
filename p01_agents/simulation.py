import os
import time
from collections import namedtuple
from .gridworld import GridWorld
from .agent import Agent

EpisodeResult = namedtuple(
    "EpisodeResult", ["score", "steps", "cleaned", "total_dirt", "hit_limit"]
)

def run_episode(world: GridWorld, agent: Agent, on_step=None):
    total_dirt = len(world.dirty_cells)

    percept = world.percept()

    if on_step is not None:
        on_step(world)

    while not world.done:
        action = agent.choose(percept)
        percept = world.step(action)

        if on_step is not None:
            on_step(world)

    hit_limit = len(world.dirty_cells) > 0

    return EpisodeResult(world.score, world.steps, world.cleaned, total_dirt, hit_limit)


# clear the terminal: Windows uses its own "cls" command (works in every
# PowerShell / cmd window); other systems use ANSI escape codes
def clear_screen():
    if os.name == "nt":
        os.system("cls")
    else:
        print("\033[H\033[2J", end="")   # ANSI: cursor to top-left, clear screen

# build an on_step function that animates the episode in the terminal:
# clear the screen, draw the world and a status line, then pause
def make_watcher(delay=0.2):
    def watch(world):
        clear_screen()
        print(world.render())
        print()
        print(f"step {world.steps}/{world.step_limit}   "
              f"cleaned {world.cleaned}   score {world.score}")
        time.sleep(delay)

    return watch