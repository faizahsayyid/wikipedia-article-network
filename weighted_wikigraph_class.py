"""CSC111 Winter 2021 Final Project: Weighted Wikipedia Graph Class

Module Description
===============================

This module contains the WeightedWikiGraph class, which is graph used to represent a
network of wikipedia articles.

Each vertex in the graph represents a Wikipedia page, and an edge exist between
two vertices v1 and v2 if and only if v1 contains a link to v2 or v2 contains a link
to v1.

Each edge {v1, v2} contains a weight based on the average between the number of times
v1.name appears in the html code of v2 and the number of times v2.name appears in the
html code of v1.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of Faizah Sayyid, Tina Zhang,
Poorvi Sharma, and Courtney Amm (students at the University of Toronto St. George campus).
All forms of distribution of this code, whether as given or with any changes, are expressly
prohibited.
This file is Copyright (c) 2021 Faizah Sayyid, Tina Zhang, Poorvi Sharma, Courtney Amm.
"""
from __future__ import annotations
from typing import Any

from wikigraph import WikiGraph


class _WeightedVertex:
    """A vertex in a weighted Wikipedia link graph, used to represent a Wikipedia page.

    Each edge {v1, v2} contains a weight based on the average between the number of times
    v1.name appears in the html code of v2 and the number of times v2.name appears in the
    html code of v1.

    Instance Attributes:
        - name: The data stored in this vertex.
        - url: The URL of this webpage.
        - neighbours: The vertices that are adjacent to this vertex, and their corresponding
            edge weights.

    Representation Invariants:
        - self not in self.neighbours
        - all(self in u.neighbours for u in self.neighbours)
    """
    name: Any
    url: str
    neighbours: dict[_WeightedVertex, int]

    def __init__(self, name: str, url: str) -> None:
        """Initialize a new vertex with the given page name and url.

        This vertex is initialized with no neighbours.
        """
        self.name = name
        self.url = url
        self.neighbours = {}

    def degree(self) -> int:
        """Return the degree of this vertex."""
        return len(self.neighbours)


class WeightedWikiGraph(WikiGraph):
    """A weighted graph used to represent a Wikipedia link network that keeps track of
    weights.

    Each vertex in the graph represents a Wikipedia page, and an edge exist between
    two vertices v1 and v2 if and only if v1 contains a link to v2 or v2 contains a link
    to v1.

    Each edge {v1, v2} contains a weight based on the average between the number of times
    v1.name appears in the html code of v2 and the number of times v2.name appears in the
    html code of v1

    Note that this is a subclass of the WikiGraph class, and so inherits any methods
    from that class that aren't overridden here.
    """
    # Private Instance Attributes:
    #     - _vertices:
    #         A collection of the vertices contained in this graph.
    #         Maps item to _WeightedVertex object.
    _vertices: dict[Any, _WeightedVertex]

    def __init__(self) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        self._vertices = {}

        # This call isn't necessary, except to satisfy PythonTA.
        WikiGraph.__init__(self)

    def add_vertex(self, name: Any, url: str) -> None:
        """Add a vertex with the given name to this graph.

        The new vertex is not adjacent to any other vertices.
        Do nothing if the given item is already in this graph.
        """
        if name not in self._vertices:
            self._vertices[name] = _WeightedVertex(name, url)

    def add_edge(self, name1: Any, name2: Any, weight: float = 1.0) -> None:
        """Add an edge between the two vertices with the given items in this graph,
        with the given weight.

        Raise a ValueError if name1 or name2 do not appear as vertices in this graph.

        Preconditions:
            - name1 != name2
        """
        if name1 in self._vertices and name2 in self._vertices:
            v1 = self._vertices[name1]
            v2 = self._vertices[name2]

            # Add the new edge
            v1.neighbours[v2] = weight
            v2.neighbours[v1] = weight
        else:
            # We didn't find an existing vertex for both items.
            raise ValueError

    def get_neighbours(self, name: Any) -> set:
        """Return a set of the neighbours of the given page name.

        Note that the page *names* are returned, not the _Vertex objects themselves.

        Raise a ValueError if page name does not appear as a vertex in this graph.
        """
        if name in self._vertices:
            v = self._vertices[name]
            return {(neighbour.name, v.neighbours[neighbour]) for neighbour in v.neighbours}
        else:
            raise ValueError


if __name__ == '__main__':
    import python_ta.contracts

    python_ta.contracts.check_all_contracts()

    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['wikigraph'],
        'allowed-io': [],
        'max-line-length': 100,
        'disable': ['E1136', 'W0221']
    })
