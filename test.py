from planner.planner import Planner
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('source', type=str, help='Name of source node')
    parser.add_argument('destination', type=str, help='Name of destination node')
    args = parser.parse_args()

    map_file = 'planner/config/brsu.yaml'
    edge_info_path = '../ropod_rosbag_processing/ropod_rosbag_processing/angela/results/'
    min_n_runs = 1
    obstacle_interval = list(range(0, 3))

    planner = Planner(map_file, edge_info_path, min_n_runs, obstacle_interval)

    path = planner.get_path(args.source, args.destination)

    print("Path from {} to {}: {}".format(args.source, args.destination, path))

    mean, variance = planner.get_estimated_duration(path)
    print("mean: ", mean)
    print("variance: ", variance)

    graph_json = planner.to_json("brsu.json")


