

import shutil
from tkinter import E
from housing.entity.artifact_entity import ModelEvaluationArtifact,ModelPusherArtifact
from housing.entity.config_entity import ModelPusherConfig
from housing.exception import HousingException
import os, sys
from housing.logger import logging


class ModelPusher:

    def __init__ (self,model_pusher_config:ModelPusherConfig, model_evaluation_artifact:ModelEvaluationArtifact):
        try:
            logging.info(f"{'>>'*30} Model pusher log started {'<<'*30}")
            self.model_pusher_config = model_pusher_config
            self.model_evaluation_artifact = model_evaluation_artifact
        except Exception as e:
            raise HousingException (e,sys) from e

    def export_model(self)-> ModelPusherArtifact:
        try:
            evaluated_model_file_path = self.model_evaluation_artifact.evaluated_model_path
            export_dir = self.model_pusher_config.export_dir_path
            model_file_name = os.path.basename(evaluated_model_file_path)
            export_model_file_path = os.path.join(export_dir,model_file_name)
            logging.info(f"Exporting model file to: {export_model_file_path}")
            os.makedirs(export_dir, exist_ok= True)

            shutil.copy(src=evaluated_model_file_path, dst= export_model_file_path)
            #we can call this function to save module to azure blob storage / google cloud storage / s3 bucket

            logging.info(f"Trained Model: {evaluated_model_file_path} is copied in export dir:[{export_model_file_path}]")

            model_pusher_artifact = ModelPusherArtifact (is_model_pusher=True, export_model_file_path=export_model_file_path)
            logging.info(f"Model Pusher Artifact: {model_pusher_artifact}")
            return model_pusher_artifact

        except Exception as e:
            raise HousingException (e,sys) from e


    def initiate_model_pusher(self)->ModelPusherArtifact:
        try:
            self.export_model()
        except Exception as e:
            raise HousingException (e,sys) from e

    def __del__(self):
        logging.info(f"{'>>'*20} Model Pusher Log Completed. {'<<'*20}")


    