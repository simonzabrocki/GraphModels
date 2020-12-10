from graphmodels.graphmodel import GraphModel
from models.Sarah.model_agricultural_water import AgriculturalWaterNodes
from models.Sarah.model_freshwater_available import FreshwaterAvailableNodes
from models.Sarah.model_municipal_water import MunicipalWaterNodes

WaterModelNodes = AgriculturalWaterNodes + FreshwaterAvailableNodes + MunicipalWaterNodes
WaterModel = GraphModel(WaterModelNodes)
