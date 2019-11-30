from planner.planner import Planner
from planner.utils.utils import  plot_map


if __name__ == '__main__':
    map_file = 'planner/config/brsu.yaml'
    pdf_path = '../ropod_rosbag_processing/ropod_rosbag_processing/angela/'

    planner = Planner(map_file)
    min_distance, min_edge = planner.get_min_distance()
    print("minimal distance: ", min_distance)
    print("minimal edge: ", min_edge)

    source = 'Pose_220'
    destination = 'Pose_43'

    path = planner.get_path(source, destination)

    print("Path from {} to {}: {}".format(source, destination, path))

    graph_json = planner.to_json("brsu.json")
    plot_map("brsu.json")


