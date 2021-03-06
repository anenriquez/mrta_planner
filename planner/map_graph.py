import json
import os

import networkx as nx
from planner.edge import Edge
from networkx.readwrite import json_graph


class MapGraph(nx.Graph):
    def __init__(self):
        super().__init__()

    def generate_map(self, config, edge_info_path, min_n_runs, obstacle_interval, map_name):
        nodes = config.get('nodes')
        edges = config.get('edges')
        lane_connections = config.get('lane-connections')
        goals = config.get('goals')
        self.add_meta_info(min_n_runs, obstacle_interval, goals)

        for edge in edges:
            if edge in lane_connections:
                self.add_connection_lane(edge, nodes)
            else:
                # Get info for edge in both directions
                undirected_edge_info = None
                edge_info_1 = self.get_edge_info(str(edge[0]) + '_to_' + str(edge[1]), edge_info_path)
                edge_info_2 = self.get_edge_info(str(edge[1]) + '_to_' + str(edge[0]), edge_info_path)
                if edge_info_1 and edge_info_2:
                    undirected_edge_info = edge_info_1 + edge_info_2
                elif edge_info_1 and edge_info_2 is None:
                    undirected_edge_info = edge_info_1
                elif edge_info_2 and edge_info_1 is None:
                    undirected_edge_info = edge_info_2

                if undirected_edge_info:
                    self.add_undirected_edge(edge, nodes, undirected_edge_info)

        self.to_json("planner/graphs/" + map_name + ".json")

    def add_meta_info(self, min_n_runs, obstacle_interval, goals):
        self.graph['min_n_runs'] = min_n_runs
        self.graph['obstacle_interval'] = obstacle_interval
        self.graph['goals'] = goals

    def add_connection_lane(self, edge, nodes):
        self.add_edge(edge[0], edge[1], connection_lane=True)
        for node in edge:
            self.add_node(node, pose=nodes[node])

    def get_edge_info(self, edge_name, edge_info_path):
        # Each edge has a summary file which can contain several lines, one per max_n_obstacles
        file_path = edge_info_path + edge_name + '.summary'
        if os.path.isfile(file_path):
            edge = None
            with open(file_path, 'r') as source_file:
                for line in source_file.readlines():
                    n_runs, mean, stdev, max_n_obstacles = line.split(' ')

                    if int(max_n_obstacles) in self.graph['obstacle_interval']:
                        if edge is None:
                            edge = Edge(edge_name, int(n_runs), float(mean), float(stdev), int(max_n_obstacles))
                        else:
                            edge = edge + Edge(edge_name, int(n_runs), float(mean), float(stdev), int(max_n_obstacles))
            return edge
        else:
            print("File with edge info for edge {} does not exist".format(edge_name))

    def add_undirected_edge(self, edge, nodes, edge_info):
        if edge_info.n_runs >= self.graph['min_n_runs']:

            # If edge already exists combine this edge_info with the previous one
            if self.has_edge(edge[0], edge[1]):
                print("Edge already exists: ", edge_info)
                edge_previous_info = self.get_edge_data(edge[0], edge[1])
                edge_info = Edge.from_dict(edge_previous_info) + edge_info

            self.add_edge(edge[0], edge[1], **edge_info.to_dict())

            for node in edge:
                self.add_node(node, pose=nodes[node])

    def to_json(self, file_path):
        data = nx.node_link_data(self)
        with open(file_path, 'w') as outfile:
            json.dump(data, outfile, indent=2)
        return data

    @classmethod
    def from_json(cls, json_file):
        map_graph = cls()
        with open(json_file) as infile:
            json_dict = json.load(infile)

        stored_graph = json_graph.node_link_graph(json_dict)
        map_graph.add_nodes_from(stored_graph.nodes(data=True))
        map_graph.add_edges_from(stored_graph.edges(data=True))
        map_graph.graph = stored_graph.graph

        return map_graph
