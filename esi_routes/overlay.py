"""User-supplied details to overlay on top of Graph objects."""


class Overlay(object):
    """Base class for both Avoidance and Connection overlays."""

    def __init__(self, graph):
        """Initialize with the default universe Graph object."""

        self._graph = graph

    def neighbors(self, system):
        """Return neighbors from the overlayed universe."""

        return self._graph.neighbors(system)

    def security(self, system):
        """Return the security of a system in the overlayed universe."""

        return self._graph.security(system)


class AvoidanceOverlay(Overlay):
    """Overlay the default universe with systems to avoid."""

    def __init__(self, graph, avoidance_list):
        """Initialize with the default universe Graph and a list of systems."""

        super(AvoidanceOverlay, self).__init__(graph)
        self._avoidance_list = avoidance_list

    def update(self, avoidance_list):
        """Update/replace the avoided systems list."""

        self._avoidance_list = avoidance_list

    def neighbors(self, system):
        """Return non-avoided neighbors for a given system."""

        neighbors = self._graph.neighbors(system)
        return [n for n in neighbors if n not in self._avoidance_list]


class ConnectionOverlay(Overlay):
    """Overlay the default universe with another set of connections.

    The connections arg is a list of 2 item long tuples [(source, dest)].
    """

    def __init__(self, graph, connections):
        """Create a new connection overlay object."""

        super(ConnectionOverlay, self).__init__(graph)
        self._connections = connections

    def update(self, connections):
        """Update/replace the nested connections list."""

        self._connections = connections

    def neighbors(self, system):
        """Return neighbors for a given system with overlayed connections."""

        new_connections = [d for (s, d) in self._connections if s == system]
        return self._graph.neighbors(system) + new_connections
