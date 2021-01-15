__author__ = 'Hermen'
__status__ = 'Pending Validation'

"""
TO DO.
"""
from graphmodels.graphmodel import GraphModel
import numpy as np

TEE_CO2eq_nodes = [
    {'type': 'input',
     'unit': 'kg CH4 / head',
     'id': 'EF_EEi',
     'name': 'Emission factor enteric (CH4)',
     },

    {'type': 'variable',
     'unit': 'heads',
     'id': 'TAi',
     'name': 'Vector total animal population corrected (heads)',
     },


    {'type': 'variable',
     'unit': 'ggCH4',
     'id': 'EE_CH4',
     'name': 'Vector enteric emissions CH4',
     'in': ['TAi', 'EF_EEi'],
     'computation': {'name': 'TAi*EF_EEi',
                     'formula': lambda X: X['TAi'] * X['EF_EEi']}
     },
    {'type': 'parameter',
     'unit': 'CH4/CO2',
     'id': 'GWPCH4',
     'name': 'GWP conversion CO2eq',
     },

    {'type': 'output',
     'unit': 'CO2eq',
     'id': 'TEE_CO2eq',
     'name': 'CH4 emissions enteric in CO2eq',
     'in': ['GWPCH4', 'EE_CH4'],
     'computation': {'name': 'SUM(EE_CH4) * GWPCH4 ',
                     'formula': lambda X: sum(X['EE_CH4']) * X['GWPCH4']}
     },


]

FE_CO2eq_nodes = [
    {'type': 'input',
     'id': 'CL_total',
     'name': 'Cropland (including perm. and fallow land)',
     'unit': 'x 1000ha',
     },
    {'type': 'input',
     'unit': 'kg/ha',
     'id': 'FU',
     'name': 'Fertilizer use / ha',
     },
    {'type': 'variable',
     'unit': 'kgN',
     'id': 'IN_F',
     'name': 'Fertilizer input',
     'in': ['CL_total', 'FU'],
     'computation': {'name': 'CL_total * FU',
                     'formula': lambda X: X['CL_total'] * X['FU']}
     },
    {'type': 'parameter',
     'unit': 'kg N2O-N/kg N',
     'id': 'EF_F',
     'name': 'Emission factor N2O from fertilizer',
     },
    {'type': 'variable',
     'unit': 'gg N2O',
     'id': 'F_N2O',
     'name': 'N2O emissions from fertilizer use',
     'in': ['IN_F', 'EF_F'],
     'computation': {'name': 'IN_F * EF_F',
                     'formula': lambda X: X['IN_F'] * X['EF_F']}
     },
    {'type': 'parameter',
     'unit': 'N2O/CO2',
     'id': 'GWPN2O',
     'name': 'GWP conversion CO2eq',
     },
    {'type': 'output',
     'unit': 'CO2eq',
     'id': 'FE_CO2eq',
     'name': 'N2O emissions fertilizer in CO2eq',
     'in': ['GWPN2O', 'F_N2O'],
     'computation': {'name': 'F_N2O * GWPN2O',
                     'formula': lambda X: X['F_N2O'] * X['GWPN2O']}
     }


]

TMP_CO2eq_nodes = [

    {'type': 'input',
     'unit': 'heads',
     'id': 'TAi',
     'name': 'Total animal population corrected (heads)',
     },
    {'type': 'input',
     'unit': 'kgN',
     'id': 'MYi',
     'name': 'Manure yields',
     },
    {'type': 'variable',
     'unit': 'kgN',
     'id': 'TMi',
     'name': 'Vector total manure produced',
     'in': ['MYi', 'TAi'],
     'computation': {'name': 'TAi*MYi',
                     'formula': lambda X: X['TAi'] * X['MYi']}
     },

    {'type': 'input',
     'unit': '%',
     'id': 'MM_LPi',
     'name': '% total manure left on pasture',
     },


    {'type': 'variable',
     'unit': 'ggN2O',
     'id': 'E_Li',
     'name': 'N2O Emissions manure left on pasture',
     'in': ['TMi', 'MM_LPi', 'EF_Li'],
     'computation': {'name': 'TMi*MM_LPi * EF_Li',
                     'formula': lambda X: X['TMi'] * X['MM_LPi'] * X['EF_Li']}
     },
    {'type': 'parameter',
     'unit': '',
     'id': 'EF_Li',
     'name': 'Vector Emission factors N2O left on pasture',
     },
    {'type': 'parameter',
     'unit': 'N2O/CO2',
     'id': 'GWPN2O',
     'name': 'GWP conversion CO2eq',
     },

    {'type': 'output',
     'unit': 'CO2eq',
     'id': 'TMP_CO2eq',
     'name': 'Emissions from pasture CO2eq',
     'in': ['E_Li', 'GWPN2O'],
     'computation': {'name': '(SUM(E_Li)*GWPN2O',
                     'formula': lambda X: np.nansum(X['E_Li']) * X['GWPN2O']}
     }
]

TMA_CO2eq_nodes = [
    {'type': 'input',
     'unit': 'kgN',
     'id': 'TMi',
     'name': 'Vector total manure produced',
     },
    {'type': 'parameter',
     'unit': '%',
     'id': 'MM_ASi',
     'name': '% total manure applied to soil',
     },
    {'type': 'variable',
     'unit': 'kgN',
     'id': 'MASi',
     'name': 'Vector manure applied to soil',
     'in': ['TMi', 'MM_ASi'],
     'computation': {'name': 'TMi*MM_ASi',
                     'formula': lambda X: X['TMi'] * X['MM_ASi']}
     },
    {'type': 'parameter',
     'unit': '',
     'id': 'EF_ASi',
     'name': 'Vector Emission factors N2O applied to soil',
     },
    {'type': 'variable',
     'unit': 'ggN2O',
     'id': 'E_ASi',
     'name': 'N2O Emissions manure applied to soil ',
     'in': ['EF_ASi', 'MASi'],
     'computation': {'name': '(EF_ASi*MASi)',
                     'formula': lambda X: X['EF_ASi'] * X['MASi']}
     },
    {'type': 'parameter',
     'unit': 'N2O/CO2',
     'id': 'GWPN2O',
     'name': 'GWP conversion CO2eq',
     },
    {'type': 'output',
     'unit': 'CO2eq',
     'id': 'TMA_CO2eq',
     'name': 'Emissions  manure applied to soil CO2eq',
     'in': ['E_ASi', 'GWPN2O'],
     'computation': {'name': 'SUM(E_ASi)*GWPN2O',
                     'formula': lambda X: sum(X['E_ASi']) * X['GWPN2O']}
     }
]

TMT_CO2eq_nodes = [

    # N2O emissions treated

    {'type': 'input',
     'unit': 'kgN',
     'id': 'TMi',
     'name': 'Vector total manure produced',
     },
    {'type': 'parameter',
     'unit': '%',
     'id': 'MM_Ti',
     'name': '% total manure treated',
     },



    {'type': 'variable',
     'unit': 'kgN',
     'id': 'M_Ti',
     'name': 'Vector manure treated',
     'in': ['TMi', 'MM_Ti'],
     'computation': {'name': 'TMi*MM_Ti',
                     'formula': lambda X: X['TMi'] * X['MM_Ti']}
     },



    {'type': 'parameter',
     'unit': '',
     'id': 'EF_Ti',
     'name': 'Vector Emission factors N2O treated',
     },



    {'type': 'variable',
     'unit': 'ggN2O',
     'id': 'E_Ti',
     'name': 'N2O Emissions manure treated ',
     'in': ['EF_Ti', 'M_Ti'],
     'computation': {'name': 'EF_Ti*M_Ti',
                     'formula': lambda X: X['EF_Ti'] * X['M_Ti']}
     },

    {'type': 'parameter',
     'unit': 'N2O/CO2',
     'id': 'GWPN2O',
     'name': 'GWP conversion CO2eq',
     },


    {'type': 'parameter',
     'unit': 'kg/head',
     'id': 'EF_CH4Ti',
     'name': 'Vector Emission factors CH4 treated',
     'in': ['E_TCH4i_baseline', 'TAHi_2'],
     },



    {'type': 'variable',
     'unit': 'ggCH4',
     'id': 'E_TCH4i',
     'name': 'CH4 Emissions manure treated ',
     'in': ['TAi', 'EF_CH4Ti'],
     'computation': {'name': 'EF_CH4Ti*TAi',
                     'formula': lambda X: X['EF_CH4Ti'] * X['TAi']}
     },

    {'type': 'variable',
     'unit': 'heads',
     'id': 'TAi',
     'name': 'Vector total animal population corrected',
     },


    {'type': 'parameter',
     'unit': 'CH4/CO2',
     'id': 'GWPCH4',
     'name': 'GWP conversion CO2eq',
     },



    {'type': 'output',
     'unit': 'CO2eq',
     'id': 'TMT_CO2eq',
     'name': 'Emissions manure treated in CO2eq',
     'in': ['GWPCH4', 'E_TCH4i', 'E_Ti', 'GWPN2O'],
     'computation': {'name': 'SUM(E_Ti)*GWPN2O + SUM(E_TCH4i)*GWPCH4',
                     'formula': lambda X: X['E_Ti'].sum() * X['GWPN2O'] + X['E_TCH4i'].sum() * X['GWPCH4']}
     },
]

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
