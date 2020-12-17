import pandas as pd
import numpy as np


feed_demand = ['Cereals - Excluding Beer', 'Starchy Roots', 'Sugar Crops', 'Sugar & Sweeteners', 'Pulses',
               'Treenuts', 'Oilcrops', 'Vegetable Oils', 'Vegetables', 'Fruits - Excluding Wine',
               'Stimulants', 'Spices', 'Alcoholic Beverages']

croPgroups = ['Cereals - Excluding Beer', 'Fruits - Excluding Wine', 'Oilcrops',
              'Pulses', 'Starchy Roots', 'Sugar Crops', 'Treenuts', 'Vegetables']

animal_products_1 = ['Bovine meat', 'Pigmeat', 'Poultry meat',
                     'Eggs', 'Milk - Excluding Butter', 'Meat, other']
animal_products_2 = ['Bovine meat', 'Mutton & Goat meat', 'Pigmeat', 'Poultry meat', 'Meat, other', 'Offals',
                     'Animal fats', 'Eggs', 'Milk - Excluding Butter', 'Fish, Seafood', 'Aquatic Products, Other',
                     'Miscellaneous']

graph_nodes0 = [
    {'type': 'parameter',  # Type of node (input, output, variable, parameter)
     'unit': '',  # Unit
     'id': 'CRfd',  # Unique code to define the node
     'name': 'feed/forage distribution (correction)',  # Full name
     'in': ['TAFDi_cal', 'FDi'],  # Specify what comes into the node
     'computation': {'name': 'SUM(TAFDi)/sum(FDi)',  # When the node is compulationnal specify the computation like this
                     'formula': lambda X: sum(X['TAFDi_cal']) / sum(X['FDi'])}  # For now leave the formula field empty

     },
    {'type': 'variable',
     'id': 'TFFD_',
     'name': 'Total fodder/forage demand',
     'unit': 'x 1000t',
     'in': ['FDi', 'TAFDi_cal'],  # Specify what comes into the node
     'computation': {'name': 'SUM(TAFDi_cal) - SUM(FDi)',  # When the node is compulationnal specify the computation like this
                     'formula': lambda X: sum(X['TAFDi_cal']) - sum(X['FDi'])}  # For now leave the formula field empty
     },
    {'type': 'input',  # Type of node (input, output, variable, parameter)
     'unit': '1000 t',  # Unit
     'id': 'FDi',  # Unique code to define the node
     'name': 'Vector feed demand',  # Full name

     },
    {'type': 'variable',  # Type of node (input, output, variable, parameter)
     'unit': 'kg',  # Unit
     'id': 'TAFDi_cal',  # Unique code to define the node
     'name': 'vector total animal feed demand',  # Full name
     'in': ['FCRi', 'AYi', 'ANPi_cal'],  # Specify what comes into the node
     'computation': {'name': '(FRCi*AYi*ANPi_cal)/1000000',  # When the node is compulationnal specify the computation like this
                     'formula': lambda X: 1e-6 * (X['FCRi'] * X['AYi']).loc[animal_products_1] * X['ANPi_cal']}  # For now leave the formula field empty
     },
    {'type': 'input',  # Type of node (input, output, variable, parameter)
     'unit': 'kg/animal',  # Unit
     'id': 'AYi',  # Unique code to define the node
     'name': 'Vector of animal yields',  # Full name

     },
    {'type': 'parameter',  # Type of node (input, output, variable, parameter)
     'unit': 'kg DM feed/ kg EW',  # Unit
     'id': 'FCRi',  # Unique code to define the node
     'name': 'feed conversion ratio (kg/animal)',  # Full name

     },
    {'type': 'variable',
     'unit': 'heads',
     'id': 'ANPi_cal',
     'name': 'Vector animals needed for production',
     'in': ['FDi_an', 'AYi'],
     'computation': {'name': '(FDi_an*1000000)/AYi',
                     'formula': lambda X: 1e6 * X['FDi_an'] / X['AYi'].loc[animal_products_1]}

     },
    {'type': 'variable',  # Type of node (input, output, variable, parameter)
     'unit': 'heads',  # Unit
     'id': 'FDi_an',  # Unique code to define the node
     'name': 'selection animal-based food groups',  # Full name
     'in': ['FDTi_animal'],  # Specify what comes into the nod
     'computation': {'name': 'Selection animal-based food groups',  # When the node is compulationnal specify the computation like this
                     'formula': lambda X: np.array([X['FDTi_animal'][0], X['FDTi_animal'][2], X['FDTi_animal'][3], X['FDTi_animal'][7],
                                                    X['FDTi_animal'][8], (X['FDTi_animal'][1] + X['FDTi_animal'][4])])}  # selects the food groups that are animal based
     },
    {'type': 'output',
     'id': 'FDTi_animal',
     'name': 'Vector total food demand (animals/other)',
     'unit': 'x 1000 tonne',
     'in': ['FPi'],  # Specify what comes into the node
     'computation': {'name': 'FPi selection animal products',  # When the node is compulationnal specify the computation like this
                     'formula': lambda X: X['FPi'].loc[animal_products_2]}  # For now leave the formula field empty
     },
    {'type': 'input',  # Type of node (input, output, variable, parameter)
     'unit': '1000 t',  # Unit
     'id': 'FPi',  # Unique code to define the node
     'name': 'Vector food production',  # Full name
     },
    # CD_corr calibration
    # Here the food demand model is copied &  is used to compute correction for crop land demand
    # The model drivers (i.e. population, food waste reduction policies) removed so this parameter doesn't change for simulated years (not tested yet)
    # new variable: P used for population in , now 'P' can be used as normal


    # update 8-12-2020: the land demand for crops is now calculated by taking cropland [4] -  land under permanent crops [9]

    {'type': 'input',  # Type of node (input, output, variable, parameter)
     'unit': '',  # Unit
     'id': 'CD_corr',  # Unique code to define the node
     'name': 'correction parameter crop demand (calibrated for )',  # Full name
     'in': ['TCropDi_cal', 'TCLi'],  # Specify what comes into the node
     'computation': {'name': '',  # When the node is compulationnal specify the computation like this
                     'formula': lambda X: (X['LUi'].loc['Cropland'] \
                                           - X['LUi'].loc['Land under permanent crops']) \
                     / (sum(X['TCropDi_cal']) * 1e-3)}  # For now leave the formula field empty
     },




    {'type': 'variable',  # Type of node (input, output, variable, parameter)
     'unit': 'ha',  # Unit
     'id': 'TCropDi_cal',  # Unique code to define the node
     'name': 'Vector total cropland demand',  # Full name
     'in': ['FDTi_conv_cal', 'CYi'],  # Specify what comes into the node
     'computation': {'name': '(FDTi_conv_cal*1000000/(CYi/10)',  # When the node is compulationnal specify the computation like this
                     'formula': lambda X: (X['FDTi_conv_cal'] * 1e6) / (X['CYi'] * 1e-1)}  # For now leave the formula field empty
     },


    {'type': 'variable',  # Type of node (input, output, variable, parameter)
     'unit': 'x 1000t',  # Unit
     'id': 'FDTi_conv_cal',  # Unique code to define the node
     'name': 'Vector total food demand (aggregated for each crop group)',  # Full name
     'in': ['FDTi_total_cal', 'CYi', 'TCLi'],  # Specify what comes into the node
     'computation': {'name': '',  # When the node is compulationnal specify the computation like this
                     'formula': lambda X: pd.concat([X['FDTi_total_cal'].loc[croPgroups],
                                                     (X['CYi'] * 1e-6 * 1e-1 * X['TCLi']).loc[['Fibre Crops Primary']]])}  # For now leave the formula field empty
     },
    {'type': 'input',  # Type of node (input, output, variable, parameter)
     'unit': 'ha',  # Unit
     'id': 'TCLi',  # Unique code to define the node
     'name': 'Vector land used for crops in ',  # Full name
     },
    {'type': 'input',  # Type of node (input, output, variable, parameter)
     'unit': 'kg/capita/yr',  # Unit
     'id': 'FDKG_i',  # Unique code to define the node
     'name': 'Vector KG food demand',  # Full name
     },
    {'type': 'input',  # Type of node (input, output, variable, parameter)
     'unit': 'kcal/capita/day',  # Unit
     'id': 'FDKCi',  # Unique code to define the node
     'name': 'Vector of KCAL food demand',  # Full name
     },
    {'type': 'input',  # Type of node (input, output, variable, parameter)
     'unit': 'hg/ha',  # Unit
     'id': 'CYi',  # Unique code to define the node
     'name': 'Vector crop yields',  # Full name
     },
    {'type': 'variable',
     'id': 'KKRi',
     'name': 'Vector Kcal/kg ratio ',
     'unit': 'Kcal/kg',
     'in': ['FDKG_i', 'FDKCi'],  # Specify what comes into the node
     'computation': {'name': 'FDKCi/(FDKG_i/365)',  # When the node is compulationnal specify the computation like this
                     'formula': lambda X: (X['FDKCi'] / (X['FDKG_i'] / 365))}  # For now leave the formula field empty

     },
    {'type': 'variable',  # Type of node (input, output, variable, parameter)
     'unit': '%',  # Unit
     'id': 'SSRi',  # Unique code to define the node
     'name': 'Self-sufficiency ratio',  # Full name
     'in': ['FPi', 'FEi', 'FIi'],  # Specify what comes into the node
     'computation': {'name': '100*FPi/(FPi-FEi+FIi)',  # When the node is compulationnal specify the computation like this
                     'formula': lambda X: np.nan_to_num((1e2 * X['FPi']) / (X['FPi'] - X['FEi'] + X['FIi']))}  # For now leave the formula field empty
     },

    {'type': 'input',  # Type of node (input, output, variable, parameter)
     'unit': '1000 t',  # Unit
     'id': 'FPi',  # Unique code to define the node
     'name': 'Vector food production',  # Full name
     },

    {'type': 'input',  # Type of node (input, output, variable, parameter)
     'unit': '1000 t',  # Unit
     'id': 'FEi',  # Unique code to define the node
     'name': 'Vector food exports',  # Full name
     },

    {'type': 'input',  # Type of node (input, output, variable, parameter)
     'unit': '1000 t',  # Unit
     'id': 'FIi',  # Unique code to define the node
     'name': 'Vector food imports',  # Full name
     },

    {'type': 'input',  # Type of node (input, output, variable, parameter)
     'unit': 'population',  # Unit
     'id': 'P',  # Unique code to define the node
     'name': 'Total population',  # Full name
     },


    {'type': 'input',  # Type of node (input, output, variable, parameter)
     'unit': 'x 1000 t',  # Unit
     'id': 'FLOi',  # Unique code to define the node
     'name': 'Food losses',  # Full name
     },


    {'type': 'input',  # Type of node (input, output, variable, parameter)
     'unit': 'kcal/cap/day',  # Unit
     'id': 'FWPi_cal',  # Unique code to define the node
     'name': 'Vector food waste ',  # Full name
     'in': ['FLOi', 'P', 'KKRi'],  # Specify what comes into the node
     'computation': {'name': '(FLOi*KKRi*(1000000/365))/P',  # When the node is compulationnal specify the computation like this
                     'formula': lambda X: (X['FLOi'] * X['KKRi'] * (1e6 / 365)) / X['P']}  # For now leave the formula field empty
     },


    {'type': 'variable',  # Type of node (input, output, variable, parameter)
     'unit': 'heads',  # Unit
     'id': 'ANPi_calc',  # Unique code to define the node
     'name': 'Vector animals needed for production',  # Full name
     'in': ['FDi_an', 'AYi'],  # Specify what comes into the node
     'computation': {'name': '(FDi_an*1000000)/AYi',  # When the node is compulationnal specify the computation like this
                     'formula': lambda X: (X['FDi_an'] * 1e6) / X['AYi'].loc[animal_products_1]}  # For now leave the formula field empty

     },
    {'type': 'variable',  # Type of node (input, output, variable, parameter)
     'unit': '1000 t',  # Unit
     'id': 'FDi_cal',  # Unique code to define the node
     'name': 'Vector total domestic food production',  # Full name
     'in': ['KKRi', 'SSRi', 'TCDi_cal'],  # Specify what comes into the node
     'computation': {'name': '(TCDi_cal * SSRi/100 * 365)/KKRi',  # When the node is compulationnal specify the computation like this
                     'formula': lambda X: np.nan_to_num((X['TCDi_cal'] * X['SSRi'] / 1e2 * 365) / X['KKRi'])}  # For now leave the formula field empty
     },
    {'type': 'variable',  # Type of node (input, output, variable, parameter)
     'unit': '1000 t',  # Unit
     'id': 'OFi',  # Unique code to define the node
     'name': 'Other food demand',  # Full name
     'in': ['SDi', 'NFDi', 'PDi', 'RDi', 'SVi'],  # Specify what comes into the node
     'computation': {'name': 'SDi+NFDi+PDi+RDi+SVi',  # When the node is compulationnal specify the computation like this
                     'formula': lambda X: X['SDi'] + X['NFDi'] + X['PDi'] + X['RDi'] + X['SVi']}  # For now leave the formula field empty
     },

    {'type': 'input',  # Type of node (input, output, variable, parameter)
     'unit': '1000 t',  # Unit
     'id': 'SDi',  # Unique code to define the node
     'name': 'Vector seed demand',  # Full name
     },

    {'type': 'input',  # Type of node (input, output, variable, parameter)
     'unit': '1000 t',  # Unit
     'id': 'NFDi',  # Unique code to define the node
     'name': 'Vector non-food demand',  # Full name
     },

    {'type': 'input',  # Type of node (input, output, variable, parameter)
     'unit': '1000 t',  # Unit
     'id': 'PDi',  # Unique code to define the node
     'name': 'Vector processed demand',  # Full name
     },

    {'type': 'input',  # Type of node (input, output, variable, parameter)
     'unit': '1000 t',  # Unit
     'id': 'RDi',  # Unique code to define the node
     'name': 'Vector residual demand',  # Full name
     },

    {'type': 'input',  # Type of node (input, output, variable, parameter)
     'unit': '1000 t',  # Unit
     'id': 'SVi',  # Unique code to define the node
     'name': 'Vector stock variation',  # Full name
     },

    {'type': 'variable',  # Type of node (input, output, variable, parameter)
     'unit': 'kcal/day',  # Unit
     'id': 'TCDi_cal',  # Unique code to define the node
     'name': 'Total calorie demand per food group calibrated for ',  # Full name
     'in': ['P', 'FWPi_cal', 'FDKCi'],  # Specify what comes into the node
     'computation': {'name': 'P*(FDKCi+FWPi_cal)',  # When the node is compulationnal specify the computation like this
                     'formula': lambda X: X['P'] * (X['FDKCi'] + X['FWPi_cal'])}  # For now leave the formula field empty
     },


    {'type': 'variable',  # Type of node (input, output, variable, parameter)
     'unit': '1000 t',  # Unit
     'id': 'AFDi',  # Unique code to define the node
     'name': 'Vector total animal feed demand',  # Full name
     'in': ['FMi', 'FD'],  # Specify what comes into the node
     'computation': {'name': 'FMi * FD',  # When the node is compulationnal specify the computation like this
                     'formula': lambda X: X['FMi'].loc[feed_demand] * X['FD']}  # For now leave the formula field empty
     },


    {'type': 'variable',  # Type of node (input, output, variable, parameter)
     'unit': '',  # Unit
     'id': 'FMi',  # Unique code to define the node
     'name': 'Feed mix fraction',  # Full name
     'in': ['FDi'],  # Specify what comes into the node
     'computation': {'name': 'FDi/SUM(FDI)',  # When the node is compulationnal specify the computation like this
                     'formula': lambda X: X['FDi'] / sum(X['FDi'])}  # For now leave the formula field empty
     },

    {'type': 'input',  # Type of node (input, output, variable, parameter)
     'unit': '1000 t',  # Unit
     'id': 'FDi',  # Unique code to define the node
     'name': 'Vector feed demand',  # Full name

     },

    {'type': 'variable',  # Type of node (input, output, variable, parameter)
     'unit': '1ooo t',  # Unit
     'id': 'FD',  # Unique code to define the node
     'name': 'Total crop-feed demand',  # Full name
     'in': ['TAFDi', 'CRfd'],  # Specify what comes into the node
     'computation': {'name': 'SUM(TAFDi)/CRfd',  # When the node is compulationnal specify the computation like this
                     'formula': lambda X: sum(X['TAFDi']) / X['CRfd']}  # For now leave the formula field empty
     },



    {'type': 'parameter',  # Type of node (input, output, variable, parameter)
     'unit': '',  # Unit
     'id': 'CRfd',  # Unique code to define the node
     'name': 'feed/forage distribution (correction)',  # Full name
     },

    {'type': 'variable',  # Type of node (input, output, variable, parameter)
     'unit': 'kg',  # Unit
     'id': 'TAFDi',  # Unique code to define the node
     'name': 'vector total animal feed demand',  # Full name
     'in': ['FCRi', 'AYi', 'ANPi_calc'],  # Specify what comes into the node
     'computation': {'name': '(FRCi*AYi*ANPi_calc)/1000000',  # When the node is compulationnal specify the computation like this
                     'formula': lambda X: (X['FCRi'] * X['AYi']).loc[animal_products_1] * X['ANPi_calc'] * 1e-6}  # For now leave the formula field empty
     },



    {'type': 'input',  # Type of node (input, output, variable, parameter)
     'unit': 'kg/animal',  # Unit
     'id': 'AYi',  # Unique code to define the node
     'name': 'Vector of animal yields',  # Full name

     },

    {'type': 'parameter',  # Type of node (input, output, variable, parameter)
     'unit': 'kg DM feed/ kg EW',  # Unit
     'id': 'FCRi',  # Unique code to define the node
     'name': 'feed conversion ratio (kg/animal)',  # Full name

     },

    {'type': 'output',
     'id': 'FDTi_crops_cal',
     'name': 'Vector total food demand (crops)',
     'unit': 'x 1000 tonne',
     'in': ['FDi_cal', 'OFi', 'AFDi', 'SSRi'],  # Specify what comes into the node
     'computation': {'name': 'SSRi/100*(OFi+AFDi)+FDi',  # When the node is compulationnal specify the computation like this
                     'formula': lambda X: (((X['SSRi'] * 1e-2) * (X['OFi'] + X['AFDi'])) + (X['FDi_cal'] * 1e-6)).loc[feed_demand]}  # For now leave the formula field empty
     },
    {'type': 'output',
     'id': 'FDTi_animal',
     'name': 'Vector total food demand (animals/other)',
     'unit': 'x 1000 tonne',
     'in': ['FDi_cal', 'OFi', 'FDi', 'SSRi'],  # Specify what comes into the node
     'computation': {'name': 'SSRi/100*(OFi+AFDi)+FDi',  # When the node is compulationnal specify the computation like this
                     'formula': lambda X: (((X['SSRi'] * 1e-2) * (X['OFi'] + X['FDi'])) + X['FDi_cal']).loc[animal_products_2] * 1e-6}  # For now leave the formula field empty
     },
    {'type': 'output',
     'id': 'FDTi_total_cal',
     'name': 'Vector total food demand all',
     'unit': 'x 1000 tonne',
     'in': ['FDTi_animal', 'FDTi_crops_cal'],  # Specify what comes into the node
     'computation': {'name': 'concatenate FDTi_animal and FDTi_crops_cal',  # When the node is compulationnal specify the computation like this
                     'formula': lambda X: pd.concat((X['FDTi_crops_cal'], X['FDTi_animal']))}  # For now leave the formula field empty
     }
]
