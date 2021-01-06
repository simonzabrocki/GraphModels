__author__ = 'Hermen'
__status__ = 'In developement'

"""
TO DO.
"""
from graphmodels.graphmodel import GraphModel
import numpy as np


TMP_CO2eq_nodes = [

    {'type': 'input',
     'unit': 'heads',
     'id': 'TAi',
     'name': 'Total animal population corrected (heads)',
     },

    {'type': 'input',
     'unit': 'heads',
     'id': 'TAHi',
     'name': 'Total animal population per animal',
     },


    {'type': 'variable',
     'unit': 'kgN',
     'id': 'MYi',
     'name': 'Manure yields',
     'in': ['TAHi', 'TMPi_baseline'],
     'computation': {'name': 'TMPi_baseline/TAHi',
                     'formula': lambda X: X['TMPi_baseline'] / X['TAHi']}
     },

    {'type': 'input',
     'unit': 'kgN',
     'id': 'TMPi_baseline',
     'name': 'Total manure production baseline',
     },


    {'type': 'output',
     'unit': 'kgN',
     'id': 'TMi',
     'name': 'Vector total manure produced',
     'in': ['MYi', 'TAi'],
     'computation': {'name': 'TAi*MYi',
                     'formula': lambda X: X['TAi'] * X['MYi']}
     },


    {'type': 'input',
     'unit': 'kgN',
     'id': 'TM_LPi',
     'name': 'Total manure left on pasture',
     },


    {'type': 'variable',
     'unit': '%',
     'id': 'MM_LPi',
     'name': '% total manure left on pasture',
     'in': ['TMPi_baseline', 'TM_LPi'],
     'computation': {'name': 'TM_LPi/TMPi_baseline',
                     'formula': lambda X: X['TM_LPi'] / X['TMPi_baseline']}
     },


    {'type': 'variable',
     'unit': 'ggN2O',
     'id': 'E_Li',
     'name': 'N2O Emissions manure left on pasture',
     'in': ['TMi', 'MM_LPi', 'EF_Li'],
     'computation': {'name': 'TMi*MM_LPi * EF_Li',
                     'formula': lambda X: X['TMi'] * X['MM_LPi'] * X['EF_Li']}
     },
    {'type': 'input',
     'unit': 'ggN2O',
     'id': 'E_Li_Baseline',
     'name': 'N2O emissions left on pasture',
     },
    {'type': 'parameter',
     'unit': '',
     'id': 'EF_Li',
     'name': 'Vector Emission factors N2O left on pasture',
     'in': ['TM_LPi', 'E_Li_Baseline'],
     'computation': {'name': 'E_Li_Baseline / TM_LPi',
                     'formula': lambda X: X['E_Li_Baseline'] / X['TM_LPi']}  # TM_LP2017i can be 0 in some countries -> so nan_to_num used to prevent division error
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

model_TMP_CO2eq = GraphModel(TMP_CO2eq_nodes)


FE_CO2eq_nodes = [
    {'type': 'input',
     'id': 'CL_total',
     'name': 'Cropland (including perm. and fallow land)',
     'unit': 'x 1000ha',
     },
    {'type': 'input',
     'unit': 'ha',
     'id': 'TCLD_baseline',
     'name': 'Total crop land demand (baseline)',
     },
    {'type': 'input',
     'unit': 't',
     'id': 'FU_baseline',
     'name': 'Total fertilizer use baseline',
     },
    # assumed constant based on the year 2017; maybe later we can use weighted average or add a scenario that can change the fertilizer/ha intensity
    {'type': 'variable',
     'unit': 'kg/ha',
     'id': 'FU',
     'name': 'Fertilizer use / ha',
     'in': ['TCLD_baseline', 'FU_baseline'],
     'computation': {'name': 'FU_baseline / TCLD_baseline',
                     'formula': lambda X: X['FU_baseline'] / (X['TCLD_baseline'] * 1e-3)}
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
     'unit': 'gg N2O',
     'id': 'FE_baseline',
     'name': 'Fertilizer N2O emissions baseline',
     },
    {'type': 'parameter',
     'unit': 'kg N2O-N/kg N',
     'id': 'EF_F',
     'name': 'Emission factor N2O from fertilizer',
     'in': ['FU_baseline', 'FE_baseline'],
     'computation': {'name': 'FE_baseline / FU_baseline',
                     'formula': lambda X: X['FE_baseline'] / X['FU_baseline']}
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

model_FE_CO2eq = GraphModel(FE_CO2eq_nodes)


TMA_CO2eq_nodes = [
    {'type': 'input',
     'unit': 'kgN',
     'id': 'TMPi_baseline',
     'name': 'Vector manure production 2017',
     },
    {'type': 'input',
     'unit': 'kgN',
     'id': 'TMi',
     'name': 'Vector total manure produced',
     },
    {'type': 'input',
     'unit': 'kgN',
     'id': 'TM_ASi',
     'name': 'Total manure applied to soil 2017 (vector)',
     },
    {'type': 'parameter',
     'unit': '%',
     'id': 'MM_ASi',
     'name': '% total manure applied to soil',
     'in': ['TMPi_baseline', 'TM_ASi'],
     'computation': {'name': 'TM_ASi/TMPi_baseline',
                     'formula': lambda X: X['TM_ASi'] / X['TMPi_baseline']}
     },
    {'type': 'variable',
     'unit': 'kgN',
     'id': 'MASi',
     'name': 'Vector manure applied to soil',
     'in': ['TMi', 'MM_ASi'],
     'computation': {'name': 'TMi*MM_ASi',
                     'formula': lambda X: X['TMi'] * X['MM_ASi']}
     },
    {'type': 'input',
     'unit': 'ggN2O',
     'id': 'E_ASi_baseline',
     'name': 'N2O emissions applied to soil 2017',
     },
    {'type': 'parameter',
     'unit': '',
     'id': 'EF_ASi',
     'name': 'Vector Emission factors N2O applied to soil',
     'in': ['TM_ASi', 'E_ASi_baseline'],
     'computation': {'name': 'E_ASi_baseline/TM_ASi',
                     'formula': lambda X: X['E_ASi_baseline'] / X['TM_ASi']}
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

model_TMA_CO2eq = GraphModel(TMA_CO2eq_nodes)


TEE_CO2eq_nodes = [

    {'type': 'input',
     'unit': '',
     'id': 'TAHi',
     'name': 'Vector total animals (2017)',
     },
    {'type': 'input',
     'unit': 'ggCH4',
     'id': 'EECH4',
     'name': 'Vector enteric CH4 2017',
     },
    {'type': 'input',
     'unit': 'kg CH4 / head',
     'id': 'EF_EEi',
     'name': 'Emission factor enteric (CH4)',
     'in': ['EECH4', 'TAHi'],
     'computation': {'name': 'EECH4/TAHi_2',
                     'formula': lambda X: X['EECH4'] / X['TAHi']}
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

TEE_CO2eq_model = GraphModel(TEE_CO2eq_nodes)
