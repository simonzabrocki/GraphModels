#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'Sarah'
__status__ = 'Validated'

"""
Agricultural Water Use

All water metrics from FAO data needed to be converted to 10^9 before modelling
For future projections we can assume there will not be a change in type of crops.
"""


AgriculturalWaterNodes = [
    {
        'type': 'input',
        'unit': '',
        'name': 'Crop Factor Vector',
        'id': 'KC',
    },
    {
        'type': 'parameter',
        'unit': '%',
        'name': 'Cropping Intensity',
        'id': 'CI',
    },
    {
        'type': 'input',
        'unit': 'mm/year',
        'name': 'Evapotranspiration',
        'id': 'ETo',
    },
    {
        'type': 'variable',
        'name': 'Potential Crop Evaporation Vector',
        'unit': 'mm/year',
        'in': ['KC', 'ETo', 'CI'],
        'computation': {'name': 'KC * CI * ETo', 'formula': lambda X: X['KC'] * X['CI'] * X['ETo']},
        'id': 'ETc',
    },
    {
        'type': 'input',
        'unit': 'mm/year',
        'name': 'Actual Evapotranspiration',
        'id': 'ETa',
    },
    {
        'type': 'variable',
        'name': 'Irrigation Consumptive Use',
        'unit': 'mm/year',
        'in': ['ETc', 'ETa'],
        'computation': {'name': 'ETc - ETa', 'formula': lambda X: X['ETc'] - X['ETa']},
        'id': 'ICU',
    },
    {
        'type': 'input',
        'unit': 'ha (1000)',
        'name': 'Area Actually Irrigated',
        'id': 'AIR',
    },
    {
        'type': 'parameter',
        'unit': 'ha (1000)',
        'name': 'Area of Rice Paddy Irrigation',
        'id': 'ARice',
    },
    {
        'type': 'variable',
        'name': 'Irrigation Water Requirement',
        'unit': 'm3/year',
        'in': ['ICU', 'AIR', 'ARice'],
        'computation': {'name': '(ICU*AIR) + (0.2*ARice) ',
                        'formula': lambda X: sum(X['ICU'] * X['AIR'] + X['ARice'] * 0.2)},
        'id': 'IWR',
    },
    {
        'type': 'parameter',
        'name': 'Water Requirement Ratio',
        'unit': '',
        'id': 'WRR',
    },
    {
        'type': 'variable',
        'name': 'Irrigation Water Withdrawal',
        'unit': 'm3/year',
        'in': ['IWR', 'WRR'],
        'computation': {'name': 'IWR/WRR', 'formula': lambda X: X['IWR'
                                                                  ] / X['WRR']},
        'id': 'IWW',
    },
    {
        'type': 'parameter',
        'name': 'Livestock Water Use',
        'unit': 'm3/year',
        'id': 'LWU',
    },
    {
        'type': 'variable',
        'name': 'Agricultural Water Withdrawal',
        'unit': 'm3/year',
        'in': ['IWW', 'LWU'],
        'computation': {'name': 'IWW + LWU', 'formula': lambda X:
                        X['IWW'] + X['LWU']},
        'id': 'AWU',
    },
    {
        'type': 'input',
        'name': 'Industrial Water Withdrawal',
        'unit': 'm3/year',
        'id': 'IWU',
    },
    {
        'type': 'input',
        'name': 'Water Price',
        'unit': '$/15m3',
        'id': 'P',
    },
    {
        'type': 'parameter',
        'name': 'GDP per capita',
        'unit': '$',
        'id': 'GDPC',
    },
    {
        'type': 'variable',
        'name': 'Municipal Water Demand',
        'unit': 'm3/year/person',
        'in': ['P', 'GDPC'],
        'computation': {'name': '2.39 * GDPC^0.37 * Price^-0.33 ',
                        'formula': lambda X: 2.39 * X['GDPC'] ** 0.37 * X['P'] ** -0.33},
        'id': 'MWUD',
    },
    {
        'type': 'parameter',
        'name': 'Population',
        'unit': 'millions',
        'id': 'Pop',
    },
    {
        'type': 'variable',
        'name': 'Municipal Water Withdrawal',
        'unit': 'm3/year',
        'in': ['Pop', 'MWUD'],
        'computation': {'name': 'MWUD * Pop ', 'formula': lambda X:
                        X['MWUD'] * X['Pop']},
        'id': 'MWU',
    },
    {
        'type': 'variable',
        'name': 'Total Water Withdrawal',
        'unit': 'm3/year',
        'in': ['MWU', 'AWU', 'IWU'],
        'computation': {'name': 'AWU + IWU + MWU', 'formula': lambda X:
                        X['AWU'] + X['IWU'] + X['MWU']},
        'id': 'TWW',
    },
    {
        'type': 'parameter',
        'unit': 'ha (1000)',
        'name': 'Total Cultivated Land',
        'id': 'TC',
    },
    {
        'type': 'variable',
        'name': 'Proportion of Irrigated Land',
        'unit': '',
        'in': ['AIR', 'TC'],
        'computation': {'name': 'AIR/TC', 'formula': lambda X: X['AIR'] / X['TC']},
        'id': 'Ai',
    },
    {
        'type': 'variable',
        'name': 'Corrective coefficient',
        'unit': '',
        'in': ['Ai'],
        'computation': {'name': '1/(1+(Ai/(1-Ai)*0.375)',
                        'formula': lambda X: 1 / (1 + X['Ai'] / (1 - X['Ai']) * 0.375)},
        'id': 'Cr',
    },
    {
        'type': 'parameter',
        'name': 'Agricultural Gross Value Added',
        'unit': '$',
        'id': 'AGVA',
    },
    {
        'type': 'variable',
        'name': 'Agricultural Water Use Efficiency',
        'unit': '$/m3',
        'in': ['AGVA', 'Cr', 'AWU'],
        'computation': {'name': 'AGVA * (1-Cr)/AWU',
                        'formula': lambda X: X['AGVA'] * (1 - X['Cr']) / X['AWU']},
        'id': 'WUEa',
    },
    {
        'type': 'parameter',
        'name': 'Industrial Gross Value Added',
        'unit': '$',
        'id': 'IGVA',
    },
    {
        'type': 'variable',
        'name': 'Industrial Water Use Efficiency',
        'unit': '$/m3',
        'in': ['IGVA', 'IWU'],
        'computation': {'name': 'IGVA/IWU', 'formula': lambda X: X['IGVA'] / X['IWU']},
        'id': 'WUEi',
    },
    {
        'type': 'parameter',
        'name': 'Service Sector Gross Value Added',
        'unit': '$',
        'id': 'SGVA',
    },
    {
        'type': 'variable',
        'name': 'Service Sector Water Use Efficiency',
        'unit': '$/m3',
        'in': ['SGVA', 'MWU'],
        'computation': {'name': 'SGVA/MWU', 'formula': lambda X: X['SGVA'] / X['MWU']},
        'id': 'WUEs',
    },
    {
        'type': 'variable',
        'name': 'Proportion of Agricultural Water Use',
        'unit': '',
        'in': ['AWU', 'TWW'],
        'computation': {'name': 'AWU/TWW', 'formula': lambda X: X['AWU'] / X['TWW']},
        'id': 'Pa',
    },
    {
        'type': 'variable',
        'name': 'Proportion of Industrial Water Use',
        'unit': '',
        'in': ['IWU', 'TWW'],
        'computation': {'name': 'IWU/TWW', 'formula': lambda X: X['IWU'] / X['TWW']},
        'id': 'Pi',
    },
    {
        'type': 'variable',
        'name': 'Proportion of Municipal Water Use',
        'unit': '%',
        'in': ['MWU', 'TWW'],
        'computation': {'name': 'MWU/TWW', 'formula': lambda X: X['MWU'] / X['TWW']},
        'id': 'Ps',
    },
    {
        'type': 'output',
        'name': 'Total Water Use Efficiency',
        'unit': '$/m3',
        'in': [
            'WUEa',
            'Pa',
            'WUEi',
            'Pi',
            'WUEs',
            'Ps',
        ],
        'computation': {'name': 'WUEa*Pa + WUEi*Pi + WUEs*Ps',
                        'formula': lambda X: X['WUEa'] * X['Pa'] + X['WUEi'] * X['Pi'] + X['WUEs'] * X['Ps']},
        'id': 'EW 1',
    },
]
