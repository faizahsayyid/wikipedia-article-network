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

#import build_wikigraph as bw
import wikipedia_html_parsers as wh
#from typing import Any

# Wiki Graph Variables, will call variables used in the output file when its up on github
# starting_url = 'https://en.wikipedia.org/wiki/Potoooooooo'
# num_sources = 10
# sources_per_page = None

# Txt File Name
txt_file = 'research_summary.txt'

# Building the Wiki Graph, should be the same one as the dash graph
# wiki_graph = bw.build_wikigraph(starting_url, num_sources, sources_per_page)

# Random Constants
DIV = '=========='


def make_txt_file_string(graph_elements, url, title, num_sources, sources_per_page) -> bytes:
    """ Create a text file titled <txt_file> of the collected Wikipedia article networks.
    """
    # # create initial file to write
    # output_file = open(txt_file, "w")
    #
    # # create title
    # _make_title(output_file, url, title, num_sources, sources_per_page)
    #
    # output_file.close()
    #
    # # open the initial file to append
    # output_file = open(txt_file, "a")
    #
    # # create body
    # _make_body_entries(output_file, graph_elements, url)
    #
    # output_file.close()
    start_text = _make_title(url, title, num_sources, sources_per_page, "")
    text = _make_body_entries(graph_elements, url, start_text)
    return text.encode("utf8")



def _make_title(url, title, num_sources, sources_per_page, file_text) -> str:
    """ Write the title of the Wikipedia article,
    <starting_url>, <num_sources>, <sources_per_page> (if there is an input for it), and
    a brief summary of it.
    """
    # get title
    # title = wh.get_title(starting_url)

    # get title description
    summary = wh.get_summary(url)

    # create title
    header = 'Wikipedia Article Network Research Summary of ' + title
    file_text += header + '\n' + '\n'
    # output_file.write(header + '\n' + '\n')

    # create graph statistics
    starting_url_text = 'Wikipedia URL: '
    # output_file.write(starting_url_text + url + '\n')
    file_text += starting_url_text + url + '\n'

    num_sources_text = 'Number of Sources: '
    # output_file.write(num_sources_text + str(num_sources) + '\n')
    file_text += num_sources_text + str(num_sources) + '\n'

    if int(sources_per_page) > 0:
        sources_per_page_text = 'Sources Per Page: '
        # output_file.write(sources_per_page_text + str(sources_per_page) + '\n')
        file_text += sources_per_page_text + str(sources_per_page) + '\n'

    # description
    # output_file.write('\n' + summary + '\n')
    file_text += '\n' + summary + '\n'

    # divider
    # output_file.write('\n' + DIV * 10 + '\n')
    file_text += '\n' + DIV * 10 + '\n'

    # results = 'results'
    # output_file.write(results)
    file_text += 'results'

    # output_file.write('\n' + DIV * 10 + '\n')
    file_text += '\n' + DIV * 10 + '\n'

    return file_text


def _make_body_entries(elements, url, file_text) -> str:
    """ Write title, url, and a brief summary of the Wikipedia entries."""
    if elements is not None:
        for element in elements:
            try:
                if element['data']['id'] != url and \
                        element['data']['id'].split('/')[0] == 'https:':
                    element_url = element['data']['id']

                    title = element['data']['label']
                    summary = wh.get_summary(element_url)

                    if summary == '':
                        print(summary)
                        summary = 'Wikipedia article is empty.'

                    #output_file.write(title + '\n' + '\n')
                    file_text += title + '\n' + '\n'

                    #output_file.write(element_url + '\n' + '\n')
                    file_text += element_url + '\n' + '\n'

                    #output_file.write(summary + '\n')
                    file_text += summary + '\n'

                    #output_file.write('\n' + DIV * 10 + '\n')
                    file_text += '\n' + DIV * 10 + '\n'
            except KeyError:
                continue
    return file_text


def get_url(name: str) -> str:
    """ Convert the Wikipedia title to its url. """
    underline = name.replace(' ', '_')
    return 'https://en.wikipedia.org/wiki/' + underline
