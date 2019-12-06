import json
import os

import networkx as nx
import numpy as np
from planner.utils.utils import load_yaml
from planner.edge import Edge


class Planner:
    def __init__(self, map_file, edge_info_path, min_n_runs, obstacle_interval):
        map_info = load_yaml(map_file)
        self.min_n_runs = min_n_runs
        self.obstacle_interval = obstacle_interval
        self.map_graph = self.generate_map(map_info,
                                           edge_info_path)

    def generate_map(self, map_info, edge_info_path):
        nodes = map_info.get('nodes')
        edges = map_info.get('edges')
        lane_connections = map_info.get('lane-connections')
        map_graph = nx.Graph()

        for edge in edges:
            if edge in lane_connections:
                map_graph = self.add_connection_lane(map_graph, edge, nodes)
            else:
                # Get info for edge in both directions
                undirected_edge_info = None
                edge_info_1 = self.get_edge_info(edge[0] + '_to_' + edge[1], edge_info_path)
                edge_info_2 = self.get_edge_info(edge[1] + '_to_' + edge[0], edge_info_path)
                if edge_info_1 and edge_info_2:
                    undirected_edge_info = edge_info_1 + edge_info_2
                elif edge_info_1 and edge_info_2 is None:
                    undirected_edge_info = edge_info_1
                elif edge_info_2 and edge_info_1 is None:
                    undirected_edge_info = edge_info_2

                if undirected_edge_info:
                    map_graph = self.add_edge(map_graph, edge, nodes, undirected_edge_info)

        return map_graph

    @staticmethod
    def add_connection_lane(map_graph, edge, nodes):
        map_graph.add_edge(edge[0], edge[1], connection_lane=True)
        for node in edge:
            map_graph.add_node(node, pose=nodes[node])
        return map_graph

    @staticmethod
    def get_edge_info(edge_name, edge_info_path):
        file_path = edge_info_path + edge_name + '.summary'
        if os.path.isfile(file_path):
            with open(file_path, 'r') as source_file:
                for line in source_file.readlines():
                    n_runs, mean, variance, n_obstacles = line.split(' ')
                    return Edge(edge_name, int(n_runs), float(mean), float(variance), int(n_obstacles))

    def add_edge(self, map_graph, edge, nodes, edge_info):
        if edge_info.max_n_obstacles in self.obstacle_interval \
                and edge_info.n_runs >= self.min_n_runs:

            # If edge already exists combine this edge_info with the previous one
            if map_graph.has_edge(edge[0], edge[1]):
                edge_previous_info = map_graph.get_edge_data(edge[0], edge[1])
                edge_info = Edge.from_dict(edge_previous_info) + edge_info

            map_graph.add_edge(edge[0], edge[1], **edge_info.to_dict())

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
