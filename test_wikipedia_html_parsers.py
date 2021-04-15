"""CSC111 Winter 2021 Final Project: Test Suite for wikipedia_html_parsers

Module Description
===============================

This module contains tests for _WikipediaArticleParser.handle_starttag, and
_WikipediaSummaryParser.handle_data

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
# TEST _WikipediaArticleParser
# ==================================================================================================

def test_wap_mutates() -> None:
    """Test _WikipediaArticleParser.handle_starttag with <a> tag, 'href', and
    '/wiki/Rebecca_Sugar' to make sure the article is added to
    _WikipediaArticleParser.articles
    """
    article_parser = wikipedia_html_parsers.WikipediaArticleParser('')
    article_parser.handle_starttag('a', [('href', '/wiki/Rebecca_Sugar')])

    assert article_parser.articles == ['https://en.wikipedia.org/wiki/Rebecca_Sugar']


def test_wap_wrong_attrs() -> None:
    """Test _WikipediaArticleParser.handle_starttag with an <a> tag
    with the following attributes: [('href', '/wiki/Rebecca_Sugar')],
    to make sure tags with no 'href' attribute are ignored"""
    article_parser = wikipedia_html_parsers.WikipediaArticleParser('')
    article_parser.handle_starttag('a', [('id', '/wiki/Rebecca_Sugar')])

    assert article_parser.articles == []


def test_wap_wrong_tag() -> None:
    """Test _WikipediaArticleParser.handle_starttag with an <p> tag to make
    sure tags that aren't <a> tags are ignored"""
    article_parser = wikipedia_html_parsers.WikipediaArticleParser('')
    article_parser.handle_starttag('p', [('id', '/wiki/Rebecca_Sugar')])

    assert article_parser.articles == []


def test_wap_not_wiki() -> None:
    """Test _WikipediaArticleParser.handle_starttag with an <a> and the
    following attributes: [('href', 'google.com')] to make sure non wikipedia
    articles are ignored"""
    article_parser = wikipedia_html_parsers.WikipediaArticleParser('')
    article_parser.handle_starttag('a', [('href', 'google.com')])

    assert article_parser.articles == []


def test_wap_not_unwanted_url() -> None:
    """Test _WikipediaArticleParser.handle_starttag with an unwanted article
    to make sure _WikipediaArticleParser.articles does not updated"""
    article_parser = wikipedia_html_parsers.WikipediaArticleParser('')
    article_parser.handle_starttag('a', [('href', '/wiki/Help:Contents')])

    assert article_parser.articles == []


def test_wap_no_duplicates() -> None:
    """Test _WikipediaArticleParser.handle_starttag to make sure the same article
    can not be added to _WikipediaArticleParser.articles twice"""
    article_parser = wikipedia_html_parsers.WikipediaArticleParser('')
    article_parser.handle_starttag('a', [('href', '/wiki/Rebecca_Sugar')])
    article_parser.handle_starttag('a', [('href', '/wiki/Rebecca_Sugar')])

    assert article_parser.articles == ['https://en.wikipedia.org/wiki/Rebecca_Sugar']


# ==================================================================================================
# TEST _WikipediaSummaryParser
# ==================================================================================================

def test_wsp_collects_data() -> None:
    """Test _WikipediaSummaryParser.handle_data to make sure it collects data
     we found a <p> tag"""
    summary_parser = wikipedia_html_parsers.WikipediaSummaryParser()
    summary_parser.handle_starttag('p', [])

    summary_parser.handle_data('hello')

    assert summary_parser.summary == 'hello'


def test_wsp_skips_footnote() -> None:
    """Test _WikipediaSummaryParser.handle_data to make sure skips footnotes
    (<sup> tags)"""
    summary_parser = wikipedia_html_parsers.WikipediaSummaryParser()

    summary_parser.handle_starttag('p', [])
    summary_parser.handle_data('hello')

    summary_parser.handle_starttag('sup', [])
    summary_parser.handle_data('1')

    assert summary_parser.summary == 'hello'


def test_wsp_skips_non_p() -> None:
    """Test _WikipediaSummaryParser.handle_data to it collects data only when
    we are inside <p> tags. It should stop collecting data when we reach a </p> endtag"""
    summary_parser = wikipedia_html_parsers.WikipediaSummaryParser()
    summary_parser.handle_starttag('p', [])
    summary_parser.handle_data('hello')

    summary_parser.handle_endtag('p')
    summary_parser.handle_data('what is life')

    assert summary_parser.summary == 'hello'


def test_wsp_collects_2_sentences() -> None:
    """Test _WikipediaSummaryParser.handle_data to make sure it only collects
    2 sentences (when sentences wanted is set to default)"""
    summary_parser = wikipedia_html_parsers.WikipediaSummaryParser()
    summary_parser.handle_starttag('p', [])
    summary_parser.handle_data('what is life. life is meaningless.')
    summary_parser.handle_data('meaningless is life.')

    assert summary_parser.summary == 'what is life. life is meaningless.'


def test_wsp_strips_tail() -> None:
    """Test _WikipediaSummaryParser.handle_data to make sure it only collects
    2 sentences (when sentences wanted is set to default), and gets rid of any word
    tailing after the second period"""
    summary_parser = wikipedia_html_parsers.WikipediaSummaryParser()
    summary_parser.handle_starttag('p', [])
    summary_parser.handle_data('what is life. life is ')
    summary_parser.handle_data('meaningless. meaningless is life.')

    assert summary_parser.summary == 'what is life. life is meaningless.'


# ==================================================================================================
# TEST get_adjacent_url and get_adjacent_url_weighted
# ==================================================================================================


def test_get_adjacent_url() -> None:
    """ Test get_adjacent_url for getting the correct number of adjacent urls
    """
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
    """ Test get_adjacent_url_weighted for getting the correct number of adjacent urls weighted
    """
    expected = [(('https://en.wikipedia.org/wiki/Thoroughbred',
                  'Thoroughbred'), 10),
                (('https://en.wikipedia.org/wiki/Godolphin_Arabian',
                  'Godolphin Arabian'), 7),
                (('https://en.wikipedia.org/wiki/Kingdom_of_Great_Britain',
                  'Kingdom of Great Britain'), 7),
                (('https://en.wikipedia.org/wiki/Francis_Godolphin,_2nd_Earl_of_Godolphin',
                  'Francis Godolphin, 2nd Earl of Godolphin'), 6),
                (('https://en.wikipedia.org/wiki/Bald_Galloway',
                  'Bald Galloway'), 4),
                (('https://en.wikipedia.org/wiki/Leading_sire_in_Great_Britain_and_Ireland',
                  'Leading sire in Great Britain and Ireland'), 4),
                (('https://en.wikipedia.org/wiki/Matchem',
                  'Matchem'), 4),
                (('https://en.wikipedia.org/wiki/Alysheba',
                  'Alysheba'), 3),
                (('https://en.wikipedia.org/wiki/Potoooooooo',
                  'Potoooooooo'), 3),
                (('https://en.wikipedia.org/wiki/Mambrino_(horse)',
                  'Mambrino (horse)'), 2),
                (('https://en.wikipedia.org/wiki/Stallion_(horse)', 'Stallion (horse)'), 1),
                (('https://en.wikipedia.org/wiki/Foundation_bloodstock',
                  'Foundation bloodstock'), 1),
                (('https://en.wikipedia.org/wiki/Lath_(horse)',
                  'Lath (horse)'), 1),
                (('https://en.wikipedia.org/wiki/Guinea_(British_coin)',
                  'Guinea (British coin)'), 1),
                (('https://en.wikipedia.org/wiki/Boston_(horse)',
                  'Boston (horse)'), 1),
                (('https://en.wikipedia.org/wiki/Leading_sire_in_Great_Britain_%26_Ireland',
                  'Leading sire in Great Britain %26 Ireland'), 0)
                ]
    actual = wikipedia_html_parsers.get_adjacent_urls_weighted(
        'https://en.wikipedia.org/wiki/Cade_(horse)')

    assert expected == actual


# ==================================================================================================
# TEST get_summary
# ==================================================================================================


def test_get_summary() -> None:
    """ Test get_summary for getting exactly two lines of summary (the default)
    """
    expected = 'Cade (1734–1756) was an important foundation sire of Thoroughbred racehorses. ' \
               'He was the Leading sire in Great Britain and Ireland in 1752, 1753, 1758, 1759 ' \
               'and 1760.'

    actual = wikipedia_html_parsers.get_summary('https://en.wikipedia.org/wiki/Cade_(horse)')

    assert expected == actual


def test_get_summary_sentence_four() -> None:
    """ Test get_summary for getting exactly four lines of summary
    """
    expected = 'Cade (1734–1756) was an important foundation sire of Thoroughbred racehorses. ' \
               'He was the Leading sire in Great Britain and Ireland in 1752, 1753, 1758, 1759 ' \
               'and 1760.\n' + 'Bred by Francis Godolphin, 2nd Earl of Godolphin, he was by ' \
                               'the Thoroughbred foundation sire, the Godolphin Arabian. Out' \
                               ' of Roxana (1718) (by Bald Galloway), he was a full-brother ' \
                               'to the first son of the Goldophin Arabian, Lath (1732 bay colt).'

    actual = wikipedia_html_parsers.get_summary(
        'https://en.wikipedia.org/wiki/Cade_(horse)', 4)

    assert expected == actual


def test_get_summary_sentence_one() -> None:
    """ Test get_summary for getting exactly one line of summary
    """
    expected = 'Cade (1734–1756) was an important foundation sire of Thoroughbred racehorses.'

    actual = wikipedia_html_parsers.get_summary(
        'https://en.wikipedia.org/wiki/Cade_(horse)', 1)

    assert expected == actual


if __name__ == '__main__':
    import pytest
    pytest.main(['test_wikipedia_html_parsers.py', '-v'])

    import python_ta.contracts

    python_ta.contracts.check_all_contracts()

    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['wikipedia_html_parsers'],
        'allowed-io': [],
        'max-line-length': 100,
        'disable': ['E1136']
    })
