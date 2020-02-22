import yaml
import networkx as nx
import json
import numpy as np
import matplotlib.pyplot as plt


def load_yaml(file):
    """ Reads a yaml file and returns a dictionary with its contents

    :param file: file to load
    :return: data as dict()
    """
    with open(file, 'r') as file:
        data = yaml.safe_load(file)
    return data


def load_graph_from_file(json_file):
    with open(json_file) as file_:
        data = json.load(file_)
    graph = nx.node_link_graph(data)
    return graph


def plot_map(map_file):
    with open(map_file) as json_file:
        data = json.load(json_file)

    map_ = nx.node_link_graph(data)
    poses = nx.get_node_attributes(map_, 'pose')

    for node, p in poses.items():
        poses[node] = np.asarray(p[:2])

    nx.draw(map_, poses, with_labels=True)
    plt.show()


def get_pdf(path, edge_name):
    pdf_file = path + edge_name + '/pdf_file.yaml'
    try:
        pdf = load_yaml(pdf_file)
        return pdf
    except FileNotFoundError:
        print("File {} does not exist".format(pdf_file))


