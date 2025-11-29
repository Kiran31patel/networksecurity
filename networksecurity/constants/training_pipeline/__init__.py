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

SCHEMA_FILE_PATH: str = os.path.join("data_schema", "schema.yaml")

"""Data ingestion constants"""

DATA_INGESTION_COLLECTION_NAME: str = "PhisingDataCollection"
DATA_INGESTION_DATABASE_NAME: str = "NetworkSecurityDB"
DATA_INGESTION_DIRECTORY_NAME: str = "data_ingestion"
DATA_INGESTION_INGESTED_DIR : str = "ingested_data"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2  
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"

"""Data validation constants"""

DATA_VALIDATION_DIR_NAME: str = "data_validation"
DATA_VALIDATION_VALID_DIR: str = "validated"
DATA_VALIDATION_INVALID_DIR: str = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR: str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str = "report.yaml"

