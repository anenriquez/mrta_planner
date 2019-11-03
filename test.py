from planner.planner import Planner


if __name__ == '__main__':
    map_file = 'planner/config/brsu.yaml'
    pdf_path = '../ropod_rosbag_processing/ropod_rosbag_processing/angela/'

    planner = Planner(map_file, pdf_path)

    source = 'c064'
    destination = 'main_entrance'

    path = planner.get_path(source, destination)

    print("Path from {} to {}: {}".format(source, destination, path))

