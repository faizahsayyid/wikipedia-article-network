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
        - neighbours: The vertices that are adjacent to this vertex.

    Representation Invariants:
        - self not in self.neighbours
        - all(self in u.neighbours for u in self.neighbours)
    """
    name: str
    url: str
    neighbours: set[_Vertex]

    def __init__(self, name: str, url: str) -> None:
        """Initialize a new vertex with the given page name and url.

        This vertex is initialized with no neighbours.
        """
        self.name = name
        self.url = url
        self.neighbours = set()

    def degree(self) -> int:
        """Return the degree of this vertex."""
        return len(self.neighbours)

    def check_connected(self, target_item: Any, visited: set[_Vertex]) -> bool:
        """ Return whether this vertex is connected to a vertex corresponding to target_item
        by a path that DOES NOT use any vertex in visited

        Precondition:
            - self not in visited
        """
        if self.name == target_item:
            return True
        else:
            new_visited = visited.union({self})
            return any(u.check_connected(target_item, new_visited)
                       for u in self.neighbours
                       if u not in visited)


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

    def connected(self, item1: Any, item2: Any) -> bool:
        """Return whether item1 and item2 are connected vertices
        in this graph.

        Return False if item1 or item2 do not appear as vertices
        in this graph.
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            # v2 = self._vertices[item2]

            return v1.check_connected(item2, set())
        else:
            return False


# if __name__ == '__main__':
    # You can uncomment the following lines for code checking/debugging purposes.
    # However, we recommend commenting out these lines when working with the large
    # datasets, as checking representation invariants and preconditions greatly
    # increases the running time of the functions/methods.
    # import python_ta.contracts

    # python_ta.contracts.check_all_contracts()

    # import doctest
    #
    # doctest.testmod()
    #
    # import python_ta
    #
    # python_ta.check_all(config={
    #     'max-line-length': 100,
    #     'disable': ['E1136'],
    #     'extra-imports': ['csv', 'networkx'],
    #     'allowed-io': ['load_review_graph'],
    #     'max-nested-blocks': 4
    # })
