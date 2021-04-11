"""CSC111 Winter 2021 Final Project: Making the txt file output

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

import build_wikigraph as bw
import wikipedia_html_parsers as wh
from wikigraph import WikiGraph
from typing import Any, Optional


def make_txt_file(starting_url: str, num_sources: int,
                  sources_per_page: Optional[int] = None) -> None:
    """ Create a text file titled <txt_file> of the collected Wikipedia article networks.
    """
    # make the WikiGraph
    wiki_graph = _make_graph(starting_url, num_sources, sources_per_page)

    # get title
    title = wh.get_title(starting_url)

    # txt file name
    txt_file = title + '_research_summary.txt'

    # create initial file to write
    output_file = open(txt_file, "w")

    # create title
    _make_title(output_file, title, starting_url, num_sources, sources_per_page)

    output_file.close()

    # open the initial file to append
    output_file = open(txt_file, "a")

    # create body
    _make_body_entries(output_file, wiki_graph, starting_url)

    output_file.close()


def _make_graph(starting_url: str, num_sources: int,
                sources_per_page: Optional[int] = None) -> WikiGraph:
    """ Returns a WikiGraph graph based on the <starting_url>, <num_sources>, <sources_per_page>.
    """
    return bw.build_wikigraph(starting_url, num_sources, sources_per_page)


def _make_title(output_file: Any, title: str, starting_url: str, num_sources: int,
                sources_per_page: Optional[int] = None) -> None:
    """ Write the title of the Wikipedia article,
    <starting_url>, <num_sources>, <sources_per_page> (if there is an input for it), and
    a brief summary of it.
    """
    # get title description
    summary = wh.get_summary(starting_url)

    # create title
    header = 'Wikipedia Article Network Research Summary of ' + title
    output_file.write(header + '\n' + '\n')

    # create graph statistics
    starting_url_text = 'Wikipedia URL: '
    output_file.write(starting_url_text + starting_url + '\n')

    num_sources_text = 'Number of Sources: '
    output_file.write(num_sources_text + str(num_sources) + '\n')

    if sources_per_page is not None:
        sources_per_page_text = 'Sources Per Page: '
        output_file.write(sources_per_page_text + str(sources_per_page) + '\n')

    # description
    output_file.write('\n' + summary + '\n')

    # divider
    div = '=========='

    output_file.write('\n' + div * 10 + '\n')

    results = 'results'
    output_file.write(results)

    output_file.write('\n' + div * 10 + '\n')


def _make_body_entries(output_file: Any, wiki_graph: WikiGraph, starting_url: str) -> None:
    """ Write title, url, and a brief summary of the Wikipedia entries."""
    for v in wiki_graph.get_all_vertices():
        if v != wh.get_title(starting_url):
            url = get_url(v)

            title = wh.get_title(url)
            summary = wh.get_summary(url)

            if summary == '':
                print(summary)
                summary = 'Wikipedia article is empty.'

            output_file.write(title + '\n' + '\n')

            output_file.write(url + '\n' + '\n')

            output_file.write(summary + '\n')

            # divider
            div = '=========='
            output_file.write('\n' + div * 10 + '\n')


def get_url(name: str) -> str:
    """ Convert the Wikipedia title to its url. """
    underline = name.replace(' ', '_')
    return 'https://en.wikipedia.org/wiki/' + underline
