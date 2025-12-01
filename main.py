from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.components.data_ingestions import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.entity.config_entity import DataIngestionConfig,TrainingPipelineConfig,DataValidationConfig,DataTransformationConfig,ModelTrainerConfig
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer 
import sys

if __name__ == "__main__":
    try:
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config)
        logging.info("Starting data ingestion process")
        data_ingestion_artifact=data_ingestion.initiate_data_ingestion()
        print(data_ingestion_artifact)
        logging.info("Data ingestion process completed")
        data_validation_config = DataValidationConfig(training_pipeline_config)
        data_validation=DataValidation(data_ingestion_artifact,data_validation_config)
        logging.info("Starting data validation process")
        data_validation_artifect=data_validation.intiate_data_validation() 
        logging.info("Data validation process completed")
        data_transformation_config = DataTransformationConfig(training_pipeline_config)
        data_tranformation = DataTransformation(data_validation_artifect,data_transformation_config)
        data_transformation_artifect = data_tranformation.initiate_data_transformation()

        model_trainer_config = ModelTrainerConfig(training_pipeline_config)
        model_trainer = ModelTrainer(model_trainer_config=model_trainer_config,data_transformationArtifact=data_transformation_artifect)
        model_trainer_artifact = model_trainer.initiate_model_trainer()

    except Exception as e:
        raise NetworkSecurityException(e, sys)
    