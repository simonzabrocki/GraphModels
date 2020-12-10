import numpy as np
import pandas as pd
import json


def parse_model_data(path):
    '''Parse the model data in json file.

    Args:
        path(str): path to the json file.

    Returns:
        inputs(dict): Inputs of the model.
        parameters(dict): Parameters of the model.
    '''
    with open(path) as json_file:
        inputs_parameters = json.load(json_file)

    inputs, parameters = inputs_parameters['inputs'], inputs_parameters['parameters']

    for dictionnary in [inputs, parameters]:
        for key, value in dictionnary.items():
            dictionnary[key] = np.array(value)

    return inputs, parameters


def parse_parameter_dict_item(parameter_dict_item):
    if len(parameter_dict_item) > 1:
        return pd.Series(parameter_dict_item).fillna(0)
    if len(parameter_dict_item) == 1:
        return parameter_dict_item['Value']


def parse_parameter_dict(parameter_dict):
    return {k: parse_parameter_dict_item(v['data']) for k, v in parameter_dict.items()}


def parse_parameter_json(path):
    with open(path) as f:
        parameters = json.load(f)
    return parse_parameter_dict(parameters)

#
# TODO Write the quick function for parse any excel template
# xl = pd.ExcelFile("models/Sarah/EW Data Template .xlsx")
# parameters = [sheet for sheet in xl.sheet_names if 'meta' not in sheet]
# data = {}
# for param in parameters:
#     if param not in ["Inventory", 'PLIR', 'PSIR', 'PSPIR', 'ESIR', 'ESPIR', 'ELIR']:
#         #print(param)
#         data[param] = {}
#         data[param]['data'] = xl.parse(param, header=None, index_col=0)[1].to_dict()
#         meta_params = xl.parse(f'{param}_metadata', header=None, index_col=0)[1].to_dict()
#         data[param].update(meta_params)
#
