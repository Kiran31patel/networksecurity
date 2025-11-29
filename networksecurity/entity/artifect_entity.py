from dataclasses import dataclass
# from networksecurity.entity.config_entity import DataIngestionConfig 


@dataclass  #acts lika a decorator varialbe for a empty class
class DataIngestionArtifact:
    training_file_path: str
    testing_file_path: str