
from collections import deque

from fibonacci_heap_mod import Fibonacci_heap


__all__ = ['dijkstra']


def prefer_shortest(graph, next_sys):
    """Return the weight to jump to the next system.

    By setting weights to nullsec or lowsec systems high, we can
    search for safest route.

    Returning a constant such as 1.0 allows us to look for the
    fastest route, but it does makes the Dijkstra beeing effectively a BFS."""
    return 1.0


def prefer_safest(graph, next_sys):
    if graph.security(next_sys) < 0.45:  # low/null
        return 50000.0
    else:
        return 1.0


def prefer_less_safe(graph, next_sys):
    if graph.security(next_sys) >= 0.45:  # high sec
        return 50000.0
    else:
        return 1.0


def path(prev, start, end):
    """Traverse the `prev`-map backwards and obtain."""
    s = deque([])
    u = end
    while u != start:
        s.appendleft(u)
        # route does not exist
        if u not in prev:
            return []
        u = prev[u]

    s.appendleft(start)
    return list(s)


cost_fn = {
    "secure": prefer_safest,
    "insecure": prefer_less_safe,
    "shortest": prefer_shortest,
}


def dijkstra(graph, start, end, flag="shortest"):
    """Given a graph, calculates the shortest path between a
    start- and an end-vertex.

    `graph` needs to support at least neighbors(n) which returns a list of new
    nodes and weight(a,b) returning a float value. Smaller weights are
    preferred by the algorithm."""
    prev = {}
    costs = {}
    entry = {}

    remaining = set([end])

    weight_fn = cost_fn[flag]
    costs[start] = 0.0

    q = Fibonacci_heap()
    entry[start] = q.enqueue(start, 0.0)
    while q:
        u = q.dequeue_min().get_value()

        if u in remaining:
            remaining.remove(u)

        # Early exit as we found everything
        if not remaining:
            break

        for v in graph.neighbors(u):
            if v in prev:  # we have already seen this vertex
                continue

            new_cost = costs[u] + weight_fn(graph, v)
            if v in costs and new_cost < costs[v]:
                costs[v] = new_cost
                prev[v] = u
                q.decrease_key(entry[v], costs[v])
            if v not in costs:
                costs[v] = new_cost
                prev[v] = u
                entry[v] = q.enqueue(v, costs[v])

    return path(prev, start, end)
