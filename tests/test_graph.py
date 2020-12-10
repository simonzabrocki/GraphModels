
import pytest
from GraphModels.models.Sarah.model_agricultural_water import AgriculturalWaterNodes
from GraphModels.models.Sarah.model_freshwater_available import FreshwaterAvailableNodes
from GraphModels.models.Sarah.model_municipal_water import MunicipalWaterNodes
from GraphModels.graphmodels.graphmodel import GraphModel

Graphs_list = [GraphModel(AgriculturalWaterNodes + FreshwaterAvailableNodes + MunicipalWaterNodes)]


@pytest.mark.parametrize(('graph'), Graphs_list)
def test_graph(graph):
    pass
