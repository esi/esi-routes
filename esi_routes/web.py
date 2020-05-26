"""ESI web handler(s)."""


import esi

from esi_routes.graph import Graph
from esi_routes.dijkstra import dijkstra
from esi_routes.overlay import AvoidanceOverlay
from esi_routes.overlay import ConnectionOverlay


DEFAULT_UNIVERSE = Graph()


@esi.endpoint(versions=["latest", "legacy", "dev", "v1"], cached=86400)
def route_get_v1(origin, destination, ctx):
    """/route/{origin}/{destination}/:
    get:
      description: Get the systems between origin and destination
      summary: Get route
      tags:
        - routes

      parameters:
        - name: origin
          in: path
          description: origin solar system ID
          type: integer
          format: int32
          required: true

        - name: destination
          in: path
          description: destination solar system ID
          type: integer
          format: int32
          required: true

        - name: avoid
          in: query
          description: avoid solar system ID(s)
          type: array
          maxItems: 100
          uniqueItems: true
          items:
            type: integer
            format: int32

        - name: connections
          in: query
          type: array
          description: connected solar system pairs
          maxItems: 300
          uniqueItems: true
          items:
            type: array
            minItems: 2
            maxItems: 2
            uniqueItems: true
            collectionFormat: pipes
            items:
              type: integer
              format: int32

        - name: flag
          in: query
          description: route security preference
          default: shortest
          type: string
          enum:
            - shortest
            - secure
            - insecure

      responses:
        200:
          description: Solar systems in route from origin to destination
          examples:
            application/json:
              - 30002771
              - 30002770
              - 30002769
              - 30002772

          schema:
            type: array
            maxItems: 1000
            description: Solar systems in route
            items:
              description: Solar system in route
              type: integer
              format: int32
              title: Solar system ID

        404:
          description: No route found
    """

    systems = dijkstra(
        ConnectionOverlay(
            AvoidanceOverlay(DEFAULT_UNIVERSE, ctx.args.get("avoid", [])),
            ctx.args.get("connections", []),
        ),
        origin,
        destination,
        flag=ctx.args["flag"],
    )

    if not systems:
        raise esi.Error(404, "No route found")

    return systems
