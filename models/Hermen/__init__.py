MWU_nodes = {'P': {'type': 'input', 'name': 'Water Price', 'unit': '$/15m3'},
             'GDPC': {'type': 'parameter', 'name': 'GDP per capita', 'unit': '$'},
             'MWUD': {'type': 'variable',
                      'name': 'Municipal Water Demand',
                      'unit': 'm3/year/person',
                      'computation': lambda GDPC, P, **kwargs: 2.39 * GDPC**0.37 * P**-0.33
                      },
             'Pop': {'type': 'parameter', 'name': 'Population', 'unit': 'millions'},
             'MWU': {'type': 'variable',
                     'name': 'Municipal Water Withdrawal',
                     'unit': 'm3/year',
                     'computation': lambda MWUD, Pop, **kwargs: MWUD * Pop
                     }
             }
MWU_model = GraphModel(MWU_nodes)
MWU_model.draw()
