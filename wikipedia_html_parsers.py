"""CSC111 Winter 2021 Final Project: Parsing Wikipedia Pages

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

import urllib.request
from html.parser import HTMLParser


class _WikipediaArticleParser(HTMLParser):
    """An Wikipedia article parser, used to extract Wikipedia links from html code.

    This article parser does not include wikipedia links that contain'Special:', 'Help:',
    'Wikipedia:', 'Category:', 'Portal:', or 'Book:' in their url.

    Instance Attributes:
        - articles: a list of wikipedia links parsed from html code

    Representation Invariants:
        - all("https://en.wikipedia.org/wiki/" in a for a in self.articles)
        - all('Special:' not in a for a in self.articles)
        - all('Help:' not in a for a in self.articles)
        - all('Wikipedia:' not in a for a in self.articles)
        - all('Category:' not in a for a in self.articles)
        - all('Portal:' not in a for a in self.articles)
        - all('Book:' not in a for a in self.articles)
    """
    articles: list[str]

    def __init__(self) -> None:
        """Initialize a new article parser.

        This article parser is initialized an empty list of articles.
        """
        super().__init__()
        self.articles = []
        self.reset()

    def error(self, message) -> None:
        """Help on function error in module _markupbase

        (This method needed to be implemented for the abstract super class HTMLParser,
         but doesn't do anything)
        """
        pass

    def handle_starttag(self, tag, attrs) -> None:
        """Parse wikipedia links from html file.
        Add those wikipedia links to self.articles.
        """
        # Only parse the 'anchor' tags.
        if tag == "a":
            for attribute in attrs:
                name, link = attribute

                unwanted_page = ('Special:' in link) or ('Help:' in link) \
                    or ('Wikipedia:' in link) or ('Category:' in link) \
                    or ('Portal:' in link) or ('Book:' in link)

                if name == "href" and link.startswith('/wiki/') and not unwanted_page:
                    self.articles.append('https://en.wikipedia.org/' + link)


class _WikipediaSummaryParser(HTMLParser):
    """An Wikipedia summary parser, used to extract the summary of a Wikipedia article
    from the html code of the article."""
    _found_info_box: bool
    _found_summary: bool
    summary: str
    _skip_footnote: bool

    def __init__(self) -> None:
        """Initialize a new summary parser.

        This summary parser is initialized an empty list of articles.
        """
        super().__init__()
        self.reset()
        self._found_summary = False
        self._found_info_box = False
        self.summary = ''
        self._skip_footnote = False

    def error(self, message) -> None:
        """Help on function error in module _markupbase

        (This method needed to be implemented for the abstract super class HTMLParser,
         but doesn't do anything)
        """
        pass

    def handle_starttag(self, tag, attrs) -> None:
        """Find the summary of the wikipedia article (update self._found_summary)
        Update self._skip_footnote whenever a footnote is encountered in the summary
        """
        if self._found_info_box and tag == 'p':
            self._found_summary = True
        elif tag == 'table':
            for attribute in attrs:
                name, value = attribute
                if name == 'class' and ('infobox' in value):
                    self._found_info_box = True

        if tag == 'sup':
            self._skip_footnote = True

    def handle_endtag(self, tag) -> None:
        """Update self._found_summary the end of the summary is reached
        Update self._skip_footnote the end of a footnote is reached
        """
        if self._found_summary and tag == 'p':
            self._found_summary = False

        if tag == 'sup':
            self._skip_footnote = False

    def handle_data(self, data) -> None:
        """Add parts of the summary of the article to self.summary"""
        if self._found_summary and (self.summary.count('.') < 2) and not self._skip_footnote:
            self.summary += data


class _WikipediaTitleParser(HTMLParser):
    _found_title: bool
    title: str

    def __init__(self) -> None:
        """Initialize a new article parser.

        This article parser is initialized an empty list of articles.
        """
        super().__init__()
        self.reset()
        self._found_title = False
        self.title = ''

    def error(self, message) -> None:
        """Help on function error in module _markupbase

        (This method needed to be implemented for the abstract super class HTMLParser,
         but doesn't do anything)
        """
        pass

    def handle_starttag(self, tag: str, attrs: tuple) -> None:
        """..."""
        if tag == 'h1' and self.title == '':
            for attribute in attrs:
                name, value = attribute
                if name == 'class' and value == 'firstHeading':
                    self._found_title = True

    def handle_data(self, data) -> None:
        """..."""
        if self._found_title:
            self.title = data
            self._found_title = False


def get_adjacent_urls(url: str) -> list[str]:
    """Return a List of all adjacent urls in strings to the input url."""

    data_to_parse = urllib.request.urlopen(url)
    html = data_to_parse.read().decode()
    data_to_parse.close()

    parser = _WikipediaArticleParser()
    parser.feed(html)

    return parser.articles


def get_summary(url: str) -> str:
    """Return the summary of the given wikipedia article

    Precondtion
        - 'https://en.wikipedia.org/wiki/' in url
    """

    data_to_parse = urllib.request.urlopen(url)
    html = data_to_parse.read().decode()
    data_to_parse.close()

    parser = _WikipediaSummaryParser()
    parser.feed(html)

    return parser.summary


def get_title(url: str):
    """Return the title of the given wikipedia article"""
    data_to_parse = urllib.request.urlopen(url)
    html = data_to_parse.read().decode()
    data_to_parse.close()

    parser = _WikipediaTitleParser()
    parser.feed(html)

    return parser.title
