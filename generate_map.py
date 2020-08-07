from planner.planner import Planner
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("map_name", type=str, help="Name of the map")
    parser.add_argument("min_n_runs", type=int, help="Minimum number of runs per edge")
    parser.add_argument("min_n_obstacles", type=int, help="Minimum number of obstacles per edge")
    parser.add_argument("max_n_obstacles", type=int, help="Maximum number of obstacles per edge")

    args = parser.parse_args()
    obstacle_interval = list(range(args.min_n_obstacles, args.max_n_obstacles + 1))

    print("obstacle interval: ", obstacle_interval)

    config_file = 'planner/config/config.yaml'
    edge_info_path = '../ropod_rosbag_processing/ropod_rosbag_processing/angela/results/'

    planner = Planner()
    planner.generate_map(config_file, edge_info_path, args.min_n_runs, obstacle_interval, args.map_name)

