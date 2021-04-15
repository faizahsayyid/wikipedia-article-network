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
import wikipedia_html_parsers

from wikigraph_copy import WikiGraph


class _WeightedVertex:
    """A vertex in a weighted Wikipedia link graph, used to represent a Wikipedia page.

    Same documentation as _Vertex from Part 1, except now neighbours is a dictionary mapping
    a neighbour vertex to the weight of the edge to from self to that neighbour.

    A weight between 2 vertices is the average of the frequency of the names in each webpage.

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
    class_id: str
    neighbours: dict[_WeightedVertex, int]

    def __init__(self, name: str, url: str) -> None:
        """Initialize a new vertex with the given page name and url.

        This vertex is initialized with no neighbours.
        """
        self.name = name
        self.url = url
        self.class_id = ''.join([str(ord(letter)) for letter in name])
        self.neighbours = {}

    def degree(self) -> int:
        """Return the degree of this vertex."""
        return len(self.neighbours)


class WeightedWikiGraph(WikiGraph):
    """A weighted graph used to represent a Wikipedia link network that keeps track of
    weights.

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

    # def get_all_vertices(self) -> set:
    #     """Return a set of all vertex page names in this graph.
    #     """
    #     return set(self._vertices.keys())
    #
    # def is_vertex_in_graph(self, name) -> bool:
    #     """Return whether <name> is a vertex in this graph"""
    #     return name in self._vertices
    #
    # def get_vertex(self, name) -> _Vertex:
    #     """Returns the vertex based on the given key"""
    #     return self._vertices[name]
    #
    # def get_class_id(self, name) -> str:
    #     """Returns the class id of a vertex"""
    #     return self._vertices[name].class_id
    #
    # def get_image(self, name) -> str:
    #     """Returns the page image"""
    #     return self._vertices[name].image

    def to_cytoscape(self) -> list[dict]:
        """Returns the list of graph data needed to display the graph in cytoscape"""
        cyto_elements = []
        for vertex in self._vertices:
            cyto_elements.append({'data': {'id': self._vertices[vertex].url,
                                           'label': self._vertices[vertex].name},
                                  'classes': self._vertices[vertex].class_id})
            for neighbour in self._vertices[vertex].neighbours:
                cyto_elements.append({'data': {'source': self._vertices[vertex].url,
                                               'target': neighbour.url,
                                               'label': self._vertices[vertex].name +
                                                        ' to ' + neighbour.name}})
        return cyto_elements


if __name__ == '__main__':
    import doctest

    doctest.testmod()