FDi_nodes = [
    # FDTi from the previous function
    {'type': 'input',
     'unit': '1000 t',
     'id': 'FDTi',
     'name': 'Total food demand per food group',

     },
    {'type': 'variable',
     'unit': '1000 t',
     'id': 'FDi_baseline',
     'name': 'Vector total animal feed demand per crop',
     'in': ['FMi', 'FD'],
     'computation': {'name': 'FMi * FD',
                     'formula': lambda X: X['FMi']*X['FD']}
     },
    # Note1: The vector 'FMi' might contain animal-based feed (i.e. Milk) which caused a cycle error in my previous model; so we want to select only crops from the vector FMI
    {'type': 'variable',
     'unit': '',
     'id': 'FMi',
     'name': 'Feed mix fraction',
     'in': ['FDi'],
     'computation': {'name': 'FDi/SUM(FDi)',
                     'formula': lambda X: X['FDi'].loc[Crop_group]/sum(X['FDi'])}
     },
    {'type': 'input',
     'unit': '1000 t',
     'id': 'FDi',
     'name': 'Vector feed demand',

     },

    # Note2: the CRfd is calculated for the year 2017; and assumed constant. For hungary the value of CRfd is: 1.58729526339088

    {'type': 'variable',
     'unit': '1ooo t',
     'id': 'FD',
     'name': 'Total crop-feed demand',
     'in': ['TAFDi', 'CRfd'],
     'computation': {'name': 'SUM(TAFDi)/CRfd',
                     'formula': lambda X: sum(X['TAFDi'])/X['CRfd']}
     },

    # CRfd is calculated with model data from  & assumed constant for simulated years (for now)
    {'type': 'parameter',
     'unit': '',
     'id': 'CRfd',
     'name': 'feed/forage distribution (correction)',
     },

    {'type': 'parameter',
     'unit': 'kg DM feed/ kg EW',
     'id': 'FCRi',
     'name': 'feed conversion ratio ',
     },
    {'type': 'variable',
     'unit': 'kg',
     'id': 'TAFDi',
     'name': 'vector total animal feed demand per animal',
     'in': ['FCRi', 'FDTi'],
     'computation': {'name': 'FRCi*FDTi_animal',
                     'formula': lambda X: (X['FCRi'] * X['FDTi'].loc[Animal_group])}
     }
]
