"""CSC111 Winter 2021 Final Project: Test Suite for wikipedia_html_parsers

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

import wikipedia_html_parsers


# ==================================================================================================
# TEST BUILD_HTML_PARSERS
# ==================================================================================================

def test_get_adjacent_url() -> None:
    """ ... """
    expected = {'https://en.wikipedia.org/wiki/Thoroughbred',
                'https://en.wikipedia.org/wiki/Leading_sire_in_Great_Britain_and_Ireland',
                'https://en.wikipedia.org/wiki/Francis_Godolphin,_2nd_Earl_of_Godolphin',
                'https://en.wikipedia.org/wiki/Foundation_bloodstock',
                'https://en.wikipedia.org/wiki/Godolphin_Arabian',
                'https://en.wikipedia.org/wiki/Bald_Galloway',
                'https://en.wikipedia.org/wiki/Stallion_(horse)',
                'https://en.wikipedia.org/wiki/Kingdom_of_Great_Britain',
                'https://en.wikipedia.org/wiki/Leading_sire_in_Great_Britain_and_Ireland',
                'https://en.wikipedia.org/wiki/Lath_(horse)',
                'https://en.wikipedia.org/wiki/Guinea_(British_coin)',
                'https://en.wikipedia.org/wiki/Leading_sire_in_Great_Britain_%26_Ireland',
                'https://en.wikipedia.org/wiki/Mambrino_(horse)',
                'https://en.wikipedia.org/wiki/Alysheba',
                'https://en.wikipedia.org/wiki/Boston_(horse)',
                'https://en.wikipedia.org/wiki/Matchem',
                'https://en.wikipedia.org/wiki/Potoooooooo'
                }
    actual = set(wikipedia_html_parsers.get_adjacent_urls
                 ('https://en.wikipedia.org/wiki/Cade_(horse)'))

    assert actual == expected


def test_get_adjacent_url_weighted() -> None:
    """ ... """
    expected = {(('https://en.wikipedia.org/wiki/Thoroughbred',
                  'Thoroughbred'), 1),
                (('https://en.wikipedia.org/wiki/Leading_sire_in_Great_Britain_and_Ireland',
                  'Leading sire in Great Britain and Ireland'), 9),
                (('https://en.wikipedia.org/wiki/Francis_Godolphin,_2nd_Earl_of_Godolphin',
                  'Francis Godolphin, 2nd Earl of Godolphin'), 3),
                (('https://en.wikipedia.org/wiki/Foundation_bloodstock',
                  'Foundation bloodstock'), 1),
                (('https://en.wikipedia.org/wiki/Godolphin_Arabian',
                  'Godolphin Arabian'), 3),
                (('https://en.wikipedia.org/wiki/Bald_Galloway',
                  'Bald Galloway'), 3),

                (('https://en.wikipedia.org/wiki/Stallion_(horse)', 'Stallion (horse)'), 1),
                (('https://en.wikipedia.org/wiki/Kingdom_of_Great_Britain',
                  'Kingdom of Great Britain'), 1),

                (('https://en.wikipedia.org/wiki/Lath_(horse)',
                  'Lath (horse)'), 2),
                (('https://en.wikipedia.org/wiki/Guinea_(British_coin)',
                  'Guinea (British_coin)'), 1),

                (('https://en.wikipedia.org/wiki/Leading_sire_in_Great_Britain_%26_Ireland',
                  'Leading sire in Great Britain %26 Ireland'), 0),

                (('https://en.wikipedia.org/wiki/Mambrino_(horse)',
                  'Mambrino (horse)'), 3),
                (('https://en.wikipedia.org/wiki/Alysheba',
                  'Alysheba'), 1),
                (('https://en.wikipedia.org/wiki/Boston_(horse)',
                  'Boston (horse)'), 1),
                (('https://en.wikipedia.org/wiki/Matchem',
                  'Matchem'), 1),
                (('https://en.wikipedia.org/wiki/Potoooooooo',
                  'Potoooooooo'), 2)
                }
    actual = set(wikipedia_html_parsers.get_adjacent_urls_weighted
                 ('https://en.wikipedia.org/wiki/Cade_(horse)'))

    assert expected == actual


def test_get_summary() -> None:
    """ ... """
    expected = 'Cade (1734–1756) was an important foundation sire of Thoroughbred racehorses. ' \
               'He was the Leading sire in Great Britain and Ireland in 1752, 1753, 1758, 1759 ' \
               'and 1760.'

    actual = wikipedia_html_parsers.get_summary('https://en.wikipedia.org/wiki/Cade_(horse)')

    assert expected == actual


if __name__ == '__main__':
    import pytest
    pytest.main(['test_wikipedia_html_parsers_tina.py', '-vv'])
