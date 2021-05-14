from ggmodel_dev.models.greengrowth import GGGM
import pandas as pd


all_model_properties_df = (
            pd.DataFrame.from_dict(GGGM.all_model_properties, orient='index')
            .reset_index()
            .rename(columns={'index': 'model'})
)


all_model_properties = GGGM.all_model_properties
all_model_dictionary = GGGM.all_model_dictionary