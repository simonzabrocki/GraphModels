from data_utils.database import select_dataset, upload_dataset

def get_X_y_from_data(model, data_dict):
    '''TO CLEAN UP'''
    X = {key: data_dict[key] for key in model.inputs_() + model.parameters_()}
    y = {key: data_dict[key] for key in model.variables_() + model.outputs_() if key in data_dict}
    return X, y


def pivot_db_table(df):
    index = [col for col in df.columns if col not in ['Variable', 'Description', 'Unit', 'Value']]
    return df.pivot(index=index, columns='Variable', values='Value')


def df_to_dict(df):
    X = {}
    for code in df.columns:
        X[code] = df[code]
    return X


def concat_list_of_dict(list_of_dict):
    results = {}
    for dictionnary in list_of_dict:
        results.update(dictionnary)
    return results


def data_dict_from_df_tables(table_df_list):
    
    table_dict_list = [df_to_dict(pivot_db_table(df)) for df in table_df_list]
    
    data_dict = concat_list_of_dict(table_dict_list)
        
    return data_dict


def data_dict_from_db(db_table_names):
    table_df_list = [select_dataset(table) for table in db_table_names]
        
    data_dict = data_dict_from_df_tables(table_df_list)
        
    return data_dict


