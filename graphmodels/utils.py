import numpy as np
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
