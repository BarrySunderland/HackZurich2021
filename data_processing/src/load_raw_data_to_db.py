# load raw rssi data to database
import pandas as pd
import sqlite3
import os


def get_conn(sqlite_path):
    
    try:
        con = sqlite3.connect(sqlite_path)
    except Exception as e:
        print(f"connection error: {e}")
    
    return con


def table_exists(table_name, con):

    curs = con.cursor()
    curs.execute("""
    SELECT COUNT(*) 
    FROM sqlite_master 
    WHERE type='table' AND name=(?);
    """, (table_name,))
    
    return bool(curs.fetchone()[0])

def check_csv_file_length(input_fpath):
    
    msg = f"\rchecking length of {input_fpath}: ..."
    print(msg, end="")
    total_csv_len = sum(1 for row in open(input_fpath, 'r'))
    print(msg[:-3] + "{:,} rows found".format(total_csv_len))
    
    return total_csv_len

def load_data_to_sql(input_fpath, table_name, con):
    
    
    if table_exists(table_name, con):
        print(f"skipping import, table '{table_name}' already exists")
        return
    
    total_csv_len = check_csv_file_length(input_fpath)

    progress = 0
    chunksize = 100000
    df_chunks = pd.read_csv(input_fpath, index_col="ID", chunksize=chunksize)

    for df in df_chunks:
        df.to_sql(table_name, con, if_exists='append')
        progress += df.shape[0]
        percent = progress/total_csv_len
        print("\r{:,} rows of {:,} ( {:0.2%})".format(progress, total_csv_len, percent), end='')

    return
    

if __main__ == '__main__':

    base_path = os.environ.get("BASE_PATH","../../")
    
    table_name='rssi'
    sqlite_path = os.path.join(base_path, "data/processed/rssi.db")
    con = get_conn(sqlite_path)

    raw_data_dir = os.path.join(base_path, "data/raw")
    input_fpath = os.path.join(raw_data_dir, "rssi.csv")

    load_data_to_sql(input_fpath, table_name, con)
    
    con.close()

