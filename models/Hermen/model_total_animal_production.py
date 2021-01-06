# !/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'Hermen'
__status__ = 'In developement'

"""
This part of the model is not finished at the moment and still under active developement.
"""

from graphmodels.graphmodel import GraphModel
import numpy as np

other_animals = [("Asses" + "Mules" + "Horse")]
Animal_group_emissions = ['Bovine meat', 'Pigmeat', 'Poultry meat',
                          'Eggs', 'Milk - Excluding Butter', 'Mutton & Goat meat']


# not sure if this works; but in this group (in ANPi_baseline) the eggs+meat should be added (in faostat ANPI doesn't have poultry meat and eggs seperated)
ANPi_group = ["Milk - Excluding Butter", 'Bovine meat',
              'Pigmeat', ('Poultry meat' + 'Eggs'), "Mutton & Goat meat"]
TAHi_group = ["Milk - Excluding Butter", "Bovine meat",
              "Pigmeat", "Poultry meat", "Mutton & Goat meat"]

# Milk &Bovine are aggregated into 'cattle' ; Asses, Mules and Horse into 'other'
Emission_groups = [("Milk - Excluding Butter" + "Bovine meat"), "Pigmeat",
                   "Poultry meat", "Mutton & Goat meat", ("Asses" + "Mules", "Horse")]

TAPi_nodes = [

    {'type': 'variable',
     'unit': '1000 t',
     'id': 'FDTi',
     'name': 'Total food demand per food group',

     },

    # add: "Sheep and Goat Meat" to AYi vector (value: 16.7) from: http://www.fao.org/faostat/en/#data/QL
    {'type': 'input',
     'unit': 'kg/animal',
     'id': 'AYi',
     'name': 'Animal yields per animal group',

     },
    {'type': 'variable',
     'unit': 'x1 million animals',
     'id': 'ANPi',
     'name': 'Animals needed for production',
     'in': ['FDTi', 'AYi'],
     'computation': {'name': 'FDTi/AYi',
                     'formula': lambda X: X['FDTi'].loc[Animal_group_emissions] / X['AYi'].loc[Animal_group_emissions]
                     }

     },
    # ANPI data from 2017 is used to calculate the PTTAi -> in JSON file this is still 'ANPi'
    # ADD: "Sheep and Goats" to JSON file for ANPi_baseline, value: 107764
    {'type': 'input',
     'unit': 'heads',
     'id': 'ANPi_baseline',
     'name': 'Total production animals per animal group',
     },


    # ADD: "Sheep and Goats" to JSON file for TAHi_baseline, value: 1222000
    {'type': 'input',
     'unit': 'heads',
     'id': 'TAHi_baseline',
     'name': 'Total animals per animal group',
     },


    {'type': 'variable',
     'unit': '',
     'id': 'PTTAi',
     'name': 'Production-to-total animals ratio per animal group',
     'in': ['TAHi_baseline', 'ANPi_baseline'],
     'computation': {'name': 'TAHi_baseline / ANPi_baseline',
                     'formula': lambda X: (X['TAHi_baseline'].loc[TAHi_group] / X['ANPi_baseline'].loc[ANPi_group])}
     },


    {'type': 'variable',
     'unit': 'heads',
     'id': 'TAPi',
     'name': 'Animal population per animal group',
     'in': ['ANPi', 'PTTAi'],
     'computation': {'name': 'ANPi*PTTAi',
                     'formula': lambda X: np.array([(X['ANPi'].loc[ANPi_group] * X['PTTAi'].loc[TAHi_group]), sum(X['TAHi_baseline'].loc[other_animals])])}
     },



    # the data on FAOstat did not match 100% so a small correction was used (still need to check why this difference emerges)  --> calculated using 2017 input data & comparing it with FAO data
    {'type': 'parameter',
     'unit': '',
     'id': 'CPTAi_cal',
     'name': 'correction total animals (vector)',
     },


    {'type': 'parameter',
     'unit': 'heads',
     'id': 'TAi',
     'name': 'Total animal population corrected (heads)',
     'in': ['CPTAi_cal', 'TAPi'],
     'computation': {'name': 'TAPi*CPTAi_cal',
                     'formula': lambda X: X['TAPi'] * X['CPTAi_cal']}
     },





]

model_TAPi = GraphModel(TAPi_nodes)

model_TAPi.draw()
