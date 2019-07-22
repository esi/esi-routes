"""This can recreate the jumpmap.json should the universe ever change."""


import time
import json
from concurrent.futures import ThreadPoolExecutor

try:
    from bravado.requests_client import RequestsClient
    from bravado.client import SwaggerClient
except ImportError:
    print("You need to install the generate extras to use this")
else:
    ESI = SwaggerClient.from_url(
        "https://esi.evetech.net/latest/swagger.json",
        http_client=RequestsClient(),
        config={
            "validate_swagger_spec": False,
            "validate_requests": False,
            "validate_responses": False,
            "use_models": False,
            "include_missing_properties": False,
        }
    )


def retry_get(function, **params):
    """Retry the function return's `result` method until it succeeds."""

    for _ in range(3):
        try:
            return function(**params).result()
        except Exception as error:  # pylint: disable=broad-except
            print("Error: {}".format(
                error.response.text if  # pylint: disable=no-member
                getattr(error, "response", None) else
                repr(error)
            ))
            time.sleep(0.1)


def system_get(system):
    """Get details for a single system."""

    system_details = retry_get(
        ESI.Universe.get_universe_systems_system_id,
        system_id=system,
    )

    if system_details is None:
        return system, None

    this_system = {
        "neighbors": [],
        "security": system_details["security_status"],
    }

    for gate in system_details.get("stargates", []):
        gate_details = retry_get(
            ESI.Universe.get_universe_stargates_stargate_id,
            stargate_id=gate,
        )

        if gate_details is None:  # this shouldn't happen
            print("Warning: failed to lookup gate {} in system {}".format(
                gate,
                system,
            ))
            return system, None

        this_system["neighbors"].append(
            gate_details["destination"]["system_id"]
        )

    return system, this_system


def main():
    """Generate the jumpmap.json with ESI."""

    try:
        all_systems = retry_get(ESI.Universe.get_universe_systems)
    except NameError:
        raise SystemExit(1)

    if all_systems is None:
        raise SystemExit(1)

    num_systems = len(all_systems)
    complete = 0
    systems = {}
    failed_systems = []
    with ThreadPoolExecutor(max_workers=100) as executor:
        for future in executor.map(system_get, all_systems):
            complete += 1
            system, result = future
            if result is None:
                failed_systems.append(system)
            else:
                systems[system] = result
            print("{}/{} systems complete".format(complete, num_systems))

    with open("jumpmap.json", "w") as openjumpmap:
        openjumpmap.write(json.dumps(systems, indent=4, sort_keys=True))

    print("updated jumpmap.json")

    if failed_systems:
        print("Warning: the following system_ids failed: {}".format(
            ", ".join(str(x) for x in failed_systems)
        ))


if __name__ == "__main__":
    main()
