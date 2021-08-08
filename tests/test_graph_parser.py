import pytest
from GraphModels.graphmodels.graphmodel import GraphParser


nodes_1 = {
    'In_1': {'type': 'input',
             'unit': '1',
             'name': 'Input 1'},
    'Par_1': {'type': 'parameter',
              'unit': '1',
              'name': 'Parameter 1'},
    'Var_1': {'type': 'variable',
              'name': 'Variable 1',
              'unit': '1',
              'computation': lambda Par_1, In_1, **kwargs: Par_1 * In_1
              },
    'Par_3': {'type': 'parameter',
              'unit': '1',
              'name': 'Parameter 3'},
    'Out_1': {'type': 'output',
              'name': 'Output 1',
              'unit': '1',
              'computation': lambda Var_1, Var_2, Par_3, **kwargs: Var_1 + Var_2 + Par_3
              },
    'In_2': {'type': 'input',
             'unit': '1',
             'name': 'Input 2'},
    'Par_2': {'type': 'parameter',
              'unit': '1',
              'name': 'Variable 2'},
    'Var_2': {'type': 'variable',
              'name': 'Output 1',
              'unit': '1',
              'computation': lambda In_2, Par_2, **kwargs: Par_2 / In_2
              }
}

X = {
    'In_1': 5,
    'In_2': 4,
    'Par_1': 3,
    'Par_2': 5,
    'Par_3': 5
}

nodes_list = [nodes_1]


@pytest.mark.parametrize(('nodes'), nodes_list)
def test_comp_nodes(nodes):
    node, egde, summary = GraphParser().parse(nodes)
    assert set(['Out_1_comp', 'Var_1_comp', 'Var_2_comp']) < set([n[0] for n in node])



@pytest.mark.parametrize(('nodes'), nodes_list)
def test_non_comp_nodes(nodes):
    node, egde, summary = GraphParser().parse(nodes)
    assert set(['Out_1', 'Var_1', 'Var_2', 'In_1', 'In_2', 'Par_1', 'Par_2', 'Par_3']) < set([n[0] for n in node])
