import pandas as pd
import os
from sqlalchemy import create_engine
import logging 
import time 

logging.basicConfig(
    filename="logs/ingeston_db.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a"
)


engine = create_engine('sqlite:///vendor_performance.db')

def ingest_db(df,table_name,engine):
    '''This function will ingest the dataframe into the database as a table'''
    df.to_sql(table_name, engine, if_exists='replace', index=False)


def load_raw_data(): 
    '''Function to load raw data from csv files as dataframe and ingest into db'''
    start =time.time()
    for file in os.listdir("C:\\Users\\risha\\OneDrive\\Desktop\\Project\\Vendor Performance DA\\data"):
        if file.endswith(".csv"):
            full_path = os.path.join("C:\\Users\\risha\\OneDrive\\Desktop\\Project\\Vendor Performance DA\\data", file)  
            df = pd.read_csv(full_path)
            logging.info(f'Ingesting {file} in db')
            ingest_db(df, file[:-4], engine)
    end = time.time()
    total_time = (end - start)/60
    logging.info('-----------Ingestion Complete------------')
    logging.info(f'\nTotal Time Taken: {total_time} minutes')        

if __name__ == '__main__':
    load_raw_data()