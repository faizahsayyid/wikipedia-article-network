"""CSC111 Winter 2021 Final Project: Wikipedia Graph Class
Module Description
===============================
[INSERT MODULE DESCRIPTION]
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


class _Vertex:
    """A vertex in a Wikipedia link graph, used to represent a Wikipedia page.

    Each vertex name is represented as a string.

    Instance Attributes:
        - name: The data stored in this vertex.
        - url: The URL of this webpage.
        - class_id: A numeric representation of the vertex name to be used as an id for node styling
        - neighbours: The vertices that are adjacent to this vertex.

    Representation Invariants:
        - self not in self.neighbours
        - all(self in u.neighbours for u in self.neighbours)
    """
    name: str
    url: str
    class_id: str
    neighbours: set[_Vertex]

    def __init__(self, name: str, url: str) -> None:
        """Initialize a new vertex with the given page name and url.

        This vertex is initialized with no neighbours.
        """
        self.name = name
        self.url = url
        self.class_id = ''.join([str(ord(letter)) for letter in name])
        self.neighbours = set()

    def degree(self) -> int:
        """Return the degree of this vertex."""
        return len(self.neighbours)


class WikiGraph:
    """A graph used to represent a Wikipedia pages network.
    """
    # Private Instance Attributes:
    #     - _vertices:
    #         A collection of the vertices contained in this graph.
    #         Maps item to _Vertex object.
    _vertices: dict[Any, _Vertex]

    def __init__(self) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        self._vertices = {}

    def add_vertex(self, name: str, url: str) -> None:
        """Add a vertex with the given page name and url to this graph.

        The new vertex is not adjacent to any other vertices.
        Do nothing if the given page is already in this graph.
        """
        if name not in self._vertices:
            self._vertices[name] = _Vertex(name, url)

    def add_edge(self, name1: Any, name2: Any) -> None:
        """Add an edge between the two vertices with the given names in this graph.

        Raise a ValueError if name1 or name2 do not appear as vertices in this graph.

        Preconditions:
            - name1 != name2
        """
        if name1 in self._vertices and name2 in self._vertices:
            v1 = self._vertices[name1]
            v2 = self._vertices[name2]

            v1.neighbours.add(v2)
            v2.neighbours.add(v1)
        else:
            raise ValueError

    def adjacent(self, name1: Any, name2: Any) -> bool:
        """Return whether name1 and name2 are adjacent vertices in this graph.

        Return False if name1 or name2 do not appear as vertices in this graph.
        """
        if name1 in self._vertices and name2 in self._vertices:
            v1 = self._vertices[name1]
            return any(v2.name == name2 for v2 in v1.neighbours)
        else:
            return False

    def get_neighbours(self, name: Any) -> set:
        """Return a set of the neighbours of the given page name.

        Note that the page *names* are returned, not the _Vertex objects themselves.

        Raise a ValueError if page name does not appear as a vertex in this graph.
        """
        if name in self._vertices:
            v = self._vertices[name]
            return {neighbour.name for neighbour in v.neighbours}
        else:
            raise ValueError

    def get_all_vertices(self) -> set:
        """Return a set of all vertex page names in this graph.
        """
        return set(self._vertices.keys())

    def is_vertex_in_graph(self, name) -> bool:
        """Return whether <name> is a vertex in this graph"""
        return name in self._vertices

    def get_vertex(self, name) -> _Vertex:
        """Returns the vertex based on the given key"""
        return self._vertices[name]

    def get_class_id(self, name) -> str:
        """Returns the class id of a vertex"""
        return self._vertices[name].class_id

    def to_cytoscape(self) -> list[dict]:
        """Returns the list of graph data needed to display the graph in cytoscape.

        Each node is represented as a dictionary, with the node's data containing an identifying
        id and label and it's classes containing it's class_id for custom styling in the graph.

        Each edge is also a dictionary, containing the source of the edge, target of the edge, and
        the label of the edge.
        """
        cyto_elements = []

        # Iterate through every vertex in the graph
        for vertex in self._vertices:

            # Add the vertex to the graph
            cyto_elements.append({'data': {'id': self._vertices[vertex].url,
                                           'label': self._vertices[vertex].name},
                                  'classes': self._vertices[vertex].class_id})

            # Add all of the vertex's edges
            for neighbour in self._vertices[vertex].neighbours:
                cyto_elements.append({'data': {'source': self._vertices[vertex].url,
                                               'target': neighbour.url,
                                               'label': self._vertices[vertex].name + ' to ' +
                                                        neighbour.name}})
        return cyto_elements


if __name__ == '__main__':
    import python_ta.contracts

    python_ta.contracts.check_all_contracts()

    import python_ta

    python_ta.check_all(config={
        'max-line-length': 100,
        'disable': ['E1136', 'E9999'],
        'max-nested-blocks': 4
    })
