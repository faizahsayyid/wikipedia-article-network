"""CSC111 Winter 2021 Final Project: Parsing Wikipedia Pages

Module Description
===============================

This module contains functions and classes used to parse wikipedia article links and
summaries from a specific wikipedia article.

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
            'Module talk:', 'User:', ':', '(disambiguation)', 'Main_Page']


class WikipediaArticleParser(HTMLParser):
    """A Wikipedia article parser, used to extract Wikipedia links from html code.

    This article parser does not include wikipedia links that contain links from UNWANTED.

    Instance Attributes:
        - articles: a list of wikipedia links parsed from html code

    Representation Invariants:
        - all("https://en.wikipedia.org/wiki/" in a for a in self.articles)
        - all(all(k not in a for k in UNWANTED) for a in self.articles)
        - all(self.articles.count(a) == 1 for a in self.articles)
    """
    articles: list[str]
    original_url: str

    def __init__(self, original_url: str) -> None:
        """Initialize a new article parser.

        This article parser is initialized an empty list of articles and
        the given <original_url>.
        """
        super().__init__()
        self.articles = []
        self.reset()
        self.original_url = original_url

    def error(self, message: str) -> None:
        """Help on function error in module _markupbase

        (This method needed to be implemented for the abstract super class HTMLParser,
         but doesn't do anything)
        """

    def handle_starttag(self, tag: str, attrs: list[tuple]) -> None:
        """Parse wikipedia links from html file.
        Add those wikipedia links to self.articles.
        """
        # Only parse the <a> tags.
        if tag == "a":
            for attribute in attrs:
                name, link = attribute
                unwanted_page = any((unwanted in link) for unwanted in UNWANTED)

                self._add_article(name, link, unwanted_page)

    def _add_article(self, name: str, link: str, unwanted_page: bool) -> None:
        """Add <link> to self.articles if name is 'href' (meaning it is actually a link
        and not different attribute), if <unwanted_page> is false, and if <link> is a
        wikipedia article"""
        if name == "href" and link.startswith('/wiki/') and not unwanted_page:
            link = 'https://en.wikipedia.org' + link
            if link not in self.articles and link != self.original_url:
                self.articles.append(link)


class WikipediaSummaryParser(HTMLParser):
    """A Wikipedia summary parser, used to extract the summary of a Wikipedia article
    from the html code of the article.

    Instance Attributes:
        - summary: the summary of the article being parsed
        - sentences_wanted: the number of sentences to parse

    Representation Invariants:
        - self.summary.count('.') <= self.sentences_wanted
    """
    # Private Instance Attributes:
    #     - _found_p:
    #         whether or not we are inside a <p> tag
    #     - _skip_footnote:
    #         whether or not we are inside a <sup> tag

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

    def error(self, message: str) -> None:
        """Help on function error in module _markupbase

        (This method needed to be implemented for the abstract super class HTMLParser,
         but doesn't do anything)
        """

    def handle_starttag(self, tag: str, attrs: list[tuple]) -> None:
        """Update self._found_p if tag is <p>
        Update self._skip_footnote whenever a footnote is encountered in the summary
        (if tag is <sup>)

        >>> summary_parser = WikipediaSummaryParser()
        >>> summary_parser.handle_starttag('p', [])
        >>> summary_parser._found_p
        True
        >>> summary_parser.handle_starttag('sup', [])
        >>> summary_parser._skip_footnote
        True
        >>> summary_parser.handle_starttag('h1', [])
        >>> summary_parser._found_p
        True
        >>> summary_parser._skip_footnote
        True
        """
        if tag == 'p':
            self._found_p = True

        if tag == 'sup':
            self._skip_footnote = True

    def handle_endtag(self, tag: str) -> None:
        """Update self._found_p if tag is <p>
        Update self._skip_footnote the end of a footnote is reached (if tag is <sup>)

        >>> summary_parser = WikipediaSummaryParser()
        >>> summary_parser.handle_endtag('p')
        >>> summary_parser._found_p
        False
        >>> summary_parser.handle_endtag('sup')
        >>> summary_parser._skip_footnote
        False
        >>> summary_parser.handle_endtag('h1')
        >>> summary_parser._found_p
        False
        >>> summary_parser._skip_footnote
        False
        """
        if tag == 'p':
            self._found_p = False

        if tag == 'sup':
            self._skip_footnote = False

    def handle_data(self, data: str) -> None:
        """Add parts of the summary of the article to self.summary"""
        if self._found_p and (self.summary.count('.') < self.sentences_wanted) \
                and not self._skip_footnote and data != '\n':
            self.summary += data
            if (self.summary.count('.') >= self.sentences_wanted) \
                    and not self.summary.endswith('.'):
                index_of_last_period = self.summary.rindex('.')
                self.summary = self.summary[:index_of_last_period + 1]
            elif self.summary.count('.') > self.sentences_wanted:
                sentences = self.summary.split('.')
                self.summary = '.'.join(sentences[:2]) + '.'
        elif self.summary.count('.') > self.sentences_wanted:
            sentences = self.summary.split('.')
            self.summary = '.'.join(sentences[:2]) + '.'


def get_adjacent_urls(url: str) -> list[str]:
    """Return a list of all wikipedia pages that are adjacent to <url>"""
    try:
        data_to_parse = urllib.request.urlopen(url)
        html = data_to_parse.read().decode()
        data_to_parse.close()

        parser = WikipediaArticleParser(url)
        parser.feed(html)

        return parser.articles

    except urllib.error.HTTPError:
        return []


def get_adjacent_urls_weighted(url: str) -> list:
    """Return a list in where each element is in the format ((link, name) weight)
    for each wikipedia page that is adjacent to <url>
    """

    try:
        data_to_parse = urllib.request.urlopen(url)
        html = data_to_parse.read().decode()
        data_to_parse.close()

        parser = WikipediaArticleParser(url)
        parser.feed(html)

        neighbours_to_weights = {}

        for article_link in parser.articles:
            if article_link != url:
                article_name = get_title(article_link)
                weight1 = html.count(article_name)
                neighbours_to_weights[(article_link, article_name)] = weight1

        return sorted(list(neighbours_to_weights.items()),
                      key=lambda item: item[1], reverse=True)

    except urllib.error.HTTPError:
        return []


def get_summary(url: str, sentences_wanted: int = 2) -> str:
    """Return the summary of the given wikipedia article with <sentences_wanted> being
    the number of sentences in the summary
    (the summary may contain less than <sentences_wanted> sentence if the article
    corresponding to <url> only has one sentence in it)

    Precondition
        - 'https://en.wikipedia.org/wiki/' in url
    """
    data_to_parse = urllib.request.urlopen(url)
    html = data_to_parse.read().decode()
    data_to_parse.close()

    parser = WikipediaSummaryParser(sentences_wanted)
    parser.feed(html)

    return parser.summary


def get_title(url: str) -> str:
    """Return the title of the given wikipedia article

    >>> get_title('https://en.wikipedia.org/wiki/Rebecca_Sugar')
    'Rebecca Sugar'
    """

    title = url.replace('https://en.wikipedia.org/wiki/', '')

    return title.replace('_', ' ')


if __name__ == '__main__':

    import doctest
    doctest.testmod()

    import python_ta.contracts

    python_ta.contracts.check_all_contracts()

    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['urllib.error', 'urllib.request', 'html.parser'],
        'allowed-io': [],
        'max-line-length': 100,
        'disable': ['E1136']
    })
