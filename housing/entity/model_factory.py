
from sklearn.metrics import r2_score,mean_squared_error
from tkinter.constants import E
from housing.logger import logging
from collections import namedtuple
import numpy as np
import yaml
import os,sys
import importlib
from typing import List

from housing.exception import HousingException


GRID_SEARCH_KEY = 'grid_search'
MODULE_KEY = 'module'
CLASS_KEY = 'class'
PARAM_KEY = 'params'
MODEL_SELECTION_KEY = 'model_selection'
SEARCH_PARAM_GRID_KEY = "search_param_grid"

InitializedModelDetail = namedtuple("InitializedModelDetail",
                                    ["model_serial_number","model","param_grid_search","model_name"])

GridSearchedBestModel = namedtuple("GridSearchedBestModel",
                                    ["model_serial_number",
                                    "model",
                                    "best_model",
                                    "best_parameters", "best_score"])

MetricInfoArtifact = namedtuple("MetricInfoArtifact",
                                ["model_name","model_object","train_rmse","test_rmse","train_accuracy","test_accuracy","model_accuracy","index_number"])


BestModel=namedtuple("BestModel",
                    ["model_serial_number","model","best_model","best_parameters","best_score"])




def evaluate_regression_model(model_list:list,X_train:np.ndarray,y_train:np.ndarray,X_test:np.ndarray,y_test:np.ndarray,base_accuracy:float=0.6) -> MetricInfoArtifact:
    """ 
    Description:

    This function compare multiple regression model and returns best model

    Params:
    model_list: list of model 
    X_train: Training dataset input feature
    y_train: Training dataset target feature
    X_test: Testing dataset input feature
    y_test: Testing dataset target feature
    base_accuracy:float=0.6

    Return:

    It returns the named tuple

    MetricInfoArtifact = namedtuple("MetricInfoArtifact",["model_name","model_object","train_rmse","test_rmse","train_accuracy","test_accuracy",
                                    "model_accuracy","index_number"])

     """

    try:

        #model_list=[model.best_model for model in model_list]
        index_number=0
        metric_info_artifact=None

        for model in model_list:
            model_name=str(model) #getting model name based on model object
            logging.info(f"{'>>'*30} Started evaluatig model: [{type(model).__name__}] {'<<'*30}")

            #Getting prediction for training and testing dataset
            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)

            #Calculating r squared score on training and testing dataset
            train_acc = r2_score(y_train,y_train_pred)
            test_acc= r2_score(y_test,y_test_pred)

            #Calculating mean squared error on training and testing dataset
            train_rmse= np.sqrt(mean_squared_error(y_train,y_train_pred))
            test_rmse=np.sqrt(mean_squared_error(y_test,y_test_pred))


            #Calculating Harmonic mean of train_accuracy and test_accuracy
            model_accuracy=(2* (train_acc * test_acc)) / (train_acc + test_acc)
            diff_test_train_accuracy = abs(test_acc - train_acc)

            #Logging all important metric
            logging.info(f"{'>>'*30} Score {'<<'*30}")
            logging.info(f"Train Score\t\t Test Score\t\t Average Score")
            logging.info(f"{np.round(train_acc,2)}\t\t {np.round(test_acc,2)}\t\t {np.round(model_accuracy,2)}")

            logging.info(f"{'>>'*30} Loss {'<<'*30}")
            logging.info(f"Diff train test accuracy: [{diff_test_train_accuracy}].")
            logging.info(f"Train root mean squared error: [{train_rmse}].")
            logging.info(f"Test root mean square error: [{test_rmse}].")

            #If model accuracy is greater than base accuracy and train and test scores are within certain threshold
            #We will accept that model as accepted model

            if model_accuracy >= base_accuracy and diff_test_train_accuracy < 0.05:
                base_accuracy=model_accuracy
                metric_info_artifact = MetricInfoArtifact(model_name=model_name,
                                                            model_object=model,
                                                            train_rmse=train_rmse,
                                                            test_rmse=test_rmse,
                                                            train_accuracy=train_acc,
                                                            test_accuracy=test_acc,
                                                            index_number=index_number,
                                                            model_accuracy=model_accuracy)

                logging.info(f"Acceptable model found {metric_info_artifact}.")
            index_number +=1

            if metric_info_artifact is None:
                logging.info(f"No model found with higher accuracy than base accuracy")

            return metric_info_artifact
        
    except Exception as e:
        raise HousingException (e,sys) from e




def get_sample_model_config_yaml_file(export_dir:str):
    try:
        model_config= {
            GRID_SEARCH_KEY : {
                MODULE_KEY : "sklearn.model_selection",
                CLASS_KEY : "GridSearchCV",
                PARAM_KEY : {
                    "cv":3,
                    "verbose":1
                }
            },

            MODEL_SELECTION_KEY:{
                "module_0":{
                    MODULE_KEY:"module of model",
                    CLASS_KEY:"ModelClassName",
                    PARAM_KEY:
                        {"param_name1":"value1",
                        "param_name2":"value2"
                        },
                    SEARCH_PARAM_GRID_KEY:{
                        "param_name":["param_value_1","param_value_2"]
                    }

                },
            }
        }


        os.makedirs(export_dir,exist_ok=True)
        export_file_path = os.path.join(export_dir,"model.yaml")

        with open(export_file_path,'w') as file:
            yaml.dump(model_config,file)
        return export_file_path


    except Exception as e:
        raise HousingException(e,sys) from e





class ModelFactory:

    def __init__(self,  model_config_path : str = None):
        try:
            self.config:dict = ModelFactory.read_params(model_config_path)
            self.grid_search_cv_module:str = self.config[GRID_SEARCH_KEY][MODULE_KEY]
            self.grid_search_Class_name:str = self.config[GRID_SEARCH_KEY][CLASS_KEY]
            self.grid_search_property_data:dict = dict(self.config[GRID_SEARCH_KEY][PARAM_KEY])  

            self.models_initialization_config:dict = dict(self.config[MODEL_SELECTION_KEY])

            self.initialised_model_list = None
            self.grid_searched_best_model_list = None


        except Exception as e:
            raise HousingException (e,sys) from e



    @staticmethod
    def update_property_of_class(instance_ref:object, property_data:dict):
        try:
            if not isinstance(property_data,dict):
                raise Exception ("Property data required to be dictionary")
            print(property_data)

            for key,value in property_data.items():
                logging.info(f"Executing:$ {str(instance_ref)}.{key}={value}")
                setattr(instance_ref,key,value)
            return instance_ref

        except Exception as e:
            raise HousingException(e,sys) from e



    @staticmethod
    def read_params(config_path:str)->dict:
        try:
            with open(config_path) as yaml_file:
                config:dict = yaml.safe_load(yaml_file)
            return config

        except Exception as e:
            raise HousingException (e,sys) from e


    @staticmethod    
    def class_for_name(module_name:str,class_name:str):
        try:
            #Load the module, will raise ImportantError if module cannot be loaded
            module= importlib.import_module(module_name)

            #get the class, will raise Attribute error if class cannot be found
            logging.info(f"Executing command: from {module} import {class_name}")

            class_ref = getattr(module,class_name)
            return class_ref
        except Exception as e:
            raise HousingException(e,sys) from e

    
    def execute_grid_search_operation(self, initialized_model:InitializedModelDetail, input_feature, output_feature) -> GridSearchedBestModel:
        """ 
        Description:

        This function will perform parameter search operation and it will return the best optimistic model with best parameters
        estimator: model object
        param_grid: dictionary of parameters to perform operation
        input_feature: all input features
        output_feature: Target feature

        Return:
        it will return GridSearchOperation object
         """

        try:
            # Instantiating GridSearchCV Class

            grid_search_cv_ref = ModelFactory.class_for_name(module_name=self.grid_search_cv_module,
                                                            class_name= self.grid_search_Class_name)

            grid_search_cv = grid_search_cv_ref(estimator=initialized_model.model,
                                                param_grid=initialized_model.param_grid_search)

            grid_search_cv = ModelFactory.update_property_of_class(grid_search_cv,self.grid_search_property_data)

            message= f"{'>>'*30} Training {type(initialized_model.model).__name__} Started. {'<<'*30}"
            logging.info(message)

            grid_search_cv.fit(input_feature,output_feature)

            message= f"{'>>'*30} Training {type(initialized_model.model).__name__} Completed. {'<<'*30}"

            grid_searched_best_model = GridSearchedBestModel(model_serial_number=initialized_model.model_serial_number,
                                                            model= initialized_model.model,
                                                            best_model=grid_search_cv.best_estimator_,
                                                            best_parameters = grid_search_cv.best_params_,
                                                            best_score = grid_search_cv.best_score_

                                                            )

            return grid_searched_best_model

        except Exception as e :
            raise HousingException (e,sys) from e



    def get_initialized_model_list(self) -> List[InitializedModelDetail]:

        """ This function will return a list of model details. """

        try:
            initialized_model_list=[]

            for model_serial_number in self.models_initialization_config.keys():

                model_initialization_config=self.models_initialization_config[model_serial_number]
                model_obj_ref = ModelFactory.class_for_name(module_name=model_initialization_config[MODULE_KEY],
                                                            class_name= model_initialization_config[CLASS_KEY]
                                                            )

                model=model_obj_ref()

                if PARAM_KEY in model_initialization_config:
                    model_obj_property_data = dict(model_initialization_config[PARAM_KEY])
                    model = ModelFactory.update_property_of_class(instance_ref=model,
                                                                property_data=model_obj_property_data)


                param_grid_search = model_initialization_config[SEARCH_PARAM_GRID_KEY]
                model_name=f"{model_initialization_config[MODULE_KEY]}.{model_initialization_config[CLASS_KEY]}"

                model_initialization_config = InitializedModelDetail(model_serial_number=model_serial_number,
                                                                    model=model,
                                                                    param_grid_search=param_grid_search,
                                                                    model_name=model_name
                )

                initialized_model_list.append(model_initialization_config)
            
            self.initialised_model_list = initialized_model_list
            
            return self.initialised_model_list

        except Exception as e:
            raise HousingException (e,sys) from e


    
    def initiate_best_parameter_search_for_initialized_model(self,initialized_model: InitializedModelDetail,input_feature,
    output_feature) -> GridSearchedBestModel:

        """ This function will perform parameter search operation and it will return the best optimistic model with the best parameters
            estimator: Model Object
            param_grid : dictionary of parameters to perform search operation
            input_feature: All Input features 
            output_feature: target feature
            
            Return:
            it will return GridSearchOperation"""
        
        
            

        try:
            
            return self.execute_grid_search_operation(initialized_model=initialized_model,
                                                        input_feature=input_feature,
                                                        output_feature=output_feature)

        except Exception as e:
            raise HousingException (e,sys) from e 
        
    

    def initiate_best_parameter_search_for_initializes_models(self,
                                                                initialized_model_list:List[InitializedModelDetail],
                                                                input_feature,
                                                                output_feature) -> List[GridSearchedBestModel]:

        try:
            self.grid_searched_best_model_list=[]

            for initialized_model_list in initialized_model_list:
                grid_searched_best_model = self.initiate_best_parameter_search_for_initialized_model(
                    initialized_model=initialized_model_list,
                    input_feature=input_feature,
                    output_feature=output_feature
                )
                self.grid_searched_best_model_list.append(grid_searched_best_model)
            return self.grid_searched_best_model_list
        
        except Exception as e:
            raise HousingException(e,sys) from e 


    @staticmethod
    def get_model_detail(model_details:List[InitializedModelDetail],
                        model_serial_number:str)-> InitializedModelDetail:
        """ This fuction returns ModelDetails """

        try:
            for model_data in model_details:
                if model_data.model_serial_number == model_serial_number :
                    return model_data
        except Exception as e:
            raise HousingException(e,sys) from e 

    
    @staticmethod
    def get_best_model_from_grid_searched_best_model_list(grid_searched_best_model_list: List[GridSearchedBestModel],
    base_accuracy=0.6) -> BestModel:
        try:
            best_model=None

            for grid_searched_best_model in grid_searched_best_model_list:
                if base_accuracy < grid_searched_best_model.best_score:
                    logging.info(f"Acceptable Model Found: [{grid_searched_best_model}]")
                    base_accuracy=grid_searched_best_model.best_score

                    best_model=grid_searched_best_model
                
            if not best_model:
                raise Exception(f"None of Model has base accuracy: {base_accuracy}")

            logging.info(f"Best model:{best_model}")

            return best_model
        except Exception as e:
            raise HousingException (e,sys) from e 


    def get_best_model(self,X,y,base_accuracy=0.6) -> BestModel:
        try:
            logging.info("Started initializing model from config file")
            initialized_model_list = self.get_initialized_model_list()

            logging.info(f"Initialized model: {initialized_model_list}")
            grid_searched_best_model_list = self.initiate_best_parameter_search_for_initializes_models(
                initialized_model_list=initialized_model_list,
                input_feature=X,
                output_feature=y
            )
            return ModelFactory.get_best_model_from_grid_searched_best_model_list(grid_searched_best_model_list,base_accuracy=base_accuracy)
        
        except Exception as e:
            raise HousingException(e,sys) from e 

