class Edge:
    def __init__(self, name, n_runs, mean, variance, max_n_obstacles):
        self.name = name
        self.n_runs = n_runs
        self.mean = mean
        self.variance = variance
        self.max_n_obstacles = max_n_obstacles

    def __add__(self, other):
        if self.name != other.name:
            name = self.name + '<->' + other.name
        else:
            name = self.name
        n_runs = self.n_runs + other.n_runs
        mean = self.mean + other.mean
        variance = self.variance + other.variance
        max_n_obstacles = max(self.max_n_obstacles, other.max_n_obstacles)
        return Edge(name, n_runs, mean, variance, max_n_obstacles)

    def to_dict(self):
        edge = dict()
        edge['name'] = self.name
        edge['n_runs'] = self.n_runs
        edge['mean'] = self.mean
        edge['variance'] = self.variance
        edge['max_n_obstacles'] = self.max_n_obstacles
        return edge

    @classmethod
    def from_dict(cls, edge_dict):
        name = edge_dict['name']
        n_runs = edge_dict['n_runs']
        mean = edge_dict['mean']
        variance = edge_dict['variance']
        max_n_obstacles = edge_dict['max_n_obstacles']
        return cls(name, n_runs, mean, variance,  max_n_obstacles)

