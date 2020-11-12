import numpy as np

model_1 = [
    {'type': 'input',  # Type of node (input, output, variable, parameter)
     'unit': 'kg/capita/yr',  # Unit
     'id': 'FDKG2017_i',  # Unique code to define the node
     'name': 'Vector KG food demand',  # Full name
     },
    {'type': 'input',  # Type of node (input, output, variable, parameter)
     'unit': 'kcal/capita/day',  # Unit
     'id': 'FDKC2017_i',  # Unique code to define the node
     'name': 'Vector of KCAL food demand',  # Full name
     },
    {'type': 'input',  # Type of node (input, output, variable, parameter)
     'unit': 'hg/ha',  # Unit
     'id': 'CYi',  # Unique code to define the node
     'name': 'Vector crop yields',  # Full name
     },
    {'type': 'variable',
     'id': 'KKRi',
     'name': 'Vector Kcal/kg ratio 2017',
     'unit': 'Kcal/kg',
     'in': ['FDKG2017_i', 'FDKC2017_i'],  # Specify what comes into the node
     'computation': {'name': 'FDKC2017_i/(FDKG2017_i/365)',  # When the node is compulationnal specify the computation like this
                     'formula': lambda X: (X['FDKC2017_i'] / (X['FDKG2017_i'] / 365))}  # For now leave the formula field empty

     },
    {'type': 'variable',  # Type of node (input, output, variable, parameter)
     'unit': '%',  # Unit
     'id': 'SSRi',  # Unique code to define the node
     'name': 'Self-sufficiency ratio',  # Full name
     'in': ['FPi', 'FEi', 'FIi'],  # Specify what comes into the node
     'computation': {'name': '100*FPi/(FPi-FEi+FIi)',  # When the node is compulationnal specify the computation like this
                     'formula': lambda X: np.nan_to_num((100 * X['FPi']) / (X['FPi'] - X['FEi'] + X['FIi']))}  # For now leave the formula field empty
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
    {'type': 'variable',  # Type of node (input, output, variable, parameter)
     'unit': 'kcal/cap/day',  # Unit
     'id': 'FWi',  # Unique code to define the node
     'name': 'Vector food waste',  # Full name
     'in': ['FWP2017i', 'FWPPi'],  # Specify what comes into the node
     'computation': {'name': 'FWP2017i*FWPPi',  # When the node is compulationnal specify the computation like this
                     'formula': lambda X: X['FWP2017i'] * X['FWPPi']}  # For now leave the formula field empty
     },
    {'type': 'input',  # Type of node (input, output, variable, parameter)
     'unit': 'kcal/cap/day',  # Unit
     'id': 'FWP2017i',  # Unique code to define the node
     'name': 'Vector food waste 2017',  # Full name
     },
    {'type': 'variable',  # Type of node (input, output, variable, parameter)
     'unit': 'heads',  # Unit
     'id': 'ANPi',  # Unique code to define the node
     'name': 'Vector animals needed for production',  # Full name
     'in': ['FDi_an', 'AYi'],  # Specify what comes into the node
     'computation': {'name': '(FDi_an*1000000)/AYi',  # When the node is compulationnal specify the computation like this
                     'formula': lambda X: (X['FDi_an'] * 1000000) / X['AYi']}  # For now leave the formula field empty

     },
    {'type': 'variable',  # Type of node (input, output, variable, parameter)
     'unit': 'heads',  # Unit
     'id': 'FDi_an',  # Unique code to define the node
     'name': 'selection animal-based food groups',  # Full name
     'in': ['FDTi_animal'],  # Specify what comes into the nod
     'computation': {'name': 'Selection animal-based food groups',  # When the node is compulationnal specify the computation like this
                     'formula': lambda X: np.array([X['FDTi_animal'][0], X['FDTi_animal'][2], X['FDTi_animal'][3], X['FDTi_animal'][7], X['FDTi_animal'][8], (X['FDTi_animal'][1] + X['FDTi_animal'][4])])}  # selects the food groups that are animal based


     },
    {'type': 'input',  # Type of node (input, output, variable, parameter)
     'unit': '%',  # Unit
     'id': 'FWPPi',  # Unique code to define the node
     'name': 'Food waste reduction policy',  # Full name
     },
    {'type': 'input',  # Type of node (input, output, variable, parameter)
     'unit': 'kcal/cap/day',  # Unit
     'id': 'FWCRi',  # Unique code to define the node
     'name': 'Vector waste reduction policy consumption',  # Full name
     },
    {'type': 'variable',  # Type of node (input, output, variable, parameter)
     'unit': '1000 t',  # Unit
     'id': 'FDi',  # Unique code to define the node
     'name': 'Vector total domestic food production',  # Full name
     'in': ['KKRi', 'SSRi', 'TCDi'],  # Specify what comes into the node
     'computation': {'name': '(TCDi * SSRi/100 * 365)/KKRi',  # When the node is compulationnal specify the computation like this
                     'formula': lambda X: np.nan_to_num((X['TCDi'] * X['SSRi'] / 100 * 365) / X['KKRi'])}  # For now leave the formula field empty
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
     'id': 'TCDi',  # Unique code to define the node
     'name': 'Total calorie demand per food group',  # Full name
     'in': ['P', 'FWi', 'FWCRi', 'FDKC2017_i'],  # Specify what comes into the node
     'computation': {'name': 'P*(FDKC2017_i+FWi-FWCRi)',  # When the node is compulationnal specify the computation like this
                     'formula': lambda X: X['P'] * (X['FDKC2017_i'] + X['FWi'] - X['FWCRi'])}  # For now leave the formula field empty
     },
    {'type': 'variable',  # Type of node (input, output, variable, parameter)
     'unit': '1000 t',  # Unit
     'id': 'AFDi',  # Unique code to define the node
     'name': 'Vector total animal feed demand',  # Full name
     'in': ['FMi', 'FD'],  # Specify what comes into the node
     'computation': {'name': 'FMi * FD',  # When the node is compulationnal specify the computation like this
                     'formula': lambda X: X['FMi'][0:13] * X['FD']}  # For now leave the formula field empty
     },


    {'type': 'variable',  # Type of node (input, output, variable, parameter)
     'unit': '',  # Unit
     'id': 'FMi',  # Unique code to define the node
     'name': 'Feed mix fraction',  # Full name
     'in': ['FDi2017'],  # Specify what comes into the node
     'computation': {'name': 'FDi2017/SUM(FDI2017)',  # When the node is compulationnal specify the computation like this
                     'formula': lambda X: X['FDi2017'] / sum(X['FDi2017'])}  # For now leave the formula field empty
     },
    {'type': 'input',  # Type of node (input, output, variable, parameter)
     'unit': '1000 t',  # Unit
     'id': 'FDi2017',  # Unique code to define the node
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
     'in': ['FCRi', 'AYi', 'ANPi'],  # Specify what comes into the node
     'computation': {'name': '(FRCi*AYi*ANPi)/1000000',  # When the node is compulationnal specify the computation like this
                     'formula': lambda X: (X['FCRi'] * X['AYi'] * X['ANPi']) / 1000000}  # For now leave the formula field empty
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
    # crops vs. animals are split to prevent cycle error; (2017 values for 'milk' as animal feed' are used)
    {'type': 'output',
     'id': 'FDTi_crops',
     'name': 'Vector total food demand (crops)',
     'unit': 'x 1000 tonne',
     'in': ['FDi', 'OFi', 'AFDi', 'SSRi'],  # Specify what comes into the node
     'computation': {'name': 'SSRi/100*(OFi+AFDi)+FDi',  # When the node is compulationnal specify the computation like this
                     'formula': lambda X: ((X['SSRi'][0:13] / 100) * (X['OFi'][0:13] + X['AFDi'][0:13])) + (X['FDi'][0:13] / 1000000)}  # For now leave the formula field empty
     },
    {'type': 'output',
     'id': 'FDTi_animal',
     'name': 'Vector total food demand (animals/other)',
     'unit': 'x 1000 tonne',
     'in': ['FDi', 'OFi', 'FDi2017', 'SSRi'],  # Specify what comes into the node
     'computation': {'name': 'SSRi/100*(OFi+AFDi)+FDi',  # When the node is compulationnal specify the computation like this
                     'formula': lambda X: ((X['SSRi'][13:25] / 100) * (X['OFi'][13:25] + X['FDi2017'][13:25])) + X['FDi'][13:25] / 1000000}  # For now leave the formula field empty
     },
    {'type': 'output',
     'id': 'FDTi_total',
     'name': 'Vector total food demand all',
     'unit': 'x 1000 tonne',
     'in': ['FDTi_animal', 'FDTi_crops'],  # Specify what comes into the node
     'computation': {'name': '',  # When the node is compulationnal specify the computation like this
                     'formula': lambda X: np.append(X['FDTi_crops'], X['FDTi_animal'])}  # For now leave the formula field empty
     },
]
