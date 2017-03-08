class Overlay(object):

    def __init(self, graph):
        self._graph = graph

    def neighbors(self, system):
        return self._graph.neighbors(system)

    def security(self, system):
        return self._graph.security(system)


class AvoidanceOverlay(Overlay):

    def __init__(self, graph, avoidance_list):
        self._graph = graph
        self._avoidance_list = avoidance_list

    def update(self, avoidance_list):
        self._avoidance_list = avoidance_list

    def neighbors(self, system):
        neighbors = self._graph.neighbors(system)
        return [n for n in neighbors if n not in self._avoidance_list]


class ConnectionOverlay(Overlay):

    def __init__(self, graph, connections):
        self._graph = graph
        self._connections = connections

    def update(self, connections):
        self._connections = connections

    def neighbors(self, system):
        new_connections = [d for (s, d) in self._connections if s == system]
        return self._graph.neighbors(system) + new_connections
