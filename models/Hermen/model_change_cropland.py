# Refactored

BE2_nodes = [
    {'type': 'input',
     'unit': '1000 ha',
     'id': 'LUi',
     'name': 'vector land use',
     },

    # from previous part
    {'type': 'variable',
     'id': 'chCL',
     'name': 'Change in cropland',
     'unit': 'x 1000ha'
     },

    {'type': 'variable',
     'id': 'TCropDi_sum',
     'name': 'Sum total cropland demand',
     'unit': 'x 1000ha'
     },
    # for the land stocks you start with the baseline & for each iteration the old value should be stored. So for the next iteration in t+2, this updated land-stocks from t+1 are used
    # After the new land use distribution these values should be updated:
    # IL_stock_newRF --> IL_stock
    # FL_stock_newRF --> FL_stock
    # CL_stock_new--> CL_stock

    {'type': 'input',
     'unit': 'x1000 ha',
     'id': 'CL_stock',
     'name': 'Cropland t-1',
     },
    {'type': 'input',
     'unit': 'x1000 ha',
     'id': 'IL_stock',
     'name': 'Inactive land t-1',
     },
    {'type': 'input',
     'unit': 'x1000 ha',
     'id': 'FL_stock',
     'name': 'Forest land t-1',
     },
    {'type': 'variable',
     'id': 'CL_stock_new',
     'name': 'Cropland stock',
     'unit': 'x 1000ha',
     'in': ['chCL', 'CL_stock'],
     'computation': {'name': 'CL_stock + chCL',
                     'formula': lambda X: CL(X['chCL'], X['CL_stock'])}
     },
    {'type': 'variable',
     'id': 'IL_stock_new',
     'name': 'Inactive land stock',
     'unit': 'x 1000 ha',
     'in': ['chCL', 'IL_stock'],
     'computation': {'name': 'f(chCL, CL_stock) ',
                     'formula': lambda X: IL(X['chCL'], X['IL_stock'])}
     },
    {'type': 'variable',
     'id': 'FL_stock_new',
     'name': 'Forest land stock',
     'unit': 'x 1000ha',
     'in': ['chCL', 'FL_stock', 'IL_stock_new'],
     'computation': {'name': 'f(chCL, FL_stock, IL_stock_new)',
                     'formula': lambda X: FL(X['chCL'], X['FL_stock'], X['IL_stock_new'])}
     },
    {'type': 'parameter',
     'unit': '%',
     'id': 'R_rate',
     'name': 'Rate of reforestation',
     },
    {'type': 'variable',
     'id': 'RF_land',
     'name': 'Reforestation of land',
     'unit': 'x 1000ha',
     'in': ['R_rate', 'IL_stock_new'],
     'computation': {'name': 'R_rate*IL_stock_new',
                     'formula': lambda X: X['R_rate']*1e-2*X['IL_stock_new']}
     },
    {'type': 'variable',
     'id': 'FL_stock_new_RF',
     'name': 'New forest land stock after reforestation policy',
     'unit': 'x 1000ha',
     'in': ['RF_land', 'FL_stock_new'],
     'computation': {'name': 'FL_stock_new+RF_land',
                     'formula': lambda X: X['FL_stock_new']+X['RF_land']}
     },
    {'type': 'variable',
     'id': 'IL_stock_new_RF',
     'name': 'New inactive land stock after reforestation policy',
     'unit': 'x 1000ha',
     'in': ['RF_land', 'IL_stock_new'],
     'computation': {'name': 'IL_stock_new-RF_land',
                     'formula': lambda X: X['IL_stock_new'] - X['RF_land']}
     },
    {'type': 'input',
     'unit': '1000 ha',
     'id': 'TLA',
     'name': 'Total land area',
     'in': ['LUi'],
     'computation': {'name': 'Select',
                     'formula': lambda X: X['LUi'].loc['Land area']}
     },
    {'type': 'input',
     'unit': '1000 ha',
     'id': 'TFA2017',
     'name': 'Forest land area (2017)',
     'in': ['LUi'],
     'computation': {'name': 'Select',
                     'formula': lambda X: X['LUi'].loc['Forest land']}
     },
    {'type': 'output',
     'id': 'BE2',
     'name': 'Share of forest area to total land area',
     'unit': '%',
     'in': ['TLA', 'FL_stock_new_RF'],
     'computation': {'name': '100*(FL_stock_new_RF / TLA)',
                     'formula': lambda X:  100 * (X['FL_stock_new_RF']) / X['TLA']}
     },
    # Used in fertilizer computation -> as FAO nutrient balance uses the total cropland including permanent + fallow lands for fertilizer; LUi['land under permanent crops'] is added again; assumed constant)
    {'type': 'output',
     'id': 'TOT_CL_NEW',
     'name': 'Total new cropland (including perm. and fallow land)',
     'unit': 'x 1000ha',
     'in': ['TCropDi_sum', 'chCL', 'LUi', 'FL_stock', 'FL_stock_new'],
     'computation': {'name': 'TCropDi_sum+chCL+CL_perm+(IL_stock-IL_stock_new)',
                     'formula': lambda X: (X['TCropDi_sum']-X['chCL']+X['LUi'].loc['Land under permanent crops']+(X['IL_stock']-X['IL_stock_new']))}
     },


]


def CL(chCL, CL_stock):
    return chCL + CL_stock


def FL(chCL, FL_stock, IL_stock):
    if (chCL > 0) and (IL_stock - chCL < 0):
        return FL_stock + IL_stock - chCL
    else:
        return FL_stock


def IL(chCL, IL_stock):
    if (chCL > 0) and (IL_stock - chCL < 0):
        return 0
    else:
        return IL_stock - chCL


model_BE2 = GraphModel(BE2_nodes)

model_BE2.draw()
