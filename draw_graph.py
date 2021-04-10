import dash
import dash_cytoscape as cyto
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import build_wikigraph
import wikipedia_html_parsers

cyto.load_extra_layouts()
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

initial_graph = build_wikigraph.build_wikigraph('https://en.wikipedia.org/wiki/Wikipedia', 20, 5)
initial_graph_elements = initial_graph.to_cytoscape()

app.layout = html.Div(children=[
    html.Div(
        [html.H5(
            "Input the wikipedia page link that you would like to generate a graph for here!"),
            dcc.Input(
                id='wiki_url_input',
                placeholder='Enter a topic...',
                type='text',
                value='https://en.wikipedia.org/wiki/Wikipedia',
                style={'width': '100%'}
            ),
            html.H5(
                "Input the number of sources you want to generate here!"),
            dcc.Input(
                id='wiki_num_sources_input',
                placeholder='Enter a number',
                type='text',
                value=20
            ),

            html.H5(
                "Input the total number of sources per page you want to generate here! "
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
                     })],
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
                               'name': 'klay'
                           },
                           style={'width': '100%', 'height': '50em', 'border-style': 'solid'},
                           elements=initial_graph_elements
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
                 'height': '9em',
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
            'height': '3em',
            'shape': 'ellipse',
            'text-valign': 'center',
            'text-background-shape': 'round-rectangle',
            'text-background-color': '#f0f0f0',
            'text-background-opacity': '1',
            'text-background-padding': '.25em',
            'background-color': '#011C27',
            'color': '#03254E'
        }
    }]

    if n_clicks > -1 and int(sources_per_page) < 1:
        new_graph = build_wikigraph.build_wikigraph(url, int(num_sources))
        graph_elements = new_graph.to_cytoscape()
        for vertex in new_graph.get_all_vertices():
            em_len = len(vertex) + 1
            style_sheet.append({
                'selector': '.' + new_graph.get_class_id(vertex),
                'style': {
                    'width': str(em_len) + 'em',
                    'label': vertex
                }
            })
        return graph_elements, style_sheet
    else:
        new_graph = build_wikigraph.build_wikigraph(url, int(num_sources), int(sources_per_page))
        graph_elements = new_graph.to_cytoscape()
        for vertex in new_graph.get_all_vertices():
            em_len = len(vertex) + 1
            style_sheet.append({
                'selector': '.' + new_graph.get_class_id(vertex),
                'style': {
                    'width': str(em_len) + 'em',
                    'label': vertex
                }
            })
        return graph_elements, style_sheet


@app.callback(Output('cytoscape_article', 'children'),
              Output('cytoscape_url', 'children'),
              Output('cytoscape_summary', 'children'),
              Input('cytoscape_wiki_graph', 'tapNodeData'))
def displayTapNodeData(data):
    if data:
        summary = wikipedia_html_parsers.get_summary(data['id'])
        return ("Article: '" + data['label'] + "'", "URL: " + data['id'],
                'Summary: ' + summary)


if __name__ == '__main__':
    app.run_server(debug=True, port=3004)
