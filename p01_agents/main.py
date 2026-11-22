"""P1: Agent simulator. Run with: python -m p01_agents.main"""
import argparse
from . import map as mp
from .gridworld import GridWorld
from .agent import ReflexAgent, ModelBasedAgent, GoalBasedAgent
from .simulation import run_episode, make_watcher

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--map", help="load the map file you want to test")
    parser.add_argument("--size", type=int, help="generate a nxn map with size")
    parser.add_argument("--seed", type=int, help="generate a map from a seed")
    parser.add_argument("--walls", type=float, help="wall density")
    parser.add_argument("--dirt", type=float, help="dirt density")
    parser.add_argument("--agent", choices=["reflex", "model", "goal"], default="reflex",
                        help="which agent to run: reflex, model or goal (default: reflex)")
    parser.add_argument("--agent-seed", type=int, default=0,
                        help="seed for the agent's random choices (default: 0)")
    parser.add_argument("--watch", action="store_true",
                        help="animate the episode in the terminal")
    parser.add_argument("--delay", type=float, default=0.2,
                        help="seconds between frames when watching (default: 0.2)")
    args = parser.parse_args()

    if args.delay < 0:
        parser.error("--delay: must not be negative")

    world_map = None
    if args.map:
        if args.size is not None or args.seed is not None or \
            args.walls is not None or args.dirt is not None:
            parser.error("Argument conflict, cannot load map with size, seed, walls, "
            "and dirt arguments given. Either load a map or provided those 4 arguments, but not both.")
        try:
            world_map = mp.Map.from_file(args.map)
        except ValueError as e:
            parser.error(str(e))
        except FileNotFoundError as fe:
            parser.error(str(fe))

    else:
        # default values
        if args.size is None:
            args.size = 10

        if args.walls is None:
            args.walls = 0.2

        if args.dirt is None:
            args.dirt = 0.2

        if args.seed is None:
            args.seed = 42
        
        # check wall density value
        if args.walls < 0 or args.walls > 0.25:
            parser.error("--walls: wall density range must be between 0 and 0.25")

        # check dirt density value
        if args.dirt <= 0:
            parser.error("--dirt: dirt density must be greater than 0")
        
        # check that the combined densities of dirt and walls is less than 0.5
        densities = args.walls + args.dirt
        if densities >= 1:
            parser.error("sum of wall and dirt densities must be less than 1")

        try:
            world_map = mp.Map.generate(args.size, args.seed, args.walls, args.dirt)
        except ValueError as e:
            parser.error(str(e))
    
    # run one episode of the chosen agent on the map
    world = GridWorld(world_map)
    if args.agent == "reflex":
        agent = ReflexAgent(args.agent_seed)
    elif args.agent == "model":
        agent = ModelBasedAgent(args.agent_seed)
    elif args.agent == "goal":
        # knows the whole map; uses no randomness, so --agent-seed has no effect
        agent = GoalBasedAgent(world.initial_knowledge())

    if args.watch:
        on_step = make_watcher(args.delay)
    else:
        print(world.render())
        on_step = None

    result = run_episode(world, agent, on_step)

    print()
    print(f"agent:   {args.agent} (seed {args.agent_seed})")
    print(f"score:   {result.score}")
    print(f"steps:   {result.steps}/{world.step_limit}")
    print(f"cleaned: {result.cleaned}/{result.total_dirt}")
    print("ended:   " + ("ran out of steps" if result.hit_limit else "all dirt cleaned"))


if __name__ == "__main__":
    main()
