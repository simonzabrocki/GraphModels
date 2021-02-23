import dash
import dash_cytoscape as cyto
import dash_html_components as html
from dash.dependencies import Input, Output

cyto.load_extra_layouts()

app = dash.Dash(__name__)


data = {
 'elements': {'nodes': [{'data': {'type': 'input',
     'unit': '$/15m3',
     'name': 'Water Price',
     'id': 'WP',
     'value': 'WP'}},
   {'data': {'type': 'parameter',
     'unit': '$',
     'name': 'GDP per capita',
     'id': 'GDPC',
     'value': 'GDPC'}},
   {'data': {'type': 'parameter',
     'unit': 'capita',
     'name': 'Population',
     'id': 'Pop',
     'value': 'Pop'}},
   {'data': {'type': 'variable',
     'unit': 'm3/year',
     'name': 'Municipal Water Withdrawal',
     'id': 'MWU',
     'value': 'MWU'}},
   {'data': {
     'name': 'model_MWU(GDPC, WP, Pop)',
     'out': 'MWU',
     'in': ['GDPC', 'WP', 'Pop'],
     'type': 'computationnal',
     'id': 'MWU_comp',
     'value': 'MWU_comp'}},
   {'data': {'type': 'input',
     'unit': 'm3/year',
     'name': 'Industrial Water Withdrawal',
     'id': 'IWU',
     'value': 'IWU'}},
   {'data': {'type': 'input',
     'unit': 'm3/year',
     'name': 'Agricultural Water Withdrawal',
     'id': 'AWU',
     'value': 'AWU'}},
   {'data': {'type': 'variable',
     'unit': 'm3/year',
     'name': 'Total Water Withdrawal',
     'id': 'TWW',
     'value': 'TWW'}},
   {'data': {
     'name': 'AWU + IWU + MWU',
     'out': 'TWW',
     'in': ['AWU', 'IWU', 'MWU'],
     'type': 'computationnal',
     'id': 'TWW_comp',
     'value': 'TWW_comp'}},
   {'data': {'type': 'parameter',
     'unit': '$',
     'name': 'Agricultural Gross Value Added',
     'id': 'AGVA',
     'value': 'AGVA'}},
   {'data': {'type': 'parameter',
     'unit': '$',
     'name': 'Industrial Gross Value Added',
     'id': 'IGVA',
     'value': 'IGVA'}},
   {'data': {'type': 'parameter',
     'unit': '$',
     'name': 'Service Sector Gross Value Added',
     'id': 'SGVA',
     'value': 'SGVA'}},
   {'data': {'type': 'output',
     'unit': '$/(m3/year)',
     'name': 'Water Use Efficiency',
     'id': 'EW1',
     'value': 'EW1'}},
   {'data': {
     'name': '1e-9 * (IGVA + SGVA + AGVA) / TWW',
     'out': 'EW1',
     'in': ['TWW', 'IGVA', 'SGVA', 'AGVA'],
     'type': 'computationnal',
     'id': 'EW1_comp',
     'value': 'EW1_comp'}}],
  'edges': [{'data': {'source': 'WP', 'target': 'MWU_comp'}},
   {'data': {'source': 'GDPC', 'target': 'MWU_comp'}},
   {'data': {'source': 'Pop', 'target': 'MWU_comp'}},
   {'data': {'source': 'MWU', 'target': 'TWW_comp'}},
   {'data': {'source': 'MWU_comp', 'target': 'MWU'}},
   {'data': {'source': 'IWU', 'target': 'TWW_comp'}},
   {'data': {'source': 'AWU', 'target': 'TWW_comp'}},
   {'data': {'source': 'TWW', 'target': 'EW1_comp'}},
   {'data': {'source': 'TWW_comp', 'target': 'TWW'}},
   {'data': {'source': 'AGVA', 'target': 'EW1_comp'}},
   {'data': {'source': 'IGVA', 'target': 'EW1_comp'}},
   {'data': {'source': 'SGVA', 'target': 'EW1_comp'}},
   {'data': {'source': 'EW1_comp', 'target': 'EW1'}}]}}



app.layout = html.Div([
        html.P(id='cytoscape-mouseoverNodeData-output'),

    cyto.Cytoscape(
        id='cytoscape-graph-model',
        layout={'name': 'dagre', 'roots': '[id="EW1"]'},
        style={'width': '100%', 'height': '1000px'},
        elements=data['elements'],
        stylesheet=[
        # Group selectors
        {
            'selector': 'node',
             
            'style': {'content': 'data(type)',
                      'label': 'data(id)',
                     'text-halign':'center',
                     'text-valign':'center',
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
        }},
        {'selector': '[type = "parameter"]',
            'style': {
                'background-color': '#e9c46a',
        }},
        {'selector': '[type = "variable"]',
            'style': {
                'background-color': '#f4a261',
        }},
        {'selector': '[type = "output"]',
            'style': {
                'background-color': '#2a9d8f',
                'height': 150, 'width': 150,
        }},
            
        ]
    ),
])

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
