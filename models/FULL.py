from graphmodels.graphmodel import GraphModel, merge_models

from models.water import EW
from models.landuse import BE2, GE3, SL1_BE3


def merge_all_models():
    model_list = [EW, BE2, GE3, SL1_BE3]

    graphmodel_list = []

    for model in model_list:
        model_dict = model.model_dictionnary

        for name, gm in model_dict.items():
            graphmodel_list.append(gm)

    full_model = merge_models(graphmodel_list)

    return full_model

model = merge_all_models()

model_dictionnary = {'full_model': model}