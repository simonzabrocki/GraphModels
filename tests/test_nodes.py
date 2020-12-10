
import pytest

from GraphModels.models.Sarah.model_agricultural_water import AgriculturalWaterNodes
from GraphModels.models.Sarah.model_freshwater_available import FreshwaterAvailableNodes
from GraphModels.models.Sarah.model_municipal_water import MunicipalWaterNodes

nodes_list = AgriculturalWaterNodes + FreshwaterAvailableNodes + MunicipalWaterNodes

computationnal_nodes = [node for node in nodes_list if 'computation' in node.keys()]


@pytest.mark.parametrize(('node'), nodes_list)
def test_node_minimal_keys(node):
    assert set(['type', 'unit', 'id', 'name']) <= set(node.keys())


@pytest.mark.parametrize(('node'), computationnal_nodes)
def test_node_computationnal(node):
    assert set(['formula', 'name']) == set(node['computation'].keys())


def test_inputs_computation():
    inputs_computation = [val for sublist in [node['in'] for node in nodes_list if 'in' in node] for val in sublist]
    node_ids = [node['id'] for node in nodes_list]
    assert set(inputs_computation) <= set(node_ids)
