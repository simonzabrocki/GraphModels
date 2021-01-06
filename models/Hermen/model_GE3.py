__author__ = 'Hermen'
__status__ = 'In developement'

"""
TO DO.
"""
from graphmodels.graphmodel import GraphModel

GE3_nodes = [
    {'type': 'input',
     'unit': 'population',
     'id': 'P',
     'name': 'Total population',
     },
    {'type': 'input',
     'unit': 'CO2eq',
        'id': 'TEE_CO2eq',
     'name': 'CH4 emissions enteric in CO2eq',
     },
    {'type': 'input',
     'unit': 'CO2eq',
     'id': 'TMT_CO2eq',
     'name': 'Emissions manure treated in CO2eq',
     },
    {'type': 'input',
     'unit': 'CO2eq',
     'id': 'TMA_CO2eq',
     'name': 'Emissions  manure applied to soil CO2eq',
     },
    {'type': 'input',
     'unit': 'CO2eq',
     'id': 'TMP_CO2eq',
     'name': 'Emissions  manure left on pasture CO2eq',
     },
    {'type': 'input',
     'unit': 'CO2eq',
     'id': 'FE_CO2eq',
     'name': 'Emissions fertilizer CO2eq',
     },
    {'type': 'input',
     'unit': 'gg CO2eq',
     'id': 'OEi',
     'name': 'Vector of other emissions',
     },
    {'type': 'output',
     'unit': '',
     'id': 'GE3',
     'name': 'Ratio of non-CO2 emissions in agriculture to population',
     'in': ['TMP_CO2eq', 'TMA_CO2eq', 'TMT_CO2eq', 'TEE_CO2eq', 'FE_CO2eq', 'OEi', 'P'],
     'computation': {'name': '(SUM(OEI) + TEE_CO2eq + TMT_CO2eq + TMP_CO2eq + TMA_CO2eq) / P *1000',
                     'formula': lambda X: (X['OEi'] + X['TEE_CO2eq'] + X['TMT_CO2eq'] + X['TMP_CO2eq'] + X['TMA_CO2eq'] + X['FE_CO2eq']) / X['P'] * 1e3}
     },


]


model_GE3 = GraphModel(GE3_nodes)
