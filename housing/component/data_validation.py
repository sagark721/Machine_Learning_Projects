from housing.logger import logging
from housing.exception import HousingException
from housing.entity.config_entity import DataValidationConfig
from housing.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
import os,sys
from housing.constant import *
import pandas as pd
import json
from housing.util import util
import numpy as np

#evidently imports
from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection
from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab 






class DataValidation:
    
    def __init__(self, data_validation_config:DataValidationConfig, 
        data_ingestion_artifact:DataIngestionArtifact,
        schema_file_path:str = SCHEMA_FILE_PATH ):
        try:
            logging.info(f"\n\n{'='*20} Data Validation Log Started. {'='*20} \n\n")
            self.data_validation_config=data_validation_config
            self.data_ingestion_artifact=data_ingestion_artifact
            self.schema_file_path=schema_file_path
            
        except Exception as e:
            raise HousingException (e,sys) from e 

    def get_train_test_df(self):
        try:
            train_df=pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df=pd.read_csv(self.data_ingestion_artifact.test_file_path)
            return train_df,test_df

        except Exception as e:
            raise HousingException(e,sys) from e 


    def is_train_test_file_exists(self)-> bool:
        try:

            logging.info("Checking if Train and Test file is available")
            is_train_file_exists=False
            is_test_file_exists=False

            train_file_path= self.data_ingestion_artifact.train_file_path
            test_file_path=self.data_ingestion_artifact.test_file_path

            is_train_file_exists=os.path.exists(train_file_path)
            is_test_file_exists=os.path.exists(test_file_path)

            is_available= is_train_file_exists and is_test_file_exists

            logging.info(f"Is Train and Test file exist? -> {is_available}")

            if not is_available:

                train_file=self.data_ingestion_artifact.train_file_path
                test_file=self.data_ingestion_artifact.test_file_path
                message=f"Train file: {train_file} or Test file: {test_file}"\
                "is NOT present"
                raise  Exception(message)

            

            return is_available


        except Exception as e:
            raise HousingException (e,sys) from e 


    def validate_dataset_schema(self)-> bool:
        try:

            """
            Assignment: Validate Train Test datasets using schema file
            
            1. Number of columns
            2. Check Column names
            3. Check values of Ocean Proximity:
                Acceptable values:
                    - <1H OCEAN
                    - INLAND
                    - ISLAND
                    - NEAR BAY
                    - NEAR OCEAN
            """
            
            validation_status=False
            logging.info("Schema Validation Started")
            schema_file=util.read_yaml_file(self.schema_file_path)
            train_df,test_df=self.get_train_test_df()
            
            logging.info("'Train df' validation started")

            ##<< Train df >>##

            #Number of columns:
            train_no_cols=False
            try:
                train_no_cols= len(train_df.columns) == len(schema_file['columns'].keys())
            except Exception as e:
                raise HousingException(e,sys) from e

            if train_no_cols==True:
                logging.info("Number of columns in 'Train df' is inline with Schema file")
            else:
                logging.info("Number of columns in 'Train df' is NOT inline with Schema file")

            #column names:
            train_col_names=False
            try:
                train_col_names=list(train_df.columns) == list(schema_file['columns'].keys())
            except Exception as e:
                raise HousingException (e,sys) from e
            if train_col_names==True:
                logging.info("Column names in 'Train df' are inline with Schema file")
            else:
                logging.info("Column names in 'Train df' are NOT inline with Schema file")

            #Ocean Proximity Values:

            train_ocean_proximity_values=False

            try:
                train_ocean_proximity_values=list(np.sort(list(train_df['ocean_proximity'].unique()))) == list(np.sort(schema_file['domain_value']['ocean_proximity']))
            except Exception as e:
                raise HousingException (e,sys) from e

            if train_ocean_proximity_values==True:
                logging.info("Ocean Proximity Values in 'Train df' are inline with Schema file")
            else:
                logging.info("Ocean Proximity Values in 'Train df' are NOT inline with Schema file")



            ##<< Test df >>##

            logging.info("'Test df' validation started")
        
            #Number of columns:
            test_no_cols=False
            try:
                test_no_cols= len(test_df.columns) == len(schema_file['columns'].keys())
            except Exception as e:
                raise HousingException(e,sys) from e

            if test_no_cols==True:
                logging.info("Number of columns in 'Test df' is inline with Schema file")
            else:
                logging.info("Number of columns in 'Test df' is NOT inline with Schema file")

            #column names:
            test_col_names=False
            try:
                test_col_names=list(test_df.columns) == list(schema_file['columns'].keys())
            except Exception as e:
                raise HousingException (e,sys) from e
            if test_col_names==True:
                logging.info("Column names in 'Test df' are inline with Schema file")
            else:
                logging.info("Column names in 'Test df' are NOT inline with Schema file")

            #Ocean Proximity Values:

            test_ocean_proximity_values=False

            try:
                test_ocean_proximity_values=list(np.sort(list(test_df['ocean_proximity'].unique()))) == list(np.sort(schema_file['domain_value']['ocean_proximity']))
            except Exception as e:
                raise HousingException (e,sys) from e

            if test_ocean_proximity_values==True:
                logging.info("Ocean Proximity Values in 'Test df' are inline with Schema file")
            else:
                logging.info("Ocean Proximity Values in 'Test df' are NOT inline with Schema file")      

          
            


            validation_status= train_no_cols and train_col_names and train_ocean_proximity_values and test_col_names and test_no_cols and test_ocean_proximity_values
            #validation_status=True 
            if validation_status == True:
                logging.info(f"Dataset Schema Validated Successfully, Validation Status: {validation_status}") 
            else:
                logging.info(f"Dataset Schema Validated UNSUCCESSFULLY, Validation Status: {validation_status}")

            

            return validation_status
        except Exception as e:
            raise HousingException (e,sys) from e 


    def get_and_save_data_drift_report(self):
        try:
            profile = Profile(sections=[DataDriftProfileSection()])

            train_df,test_df=self.get_train_test_df()

            profile.calculate(train_df,test_df)

            report=json.loads(profile.json())

            report_file_path=self.data_validation_config.report_file_path

            report_dir=os.path.dirname(report_file_path)

            os.makedirs(report_dir,exist_ok=True)

            with open (report_file_path,"w") as report_file:
                json.dump(report,report_file,indent=6) 

            return report



        except Exception as e:
            raise HousingException(e,sys) from e

    def save_data_drift_report_page(self):
        try:

            dashboard=Dashboard(tabs=[DataDriftTab()])
            train_df,test_df=self.get_train_test_df()
            dashboard.calculate(train_df,test_df)

            report_page_file_path=self.data_validation_config.report_page_file_path

            report_page_dir=os.path.dirname(report_page_file_path)

            os.makedirs(report_page_dir,exist_ok=True)


            dashboard.save(report_page_file_path) 

        except Exception as e:
            raise HousingException(e,sys) from e



    def is_data_drift_found(self) -> bool:
        try:
            report=self.get_and_save_data_drift_report()
            self.save_data_drift_report_page()
            return True
        except Exception as e:
            raise HousingException(e,sys) from e


    def initiate_data_validation(self)-> DataValidationArtifact:
        try:

            self.is_train_test_file_exists()
            self.validate_dataset_schema()
            self.is_data_drift_found()

            data_validation_artifact=DataValidationArtifact(
                schema_file_path=self.data_validation_config.schema_file_path,
                report_file_path=self.data_validation_config.report_file_path,
                report_page_file_path=self.data_validation_config.report_page_file_path,
                is_validated=True,
                message="Data validation performed successfully"
            )

            logging.info(f"Data validation artifact: {data_validation_artifact}")

            return data_validation_artifact



        except Exception as e:
            raise HousingException (e,sys) from e 

    
    def __del__(self):
        logging.info(f"\n\n{'='*20} Data Validation Log Completed. {'='*20} \n\n")


