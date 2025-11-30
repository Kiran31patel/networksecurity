import sys,os
import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.entity.artifect_entity import DataIngestionArtifact,DataValidationArtifact,DataTransformationArtifact
from networksecurity.constants.training_pipeline import TARGET_COLUMN, DATA_TRANSFORMATION_IMPUTER_PARAMS

from networksecurity.utils.main_utils.utils import save_numpy_array_data,save_object


class DataTransformation:
    def __init__(self,
                 data_validation_artifact:DataValidationArtifact,
                 data_transformation_config:DataTransformationConfig):
        try:
            self.data_validation_artifact=data_validation_artifact
            self.data_transformation_config=data_transformation_config
        except Exception as e:
            raise NetworkSecurityException(e,sys) from e
        
    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys) from e

    def get_transformer_object(cls)->Pipeline:
        
        logging.info('Enter get method')

        try:
           imputer:KNNImputer= KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
           processor:Pipeline=Pipeline([("imputer",imputer)])
           return processor
        except Exception as e:
            raise NetworkSecurityException(e,sys) from e
  

    def initiate_data_transformation(self)->DataTransformationArtifact:
        logging.info("Data Transformation started")
        try:
            train_df=self.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df=self.read_data(self.data_validation_artifact.valid_test_file_path)
            # Traning Pipeline
            input_feature_train_df=train_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_train_df=train_df[TARGET_COLUMN]

            target_feature_train_df = target_feature_train_df.replace(-1, 0)

            # Testing Pipeline
            input_feature_test_df=test_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_test_df=test_df[TARGET_COLUMN]
            target_feature_test_df = target_feature_test_df.replace(-1, 0)

            preprocessor = self.get_transformer_object()

            preprocessor_object = preprocessor.fit(input_feature_train_df)
            transform_input_train_feature = preprocessor_object.transform(input_feature_train_df)
            transform_input_test_feature = preprocessor_object.transform(input_feature_test_df)

            train_arr = np.c_[transform_input_train_feature,np.array(target_feature_train_df)]
            test_arr = np.c_[transform_input_test_feature,np.array(target_feature_test_df)]

            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path,array=train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path,array=test_arr)
            save_object(self.data_transformation_config.transformed_object_file_path,preprocessor_object)

            # Preparing artifects
            data_transformation_artifatc=DataTransformationArtifact(
                transformed_object_file_path  = self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path = self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path = self.data_transformation_config.transformed_test_file_path
            )
            return data_transformation_artifatc
        except Exception as e:
            raise NetworkSecurityException(e,sys) from e