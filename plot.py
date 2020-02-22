import matplotlib.pyplot as plt
import networkx as nx
from planner.utils.utils import load_graph_from_file


def plot(graph, occ_grid, meta_data, pos='pose'):
    plt.rcParams['figure.figsize'] = [50, 50]
    ax = plt.axes()
    ax.imshow(occ_grid, cmap='gray', interpolation='none', origin='lower')
    resolution = meta_data.get('resolution')
    origin = meta_data.get('origin')
    ymax, xmax = occ_grid.shape

    def map_to_img(x, y):
        x_ = (x - origin[0]) / resolution
        y_ = ymax - ((y - origin[1]) / resolution)
        return [x_, y_]

    pose = nx.get_node_attributes(graph, pos)
    pos_ = {p: map_to_img(coord[0], coord[1]) for p, coord in pose.items()}

    nx.draw_networkx(graph, pos=pos_, node_size=1 / resolution, ax=ax)
    plt.savefig("planner/config/roadmap.png", dpi=300, bbox_inches='tight')
    plt.show()


if __name__ == '__main__':
    from matplotlib.pyplot import imread

    occ_grid = imread('planner/config/map.pgm', True)
    meta_data = nx.read_yaml('planner/config/map.yaml')

    G = load_graph_from_file('planner/graphs/brsu.json')
    plot(G, occ_grid, meta_data)
