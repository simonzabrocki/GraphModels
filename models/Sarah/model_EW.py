__author__ = 'Sarah'
__status__ = 'Pending Validation'

"""
TO DO.
"""
from graphmodels.graphmodel_exp import GraphModel, concatenate_graph_specs

# Conversions
height_rice = 0.2
ha_to_m2 = 1e3
mm_to_m = 1e-3

TWW_nodes = {'KC': {'type': 'parameter', 'unit': '1', 'name': 'Crop Factor Vector'},
             'CI': {'type': 'parameter', 'unit': '%', 'name': 'Cropping Intensity'},
             'ETo': {'type': 'input', 'unit': 'mm/year', 'name': 'Evapotranspiration'},
             'ETc': {'type': 'variable',
                     'name': 'Potential Crop Evaporation Vector',
                     'unit': 'mm/year',
                     'computation': lambda KC, CI, ETo, **kwargs: KC * ETo
                     },
             'ETa': {'type': 'input',
                     'unit': 'mm/year',
                     'name': 'Actual Evapotranspiration'},
             'ICU': {'type': 'variable',
                     'name': 'Irrigation Consumptive Use',
                     'unit': 'mm/year',
                     'computation': lambda ETc, ETa, **kwargs: ETc - ETa
                     },
             'AIR': {'type': 'parameter',
                     'unit': '1000 ha',
                     'name': 'Area Actually Irrigated'},
             'Arice': {'type': 'parameter',
                       'unit': '1000 ha',
                       'name': 'Area of Rice Paddy Irrigation'},
             'WRR': {'type': 'parameter', 'name': 'Water Requirement Ratio', 'unit': '1'},
             'PSIR': {'type': 'input',
                      'unit': '1',
                      'name': 'Proportion of Surface Irrigation'},
             'PSPIR': {'type': 'input',
                       'unit': '1',
                       'name': 'Proportion of Sprinker Irrigation'},
             'PLIR': {'type': 'input',
                      'unit': '1',
                      'name': 'Proportion of Localised Irrigation'},
             'ESIR': {'type': 'parameter',
                      'unit': '1',
                      'name': 'Efficiency of Surface Irrigation'},
             'ESPIR': {'type': 'parameter',
                       'unit': '1',
                       'name': 'Efficiency of Sprinker Irrigation'},
             'ELIR': {'type': 'parameter',
                      'unit': '1',
                      'name': 'Efficiency of Localised Irrigation'},
             'WRR_policy': {'type': 'variable',
                            'name': 'Water Requirement Ratio',
                            'unit': '1',
                            'computation': lambda PSIR, ESIR, PSPIR, ESPIR, PLIR, ELIR, **kwargs: PSIR / ESIR + PSPIR / ESPIR + PLIR / ELIR
                            },
             'IWR': {'type': 'variable',
                     'name': ' Irrigation Water Requirement',
                     'unit': 'm3/year',
                     'computation': lambda ICU, AIR, Arice, **kwargs: ha_to_m2 * ((mm_to_m * ICU * AIR).groupby(level='ISO').sum() + Arice * height_rice)
                     },
             'IWW': {'type': 'variable',
                     'name': ' Irrigation Water Withdrawal',
                     'unit': 'm3/year',
                     'computation': lambda IWR, WRR, **kwargs: IWR / WRR * 1e2
                     },
             'LWU': {'type': 'input', 'name': 'Livestock Water Use', 'unit': 'm3/year'},
             'AWU': {'type': 'variable', 'unit': 'm3/year',
                     'name': 'Agricultural Water Withdrawal',
                     'computation': lambda LWU, IWW, **kwargs: LWU + IWW
                     },
             'MWU': {'type': 'input',
                     'name': 'Municipal Water Withdrawal',
                     'unit': 'm3/year'},
             'IWU': {'type': 'parameter',
                     'name': 'Industrial Water Withdrawal',
                     'unit': 'm3/year'},
             'TWW': {'type': 'variable',
                     'name': 'Total Water Withdrawal',
                     'unit': 'm3/year',
                     'computation': lambda AWU, IWU, MWU, **kwargs: AWU + IWU + MWU
                     },
             }

EW1_nodes = {
    'AIR': {'type': 'parameter',
            'unit': '1000 ha',
            'name': 'Area Actually Irrigated'},
    'TC': {'type': 'parameter',
           'unit': '1000 ha',
           'name': 'Total Cultivated Land'},
    'Ai': {'type': 'variable',
           'name': 'Proportion of Irrigated Land',
           'unit': '',
           'computation': lambda AIR, TC, **kwargs: AIR / TC
           },
    'Cr': {'type': 'variable',
           'name': 'Corrective coefficient',
           'unit': '',
           'computation': lambda Ai, **kwargs: 1 / (1 + (Ai / (1 - Ai) * 0.375))
           },
    'AGVA': {'type': 'parameter',
             'name': 'Agricultural Gross Value Added',
             'unit': '$'},
    'IGVA': {'type': 'parameter',
             'name': 'Industrial Gross Value Added',
             'unit': '$'},
    'SGVA': {'type': 'parameter',
             'name': 'Service Sector Gross Value Added',
             'unit': '$'},
    'EW1': {'type': 'output',
            'name': 'Water Use Efficiency',
            'unit': '$/(m3/year)',
            'computation': lambda TWW, IGVA, SGVA, AGVA, **kwargs: (IGVA + SGVA + AGVA) / TWW
            }}


EW2_nodes = {'P': {'type': 'input', 'unit': 'mm/year', 'name': 'Precipitation'},
             'ETa': {'type': 'input', 'unit': 'mm/year', 'name': 'Actual Evapotranspiration'},
             'A': {'type': 'input', 'unit': 'ha', 'name': 'Catchment Size'},
             'S': {'type': 'variable',
                   'name': 'Change in Surface Water Storage',
                   'unit': 'm3/year',
                   'computation': lambda P, ETa, A, **kwargs: (P - ETa) * A * ha_to_m2 * mm_to_m
                   },
             'SW': {'type': 'parameter', 'unit': 'm3/year', 'name': 'Surface Water'},
             'GW': {'type': 'parameter', 'unit': 'm3/year', 'name': 'Groundwater Water'},
             'Overlap': {'type': 'parameter',
                         'unit': 'm3/year',
                         'name': 'Overlap (Surface - Groundwater)'},
             'IRWR': {'type': 'variable',
                      'name': 'Internal Renewable Water Resources',
                      'unit': 'm3/year',
                      'computation': lambda GW, SW, S, Overlap, **kwargs: GW + (SW - S) - Overlap
                      },
             'ERWR': {'type': 'parameter',
                      'unit': 'm3/year',
                      'name': 'External Renewable Water Resources'},
             'TRF': {'type': 'variable',
                     'name': 'Total Renewable Freshwater',
                     'unit': 'm3/year',
                     'computation': lambda IRWR, ERWR, **kwargs: IRWR + ERWR
                     },
             'DW': {'type': 'parameter', 'unit': 'm3/year', 'name': 'Desalination Water'},
             'TW': {'type': 'parameter', 'unit': 'm3/year', 'name': 'Treated Wastewater'},
             'TNCW': {'type': 'variable',
                      'name': 'Total Non Conventional Water',
                      'unit': 'm3/year',
                      'computation': lambda DW, TW, **kwargs: DW + TW
                      },
             'TFA': {'type': 'variable',
                     'name': 'Total Freshwater Available',
                     'unit': 'm3/year',
                     'computation': lambda TRF, TNCW, **kwargs: TRF + TNCW
                     },
             'TWW': {'type': 'input', 'unit': 'm3/year', 'name': 'Total Water Withdrawal'},
             'EFR': {'type': 'parameter',
                     'unit': 'm3/year',
                     'name': 'Environmental Flow Requirement'},
             'EW2': {'type': 'output',
                     'name': 'Share of Freshwater Withdrawal to Freshwater Availability',
                     'unit': '1',
                     'computation': lambda TWW, TFA, EFR, **kwargs: TWW / (TFA - EFR)
                     },
             'Natural EW2': {'type': 'output',
                             'name': 'Share of Freshwater Withdrawal to Freshwater Availability',
                             'unit': '1',
                             'computation': lambda TWW, TRF, EFR, **kwargs: TWW / (TRF - EFR)
                             }
             }

model_EW1 = GraphModel(concatenate_graph_specs([TWW_nodes, EW1_nodes]))

model_EW2 = GraphModel(concatenate_graph_specs([TWW_nodes, EW2_nodes]))
