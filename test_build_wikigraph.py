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

from build_wikigraph import build_wikigraph


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


if __name__ == '__main__':
    import pytest
    pytest.main(['test_build_wikigraph.py', '-v'])
