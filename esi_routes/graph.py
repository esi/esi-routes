import os
import json

from esi import Error


def _load_starmap():
    """Loads the starmap from static data."""

    static = os.environ.get("STATIC_DATA", os.path.realpath(
        os.path.dirname(__file__)))

    jump_map = os.path.join(static, "jumpmap.json")

    if not os.path.isfile(jump_map):
        raise RuntimeError("missing data: {}".format(jump_map))

    with open(jump_map, "r") as open_jump_map:
        # JSON doesn't allow int keys
        return {int(k): v for k, v in json.load(open_jump_map).items()}


class GraphLoader(object):
    """Loads the graph then holds it in memory."""

    @staticmethod
    def load_starmap():
        if not hasattr(GraphLoader, "_graph"):
            GraphLoader._graph = _load_starmap()
        return GraphLoader._graph


class Graph(object):
    def __init__(self, starmap):
        self._starmap = starmap

    def neighbors(self, system):
        return self.get_system(system)['neighbors']

    def security(self, system):
        return self.get_system(system)['security']

    def get_system(self, system):
        system_info = self._starmap.get(system)
        if system_info is None:
            raise Error(404, "System not found")
        return system_info
