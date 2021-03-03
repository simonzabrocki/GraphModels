import dash
import dash_cytoscape as cyto
import dash_html_components as html
from dash.dependencies import Input, Output
from models.Sarah.model_EW import MWU_nodes, EW1_nodes, concatenate_graph_specs
from graphmodels.graphmodel import GraphModel
import networkx as nx

model_dictionnary = {
    'EW1': GraphModel(concatenate_graph_specs([MWU_nodes, EW1_nodes]))
}

cyto.load_extra_layouts()

app = dash.Dash(__name__)


stylesheet = [
    # Group selectors
    {
        'selector': 'node',

        'style': {'content': 'data(type)',
                  'label': 'data(id)',
                  'text-halign': 'center',
                  'text-valign': 'center',
                  'height': 80, 'width': 80}
    },
    {
        'selector': 'edge',
        'style': {
            'curve-style': 'bezier',
            'target-arrow-shape': 'triangle',
        }
    },
    {'selector': '[type = "input"]',
     'style': {
         'background-color': '#e76f51',
     }
     },
    {'selector': '[type = "parameter"]',
     'style': {
         'background-color': '#e9c46a',
     }
     },
    {'selector': '[type = "variable"]',
     'style': {
         'background-color': '#f4a261',
     }
     },
    {'selector': '[type = "output"]',
     'style': {
         'background-color': '#2a9d8f',
         'height': 150, 'width': 150,
     }
     },
]



def GraphModel_to_cytodata(model):
    data = nx.readwrite.json_graph.cytoscape_data(model)
    
    for dic in data['elements']['nodes']:
        if 'formula' in dic['data']:
            del dic['data']['formula']
            
    return data
            
data = GraphModel_to_cytodata(model_dictionnary['EW1'])

def plot_graphmodel(model, stylesheet=stylesheet):
    cytoscape_data = GraphModel_to_cytodata(model)
    print(cytoscape_data['elements'])
    layout = html.Div([
        html.P(id='cytoscape-mouseoverNodeData-output'),
        cyto.Cytoscape(
            id='cytoscape-graph-model',
            layout={'name': 'dagre', 'roots': '[type="EW1"]'},
            style={'width': '100%', 'height': '1000px'},
            elements=cytoscape_data['elements'],
            stylesheet=stylesheet,
        ),
    ]
    )

    return layout


app.layout = plot_graphmodel(model_dictionnary['EW1'])

@app.callback(Output('cytoscape-mouseoverNodeData-output', 'children'),
              Input('cytoscape-graph-model', 'mouseoverNodeData'))
def displayTapNodeData(data):
    if data:
        if data['type'] != 'computationnal':
            return f"This node represents the {data['type']} {data['name']} expressed in {data['unit']}."
        else:
            return f"This node computes {data['out']} = {data['name']}"


if __name__ == '__main__':
    app.run_server(debug=True, host='localhost')

