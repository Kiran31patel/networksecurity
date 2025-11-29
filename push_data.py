import os
import sys
import json
from dotenv import load_dotenv
load_dotenv()
import certifi

MONGODB_URL = os.getenv("MONGODBURL")
print(MONGODB_URL)

ca=certifi.where()

import pandas as pd
import numpy as np
from pymongo import MongoClient
import pymongo
 
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging


class NetworkDataExtract():

    def __int__(self):
        try:
           pass
        except Exception as e:
            raise NetworkSecurityException(e,sys) from e
        
    def csv_json_converter(self,file_path):

        """
        This function will convert csv file to json format
        """
        try:
            data=pd.read_csv(file_path)
            logging.info(f"csv file: {file_path} loaded successfully")
            data.reset_index(drop=True,inplace=True) 
            json_data=list(json.loads(data.T.to_json()).values())
            return json_data
            logging.info(f"csv file: {file_path} converted to json format successfully")
        except Exception as e:
            raise NetworkSecurityException(e,sys) from e
        
    def insert_data_mongidb(self,records,database,collection):

        """
        This function will insert data into mongodb
        """
        try:
           self.database=database
           self.collection=collection
           self.records=records
           self.mongo_client=MongoClient(MONGODB_URL)
           self.database=self.mongo_client[self.database]
           self.collection=self.database[self.collection]
           self.collection.insert_many(self.records)
           logging.info(f"Data inserted successfully into Mongodb database: {database} and collection: {collection}")
           return (len(self.records))
        except Exception as e:
            raise NetworkSecurityException(e,sys) from e
        
if __name__=="__main__":
    FILE_PATH="Network_Data\phisingData.csv"
    database="NetworkSecurityDB"
    collection="PhisingDataCollection"

    network_obj=NetworkDataExtract()
    json_data=network_obj.csv_json_converter(file_path=FILE_PATH)
    records_inserted=network_obj.insert_data_mongidb(records=json_data,database=database,collection=collection)
    print(f"Total records inserted: {records_inserted}")
     