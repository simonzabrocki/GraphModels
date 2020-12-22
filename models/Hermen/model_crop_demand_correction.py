#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Hermen'
__status__ = 'Pending Validation'

"""
TO DO.
"""
from graphmodels.graphmodel import GraphModel

CD_corr_nodes = [
    {'type': 'input',
     'unit': '1000 tons',
     'id': 'FDTi',
     'name': 'Total food demand per food group',
     },
    {'type': 'input',
     'unit': 'hg/ha',
     'id': 'CYi',
     'name': 'Crop yields per crop type'},
    # Unit conversion factor 1e4 (ha -> 1000 ha, hg -> 1000 tons)
    {'type': 'variable',
     'unit': '',
     'id': 'TCLD',
     'name': 'Total crop land demand',
     'in': ['FDTi', 'CYi'],
     'computation':{'name': 'FDTi * CYi', 'formula': lambda X: 1e4 * (X['FDTi'] / X['CYi']).sum()}
     },
    {'type': 'input',
     'unit': '1000 ha',
     'id': 'LUi_baseline',
     'name': 'Land use per group'
     },
    {'type': 'variable',
     'unit': 'ha',
     'id': 'TCLD_baseline',
     'name': 'Total crop land demand (baseline)',
     'in': ['LUi_baseline'],
     'computation': {'name': 'LU_Cropland - LU_Land_under_permanent_crops',
                     'formula': lambda X: X['LUi'].loc['Cropland'] - X['LUi'].loc['Land under permanent crops']}
     },
    {'type': 'output',
     'unit': '',
     'id': 'CD_corr',
     'name': 'Correction parameter crop demand',
     'in': ['TCLD', 'TCLD_baseline'],
     'computation': {'name': 'TCLD_baseline / TCLD',
                     'formula': lambda X: X['TCLD_baseline'] / X['TCLD']}
     },
]

CD_corr_model = GraphModel(CD_corr_nodes)
