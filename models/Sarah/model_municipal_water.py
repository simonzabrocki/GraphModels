#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Sarah'
__status__ = 'Validated'

"""
Municipal Water

Short description of input/outputs assumptions etc etc
"""

MunicipalWaterNodes = [
    {'type': 'input',
     'name': 'Municipal Water Withdrawal',  # should be connecting to MWU variable from first water use model
     'unit': 'm3/year',
     'id': 'MWU'},

    {'type': 'input',
        'name': 'Water Supply Efficiency',  # can also be a parameter if we want to keep constant
        'unit': '',
        'id': 'WSE'},

    {'type': 'variable',
        'name': 'Municipal Water Consumption',
        'unit': 'm3/year',
        'in': ['MWU', 'WSE'],
        'computation': {'name': 'MWU * WSE', 'formula': lambda X: X['MWU'] * X['WSE']}, 'id': 'MWC'},

    # Identifying proportion of urban population with sanitation
    {'type': 'parameter',
     'name': 'Fraction of Urban to Total Pop',
     'unit': '',
     'id': 'Upop'},

    {'type': 'parameter',  # should be the output value from the AB1 indicator model
     'name': 'AB1 Urban Access to Sanitation',
     'unit': '',
     'id': 'UAB1'},

    {'type': 'variable',
     # current only consider wastewater from urban areas, could include rural by using same methodology above
     'name': ' Urban Wastewater Collected',
        'unit': 'm3',
        'in': ['MWC', 'Upop', 'UAB1'],
     'computation': {'name': '((MWC * Upop * UAB1)', 'formula': lambda X: X['MWC'] * X['Upop'] * X['UAB1']}, 'id': 'UW'},

    # Wastewater treatment scenario
    {'type': 'input',
     'name': 'Number of Activated Sludge Treatment Facilities',
     'unit': '',
     'id': 'ASF'},
    {'type': 'parameter',
     'name': 'Activated Sludge Treatment Capacity',
     'unit': 'kilotons',
     'id': 'ASTC'},
    {'type': 'parameter',
     'name': 'AS Sewage Efficiency',
     'unit': '',
     'id': 'ASE'},
    {'type': 'variable',
     'name': 'AS Treated Wastewater',
     'unit': 'kilotons',
     'in': ['ASF', 'ASTC', 'ASE'],
     'computation': {'name': 'Facilities * ASTC * Sewage Efficiency ', 'formula': lambda X: X['ASF'] * X['ASTC'] * X['ASE']}, 'id': 'ASTW'},

    {'type': 'input',
     'name': 'Number of Biomembrane Treatment Facilities',
     'unit': '',
     'id': 'BF'},
    {'type': 'parameter',
     'name': 'Biomembrane Treatment Capacity',
     'unit': 'kilotons',
     'id': 'BMTC'},
    {'type': 'parameter',
     'name': 'BM Sewage Efficiency',
     'unit': '',
     'id': 'BME'},
    {'type': 'variable',
     'name': 'BM Treated Wastewater',
     'unit': 'kilotons',
     'in': ['BF', 'BMTC', 'BME'],
     'computation': {'name': 'Facilities * BMTC * Sewage Efficiency', 'formula': lambda X: X['BF'] * X['BMTC'] * X['BME']}, 'id': 'BMTW'},

    {'type': 'variable',
     'name': 'Total Treated Capacity',
     'unit': 'kilotons',
     'in': ['ASTW', 'BMTW'],
     'computation': {'name': 'ASWT + BMTW', 'formula': lambda X: X['ASTW'] + X['BMTW']}, 'id': 'TTC'},


    # converting from kiloton -> kg -> m3 - this will be the input for the Total Treated Wastewater in the Freshwater Availability part of the model
    {'type': 'output',
     'name': 'Total Treated Wastewater',
     'unit': 'm3/year',
     'in': ['TTC'],
     'computation': {'name': '((TTC)*1000000)/1000', 'formula': lambda X: X['TTC'] * 1000000 / 1000}, 'id': 'TTW'},

    # amount of investment required per technology
    {'type': 'parameter',
     'name': 'AS Construction Cost',
     'unit': '$',
     'id': 'ASCAPEX'},

    {'type': 'parameter',
     'name': 'AS Operational Cost Vector',
     'unit': '$/ton',
     'id': 'ASOPEX'},

    {'type': 'variable',
     'name': 'Potential AS Investment Cost',
     'unit': '$',
     'in': ['ASCAPEX', 'ASOPEX', 'ASTW'],
     'computation': {'name': 'CAPEX + (OPEX*1000)*ASTW', 'formula': lambda X: X['ASCAPEX'] + X['ASOPEX'] * 1000 * X['ASTW']}, 'id': 'ASIC'},

    {'type': 'parameter',
        'name': 'BM Construction Cost',
        'unit': '$',
        'id': 'BMCAPEX'},
    {'type': 'parameter',
     'name': 'AS Operational Cost Vector',
     'unit': '$/ton',
     'id': 'BMOPEX'},
    {'type': 'variable',
     'name': 'Potential BM Investment Cost',
     'unit': '$',
     'in': ['BMCAPEX', 'BMOPEX', 'BMTW'],
     'computation': {'name': 'CAPEX + (OPEX*1000)*BMTW', 'formula': lambda X: X['BMCAPEX'] + X['BMOPEX'] * 1000 * X['BMTW']}, 'id': 'BMIC'},

    {'type': 'output',
     'name': 'Potential Investment Cost',
     'unit': '$',
     'in': ['ASIC', 'BMIC'],
     'computation': {'name': 'ASIC + BMIC', 'formula': lambda X: X['ASIC'] + X['BMIC']}, 'id': 'PIC'},

    # amount of untreated wastewater and link to DALY
    {'type': 'variable',
     'name': 'Untreated Wastewater',
     'unit': 'kilotons',
     'in': ['TTW', 'UW'],
     'computation': {'name': 'UW - TWW', 'formula': lambda X: X['UW'] - X['TTW']}, 'id': 'UTW'},

    # for further discussion
    # how untreated wastewater increases the burden of disease -> social cost of pollution
    # comparing the potential investment costs to the social benefit of reducing wastewater pollution.
]
