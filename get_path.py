import argparse

from planner.planner import Planner

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('source', type=str, help='Name of source node')
    parser.add_argument('destination', type=str, help='Name of destination node')
    args = parser.parse_args()

    planner = Planner('brsu')

    path = planner.get_path(args.source, args.destination)

    print("Path from {} to {}: {}".format(args.source, args.destination, path))

    mean, variance = planner.get_estimated_duration(path)
    print("mean: ", mean)
    print("variance: ", variance)
