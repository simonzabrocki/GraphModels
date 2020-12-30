# These are the animal population groups that are used for the manure- and enteric emissions -> we need to aggregate to this from: ANPi & the Animal_group
# 'Other' contains: Horses, Asses and Mules; these animal populations are quite small & generally not eaten -> so assumed constant from the 2017 dataset

other_animals = [("Asses" + "Mules" + "Horse")]
Animal_group_emissions = ['Bovine meat', 'Pigmeat', 'Poultry meat',
                          'Eggs', 'Milk - Excluding Butter', 'Mutton & Goat meat']


# not sure if this works; but in this group (in ANPi_baseline) the eggs+meat should be added (in faostat ANPI doesn't have poultry meat and eggs seperated)
ANPi_group = ["Milk - Excluding Butter", 'Bovine meat',
              'Pigmeat', ('Poultry meat'+'Eggs'),  "Mutton & Goat meat"]
TAHi_group = ["Milk - Excluding Butter", "Bovine meat",
              "Pigmeat", "Poultry meat", "Mutton & Goat meat"]

# Milk &Bovine are aggregated into 'cattle' ; Asses, Mules and Horse into 'other'
Emission_groups = [("Milk - Excluding Butter" + "Bovine meat"), "Pigmeat",
                   "Poultry meat", "Mutton & Goat meat", ("Asses" + "Mules", "Horse")]

animals_nodes = [

    {'type': 'variable',
     'unit': '1000 t',
     'id': 'FDTi',
     'name': 'Total food demand per food group',

     },

    # add: "Sheep and Goat Meat" to AYi vector (value: 16.7) from: http://www.fao.org/faostat/en/#data/QL
    {'type': 'input',
     'unit': 'kg/animal',
     'id': 'AYi',
     'name': 'Vector of animal yields',

     },


    {'type': 'variable',
     'unit': 'x1 million animals',
     'id': 'ANPi',
     'name': 'Vector animals needed for production',
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
     'name': 'Vector total production animals (2017)',
     },


    # ADD: "Sheep and Goats" to JSON file for TAHi_baseline, value: 1222000
    {'type': 'input',
     'unit': 'heads',
     'id': 'TAHi_baseline',
     'name': 'Vector total animals (2017)',
     },


    {'type': 'variable',
     'unit': '',
     'id': 'PTTAi',
     'name': 'vector production-to-total animals ratio',
     'in': ['TAHi_baseline', 'ANPi_baseline'],
     'computation': {'name': 'TAHi_baseline/ANPi_baseline',
                     'formula': lambda X: (X['TAHi_baseline'].loc[TAHi_group] / X['ANPi_baseline'].loc[ANPi_group])}
     },


    {'type': 'variable',
     'unit': 'heads',
     'id': 'TAPi',
     'name': 'Vector total animal population (heads)',
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
     'name': 'Vector total animal population corrected (heads)',
     'in': ['CPTAi_cal', 'TAPi'],
     'computation': {'name': 'TAPi*CPTAi_cal',
                     'formula': lambda X: X['TAPi'] * X['CPTAi_cal']}
     },





]

G7 = GraphModel(animals_nodes)

G7.draw(draw_properties)
