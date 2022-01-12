# load raw rssi data to database
import pandas as pd
import sqlite3
import os
from sqlalchemy import create_engine, text


def get_conn(db_name="sensor"):

    try:
        engine = create_engine(f"postgresql://app:example@localhost:5432/{db_name}")
        con = engine.connect()
    except Exception as e:
        print(f"connection error: {e}")
        con=None

    return con


def table_exists(table_name, con):

    stmt = text(
    """
        IF EXISTS (
                    SELECT 1
                    FROM information_schema.tables
                    WHERE table_name = :table_name
                  )
                ;
    """)
    params={"table_name":table_name}
    result = con.execute(stmt, params)
    row = result.first()
    return bool(row[0])


def check_csv_file_length(input_fpath):
    
    msg = f"\rchecking length of {input_fpath}: ..."
    print(msg, end="")
    total_csv_len = sum(1 for row in open(input_fpath, 'r'))
    print(msg[:-3] + "{:,} rows found".format(total_csv_len))
    
    return total_csv_len


def process_df(df):

    # df["DateTimeInt"] = pd.to_datetime(df["DateTime"]).values
    # df = df.rename(columns={"ID":"id"})
    return df


def load_data_to_sql(input_fpath, table_name, con):
    
    
    # if table_exists(table_name, con):
    #     print(f"skipping import, table '{table_name}' already exists")
    #     return
    
    total_csv_len = check_csv_file_length(input_fpath)

    progress = 0
    chunksize = 100000
    df_chunks = pd.read_csv(input_fpath, index_col="ID", chunksize=chunksize)

    for df in df_chunks:
        df = process_df(df)
        df.to_sql(table_name, con, if_exists='append')
        progress += df.shape[0]
        percent = progress/total_csv_len
        print("\r{:,} rows of {:,} ( {:0.2%})".format(progress, total_csv_len, percent), end='')

    return
    

def load_raw_data(con):
    
    table_name='rssi'
    # sqlite_path = os.path.join(base_path, "data/processed/rssi.db")
    dir = os.path.join(base_path, "data/raw")
    input_fpath = os.path.join(dir, "rssi.csv")

    load_data_to_sql(input_fpath, table_name, con)

    return

def load_mean_data(con):
    
    table_name='rssi_mean'
    # sqlite_path = os.path.join(base_path, "data/processed/rssi.db")
    dir = os.path.join(base_path, "data/processed")
    input_fpath = os.path.join(dir, "rssi_mean.csv")
    load_data_to_sql(input_fpath, table_name, con)

    return

if __name__ == '__main__':

    base_path = os.environ.get("BASE_PATH","../../")
    con = get_conn(db_name="sensor")
    load_raw_data(con)
    load_mean_data(con)
    con.close()
