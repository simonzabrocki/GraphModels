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


def get_X_y_from_data(model, data_dict):
    '''TO CLEAN UP'''
    X = {key: data_dict[key] for key in model.inputs_() + model.parameters_()}
    y = {key: data_dict[key] for key in model.variables_() + model.outputs_() if key in data_dict}
    return X, y
