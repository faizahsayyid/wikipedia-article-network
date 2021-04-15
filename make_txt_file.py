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
import wikipedia_html_parsers as wh

# Constant for divider
DIV = '=========='


def make_txt_file_string(graph_elements: list, url: str, title: str, num_sources: str,
                         sources_per_page: str) -> str:
    """ Create a text file titled <txt_file> of the collected Wikipedia article networks.
    """
    start_text = _make_title(url, title, num_sources, sources_per_page, "")
    text = _make_body_entries(graph_elements, url, start_text)
    return text


def _make_title(url: str, title: str, num_sources: str, sources_per_page: str,
                file_text: str) -> str:
    """ Write the title of the Wikipedia article,
    <starting_url>, <num_sources>, <sources_per_page> (if there is an input for it), and
    a brief summary of it.
    """
    # get title

    # get title description
    summary = wh.get_summary(url)

    # create title
    header = 'Wikipedia Article Network Research Summary of ' + title
    file_text += header + '\n' + '\n'

    # create graph statistics
    starting_url_text = 'Wikipedia URL: '
    # output_file.write(starting_url_text + url + '\n')
    file_text += starting_url_text + url + '\n'

    num_sources_text = 'Number of Sources: '
    file_text += num_sources_text + str(num_sources) + '\n'

    if int(sources_per_page) > 0:
        sources_per_page_text = 'Sources Per Page: '
        file_text += sources_per_page_text + str(sources_per_page) + '\n'

    # description
    file_text += '\n' + summary + '\n'

    # divider
    file_text += '\n' + DIV * 10 + '\n'

    # results = 'results'
    file_text += 'results'

    file_text += '\n' + DIV * 10 + '\n'

    return file_text


def _make_body_entries(elements: list, url: str, file_text: str) -> str:
    """ Write title, url, and a brief summary of the Wikipedia entries."""
    if elements is None:
        return file_text

    for element in elements:
        try:
            if element['data']['id'] != url and \
                    element['data']['id'].split('/')[0] == 'https:':
                element_url = element['data']['id']

                title = element['data']['label']
                summary = wh.get_summary(element_url)

                if summary == '':
                    summary = 'Wikipedia article is empty.'

                file_text += title + '\n' + '\n'

                file_text += element_url + '\n' + '\n'

                file_text += summary + '\n'

                file_text += '\n' + DIV * 10 + '\n'
        except KeyError:
            continue

    return file_text


def get_url(name: str) -> str:
    """ Convert the Wikipedia title to its url. """
    underline = name.replace(' ', '_')
    return 'https://en.wikipedia.org/wiki/' + underline


if __name__ == '__main__':
    import python_ta.contracts

    python_ta.contracts.check_all_contracts()

    import python_ta

    python_ta.check_all(config={
        'max-line-length': 100,
        'disable': ['E1136', 'E9999'],
        'max-nested-blocks': 4
    })
