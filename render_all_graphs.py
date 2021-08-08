from models.landuse import BE2, GE3, SL1_BE3
from models.water import EW
from models import FULL


def render_model_dictionnary(model_dict, path):

    for model_name, model in model_dict.items():
        save_path = f'{path}/{model_name}.gv'
        print(model_name, save_path)
        graph_draw = model.draw()
        graph_draw.render(save_path)


def render_model(model, path='graphplots'):
    model_dict = model.model_dictionnary
    folder = model.__name__.split('.')[1]
    render_model_dictionnary(model_dict, f'{path}/{folder}')


def main():
    model_list = [EW, BE2, GE3, SL1_BE3, FULL]

    for model in model_list:
        render_model(model)


if __name__ == '__main__':
    main()
