from collections import defaultdict


class Graph:
    def __init__(self):
        self.vertices = {} # map where keys are labels for node and value is the value stored in that node
        self.edges = defaultdict(list)

    def update_vertex(self, label, value):
        # adds new vertex if it doesn't exist, otherwise updates the value
        self.vertices[label] = value

    def add_edge(self, from_v, to_v):
        # don't create an edge if the vertices don't already exist
        if from_v not in self.vertices or to_v not in self.vertices:
            return
        
        self.edges[from_v].append(to_v)

        if to_v not in self.edges.keys():
            self.edges[to_v] = []

    def get_edges_for_vertex(self, label):
        return self.edges.get(label)

    # find the values of the vertices adjacent to a vertex
    def get_adj_values(self, label) -> list:
        adj = []

        if label in self.vertices:
            for vertex in self.edges[label]:
                if self.vertices[vertex]:
                    adj.append(self.vertices[vertex])

        return adj
