import networkx as nx
import numpy as np
from importlib_resources import open_text

from planner.map_graph import MapGraph
from planner.utils.utils import load_yaml


class Planner:
    def __init__(self, map_name=None, graph=None, **kwargs):
        if map_name:
            self.map_graph = self.load_map(map_name)
        elif graph:
            self.map_graph = MapGraph(graph)

    def generate_map(self, config_file, edge_info_path, min_n_runs, obstacle_interval, map_name):
        config = load_yaml(config_file)
        self.map_graph.generate_map(config, edge_info_path, min_n_runs, obstacle_interval, map_name)

    def load_map(self, map_name):
        json_file = open_text('planner.graphs', map_name + '.json').name
        return MapGraph.from_json(json_file)

    def distance(self, node_1, node_2):
        x1, y1, z1 = self.map_graph.nodes[node_1]['pose']
        x2, y2, z2 = self.map_graph.nodes[node_2]['pose']
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

    def get_path(self, location_1, location_2):
        return nx.astar_path(self.map_graph, location_1, location_2, self.distance)

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
        for edge in nx.utils.pairwise(path):
            mean = mean + self.map_graph.edges.get(edge, {}).get('mean', 1)
            variance = variance + self.map_graph.edges.get(edge, {}).get('variance', 0)

        return mean, variance
