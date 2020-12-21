Animal_group = ['Bovine meat', 'Pigmeat', 'Poultry meat', 'Eggs',
                'Milk - Excluding Butter', ('Meat, other' + 'Mutton & Goat meat')]


CRfd_nodes = [
    {'type': 'parameter',
     'unit': '',
     'id': 'CRfd',
     'name': 'feed/forage distribution (correction)',
     'in': ['TAFDi2017_cal', 'FDi2017'],
     'computation': {'name': 'SUM((TAFDi2017_cal/FDi2017))',
                     'formula': lambda X: sum((X['TAFDi2017_cal'])/(X['FDi2017'].loc[Animal_group]))}
     },
    {'type': 'input',
     'unit': '1000 t',
     'id': 'FDi2017',
     'name': 'Vector feed demand',
     },
    # So this computation uses the 2017 'FPi' value to calculate the 'TAFDi2017_cal' instead of the whole food demand computation for 2017.
    {'type': 'variable',
     'unit': 'kg',
     'id': 'TAFDi2017_cal',
     'name': 'Vector total animal feed demand per animal',
     'in': ['FCRi', 'FPi'],
     'computation': {'name': '(FRCi*FPi)',
                     'formula': lambda X: (X['FCRi'] * X['FPi'].loc[Animal_group])}
     },
    {'type': 'parameter',
     'unit': 'kg DM feed/ kg EW',
     'id': 'FCRi',
     'name': 'feed conversion ratio ',
     },
    {'type': 'input',
     'unit': '1000 t',
     'id': 'FPi',
     'name': 'Food production per food group',
     },
]
