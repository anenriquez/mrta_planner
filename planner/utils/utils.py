import yaml


def load_yaml(file):
    """ Reads a yaml file and returns a dictionary with its contents

    :param file: file to load
    :return: data as dict()
    """
    with open(file, 'r') as file:
        data = yaml.safe_load(file)
    return data


def get_pdf(path, edge_name):
    pdf_file = path + edge_name + '/pdf_file.yaml'
    try:
        pdf = load_yaml(pdf_file)
        return pdf
    except FileNotFoundError:
        print("File {} does not exist".format(pdf_file))
