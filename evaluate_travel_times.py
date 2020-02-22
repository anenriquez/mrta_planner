import numpy as np
from planner.utils.utils import load_graph_from_file

if __name__ == '__main__':
    G = load_graph_from_file('planner/graphs/brsu.json')
    G_obs = load_graph_from_file('planner/graphs/brsu_obstacles.json')

    max_n_obstacles = -np.inf
    greater_diff = -np.inf
    edge_greater_diff = None
    n_edges = 0

    for (i, j, data) in G.edges.data():
        if G_obs.has_edge(i, j) and "connection_lane" not in data.keys():
            data_obstacles = G_obs.get_edge_data(i, j)

            mean_travel_time_without_obstacles = data.get("mean")
            mean_travel_time_with_obstacles = data_obstacles.get("mean")

            if data_obstacles.get("max_n_obstacles") > max_n_obstacles:
                max_n_obstacles = data_obstacles.get("max_n_obstacles")

            if mean_travel_time_without_obstacles > mean_travel_time_with_obstacles:
                diff = mean_travel_time_without_obstacles - mean_travel_time_with_obstacles
                n_edges += 1
                if diff > greater_diff:
                    greater_diff = diff
                    edge_greater_diff = data.get("name")

                print(data.get("name"))
                print("without obstacles: ", mean_travel_time_without_obstacles)
                print("n_runs: ", data.get("n_runs"))
                print("with obstacles: ", mean_travel_time_with_obstacles)
                print("n_runs: ", data_obstacles.get("n_runs"))
                print("max_n_obstacles: ", data_obstacles.get("max_n_obstacles"))
                print("diff: ", diff)
                print("\n")

    print("n_edges: ", n_edges)
    print("max_n_obstacles: ", max_n_obstacles)
    print("Greater diff: ", greater_diff)
    print("Edge: ", edge_greater_diff)
