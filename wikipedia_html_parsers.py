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
import urllib.error
import urllib.request
from html.parser import HTMLParser

UNWANTED = ['Special:', 'Help:', 'Wikipedia', 'Category:', 'Portal:', 'Book:', '.jpg',
            '.svg', '.png', '.JPG', '.PNG', '.SVG', 'File:', 'Talk:', '(disambiguation)'
            'Module talk:', 'User:', ':', '(disambiguation)']


class _WikipediaArticleParser(HTMLParser):
    """An Wikipedia article parser, used to extract Wikipedia links from html code.

    This article parser does not include wikipedia links that contain 'Special:', 'Help:',
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
                unwanted_page = any((unwanted in link) for unwanted in UNWANTED)

                if name == "href" and link.startswith('/wiki/') and not unwanted_page:
                    link = 'https://en.wikipedia.org' + link
                    if link not in self.articles:
                        self.articles.append(link)


class _WikipediaSummaryParser(HTMLParser):
    """An Wikipedia summary parser, used to extract the summary of a Wikipedia article
    from the html code of the article."""
    _found_p: bool
    summary: str
    sentences_wanted: int
    _skip_footnote: bool

    def __init__(self, sentences_wanted: int = 2) -> None:
        """Initialize a new summary parser.

        This summary parser is initialized an empty list of articles.
        """
        super().__init__()
        self.reset()
        self._found_p = False
        self.summary = ''
        self._skip_footnote = False
        self.sentences_wanted = sentences_wanted

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
        if tag == 'p':
            self._found_p = True

        if tag == 'sup':
            self._skip_footnote = True

    def handle_endtag(self, tag) -> None:
        """Update self._found_summary the end of the summary is reached
        Update self._skip_footnote the end of a footnote is reached
        """
        if tag == 'p':
            self._found_p = False

        if tag == 'sup':
            self._skip_footnote = False

    def handle_data(self, data) -> None:
        """Add parts of the summary of the article to self.summary"""
        if self._found_p and (self.summary.count('.') < self.sentences_wanted) \
                and not self._skip_footnote and data != '\n':
            self.summary += data
            if (self.summary.count('.') >= self.sentences_wanted) \
                    and not self.summary.endswith('.'):
                index_of_last_period = self.summary.rindex('.')
                self.summary = self.summary[:index_of_last_period + 1]


def get_adjacent_urls(url: str) -> list[str]:
    """Return a List of all adjacent urls in strings to the input url."""

    try:
        data_to_parse = urllib.request.urlopen(url)
        html = data_to_parse.read().decode()
        data_to_parse.close()

        parser = _WikipediaArticleParser()
        parser.feed(html)

        return parser.articles

    except urllib.error.HTTPError:
        return []


# list[tuple[tuple[str, str], float]]
def get_adjacent_urls_weighted(url: str) -> list:
    """Return a List of all adjacent urls in strings to the input url."""

    try:
        data_to_parse = urllib.request.urlopen(url)
        html = data_to_parse.read().decode()
        data_to_parse.close()

        parser = _WikipediaArticleParser()
        parser.feed(html)

        neighbours_to_weights = {}

        for article_link in parser.articles:
            if article_link != url:
                article_name = get_title(article_link)
                weight1 = html.count(article_name)
                neighbours_to_weights[(article_link, article_name)] = weight1

        return sorted(list(neighbours_to_weights.items()), key=lambda item: item[1], reverse=True)

    except urllib.error.HTTPError:
        return []


def get_summary(url: str) -> str:
    """Return the summary of the given wikipedia article

    Precondition
        - 'https://en.wikipedia.org/wiki/' in url
    """
    data_to_parse = urllib.request.urlopen(url)
    html = data_to_parse.read().decode()
    data_to_parse.close()

    parser = _WikipediaSummaryParser()
    parser.feed(html)

    return parser.summary


def get_title(url: str):
    """Return the title of the given wikipedia article
    >>> get_title('https://en.wikipedia.org/wiki/Rebecca_Sugar')
    'Rebecca Sugar'
    """

    title = url.replace('https://en.wikipedia.org/wiki/', '')

    return title.replace('_', ' ')


if __name__ == '__main__':
    import doctest
    doctest.testmod()
