#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Sarah'
__status__ = 'Validated'

"""
Freshwater Available

Short description of input/outputs assumptions etc etc
"""

FreshwaterAvailableNodes = [
    {'type': 'input',
     'unit': 'mm/year',
        'name': 'Precipitation',
     'id': 'P'},
    {'type': 'input',
     'unit': 'mm/year',
        'name': 'Evapotranspiration',
     'id': 'ET'},
    {'type': 'input',
     'unit': 'ha',
        'name': 'Catchment Size',
     'id': 'A'},
    {'type': 'variable',
     'name': 'Change in Surface Water Storage',
     'unit': 'mm/year',  # need to look into conversion of units think it would be m3/year
     'in': ['P', 'ET', 'A'],
     'computation': {'name': '(P - ET)*A', 'formula': lambda X: (X['P'] - X['ET']) * X['A']},
     'id': 'S'},
    # Renewable Water Resources
    {'type': 'parameter',
        'unit': 'm3/year',
        'name': 'Surface Water',
     'id': 'SW'},
    {'type': 'parameter',
        'unit': 'm3/year',
        'name': 'Groundwater Water',
     'id': 'GW'},
    {'type': 'parameter',
        'unit': 'm3/year',
        'name': 'Overlap (Surface - Groundwater)',
     'id': 'Overlap'},
    {'type': 'variable',
     'name': 'Internal Renewable Water Resources',
     'unit': 'm3/year',
     'in': ['SW', 'GW', 'Overlap', 'S'],
     'computation': {'name': 'GW + (SW + S) - Overlap', 'formula': lambda X: X['GW'] + (X['SW'] - X['S']) - X['Overlap']},
     'id': 'IRWR'},
    {'type': 'parameter',
        'unit': 'm3/year',
        'name': 'External Renewable Water Resources',
     'id': 'ERWR'},
    {'type': 'variable',
     'name': 'Total Renewable Freshwater',
     'unit': 'm3/year',
     'in': ['IRWR', 'ERWR'],
     'computation': {'name': 'IRWR + ERWR', 'formula': lambda X: X['IRWR'] + X['ERWR']}, 'id': 'TRF'},

    # Non conventional water
    {'type': 'parameter',
        'unit': 'm3/year',
        'name': 'Desalination Water',
     'id': 'DW'},
    {'type': 'parameter',
        'unit': 'm3/year',
        'name': 'Treated Wastewater',
        'id': 'TW'},
    {'type': 'variable',
     'name': 'Total Non Conventional Water',
     'unit': 'm3/year',
     'in': ['DW', 'TW'],
     'computation': {'name': 'DW + TW', 'formula': lambda X: X['DW'] + X['TW']}, 'id': 'TNCW'},
    {'type': 'variable',
        'name': 'Total Freshwater Available',
        'unit': 'm3/year',
        'in': ['TRF', 'TNCW'],
        'computation': {'name': 'TRF + TNCW', 'formula': lambda X: X['TRF'] + X['TNCW']}, 'id': 'TFA'},
    # calculation of EW 2
    # input from water use model
    {'type': 'input',
        'unit': 'm3/year',
        'name': 'Total Water Withdrawal',
     'id': 'TWW'},
    {'type': 'parameter',
     'unit': 'm3/year',
        'name': 'Environmental Flow Requirement',
     'id': 'EFR'},

    # inclusion of both natural and non-conventional water sources
    {'type': 'output',
     'name': 'Share of Freshwater Withdrawal to Freshwater Availability',
     'unit': '%',
     'in': ['TFA', 'TWW', 'EFR'],
     'computation': {'name': 'TWW/(TFA-EFR)*100', 'formula': lambda X: X['TWW'] / (X['TFA'] - X['EFR']) * 100}, 'id': 'EW2'},

    # only natural water sources
    {'type': 'output',
     'name': 'Share of Freshwater Withdrawal to Freshwater Availability',
     'unit': '%',
     'in': ['TRF', 'TWW', 'EFR'],
     'computation': {'name': 'TWW/(TRF-EFR)*100', 'formula': lambda X: X['TWW'] / (X['TRF'] - X['EFR']) * 100}, 'id': 'Natural EW2'},

]
