import networkx as nx
import numpy as np
from planner.map_graph import MapGraph
from planner.utils.utils import load_yaml
from importlib_resources import open_text


class Planner:
    def __init__(self, map_name, load_map=True, **kwargs):
        self.map_graph = MapGraph(map_name)
        self.map_name = map_name
        if load_map:
            self.load_map()

    def generate_map(self, config_file, edge_info_path, min_n_runs, obstacle_interval):
        config = load_yaml(config_file)
        self.map_graph.generate_map(config, edge_info_path, min_n_runs, obstacle_interval)

    def load_map(self):
        json_file = open_text('planner.graphs', self.map_name + '.json').name
        self.map_graph = self.map_graph.from_json(json_file, self.map_name)

    def distance(self, node_1, node_2):
        x1, y1, z1 = self.map_graph.nodes[node_1]['pose']
        x2, y2, z2 = self.map_graph.nodes[node_2]['pose']
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

    def get_path(self, node_1, node_2):
        return nx.astar_path(self.map_graph, node_1, node_2, self.distance)

    def get_node(self, x, y):
        poses = nx.get_node_attributes(self.map_graph, 'pose')
        for node, pose in poses.items():
            if pose == [x, y, 0]:
                return node

    def get_pose(self, node_name):
        for node_id, data in self.map_graph.nodes(data=True):
            if node_id == node_name:
                return data["pose"]

    def get_min_distance(self):
        """ Returns the minimal distance between all edges and the edge name
        with the minimal distance
        """
        min_distance = np.inf
        min_edge = None
        for edge in self.map_graph.edges():
            distance = self.distance(edge[0], edge[1])
            if distance < min_distance:
                min_distance = distance
                min_edge = edge
        return min_distance, min_edge

    def get_estimated_duration(self, path):
        """ Returns the estimated duration to go from the first to the last location
        of a given path
        args:
            path (list): list of nodes
        return:
            mean (float)
            variance (float)
        """
        mean = 0
        variance = 0
        for i in range(0, len(path)-1):
            edge_data = self.map_graph.get_edge_data(path[i], path[i+1])
            if edge_data.get('connection_lane'):
                # No experimental info for this edge, add a duration of 1 unit with no variance
                mean += 1
            else:
                mean += edge_data.get('mean')
                variance += edge_data.get('variance')

        return mean, variance

