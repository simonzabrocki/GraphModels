import pandas as pd
from sqlalchemy import create_engine

# TO BE HIDDEN in environnement var
username = 'postgres'
password = 'lHeJnnRINyWCzfkDOzKl'
endpoint = 'database-gggi-1.cg4tog4qy0py.ap-northeast-2.rds.amazonaws.com'
port = 5432


db_connection_url = f"postgresql://{username}:{password}@{endpoint}:{port}"
engine = create_engine(db_connection_url)


def upload_df_to_dbtable(df, tablename, engine=engine):
    with engine.connect().execution_options(autocommit=True) as conn:
        df.to_sql(tablename, con=conn,
                  if_exists="replace", 
                  index=False, method="multi",
                  chunksize=10000)
        

def upload_dataset(df, meta_df, dataset, engine=engine):
    upload_df_to_dbtable(meta_df, f'meta{dataset}')
    upload_df_to_dbtable(df, dataset)        

    
def select_table(tablename, engine=engine):
    sql = f'SELECT * FROM {tablename}'
    with engine.connect() as conn:
        df = pd.read_sql(sql, conn)
    return df


def select_dataset(dataset, engine=engine):
    '''Merge is done localy because otherwise data is too big to be pulled (Unless )
    '''
    df = select_table(dataset)
    meta_df = select_table(f'meta{dataset}')
    return pd.merge(df, meta_df, on='Variable')


# def select_dataset(dataset_name='aquastat', engine=engine):
#     sql = f'SELECT * FROM {dataset_name} INNER JOIN meta{dataset_name} ON meta{dataset_name}.\\\"Variable\\\"={dataset_name}.\\\"Variable\\\";',
#     with engine.connect() as conn:
#         df = pd.read_sql(sql, conn)
#     df = df.loc[:,~df.columns.duplicated()]
#     return df