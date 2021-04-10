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
import networkx as nx
import random


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


class WikiGraph:
    """A graph used to represent a Wikipedia pages network.
    """
    # Private Instance Attributes:
    #     - _vertices:
    #         A collection of the vertices contained in this graph.
    #         Maps item to _Vertex object.
    vertices: dict[Any, _Vertex]

    def __init__(self) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        self.vertices = {}

    def add_vertex(self, name: str, url: str) -> None:
        """Add a vertex with the given page name and url to this graph.

        The new vertex is not adjacent to any other vertices.
        Do nothing if the given page is already in this graph.
        """
        if name not in self.vertices:
            self.vertices[url] = _Vertex(name, url)

    def add_edge(self, url1: Any, url2: Any) -> None:
        """Add an edge between the two vertices with the given names in this graph.

        Raise a ValueError if name1 or name2 do not appear as vertices in this graph.

        Preconditions:
            - name1 != name2
        """
        if url1 in self.vertices and url2 in self.vertices:
            v1 = self.vertices[url1]
            v2 = self.vertices[url2]

            v1.neighbours.add(v2)
            v2.neighbours.add(v1)
        else:
            raise ValueError

    def adjacent(self, url1: Any, url2: Any) -> bool:
        """Return whether name1 and name2 are adjacent vertices in this graph.

        Return False if name1 or name2 do not appear as vertices in this graph.
        """
        if url1 in self.vertices and url2 in self.vertices:
            v1 = self.vertices[url1]
            return any(v2.name == url2 for v2 in v1.neighbours)
        else:
            return False

    def get_neighbours(self, url: Any) -> set:
        """Return a set of the neighbours of the given page name.

        Note that the page *names* are returned, not the _Vertex objects themselves.

        Raise a ValueError if page name does not appear as a vertex in this graph.
        """
        if url in self.vertices:
            v = self.vertices[url]
            return {neighbour.name for neighbour in v.neighbours}
        else:
            raise ValueError

    def get_all_vertices(self) -> set:
        """Return a set of all vertex page names in this graph.
        """
        return set(self.vertices.keys())

    def to_networkx(self, max_vertices: int = 5000) -> nx.Graph:
        """Convert this graph into a networkx Graph.

        max_vertices specifies the maximum number of vertices that can appear in the graph.
        (This is necessary to limit the visualization output for large graphs.)

        Note that this method is provided for you, and you shouldn't change it.
        """
        graph_nx = nx.Graph()
        for v in self.vertices.values():
            graph_nx.add_node(v.name)

            for u in v.neighbours:
                if graph_nx.number_of_nodes() < max_vertices:
                    graph_nx.add_node(u.name)

                if u.name in graph_nx.nodes:
                    graph_nx.add_edge(v.name, u.name)

            if graph_nx.number_of_nodes() >= max_vertices:
                break

        return graph_nx

    def to_cytoscape(self) -> list[dict]:
        """Returns the list of graph data needed to display the graph in cytoscape"""
        cyto_elements = []
        for vertex in self.vertices:
            cyto_elements.append({'data': {'id': self.vertices[vertex].url,
                                           'label': self.vertices[vertex].name.replace('_', ' ')}})
            for neighbour in self.vertices[vertex].neighbours:
                cyto_elements.append({'data': {'source': self.vertices[vertex].url, 'target': neighbour.url,
                                               'label': self.vertices[vertex].name + ' to ' + neighbour.name}})
        return cyto_elements

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
