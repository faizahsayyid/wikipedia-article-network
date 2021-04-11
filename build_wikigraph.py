"""CSC111 Winter 2021 Final Project: Building the WikiGraph

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
from typing import Any, Optional
from wikigraph_copy import WikiGraph
from wikipedia_html_parsers import get_adjacent_urls, get_title


class Queue:
    """A first-in-first-out (FIFO) queue of items.

    Stores data in a first-in, first-out order. When removing an item from the
    queue, the most recently-added item is the one that is removed.

    >>> q = Queue()
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
    _item: list

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


def build_wikigraph(starting_url: str, num_sources: int, sources_per_page: Optional[int] = None) \
        -> WikiGraph:
    """ Find <num_sources> number of sources from the <starting_url> Wikipedia.

    Return a Graph with all the sources and the <starting_url> as its vertex.

    If one wikipedia article contains the link to another wikipedia article,
    then they are adjacent.
    """
    q = Queue()
    curr_url = starting_url
    visited = []
    wiki_network_so_far = WikiGraph()
    sources_found = 0

    q.enqueue(curr_url)
    visited.append(curr_url)
    curr_name = get_title(curr_url)
    wiki_network_so_far.add_vertex(curr_name, curr_url)

    while not (q.is_empty() or sources_found >= num_sources):
        curr_url = q.dequeue()
        curr_name = get_title(curr_url)

        neighbours = get_adjacent_urls(curr_url, sources_per_page)

        i = 0

        while not (i >= len(neighbours) or sources_found >= num_sources):
            v = neighbours[i]
            i += 1
            if v not in visited:
                q.enqueue(v)
                visited.append(v)
                v_name = get_title(v)
                if not wiki_network_so_far.is_vertex_in_graph(v_name):
                    wiki_network_so_far.add_vertex(v_name, v)
                    sources_found += 1

                wiki_network_so_far.add_edge(curr_name, v_name)

    return wiki_network_so_far


