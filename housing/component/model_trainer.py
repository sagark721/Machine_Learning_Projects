
from housing.constant import *
import os,sys
from housing.entity.artifact_entity import DataTransformationArtifact
from housing.entity.config_entity import ModelTrainerConfig
from housing.exception import HousingException
from housing.logger import logging
from housing.util.util import *
from housing.entity.model_factory import *


class Model_Trainer:
    

    def __init__(self,model_trainer_config:ModelTrainerConfig, data_transformation_artifact: DataTransformationArtifact):
        try:
            logging.info(f"{'>>'*30} Model Trainer Log Started. {'<<'*30}")
            self.model_trainer_config= model_trainer_config
            self.data_transformation_artifact=data_transformation_artifact

        except Exception as e:
            raise HousingException (e,sys) from e

    def initiate_model_trainer(self)-> ModelTrainerArtifact:
        try:
            logging.info(f"Loading transformed training dataset")
            transformed_train_file_path = self.data_transformation_artifact.transformed_train_file_path
            train_array=load_numpy_array_data(file_path=transformed_train_file_path)

            logging.info(f"Loading transformed testing dataset")
            transformed_test_file_path = self.data_transformation_artifact.transformed_test_file_path
            test_array = load_numpy_array_data(file_path= transformed_test_file_path)

            logging.info(f"Splitting training and testing input and target feature")
            x_train,y_train,x_test,y_test=train_array[:,:-1],train_array[:,-1],test_array[:,:-1],test_array[:,-1]

            logging.info(f"Extracting model config file path")
            model_config_file_path=self.model_trainer_config.model_config_file_path

            logging.info(f"Initialising model factory class using above model config file: {model_config_file_path}")
            model_factory = ModelFactory(model_config_file_path=model_config_file_path)

            base_accuracy = self.model_trainer_config.base_accuracy
            logging.info(f"Expected accuracy: {base_accuracy}")

            logging.info(f"Initiatine operation model selection")
            best_model=model_factory.get_best_model(X=x_train,y=y_train,base_accuracy=base_accuracy)

            logging.info(f"Best Model found on Training dataset is : {best_model}")

            logging.info(f"Exctracting trained model list")

            grid_searched_best_model_list:List[GridSearchedBestModel] = model_factory.grid_searched_best_model_list

