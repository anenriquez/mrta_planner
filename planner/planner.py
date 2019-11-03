import networkx as nx
from planner.utils.utils import load_yaml, get_pdf


class Planner:
    def __init__(self, map_file, pdf_path):

        map_info = load_yaml(map_file)
        nodes = map_info.get('nodes')
        edges = map_info.get('edges')

        self.map_graph = nx.Graph()
        self.add_nodes(nodes)
        self.add_edges(edges, pdf_path)

    def add_nodes(self, nodes_dict):
        for node, pose in nodes_dict.items():
            self.map_graph.add_node(node, pose=pose)

    def add_edges(self, edges_list, pdf_path):

        for edge in edges_list:
            edge_name = edge[0] + '_to_' + edge[1]
            pdf = get_pdf(pdf_path, edge_name)
            if pdf:
                mean = pdf.get('mean')
                standard_deviation = pdf.get('standard_deviation')
                self.map_graph.add_edge(edge[0], edge[1], weight=mean,
                                        mean=mean,
                                        standard_deviation=standard_deviation)
            else:
                self.map_graph.add_edge(edge[0], edge[1])

    def distance(self, waypoint_1, waypoint_2):
        x1, y1, z1 = self.map_graph.nodes[waypoint_1]['pose']
        x2, y2, z2 = self.map_graph.nodes[waypoint_2]['pose']

        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

    def get_path(self, waypoint_1, waypoint_2):
        return nx.astar_path(self.map_graph, waypoint_1, waypoint_2, self.distance)




