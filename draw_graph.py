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
import build_wikigraph
import wikipedia_html_parsers
import make_txt_file
#import os
#import flask

cyto.load_extra_layouts()
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.Div(
        [html.H5(
            "Input the wikipedia page link that you would like to generate a graph for here!"),
            dcc.Input(
                id='wiki_url_input',
                placeholder='Enter a topic...',
                type='text',
                value='https://en.wikipedia.org/wiki/Alan_Turing',
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
                "Input the number of sources per page you want to generate here! "
                "(Leave this as 0 if you don't want to specify this value)"),
            dcc.Input(
                id='wiki_num_sources_per_page_input',
                placeholder='Enter a number',
                type='text',
                value=5
            ),

            html.Div(children=[html.Button(id='update_graph_button', n_clicks=0,
                                           children='Press to update graph!')],
                     style={
                         'padding-top': '15px',
                         'padding-bottom': '30px'
                     }),
            html.Button(id='generate_txt_file', n_clicks=0,
                        children='Press to download a txt file '
                                 'of all nodes in the graph!'),
            html.Div(id='txt_download_area')],
        style={
            'width': '27%',
            'float': 'left',
            'border-style': 'solid',
            'padding': '.5em .5em .5em .5em',
            'margin-top': '4em'
        }
    ),

    html.Div(children=[html.H6('Generated Graph:'),
                       cyto.Cytoscape(
                           id='cytoscape_wiki_graph',
                           layout={
                               'name': 'cose-bilkent'
                           },
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
        'background-color': '#191308',
        'opacity': '1'
    }
)


@app.callback(
    Output('cytoscape_wiki_graph', 'elements'),
    Output('cytoscape_wiki_graph', 'stylesheet'),
    Input('update_graph_button', 'n_clicks'),
    State('wiki_url_input', 'value'),
    State('wiki_num_sources_input', 'value'),
    State('wiki_num_sources_per_page_input', 'value')
)
def update_cytoscape_display(n_clicks, url, num_sources, sources_per_page):
    # Going to add try catch here later - we should do some error catching the the
    # BFS search so that we know what exceptions to catch
    style_sheet = [{
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
            'color': '#03254E'
        }
    }
    ]

    if n_clicks > -1 and int(sources_per_page) < 1:
        new_graph = build_wikigraph.build_wikigraph(url, int(num_sources))
    else:
        new_graph = build_wikigraph.build_wikigraph(url, int(num_sources), int(sources_per_page))
    graph_elements = new_graph.to_cytoscape()
    for vertex in new_graph.get_all_vertices():
        temp_width = len(vertex) + 1
        if new_graph.get_vertex(vertex).url == url:
            temp_width += 15
            temp_height = temp_width
        else:
            temp_height = int(temp_width * .3)
        temp_font_size = max(int(temp_width * .025) + int(temp_height * .1), 1)

        # if new_graph.get_vertex(vertex).url == url:
        #     style_sheet.append({
        #         'selector': '.' + new_graph.get_class_id(vertex),
        #         'style': {
        #             'background-color': '#cca43b',
        #             'width': str(em_len) + 'em',
        #             'label': vertex
        #         }
        #     })
        # else:
        if new_graph.get_image(vertex) == '':
            style_sheet.append({
                'selector': '.' + new_graph.get_class_id(vertex),
                'style': {
                    'height': str(temp_height) + 'em',
                    'width': str(temp_width) + 'em',
                    'label': vertex,
                    'font-size': str(temp_font_size) + 'em'
                }
            })
        else:
            style_sheet.append({
                'selector': '.' + new_graph.get_class_id(vertex),
                'style': {
                    'height': str(temp_height) + 'em',
                    'width': str(temp_width) + 'em',
                    'label': vertex,
                    'font-size': str(temp_font_size) + 'em',
                    'background-fit': 'cover',
                    'background-image': new_graph.get_image(vertex)
                }
            })
    return graph_elements, style_sheet


@app.callback(Output('cytoscape_article', 'children'),
              Output('cytoscape_url', 'children'),
              Output('cytoscape_summary', 'children'),
              Input('cytoscape_wiki_graph', 'tapNodeData'))
def displayTapNodeData(data):
    if data:
        try:
            summary = wikipedia_html_parsers.get_summary(data['id'])
            return ("Article: '" + data['label'] + "'", "URL: " + data['id'],
                    'Summary: ' + summary)
        except KeyError:
            return ("", "", "")


@app.callback(
    Output('txt_download_area', 'children'),
    Input('generate_txt_file', 'n_clicks'),
    State('cytoscape_wiki_graph', 'elements'),
    State('wiki_url_input', 'value'),
    State('wiki_num_sources_input', 'value'),
    State('wiki_num_sources_per_page_input', 'value')
)
def create_txt_download(n_clicks, graph_elements, url, num_s, num_s_per_page):
    if n_clicks > -1 and graph_elements is not None:
        title = url.replace('https://en.wikipedia.org/wiki/', '')
        filename = f"{title}.txt"
        path = f"txt_file_downloads/{filename}"
        graph_text = make_txt_file.make_txt_file_string(graph_elements, url,
                                                        title, num_s, num_s_per_page)
        with open(path, "wb") as file:
            file.write(graph_text)
        return ""

#
# @app.server.route('/txt_file_downloads/<path>')
# def serve_static(path):
#     root_dir = os.getcwd()
#     return flask.send_from_directory(
#         os.path.join(root_dir, 'txt_file_downloads'), path
#     )


if __name__ == '__main__':
    app.run_server(debug=True, port=3004)
