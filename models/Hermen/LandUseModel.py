#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Hermen'
__status__ = 'Pending Validation'

"""
TO DO.
"""
import pandas as pd

from graphmodels.graphmodel import GraphModel
from models.Hermen.model_crop_demand_correction import CD_corr_model
from models.Hermen.model_feed_forage_distribution import CRfd_model
from models.Hermen.model_food_demand_total import FDTi_model
from models.Hermen.model_food_demand_crops import FDi_crops_model


animal_group = ['Bovine meat', 'Pigmeat', 'Poultry meat',
                'Eggs', 'Milk - Excluding Butter', 'Meat, other']

crop_group = ['Cereals - Excluding Beer', 'Starchy Roots', 'Sugar Crops',
              'Sugar & Sweeteners', 'Pulses', 'Treenuts', 'Oilcrops',
              'Vegetable Oils', 'Vegetables', 'Fruits - Excluding Wine',
              'Stimulants', 'Spices', 'Alcoholic Beverages']


LU_nodes = [
    {
        'id': 'inputs_animal_and_crops',
        'name': 'All inputs (animals and crops)',
        'unit': '',
        'type': 'input',
    },
    {
        'id': 'FDTi_animal',
        'name': 'Total food demand per food group (animals)',
        'unit': '',
        'type': 'variable',
        'in': ['inputs_animal_and_crops'],
        'computation': {'name': 'compute FDTi_animal', 'formula': lambda X: compute_FDTi_animal(X)}
    },
    {
        'id': 'FDi_crops',
        'name': 'Total domestic food production per food group (crops)',
        'unit': '',
        'type': 'variable',
        'in': ['inputs_animal_and_crops', 'FDTi_animal', 'CRfd'],
        'computation': {'name': 'compute FDi_crops', 'formula': lambda X: compute_FDi_crops(X)}
    },
    {
        'id': 'FDTi_crops',
        'name': 'Total food demand per food group (crops)',
        'unit': '',
        'type': 'variable',
        'in': ['inputs_animal_and_crops', 'FDi_crops'],
        'computation': {'name': 'compute FDTi_crops', 'formula': lambda X: compute_FDTi_crops(X)}
    },
    {
        'id': 'FDTi',
        'name': 'Total food demand per food group',
        'unit': '',
        'type': 'variable',
        'in': ['FDTi_animal', 'FDTi_crops'],
        'computation': {'name': 'concatenate FDTi_crops and FDTi_animal', 'formula': lambda X: pd.concat([X['FDTi_animal'], X['FDTi_crops']])}
    },
    {
        'id': 'CRfd',
        'name': 'Feed/forage distribution (correction)',
        'unit': '',
        'type': 'variable',
        'in': ['FCRi', 'inputs_animal_and_crops'],
        'computation': {'name': 'compute CRfd', 'formula': lambda X: compute_CRfd(X)}
    },
    {
        'id': 'FCRi',
        'name': 'Feed conversion ratio',
        'unit': '',
        'type': 'parameter',
    },
    {
        'id': 'CD_corr',
        'name': 'Correction parameter crop demand',
        'unit': '',
        'type': 'variable',
        'in': ['FDTi', 'inputs_animal_and_crops'],
        'computation': {'name': 'compute CRfd', 'formula': lambda X: compute_CD_corr(X)}
    },

]


def compute_CRfd(X):
    X = X.copy()
    X['FPi_animal'] = X['FPi'].loc[animal_group]
    result = CRfd_model.run(X)  # ['CRfd']
    return result['CRfd']


def compute_FDTi_animal(X):
    X = X.copy()
    X['FDi_baseline'] = X['FDi']
    result = FDTi_model.run(X)['FDTi']
    return result.loc[animal_group]


def compute_FDTi_crops(X):
    X = X.copy()
    X['FDi_baseline'] = X['FDi']
    result = FDTi_model.run(X)['FDTi']
    return result.loc[crop_group]


def compute_FDi_crops(X):
    X = X.copy()
    X['FDi_baseline'] = X['FDi']
    result = FDi_crops_model.run(X)['FDi_crops']
    return result


def compute_CD_corr(X):
    X = X.copy()
    X['LUi_baseline'] = X['LUi']
    result = CD_corr_model.run(X)['CD_corr']
    return result


LandUseModel = GraphModel(LU_nodes)
