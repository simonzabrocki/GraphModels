#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Hermen'
__status__ = 'Pending Validation'

"""
TO DO.
"""

from graphmodels.graphmodel import GraphModel

Crop_group = ['Cereals - Excluding Beer', 'Starchy Roots', 'Sugar Crops',
              'Sugar & Sweeteners', 'Pulses', 'Treenuts', 'Oilcrops',
              'Vegetable Oils', 'Vegetables', 'Fruits - Excluding Wine',
              'Stimulants', 'Spices', 'Alcoholic Beverages']

FDi_nodes = [
    {'type': 'input',
     'unit': '1000 t',
     'id': 'FDTi_animal',
     'name': 'Total food demand per food group',
     },
    {'type': 'output',
     'unit': '1000 t',
     'id': 'FDi_crops',
     'name': 'Total animal feed demand per crop',
     'in': ['FMi', 'FD'],
     'computation': {'name': 'FMi * FD',
                     'formula': lambda X: X['FMi'] * X['FD']}
     },
    {'type': 'variable',
     'unit': '',
     'id': 'FMi',
     'name': 'Feed mix fraction',
     'in': ['FDi_baseline'],
     'computation': {'name': 'FDi_baseline_crop/SUM(FDi_baseline)',
                     'formula': lambda X: X['FDi_baseline'].loc[Crop_group] / X['FDi_baseline'].sum()}
     },
    {'type': 'input',
     'unit': '1000 t',
     'id': 'FDi_baseline',
     'name': 'Feed demand per food group',
     },
    {'type': 'variable',
     'unit': '1ooo t',
     'id': 'FD',
     'name': 'Total crop-feed demand',
     'in': ['TAFDi', 'CRfd'],
     'computation': {'name': 'SUM(TAFDi)/CRfd',
                     'formula': lambda X: X['TAFDi'].sum() / X['CRfd']}
     },
    {'type': 'parameter',
     'unit': '',
     'id': 'CRfd',
     'name': 'Feed/forage distribution (correction)',
     },
    {'type': 'parameter',
     'unit': 'kg DM feed/ kg EW',
     'id': 'FCRi',
     'name': 'Feed conversion ratio',
     },
    {'type': 'variable',
     'unit': 'kg',
     'id': 'TAFDi',
     'name': 'Total animal feed demand per food group (animals)',
     'in': ['FCRi', 'FDTi_animal'],
     'computation': {'name': 'FRCi*FDTi_animal',
                     'formula': lambda X: (X['FCRi'] * X['FDTi_animal'])}
     }
]

FDi_crops_model = GraphModel(FDi_nodes)
