import os
import sys
import pandas as pd
import numpy as np


"""common constants for training pipeline"""
TARGET_COLUMN: str = "Result"
PIPELINE_NAME: str = "NetworkSecurity"
ARTIFECTS_DIR: str = "artifacts"
FILE_NAME: str = "phishing_data.csv"
TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"

"""Data ingestion constants"""

DATA_INGESTION_COLLECTION_NAME: str = "PhisingDataCollection"
DATA_INGESTION_DATABASE_NAME: str = "NetworkSecurityDB"
DATA_INGESTION_DIRECTORY_NAME: str = "data_ingestion"
DATA_INGESTION_INGESTED_DIR : str = "ingested_data"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2  
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
