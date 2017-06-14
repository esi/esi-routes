import os
import json

from esi import Error


def _load_starmap():
    """Load the starmap from static data."""

    static = os.environ.get("STATIC_DATA", os.path.realpath(
        os.path.dirname(__file__)))

    jump_map = os.path.join(static, "jumpmap.json")

    if not os.path.isfile(jump_map):
        raise RuntimeError("missing data: {}".format(jump_map))

    with open(jump_map, "r") as open_jump_map:
        # JSON doesn't allow int keys
        return {int(k): v for k, v in json.load(open_jump_map).items()}


class Graph(object):
    """Created once during app init, this is the default universe."""

    def __init__(self):
        """Hold reference to the default starmap."""

        self._starmap = _load_starmap()

    def neighbors(self, system):
        """Return a list of neighbors for a given system."""

        return self.get_system(system)['neighbors']

    def security(self, system):
        """Return the security level for a given system."""

        return self.get_system(system)['security']

    def get_system(self, system):
        """Return a dict with both neighbors and security for a system."""

        system_info = self._starmap.get(system)
        if system_info is None:
            raise Error(404, "System not found")
        return system_info
