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

def test_wap_start_tag_mutates() -> None:
    """Test _WikipediaArticleParser.handle_starttag with <a> tag, 'href', and
    '/wiki/Rebecca_Sugar' to make sure the article is added to
    _WikipediaArticleParser.articles
    """
    article_parser = wikipedia_html_parsers._WikipediaArticleParser('')
    article_parser.handle_starttag('a', [('href', '/wiki/Rebecca_Sugar')])

    assert article_parser.articles == ['https://en.wikipedia.org/wiki/Rebecca_Sugar']


def test_wap_start_tag_wrong_attrs() -> None:
    """Test _WikipediaArticleParser.handle_starttag with an <a> tag
    with the following attributes: [('href', '/wiki/Rebecca_Sugar')],
    to make sure tags with no 'href' attribute are ignored"""
    article_parser = wikipedia_html_parsers._WikipediaArticleParser('')
    article_parser.handle_starttag('a', [('id', '/wiki/Rebecca_Sugar')])

    assert article_parser.articles == []


def test_wap_start_tag_wrong_tag() -> None:
    """Test _WikipediaArticleParser.handle_starttag with an <p> tag to make
    sure tags that aren't <a> tags are ignored"""
    article_parser = wikipedia_html_parsers._WikipediaArticleParser('')
    article_parser.handle_starttag('p', [('id', '/wiki/Rebecca_Sugar')])

    assert article_parser.articles == []


def test_wap_start_tag_not_wiki() -> None:
    """Test _WikipediaArticleParser.handle_starttag with an <a> and the
    following attributes: [('href', 'google.com')] to make sure non wikipedia
    articles are ignored"""
    article_parser = wikipedia_html_parsers._WikipediaArticleParser('')
    article_parser.handle_starttag('a', [('href', 'google.com')])

    assert article_parser.articles == []


def test_wap_start_tag_not_unwanted_url() -> None:
    """Test _WikipediaArticleParser.handle_starttag with an unwanted article
    to make sure _WikipediaArticleParser.articles does not updated"""
    article_parser = wikipedia_html_parsers._WikipediaArticleParser('')
    article_parser.handle_starttag('a', [('href', '/wiki/Help:Contents')])

    assert article_parser.articles == []


def test_wap_start_tag_no_duplicates() -> None:
    """Test _WikipediaArticleParser.handle_starttag to make sure the same article
    can not be added to _WikipediaArticleParser.articles twice"""
    article_parser = wikipedia_html_parsers._WikipediaArticleParser('')
    article_parser.handle_starttag('a', [('href', '/wiki/Rebecca_Sugar')])
    article_parser.handle_starttag('a', [('href', '/wiki/Rebecca_Sugar')])

    assert article_parser.articles == ['https://en.wikipedia.org/wiki/Rebecca_Sugar']


# ==================================================================================================
# TEST _WikipediaSummaryParser
# ==================================================================================================

def test_wsp_collects_data() -> None:
    """Test _WikipediaSummaryParser.handle_data to make sure it collects data
     we found a <p> tag"""
    summary_parser = wikipedia_html_parsers._WikipediaSummaryParser()
    summary_parser.handle_starttag('p', [])

    summary_parser.handle_data('hello')

    assert summary_parser.summary == 'hello'


def test_wsp_collects_skips_footnote() -> None:
    """Test _WikipediaSummaryParser.handle_data to make sure skips footnotes
    (<sup> tags)"""
    summary_parser = wikipedia_html_parsers._WikipediaSummaryParser()

    summary_parser.handle_starttag('p', [])
    summary_parser.handle_data('hello')

    summary_parser.handle_starttag('sup', [])
    summary_parser.handle_data('1')

    assert summary_parser.summary == 'hello'


def test_wsp_collects_skips_non_p() -> None:
    """Test _WikipediaSummaryParser.handle_data to it collects data only when
    we are inside <p> tags. It should stop collecting data when we reach a </p> endtag"""
    summary_parser = wikipedia_html_parsers._WikipediaSummaryParser()
    summary_parser.handle_starttag('p', [])
    summary_parser.handle_data('hello')

    summary_parser.handle_endtag('p')
    summary_parser.handle_data('what is life')

    assert summary_parser.summary == 'hello'


def test_wsp_collects_2_sentences() -> None:
    """Test _WikipediaSummaryParser.handle_data to make sure it only collects
    2 sentences (when sentences wanted is set to default)"""
    summary_parser = wikipedia_html_parsers._WikipediaSummaryParser()
    summary_parser.handle_starttag('p', [])
    summary_parser.handle_data('what is life. life is meaningless.')
    summary_parser.handle_data('meaningless is life.')

    assert summary_parser.summary == 'what is life. life is meaningless.'


def test_wsp_collects_strips_tail() -> None:
    """Test _WikipediaSummaryParser.handle_data to make sure it only collects
    2 sentences (when sentences wanted is set to default), and gets rid of any word
    tailing after the second period"""
    summary_parser = wikipedia_html_parsers._WikipediaSummaryParser()
    summary_parser.handle_starttag('p', [])
    summary_parser.handle_data('what is life. life is ')
    summary_parser.handle_data('meaningless. meaningless is life.')

    assert summary_parser.summary == 'what is life. life is meaningless.'


if __name__ == '__main__':
    import pytest
    pytest.main(['test_wikipedia_html_parsers.py', '-v'])
