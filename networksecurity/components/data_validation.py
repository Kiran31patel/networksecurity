# from networksecurity.constants.training_pipeline import DATA_INGESTION_DATABASE_NAME, DATA_INGESTION_COLLECTION_NAME
from networksecurity.entity.artifect_entity import DataIngestionArtifact , DataValidationArtifact
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.constants.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.utils.main_utils.utils import read_yaml_file,write_yaml_file
from scipy.stats import ks_2samp
import os
import sys
import pandas as pd


class DataValidation:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,
                 data_validation_config:DataValidationConfig):
        
        try:
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validation_config=data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys) from e

    def validate_number_of_columns(self,dataframe:pd.DataFrame)->bool:
        try:
            number_of_columns = len(self._schema_config)
            if len(dataframe.columns) == number_of_columns:
                return True
            return False
        except Exception as e:
            raise NetworkSecurityException(e,sys) from e


    def detect_data_drift(self,base_df,current_df,threshold=0.05)->dict:
        try:
            status=True
            report={}
            for column in base_df.columns:
                d1=base_df[column]
                d2=current_df[column]
                is_same_dist=ks_2samp(d1,d2)
                if threshold<=is_same_dist.pvalue:
                    is_found=False
                else:
                    is_found=True
                    status=False
                report.update({column:{"p_value":float(is_same_dist.pvalue),
                                      "drift_status":is_found}})
            drift_report_file_path=self.data_validation_config.drift_report_file_path

            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path, exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path, content=report)
            # return status
        except Exception as e:
            raise NetworkSecurityException(e,sys) from e

    def intiate_data_validation(self)->DataValidationArtifact:
        try:
            logging.info("Data Validation started")
            train_file_path=self.data_ingestion_artifact.training_file_path
            test_file_path=self.data_ingestion_artifact.testing_file_path
            # reading data from train and test file path
            train_dataframe = DataValidation.read_data(train_file_path)
            test_dataframe = DataValidation.read_data(test_file_path)
            # validate number of columns
            logging.info("Validating number of columns in train and test data")
            status = self.validate_number_of_columns(dataframe=train_dataframe)
            if not status:
                error_message=f"Train data does not contain all columns.\n"
                # raise Exception(error_message)
            status = self.validate_number_of_columns(dataframe=test_dataframe)
            if not status:
                error_message=f"Test data does not contain all columns.\n"
                # raise Exception(error_message)
            
            is_numerical_columns_exists = True
            for column in self._schema_config["numerical_columns"]:
                if column not in train_dataframe.columns:
                    is_numerical_columns_exists = False
                if column not in test_dataframe.columns:
                    is_numerical_columns_exists = False
            if not is_numerical_columns_exists:
                error_message=f"Numerical columns are missing in train or test data.\n"
                raise Exception(error_message)
            
            # data drift
            logging.info("Checking data drift in train and test data")
            status=self.detect_data_drift(base_df=train_dataframe,
                                             current_df=test_dataframe)
            logging.info("Data Validation Completed")

            dir_path=os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path,exist_ok=True)
            train_dataframe.to_csv(
                self.data_validation_config.valid_train_file_path,index=False,header=True
            )
            test_dataframe.to_csv(
                self.data_validation_config.valid_test_file_path,index=False,header=True
            ) 

            data_validation_artifact=DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_ingestion_artifact.training_file_path,
                valid_test_file_path=self.data_ingestion_artifact.testing_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )
            return data_validation_artifact

        except Exception as e:
            raise NetworkSecurityException(e,sys) from e
