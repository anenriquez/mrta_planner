class Edge:
    def __init__(self, name, n_runs, mean, stdev, max_n_obstacles):
        self.name = name
        self.n_runs = n_runs
        self.mean = mean
        self.stdev = stdev
        self.variance = stdev**2
        self.max_n_obstacles = max_n_obstacles

    def __str__(self):
        return self.name + " n_runs: " + str(self.n_runs) + " mean: " \
               + str(self.mean) + " stdev: " + str(self.stdev) + " max_n_obstacles: " + str(self.max_n_obstacles)

    def __add__(self, other):
        if self.name != other.name:
            name = self.name + '<->' + other.name
        else:
            name = self.name

        n_runs = self.n_runs + other.n_runs

        # Weighted mean
        mean = ((self.n_runs * self.mean) + (other.n_runs * other.mean))/(self.n_runs + other.n_runs)

        # Combined standard deviation
        n = (self.n_runs - 1)*self.stdev**2 + (other.n_runs - 1)*other.stdev**2 + \
             self.n_runs*(self.mean - mean)**2 + other.n_runs*(other.mean - mean)**2
        d = self.n_runs + other.n_runs - 1
        stdev = (n/d)**0.5

        max_n_obstacles = max(self.max_n_obstacles, other.max_n_obstacles)

        return Edge(name, n_runs, mean, stdev, max_n_obstacles)

    def to_dict(self):
        edge = dict()
        edge['name'] = self.name
        edge['n_runs'] = self.n_runs
        edge['mean'] = self.mean
        edge['stdev'] = self.stdev
        edge['variance'] = self.variance
        edge['max_n_obstacles'] = self.max_n_obstacles
        return edge

    @classmethod
    def from_dict(cls, edge_dict):
        name = edge_dict['name']
        n_runs = edge_dict['n_runs']
        mean = edge_dict['mean']
        stdev = edge_dict['stdev']
        max_n_obstacles = edge_dict['max_n_obstacles']
        return cls(name, n_runs, mean, stdev,  max_n_obstacles)

