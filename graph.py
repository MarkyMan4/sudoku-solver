from collections import defaultdict


class Graph:
    def __init__(self):
        self.graph = defaultdict(list)

    def add_edge(self, from_v, to_v):
        self.graph[from_v].append(to_v)

        if to_v not in self.graph.keys():
            self.graph[to_v] = []

    def get_verticies(self):
        return list(self.graph.keys())
