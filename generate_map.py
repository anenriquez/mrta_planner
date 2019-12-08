from planner.planner import Planner


if __name__ == '__main__':
    map_file = 'planner/config/brsu.yaml'
    edge_info_path = '../ropod_rosbag_processing/ropod_rosbag_processing/angela/results/'
    min_n_runs = 1
    obstacle_interval = list(range(0, 3))

    planner = Planner()
    planner.generate_map(map_file, edge_info_path, min_n_runs, obstacle_interval)

    graph_json = planner.map_graph.to_json("planner/maps/brsu.json")

