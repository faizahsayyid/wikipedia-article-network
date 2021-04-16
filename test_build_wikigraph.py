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
    """Test build_wikigraph for the correct vertex names and correct number of degrees
    """
    wikigraph = build_wikigraph('https://en.wikipedia.org/wiki/Cade_(horse)', 25, 5)

    cade_neighbours_expected = wikigraph.get_neighbours('Cade (horse)')
    cade_neighbours_actual = {'Bald Galloway',
                              'Francis Godolphin, 2nd Earl of Godolphin',
                              'Kingdom of Great Britain',
                              'Stallion (horse)',
                              'Godolphin Arabian'
                              }

    # original
    assert cade_neighbours_expected == cade_neighbours_actual

    cade_degree_expected = wikigraph._vertices['Cade (horse)'].degree()
    cade_degree_actual = 5

    # other
    assert cade_degree_expected == cade_degree_actual


# ==================================================================================================
# TEST BUILD_WEIGHTED_WIKIGRAPH
# ==================================================================================================


def test_build_weighted_wikigraph() -> None:
    """Test build_weighted_wikigraph for the correct vertex names, correct number of degrees
    and the correct number of additional sources
    """
    wikigraph = build_weighted_wikigraph('https://en.wikipedia.org/wiki/Cade_(horse)', 25, 5)
    actual = len(wikigraph.get_all_vertices())
    expected = 26

    assert expected == actual

    cade_neighbours_expected = wikigraph.get_neighbours('Cade (horse)')
    cade_neighbours_actual = {('Thoroughbred', 5.0),
                              ('Godolphin Arabian', 3.5),
                              ('Kingdom of Great Britain', 3.5),
                              ('Francis Godolphin, 2nd Earl of Godolphin', 3.0),
                              ('Bald Galloway', 2.0)
                              }

    assert cade_neighbours_expected == cade_neighbours_actual

    cade_degree_expected = wikigraph._vertices['Cade (horse)'].degree()
    cade_degree_actual = 5

    assert cade_degree_expected == cade_degree_actual


if __name__ == '__main__':
    import pytest
    pytest.main(['test_build_wikigraph.py', '-v'])