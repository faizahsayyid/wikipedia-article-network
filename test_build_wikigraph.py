"""CSC111 Winter 2021 Final Project: Test Suite for build_wikigraph

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

from build_wikigraph import build_wikigraph, build_weighted_wikigraph
from weighted_wikigraph_class import WeightedWikiGraph
from wikigraph import WikiGraph


# ==================================================================================================
# TEST BUILD_WIKIGRAPH
# ==================================================================================================


def test_num_sources() -> None:
    """Test build_wikigraph for collecting the correct number of additional sources
    """

    g = build_wikigraph('https://en.wikipedia.org/wiki/Rebecca_Sugar', 20, 3)

    actual = len(g.get_all_vertices())
    expected = 21

    assert actual == expected


def test_connected_to_source() -> None:
    """Test build_wikigraph to make sure each vertex is connected to the original article
    """

    g = build_wikigraph('https://en.wikipedia.org/wiki/Rebecca_Sugar', 20, 3)

    assert all(g.connected(v, 'Rebecca Sugar') for v in g.get_all_vertices())


def test_build_wikigraph() -> None:
    """Test build_wikigraph for the correct vertex names, correct number of vertices, and correct
    neighbours for each vertices
    """
    wikigraph = build_wikigraph('https://en.wikipedia.org/wiki/Cade_(horse)', 6, 2)

    cade_neighbours_expected = wikigraph.get_neighbours('Cade (horse)')
    cade_neighbours_actual = {'Godolphin Arabian',
                              'Bald Galloway'
                              }

    assert cade_neighbours_expected == cade_neighbours_actual

    expected_graph = WikiGraph()

    expected_graph.add_vertex('Cade (horse)', 'https://en.wikipedia.org/wiki/Cade_(horse)')
    expected_graph.add_vertex('Godolphin Arabian',
                              'https://en.wikipedia.org/wiki/Godolphin_Arabian')
    expected_graph.add_vertex('Bald Galloway',
                              'https://en.wikipedia.org/wiki/Bald_Galloway')
    expected_graph.add_vertex('George Stubbs',
                              'https://en.wikipedia.org/wiki/George_Stubbs')
    expected_graph.add_vertex('Francis Godolphin, 2nd Earl of Godolphin',
                              'https://en.wikipedia.org/wiki/'
                              'Francis_Godolphin,_2nd_Earl_of_Godolphin')
    expected_graph.add_vertex('Stallion (horse)',
                              'https://en.wikipedia.org/wiki/Stallion_(horse)')
    expected_graph.add_vertex('Kingdom of Great Britain',
                              'https://en.wikipedia.org/wiki/Kingdom_of_Great_Britain')

    expected_graph.add_edge('Cade (horse)', 'Godolphin Arabian')
    expected_graph.add_edge('Cade (horse)', 'Bald Galloway')
    expected_graph.add_edge('Godolphin Arabian', 'George Stubbs')
    expected_graph.add_edge('Godolphin Arabian', 'Francis Godolphin, 2nd Earl of Godolphin')
    expected_graph.add_edge('Bald Galloway', 'Stallion (horse)')
    expected_graph.add_edge('Bald Galloway', 'Kingdom of Great Britain')

    assert expected_graph.get_all_vertices() == wikigraph.get_all_vertices()
    assert expected_graph.get_neighbours('Cade (horse)') == wikigraph.get_neighbours('Cade (horse)')
    assert expected_graph.get_neighbours('Godolphin Arabian') == wikigraph.get_neighbours(
        'Godolphin Arabian')
    assert expected_graph.get_neighbours('Bald Galloway') == wikigraph.get_neighbours(
        'Bald Galloway')
    assert expected_graph.get_neighbours('George Stubbs') == wikigraph.get_neighbours(
        'George Stubbs')
    assert expected_graph.get_neighbours('Francis Godolphin, 2nd Earl of Godolphin') \
           == wikigraph.get_neighbours('Francis Godolphin, 2nd Earl of Godolphin')
    assert expected_graph.get_neighbours('Stallion (horse)') == wikigraph.get_neighbours(
        'Stallion (horse)')
    assert expected_graph.get_neighbours('Kingdom of Great Britain') == wikigraph.get_neighbours(
        'Kingdom of Great Britain')

# ==================================================================================================
# TEST BUILD_WEIGHTED_WIKIGRAPH
# ==================================================================================================


def test_build_weighted_wikigraph() -> None:
    """Test build_weighted_wikigraph for the correct vertex names, correct number of vertices,
    correct neighbours for each vertices, and the correct number of additional sources
    """
    wikigraph = build_weighted_wikigraph('https://en.wikipedia.org/wiki/Cade_(horse)', 6, 2)
    actual = len(wikigraph.get_all_vertices())
    expected = 7

    assert expected == actual

    cade_neighbours_actual = wikigraph.get_neighbours('Cade (horse)')
    cade_neighbours_expected = {('Thoroughbred', 5.0), ('Godolphin Arabian', 3.5)}

    assert cade_neighbours_expected == cade_neighbours_actual

    expected_graph = WeightedWikiGraph()

    expected_graph.add_vertex('Cade (horse)', 'https://en.wikipedia.org/wiki/Cade_(horse)')
    expected_graph.add_vertex('Godolphin Arabian',
                              'https://en.wikipedia.org/wiki/Godolphin_Arabian')
    expected_graph.add_vertex('Thoroughbred',
                              'https://en.wikipedia.org/wiki/Thoroughbred')
    expected_graph.add_vertex('Horse',
                              'https://en.wikipedia.org/wiki/Horse')
    expected_graph.add_vertex('Breed',
                              'https://en.wikipedia.org/wiki/Breed')
    expected_graph.add_vertex('Wandlebury',
                              'https://en.wikipedia.org/wiki/Wandlebury')
    expected_graph.add_vertex('Matchem',
                              'https://en.wikipedia.org/wiki/Matchem')

    expected_graph.add_edge('Cade (horse)', 'Godolphin Arabian', 3.5)
    expected_graph.add_edge('Cade (horse)', 'Thoroughbred', 5.0)
    expected_graph.add_edge('Thoroughbred', 'Horse', 138.0)
    expected_graph.add_edge('Thoroughbred', 'Breed', 32.5)
    expected_graph.add_edge('Godolphin Arabian', 'Wandlebury', 11.5)
    expected_graph.add_edge('Godolphin Arabian', 'Matchem', 9.0)

    assert expected_graph.get_all_vertices() == wikigraph.get_all_vertices()
    assert expected_graph.get_neighbours('Cade (horse)') == wikigraph.get_neighbours('Cade (horse)')
    assert expected_graph.get_neighbours('Godolphin Arabian') == wikigraph.get_neighbours(
        'Godolphin Arabian')
    assert expected_graph.get_neighbours('Thoroughbred') == wikigraph.get_neighbours('Thoroughbred')
    assert expected_graph.get_neighbours('Horse') == wikigraph.get_neighbours('Horse')
    assert expected_graph.get_neighbours('Breed') == wikigraph.get_neighbours('Breed')
    assert expected_graph.get_neighbours('Wandlebury') == wikigraph.get_neighbours('Wandlebury')
    assert expected_graph.get_neighbours('Matchem') == wikigraph.get_neighbours('Matchem')


if __name__ == '__main__':
    import pytest
    pytest.main(['test_build_wikigraph.py', '-vv'])
