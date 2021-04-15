"""CSC111 Winter 2021 Final Project: Building the WikiGraph

Module Description
===============================

This module contains function for building a WikiGraph and WeightedWikiGraph using
a breath-first-search algorithm.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of Faizah Sayyid, Tina Zhang,
Poorvi Sharma, and Courtney Amm (students at the University of Toronto St. George campus).
All forms of distribution of this code, whether as given or with any changes, are expressly
prohibited.

This file is Copyright (c) 2021 Faizah Sayyid, Tina Zhang, Poorvi Sharma, Courtney Amm.
"""
from typing import Any
from wikigraph import WikiGraph
from wikipedia_html_parsers import get_adjacent_urls, get_adjacent_urls_weighted, get_title
from weighted_wikigraph_class import WeightedWikiGraph


class _Queue:
    """A first-in-first-out (FIFO) queue of items.

    Stores data in a first-in, first-out order. When removing an item from the
    queue, the most recently-added item is the one that is removed.

    >>> q = _Queue()
    >>> q.is_empty()
    True
    >>> q.enqueue('hello')
    >>> q.is_empty()
    False
    >>> q.enqueue('goodbye')
    >>> q.dequeue()
    'hello'
    >>> q.dequeue()
    'goodbye'
    >>> q.is_empty()
    True
    """
    _items: list

    def __init__(self) -> None:
        """Initialize a new empty queue."""
        self._items = []

    def is_empty(self) -> bool:
        """Return whether this queue contains no items.
        """
        return self._items == []

    def enqueue(self, item: Any) -> None:
        """Add <item> to the back of this queue.
        """
        self._items.append(item)

    def dequeue(self) -> Any:
        """Remove and return the item at the front of this queue.

        Raise an EmptyQueueError if this queue is empty.
        """
        if self.is_empty():
            raise EmptyQueueError
        else:
            return self._items.pop(0)


class EmptyQueueError(Exception):
    """Exception raised when calling dequeue on an empty queue."""

    def __str__(self) -> str:
        """Return a string representation of this error."""
        return 'dequeue may not be called on an empty queue'


def build_wikigraph(starting_url: str, num_sources: int, sources_per_page: int) -> WikiGraph:
    """ Return a Graph with all the sources and the <starting_url> as its vertex.

    Find <num_sources> number of sources from the <starting_url> Wikipedia article.

    If one wikipedia article contains the link to another wikipedia article,
    then they are adjacent.

    NOTE: This function may not return <num_sources> in some cases since wikipedia may have
    deleted pages but not updated the links on its pages, or there just aren't that many
    links surrounding the <starting_url>.

    (Implemented with the Breadth-First-Search Algorithm)
    """
    # tells us which vertex we should next add to the graph
    q = _Queue()

    curr_url = starting_url

    # ACCUMULATOR visited keeps track of the vertices we have already visited to make
    # sure we don't enter an infinite loop
    visited = []

    # ACCUMULATOR wiki_graph_so_far builds up our wikigraph
    wiki_graph_so_far = WikiGraph()

    # ACCUMULATOR sources_found keeps track of the number of sources found
    sources_found = 0

    # Add initial article to queue, visited, and our wikigraph
    q.enqueue(curr_url)
    visited.append(curr_url)
    curr_name = get_title(curr_url)
    wiki_graph_so_far.add_vertex(curr_name, curr_url)

    # we will either stop when the queue is empty or, when we have found the
    # desired number of sources
    while not (q.is_empty() or sources_found >= num_sources):

        # Reassign curr_url to the next item in the queue
        curr_url = q.dequeue()
        curr_name = get_title(curr_url)

        # find the neighbouring links on the article for curr_url
        neighbours = get_adjacent_urls(curr_url)

        # Reset the counter the following while loop
        i = 0
        sources_found_per_page = 0

        # stop loop either when we've added all the neighbours or curr_url
        # or we found our desired number of sources
        while not (i >= len(neighbours) or sources_found >= num_sources
                   or sources_found_per_page >= sources_per_page):
            v_link = neighbours[i]
            v_name = get_title(v_link)
            i += 1

            # if the neighbour is not in visited, add it to the graph
            if v_link not in visited:
                q.enqueue(v_link)
                visited.append(v_link)

                if not wiki_graph_so_far.is_vertex_in_graph(v_name):
                    wiki_graph_so_far.add_vertex(v_name, v_link)
                    sources_found_per_page += 1
                    sources_found += 1

            wiki_graph_so_far.add_edge(curr_name, v_name)

    return wiki_graph_so_far


def build_weighted_wikigraph(starting_url: str, num_sources: int,
                             sources_per_page: int) -> WeightedWikiGraph:
    """ Return a Weighted Graph with all the sources and the <starting_url> as its vertex.

    Find <num_sources> number of sources from the <starting_url> Wikipedia article.

    If one wikipedia article contains the link to another wikipedia article,
    then they are adjacent.

    NOTE: This function may not return <num_sources> in some cases since wikipedia may have
    deleted pages but not updated the links on its pages, or there just aren't that many
    links surrounding the <starting_url>.

    (Implemented with the Breadth-First-Search Algorithm)
    """
    # tells us which vertex we should next add to the graph
    q = _Queue()

    curr_url = starting_url

    # ACCUMULATOR visited keeps track of the vertices we have already visited to make
    # sure we don't enter an infinite loop
    visited = []

    # ACCUMULATOR stores the edges to add to graph mapped to a list of frequencies
    # (collects the frequency of one articles name on the other article html code,
    # as well as the frequency of other articles name on that one article html code)
    edges_to_weights = {}

    # ACCUMULATOR wiki_graph_so_far builds up our wikigraph
    wiki_graph_so_far = WeightedWikiGraph()

    # ACCUMULATOR sources_found keeps track of the number of sources found
    sources_found = 0

    # Add initial article to queue, visited, and our wikigraph
    q.enqueue(curr_url)
    visited.append(curr_url)
    curr_name = get_title(curr_url)
    wiki_graph_so_far.add_vertex(curr_name, curr_url)

    # we will either stop when the queue is empty or, when we have found the
    # desired number of sources
    while not (q.is_empty() or sources_found >= num_sources):

        # Reassign curr_url to the next item in the queue
        curr_url = q.dequeue()
        curr_name = get_title(curr_url)

        # find the neighbouring links on the article for curr_url
        neighbours = get_adjacent_urls_weighted(curr_url)

        # Reset the counter the following while loop
        i = 0
        sources_found_per_page = 0

        # stop loop either when we've added all the neighbours or curr_url
        # or we found our desired number of sources
        while not (i >= len(neighbours) or sources_found >= num_sources
                   or sources_found_per_page >= sources_per_page):
            v, partial_weight = neighbours[i]
            v_link, v_name = v
            i += 1

            # if the neighbour is not in visited, add it to the graph
            if v_link not in visited:
                q.enqueue(v_link)
                visited.append(v_link)

                if not wiki_graph_so_far.is_vertex_in_graph(v_name):
                    wiki_graph_so_far.add_vertex(v_name, v_link)
                    sources_found_per_page += 1
                    sources_found += 1

            # add the edge and weight to edges_to_weights
            if (v_name, curr_name) in edges_to_weights:
                edges_to_weights[(v_name, curr_name)].append(partial_weight)
            else:
                edges_to_weights[(curr_name, v_name)] = [partial_weight]

    # add all the edges and weights to wiki_graph_so_far
    for edge in edges_to_weights:
        v1, v2 = edge
        weight = sum(edges_to_weights[edge]) / 2
        wiki_graph_so_far.add_edge(v1, v2, weight)

    return wiki_graph_so_far


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    import python_ta.contracts

    python_ta.contracts.check_all_contracts()

    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['wikigraph', 'wikipedia_html_parsers',
                          'weighted_wikigraph_class'],
        'allowed-io': [],
        'max-line-length': 100,
        'disable': ['E1136']
    })
