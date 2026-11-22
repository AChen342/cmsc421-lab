from .gridworld import GridWorld
from .map import Map
from .agent import ReflexAgent, ModelBasedAgent, GoalBasedAgent
from .simulation import run_episode, make_watcher
import csv
import os
from statistics import mean

SEED = 7
WALL_DENSITY = 0.3
DIRT_DENSITY = 0.2
MAP_SIZE = 10
RUNS = 100
# results/ folder next to this file, so it works no matter where you run from
RESULTS_PATH = os.path.join(os.path.dirname(__file__), "results", "experiment.csv")

# run one episode and also measure exploration: the share of the map's
# open (non-wall) cells the agent stood on at least once
def run_and_track(world, agent):
    visited = set()
    result = run_episode(world, agent, on_step=lambda w: visited.add(w.agent_position))

    grid = world.world_map.grid
    open_cells = len(grid) ** 2 - Map.count_walls(grid)
    explored = 100 * len(visited) / open_cells
    return result, explored

# write one row per (map, agent) episode to a CSV file
def save_csv(results_by_agent, explored_by_agent, path=RESULTS_PATH):
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["map_seed", "agent", "cleaned", "total_dirt", "steps", "hit_limit", "score", "explored"])
        for agent_name, results in results_by_agent.items():
            # the loop in main() uses the run index as the map seed
            for seed, r in enumerate(results):
                explored = explored_by_agent[agent_name][seed]
                writer.writerow([seed, agent_name, r.cleaned, r.total_dirt, r.steps, r.hit_limit,
                                 r.score, f"{explored:.1f}"])

# print one summary row per agent, averaged over all maps
def print_summary(results_by_agent, explored_by_agent):
    print(f"{'agent':<8}{'avg score':>11}{'avg steps':>11}{'% cleaned':>11}{'hit limit':>11}{'% explored':>12}")
    for agent_name, results in results_by_agent.items():
        avg_score = mean(r.score for r in results)
        avg_steps = mean(r.steps for r in results)
        pct_clean = 100 * sum(r.cleaned for r in results) / sum(r.total_dirt for r in results)
        hit_limit = sum(r.hit_limit for r in results)
        avg_explored = mean(explored_by_agent[agent_name])
        print(f"{agent_name:<8}{avg_score:>11.1f}{avg_steps:>11.1f}{pct_clean:>10.1f}%{hit_limit:>7}/{len(results)}"
              f"{avg_explored:>11.1f}%")

def main():
    reflex_agent_results = []
    model_agent_results = []
    goal_agent_results = []
    explored_by_agent = {"reflex": [], "model": [], "goal": []}
    successful_run = 0
    for i in range(RUNS):
        # for each run generate a new random seed to create a world on
        world_map = Map.generate(MAP_SIZE, i, WALL_DENSITY, DIRT_DENSITY)

        # run each agent type on this world and save its results
        result, explored = run_and_track(GridWorld(world_map), ReflexAgent(SEED))
        reflex_agent_results.append(result)
        explored_by_agent["reflex"].append(explored)

        result, explored = run_and_track(GridWorld(world_map), ModelBasedAgent(SEED))
        model_agent_results.append(result)
        explored_by_agent["model"].append(explored)

        goal_world = GridWorld(world_map)
        result, explored = run_and_track(goal_world, GoalBasedAgent(goal_world.initial_knowledge()))
        goal_agent_results.append(result)
        explored_by_agent["goal"].append(explored)
        
        successful_run += 1
    
    print(f"Experiment finished, completed {successful_run}/{RUNS} runs.")
    print()

    results_by_agent = {
        "reflex": reflex_agent_results,
        "model": model_agent_results,
        "goal": goal_agent_results,
    }
    save_csv(results_by_agent, explored_by_agent)
    print_summary(results_by_agent, explored_by_agent)
    print(f"\nPer-run results saved to {RESULTS_PATH}")

if __name__=="__main__":
    main()