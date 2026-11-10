"""P1: Agent simulator. Run with: python -m p01_agents.main"""
import argparse
from . import Map as mp

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--map", help="load the map file you want to test")
    parser.add_argument("--size", type=int, help="generate a nxn map with size")
    parser.add_argument("--seed", type=int, help="generate a map from a seed")
    parser.add_argument("--walls", type=float, help="wall density")
    parser.add_argument("--dirt", type=float, help="dirt density")
    args = parser.parse_args()

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
    
    world_map.displayMap()


if __name__ == "__main__":
    main()
