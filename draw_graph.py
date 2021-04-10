import dash
import dash_cytoscape as cyto
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import BFS_Search_copy

cyto.load_extra_layouts()
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

initial_graph = BFS_Search_copy.bfs_wikipedia('https://en.wikipedia.org/wiki/Emiko_Iiyama', 1)
initial_graph_elements = initial_graph.to_cytoscape()

app.layout = html.Div([
    html.Div([html.H5("Input the wikipedia page link that you would like to generate a graph for here!"),
    dcc.Input(
        id='wiki_url_input',
        placeholder='Enter a topic...',
        type='text',
        value='https://en.wikipedia.org/wiki/Emiko_Iiyama',
        style={'width': '100%'}
    ),
    html.H5(
        "Input the number of sources you want to generate here!"),
    dcc.Input(
        id='wiki_num_sources_input',
        placeholder='Enter a number',
        type='text',
        value=1
    ),

    html.H5(
        "Input the total number of sources per page you want to generate here! "
        "(Leave this as 0 if you don't want to specify this value)"),
    dcc.Input(
        id='wiki_num_sources_per_page_input',
        placeholder='Enter a number',
        type='text',
        value=0
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

    )], style={
        'width': '70%',
        'float': 'right'
    }),

    html.H5(id='cytoscape_url_and_name_selected', style={
        'width': '70%',
        'height': '5em',
        'border-style': 'solid',
        'float': 'right',
        'padding': '.25em .25em .25em .25em'
        })
])


@app.callback(
    Output('cytoscape_wiki_graph', 'elements'),
    Input('update_graph_button', 'n_clicks'),
    State('wiki_url_input', 'value'),
    State('wiki_num_sources_input', 'value'),
    State('wiki_num_sources_per_page_input', 'value')
)
def update_cytoscape_display(n_clicks, url, num_sources, sources_per_page):
    #Going to add try catch here later - we should do some error catching the the
    #BFS search so that we know what exceptions to catch
    if n_clicks > -1 and int(sources_per_page) < 1:
        new_graph = BFS_Search_copy.bfs_wikipedia(url, int(num_sources))
        graph_elements = new_graph.to_cytoscape()
        return graph_elements
    else:
        new_graph = BFS_Search_copy.bfs_wikipedia(url, int(num_sources), int(sources_per_page))
        graph_elements = new_graph.to_cytoscape()
        return graph_elements


@app.callback(Output('cytoscape_url_and_name_selected', 'children'),
              Input('cytoscape_wiki_graph', 'tapNodeData'))
def displayTapNodeData(data):
    if data:
        return "You clicked on the article '" + data['label'] + "' with the url " \
                + data['id']


if __name__ == '__main__':
    app.run_server(debug=True, port=3004)
