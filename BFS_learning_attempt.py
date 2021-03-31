"""
YOOOO
BFS Stuffs
"""
from lectures.week08.lec16_exercises import Graph
from typing import Any
import urllib
from html.parser import HTMLParser


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


def bfs(graph: Graph, start: str) -> list:
    """Output all the vertices

    start: vertices

    >>> g = example()
    >>> bfs(g, 'A')
    ['A', 'B', 'S', 'C', 'G', 'D', 'E', 'F', 'H']
    """
    q = Queue()
    curr_vertex = graph._vertices[start]
    visited = []
    output = []

    q.enqueue(curr_vertex)
    visited.append(curr_vertex)

    while not q.is_empty():
        curr_vertex = q.dequeue()
        print('current vertex: ' + curr_vertex.item)
        output.append(curr_vertex.item)
        print('current vertex neighbours: ' + str({u.item for u in curr_vertex.neighbours}))

        for v in curr_vertex.neighbours:
            if v not in visited:
                q.enqueue(v)
                print(v.item + ' enqueued')
                visited.append(v)

    return output


def example() -> Graph:
    """Make example graph"""
    g = Graph()
    alphabet = 'ABCDEFGHS'

    for letter in alphabet:
        g.add_vertex(letter)

    g.add_edge('A', 'B')
    g.add_edge('A', 'S')
    g.add_edge('S', 'C')
    g.add_edge('S', 'G')
    g.add_edge('C', 'D')
    g.add_edge('C', 'F')
    g.add_edge('C', 'E')
    g.add_edge('F', 'G')
    g.add_edge('G', 'H')
    g.add_edge('H', 'E')

    return g


def BFS_Wikipedia(starting_url: str, num_sources: int) -> Graph:
    """..."""
    q = Queue()
    curr_url = starting_url
    visited = []
    wiki_network_so_far = Graph()
    sources_found = 0

    q.enqueue(curr_url)
    visited.append(curr_url)
    wiki_network_so_far.add_vertex(curr_url)

    while not (q.is_empty() or sources_found >= num_sources):
        curr_url = q.dequeue()
        sources_found += 1

        # scrapy function(url) -> urls on the page

        neighbours = get_adjacent_urls(curr_url)

        for v in neighbours:
            if v not in visited:
                q.enqueue(v)
                visited.append(v)
                wiki_network_so_far.add_vertex(v)
                wiki_network_so_far.add_edge(curr_url, v)

    return wiki_network_so_far


def get_adjacent_urls(url: str) -> list[str]:
    """..."""
    # scrapy stuff
