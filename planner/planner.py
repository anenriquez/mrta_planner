import json

import networkx as nx
import numpy as np
from planner.utils.utils import load_yaml


class Planner:
    def __init__(self, map_file):

        map_info = load_yaml(map_file)
        nodes = map_info.get('nodes')
        edges = map_info.get('edges')
        self.map_graph = self.generate_map(nodes, edges)

    @staticmethod
    def generate_map(nodes, edges):
        # TODO: Only add edges that have a duration probability distribution
        map_graph = nx.Graph()
        for edge in edges:
            map_graph.add_edge(edge[0], edge[1])
            for node in edge:
                map_graph.add_node(node, pose=nodes[node])
        return map_graph

    def distance(self, node_1, node_2):
        x1, y1, z1 = self.map_graph.nodes[node_1]['pose']
        x2, y2, z2 = self.map_graph.nodes[node_2]['pose']
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

    def get_path(self, node_1, node_2):
        return nx.astar_path(self.map_graph, node_1, node_2, self.distance)

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

    def to_json(self, file_path):
        data = nx.node_link_data(self.map_graph)
        with open(file_path, 'w') as outfile:
            json.dump(data, outfile, indent=2)
        return data
