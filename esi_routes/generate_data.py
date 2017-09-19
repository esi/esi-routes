"""This can recreate the jumpmap.json should the universe ever change."""


import time
import json
from concurrent.futures import ThreadPoolExecutor

from bravado.client import SwaggerClient


ESI = SwaggerClient.from_url("https://esi.tech.ccp.is/latest/swagger.json")


def retry_get(function, **params):
    """Retry the function return's `result` method until it succeeds."""

    while True:
        try:
            return function(**params).result()
        except Exception as error:
            print("Error: {!r}".format(error))
            time.sleep(0.1)


def system_get(system):
    """Get details for a single system."""

    system_details = retry_get(
        ESI.Universe.get_universe_systems_system_id,
        system_id=system,
    )

    this_system = {
        "neighbors": [],
        "security": system_details["security_status"],
    }

    for gate in system_details["stargates"]:
        gate_details = retry_get(
            ESI.Universe.get_universe_stargates_stargate_id,
            stargate_id=gate,
        )
        this_system["neighbors"].append(
            gate_details["destination"]["system_id"]
        )

    return system, this_system


def main():
    """Generate the jumpmap.json with ESI."""

    systems = {}
    all_systems = retry_get(ESI.Universe.get_universe_systems)
    num_systems = len(all_systems)
    complete = 0

    with ThreadPoolExecutor(max_workers=100) as executor:
        for future in executor.map(system_get, all_systems):
            complete += 1
            system, result = future
            systems[system] = result
            print("{}/{} systems complete".format(complete, num_systems))

    with open("jumpmap.json", "w") as openjumpmap:
        openjumpmap.write(json.dumps(systems))


if __name__ == "__main__":
    main()
