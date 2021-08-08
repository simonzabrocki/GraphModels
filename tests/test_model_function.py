import pytest
from GraphModels.graphmodels.graphmodel import GraphModel


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

model_list = [GraphModel(nodes_1)]


@pytest.mark.parametrize(('model'), model_list)
def test_computation_output(model):
    result = model.run(X)
    assert set(['Out_1', 'Var_1', 'Var_2']) < result.keys()


@pytest.mark.parametrize(('model'), model_list)
def test_computation_values(model):
    result = model.run(X)
    assert result['Out_1'] == 21.25 and result['Var_1'] == 15 and result['Var_2'] == 5 / 4
