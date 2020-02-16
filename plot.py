import argparse

from planner.utils.utils import plot_map

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("map_name", type=str, help="Name of the map")
    args = parser.parse_args()
    path_to_map = "planner/maps/" + args.map_name + ".json"

    plot_map(path_to_map)
