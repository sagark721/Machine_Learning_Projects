from housing.pipeline.pipeline import Pipeline
from housing.exception import HousingException
from housing.logger import logging
from housing.config.configuration import Configuration
from housing.component.data_transformation import DataTransformation
import os




def main():
    try:
        config_file_path = os.path.join("config","config.yaml")
        pipeline = Pipeline(Configuration(config_file_path=config_file_path))
        pipeline.run_pipeline()
    #     data_validation_config=Configuration().get_data_transformation_config()
    
    #   print(data_validation_config)

    #     schema_file_path=r"C:\Users\pkana\Machine_Learning_Projects\config\schema.yaml"
    #     file_path=r"C:\Users\pkana\Machine_Learning_Projects\housing\artifact\data_ingestion\2022-09-29-13-48-29\ingested_data\train\housing.csv"

    #     df=DataTransformation.load_data(file_path=file_path,schema_file_path=schema_file_path)
    #     print(df.columns)
    #     print(df.dtypes)
    except Exception as e:
        logging.error(f"{e}")
        print(e)



if __name__=="__main__":
    main()






