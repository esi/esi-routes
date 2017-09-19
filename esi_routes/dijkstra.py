"""Dijkstra algorithm implementation."""


from collections import deque

from fibonacci_heap_mod import Fibonacci_heap


__all__ = ['dijkstra']


def prefer_shortest(*_):
    """Return the weight to jump to the next system.

    By setting weights to nullsec or lowsec systems high, we can
    search for safest route.

    Returning a constant such as 1.0 allows us to look for the
    fastest route, but it does makes the Dijkstra beeing effectively a BFS.
    """

    return 1.0


def prefer_safest(graph, next_sys):
    """Return a weight for prefering the safest route."""

    if graph.security(next_sys) < 0.45:  # low/null
        return 50000.0

    return 1.0


def prefer_less_safe(graph, next_sys):
    """Return a weight for prefering the less safe route."""

    if graph.security(next_sys) >= 0.45:  # high sec
        return 50000.0

    return 1.0


def path(prev, start, end):
    """Traverse the `prev`-map backwards and obtain."""

    queue = deque([])
    system = end
    while system != start:
        queue.appendleft(system)
        # route does not exist
        if system not in prev:
            return []
        system = prev[system]

    queue.appendleft(start)
    return list(queue)


COST_FN = {
    "secure": prefer_safest,
    "insecure": prefer_less_safe,
    "shortest": prefer_shortest,
}


def dijkstra(graph, start, end, flag="shortest"):
    """Calculate the shortest path between a start- and an end-vertex.

    `graph` needs to support at least neighbors(n) which returns a list of new
    nodes and weight(a,b) returning a float value. Smaller weights are
    preferred by the algorithm.
    """

    prev = {}
    costs = {}
    entry = {}

    remaining = set([end])

    weight_fn = COST_FN[flag]
    costs[start] = 0.0

    queue = Fibonacci_heap()
    entry[start] = queue.enqueue(start, 0.0)
    while queue:
        system = queue.dequeue_min().get_value()

        if system in remaining:
            remaining.remove(system)

        # Early exit as we found everything
        if not remaining:
            break

        for neighbor in graph.neighbors(system):
            if neighbor in prev:  # we have already seen this neighbor
                continue

            new_cost = costs[system] + weight_fn(graph, neighbor)
            if neighbor in costs and new_cost < costs[neighbor]:
                costs[neighbor] = new_cost
                prev[neighbor] = system
                queue.decrease_key(entry[neighbor], costs[neighbor])
            if neighbor not in costs:
                costs[neighbor] = new_cost
                prev[neighbor] = system
                entry[neighbor] = queue.enqueue(neighbor, costs[neighbor])

    return path(prev, start, end)
