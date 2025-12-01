from dataclasses import dataclass
# from networksecurity.entity.config_entity import DataIngestionConfig 


@dataclass  #acts lika a decorator varialbe for a empty class
class DataIngestionArtifact:
    training_file_path: str
    testing_file_path: str


@dataclass
class DataValidationArtifact:
    validation_status: bool
    valid_train_file_path: str
    valid_test_file_path: str
    invalid_train_file_path: str
    invalid_test_file_path: str
    drift_report_file_path: str


@dataclass
class DataTransformationArtifact:
    transformed_object_file_path: str
    transformed_train_file_path: str
    transformed_test_file_path: str

@dataclass
class ClassficationMetricArtifect:
    f1_score: float
    precision_score: float
    recall_score: float

@dataclass
class ModelTrainerArtifect:
    trained_model_file_path: str
    train_metric_artifect: ClassficationMetricArtifect
    test_metric_artifect: ClassficationMetricArtifect