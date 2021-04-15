"""CSC111 Winter 2021 Final Project: Graph Visualization

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

import dash
import dash_cytoscape as cyto
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import build_wikigraph_weighted
import wikipedia_html_parsers
import make_txt_file

cyto.load_extra_layouts()

css_stylesheet = [{'body': {
    'font-size': '4em',
    'font-family': "'Open Sans', 'Arial'",
    'line-height': '1.6',
    'font-weight': '400'
}}]

app = dash.Dash(__name__, external_stylesheets=css_stylesheet)

# Layout and initial styling of app
app.layout = html.Div(children=[
    html.Div(
        [
            html.H5(
                "Input the wikipedia page link that you would like to generate a graph for here!"),
            dcc.Input(
                id='wiki_url_input',
                placeholder='Enter a topic...',
                type='text',
                value='https://en.wikipedia.org/wiki/Computer_graphics',
                style={'width': '100%'}
            ),
            html.H5(
                "Input the total number of sources you want to generate here!"),
            dcc.Input(
                id='wiki_num_sources_input',
                placeholder='Enter a number',
                type='text',
                value=30
            ),

            html.H5(
                "Input the number of sources per page you want to generate here!"),
            dcc.Input(
                id='wiki_num_sources_per_page_input',
                placeholder='Enter a number',
                type='text',
                value=5
            ),

            dcc.RadioItems(id='images_selection',
                           options=[
                               {'label': 'Background Images on (Slower)', 'value': 'on'},
                               {'label': 'Background Images off (Faster)', 'value': 'off'}
                           ],
                           value='off',
                           style={
                               'padding-top': '1em'
                           }),
            dcc.RadioItems(id='graph_type_selection',
                           options=[
                               {'label': '(Weighted) Most common links on page',
                                'value': 'weighted'},
                               {'label': '(Unweighted) First links on page', 'value': 'unweighted'}
                           ],
                           value='weighted',
                           style={
                               'padding-top': '1em',
                               'padding-bottom': '1em'
                           }),

            html.Div(children=[
                html.Button(id='update_graph_button', n_clicks=0,
                            children='Press to update graph!',
                            style={
                                'text-align': 'left'
                            }),
                dcc.Loading(id="loading_graph",
                            type="circle",
                            children=html.Div(id="loading_graph_output"),
                            style={
                                'text-justify': 'right',
                                'padding-bottom': '2em'
                            })
            ],
                style={
                    'padding-bottom': '2em',
                    'padding-top': '1.5em'
                }
            ),

            html.Div(children=[
                html.Button(id='generate_txt_file', n_clicks=0,
                            children='Press to download a txt file '
                                     'of all nodes in the graph!'),
                dcc.Download(id='txt_download', children='Pls Work'),
                dcc.Loading(id="loading_file",
                            type="circle",
                            children=html.Div(id="loading_file_output"),
                            style={
                                'text-justify': 'right',
                                'padding-left': '15em',
                                'padding-bottom': '1em'
                            })
            ],
                style={
                    'padding-bottom': '2em'
                }
            )
        ],
        style={
            'width': '27%',
            'float': 'left',
            'padding': '.5em .5em .5em .5em',
            'border-style': 'solid',
            'margin-top': '4em',
        }
    ),

    html.Div(children=[html.H6('Generated Graph:'),
                       cyto.Cytoscape(
                           id='cytoscape_wiki_graph',
                           layout={
                               'name': 'dagre',
                               'padding': '50',
                               'avoidOverlap': 'true'
                           },
                           stylesheet=[{
                               'selector': 'node',
                               'style': {
                                   'shape': 'ellipse',
                                   'text-valign': 'center',
                                   'text-background-shape': 'round-rectangle',
                                   'text-background-color': '#f0f0f0',
                                   'text-background-opacity': '1',
                                   'text-background-padding': '.25em',
                                   'background-color': '#011C27',
                                   'text-border-opacity': '1',
                                   'text-border-color': '#242F40',
                                   'text-border-width': '2px',
                                   'text-border-style': 'solid',
                                   'color': '#03254E',
                                   'text-wrap': 'wrap'
                               }
                           }],
                           style={'width': '100%', 'height': '45em', 'border-style': 'solid'},
                       )],
             style={
                 'width': '70%',
                 'float': 'right'
             }),

    html.Div(children=[html.H5(id='cytoscape_url', children=""),
                       html.H5(id='cytoscape_article', children=""),
                       html.H5(id='cytoscape_summary', children="")],
             style={
                 'width': '70%',
                 'height': '14em',
                 'border-style': 'solid',
                 'float': 'right',
                 'padding': '.25em .25em .25em .25em',
                 'margin': '.25em .25em .25em .25em'
             })
],
    style={
        'opacity': '1'
    }
)


# Callback functions to make the graph interactive:

@app.callback(
    Output('cytoscape_wiki_graph', 'elements'),
    Output('cytoscape_wiki_graph', 'stylesheet'),
    Output("loading_graph_output", "children"),
    Input('update_graph_button', 'n_clicks'),
    State('images_selection', 'value'),
    State('graph_type_selection', 'value'),
    State('wiki_url_input', 'value'),
    State('wiki_num_sources_input', 'value'),
    State('wiki_num_sources_per_page_input', 'value'),
    State('cytoscape_wiki_graph', 'stylesheet'))
def update_cytoscape_display(n_clicks, images, weighting, url, num_sources, sources_per_page,
                             style_sheet) -> (list[dict], list[dict], None):
    """This function builds the cytoscape graph and transforms that graph in to the correct
    cytoscape format. It also adds styling to the graph as it is built"""
    # Initially builds the graph,
    # with an if statement determining whether to use a weighted graph or an unweighted graph
    if n_clicks > -1 and weighting == 'weighted':
        new_graph = build_wikigraph_weighted.build_weighted_wikigraph(url, int(num_sources), max(
            int(sources_per_page), 0))
    else:
        new_graph = build_wikigraph_weighted.build_wikigraph(url, int(num_sources), max(
            int(sources_per_page), 0))

    # Converts the graph to a cytoscape graph
    graph_elements = new_graph.to_cytoscape()

    # For Loop to add styling and sizing to each element
    for vertex in new_graph.get_all_vertices():
        if images == 'on':
            temp_image = wikipedia_html_parsers.get_image(new_graph.get_vertex(vertex).url)
        else:
            temp_image = ''

        # Separate size handling for when the node is the root page, or has a long or short title
        if new_graph.get_vertex(vertex).url == url:
            temp_width = len(vertex) + 20
            temp_height = temp_width
            temp_font_size = 3
        elif len(vertex) > 12:
            temp_width = len(vertex)
            temp_height = max(temp_width * .4, 2)
            temp_font_size = max(temp_height * .15, 1)
        else:
            temp_width = len(vertex) + 5
            temp_height = max(temp_width * .7, 2)
            temp_font_size = max(temp_height * .2, 1)

        # Adds calculated sizing styling to node.
        # Also checks if the node has a background image or not before attempting to add one to
        # avoid errors
        if temp_image == '':
            style_sheet.append({
                'selector': '.' + new_graph.get_class_id(vertex),
                'style': {
                    'height': str(temp_height) + 'em',
                    'width': str(temp_width) + 'em',
                    'text-max-width': str(temp_width - 2) + 'em',
                    'label': vertex,
                    'font-size': str(temp_font_size) + 'em',
                    'background-image-opacity': '0'
                }
            })
        else:
            style_sheet.append({
                'selector': '.' + new_graph.get_class_id(vertex),
                'style': {
                    'height': str(temp_height) + 'em',
                    'width': str(temp_width) + 'em',
                    'text-max-width': str(temp_width - 2) + 'em',
                    'label': vertex,
                    'font-size': str(temp_font_size) + 'em',
                    'background-fit': 'cover',
                    'background-image': temp_image,
                    'background-image-opacity': '1'
                }
            })

    return graph_elements, style_sheet, None


@app.callback(Output('cytoscape_article', 'children'),
              Output('cytoscape_url', 'children'),
              Output('cytoscape_summary', 'children'),
              Input('cytoscape_wiki_graph', 'tapNodeData'))
def display_name_summary_link_infobox(data) -> (str, str, str):
    """This function outputs the link, title, and summary of the selected article node in to the
    infobox below the cytoscape graph"""
    if data:
        try:
            # This retrieves the summary of the selected article using an html parser
            summary = wikipedia_html_parsers.get_summary(data['id'])
            return ("Article: '" + data['label'] + "'", "URL: " + data['id'],
                    'Summary: ' + summary)
        except NameError:
            return ("Once an article is selected, it's information will appear here", "", "")
    else:
        return ("Once an article is selected, it's information will appear here", "", "")


@app.callback(
    Output('txt_download', 'data'),
    Output('loading_file_output', 'children'),
    Input('generate_txt_file', 'n_clicks'),
    State('cytoscape_wiki_graph', 'elements'),
    State('wiki_url_input', 'value'),
    State('wiki_num_sources_input', 'value'),
    State('wiki_num_sources_per_page_input', 'value')
)
def create_txt_download(n_clicks, graph_elements, url, num_s, num_s_per_page) -> (dict, None):
    """This function builds the content of a text file of all elements in the graph for the user
    after the graph is updated, which is then sent to the dcc.download component to be downloaded by
    the user. """
    # Check that there are graph elements to write to a file
    if graph_elements is not None and n_clicks > 0:
        # Get the title from the url and use it for the filename
        title = url.replace('https://en.wikipedia.org/wiki/', '')
        filename = f"{title}.txt"

        # Call a helped function to write out the file content string that will be downloaded
        graph_text = make_txt_file.make_txt_file_string(graph_elements, url,
                                                        title, num_s, num_s_per_page)

        # Adds the content and filename to a dictionary format as this format is required by the
        # dcc.download component, which will download this content in a text file for the user
        data = {
            'content': graph_text,
            'filename': filename
        }
        return data, None
    else:
        # Return none so that nothing is downloaded if the callback runs unexpectedly
        return None, None


if __name__ == '__main__':
    app.run_server(debug=True, port=3004)
