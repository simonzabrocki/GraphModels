#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Hermen'
__status__ = 'Pending Validation'

"""
TO DO.
"""
from graphmodels.graphmodel import GraphModel


CRfd_nodes = [
    {'type': 'output',
     'unit': '',
     'id': 'CRfd',
     'name': 'Feed/forage distribution (correction)',
     'in': ['TAFDi', 'FDi'],
     'computation': {'name': 'SUM(TAFDi) / sum(FDi)',
                     'formula': lambda X: X['TAFDi'].sum() / X['FDi'].sum()}
     },
    {'type': 'input',
     'unit': '1000 t',
     'id': 'FDi',
     'name': 'Total domestic food production per food group',
     },
    {'type': 'variable',
     'unit': 'kg',
     'id': 'TAFDi',
     'name': 'Total animal feed demand per food group (animals)',
     'in': ['FCRi', 'FPi_animal'],
     'computation': {'name': 'FRCi*FPi',
                     'formula': lambda X: X['FCRi'] * X['FPi_animal']}
     },
    {'type': 'parameter',
     'unit': 'kg DM feed/ kg EW',
     'id': 'FCRi',
     'name': 'Feed conversion ratio',
     },
    {'type': 'input',
     'unit': '1000 t',
     'id': 'FPi_animal',
     'name': 'Food production per food group',
     },
]

CRfd_model = GraphModel(CRfd_nodes)
