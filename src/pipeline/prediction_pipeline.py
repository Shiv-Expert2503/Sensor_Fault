# import os
# import sys
# from dataclasses import dataclass

# import pandas as pd
# from flask import request

# from src.exception import CustomException
# from src.logger import logging
# from src.utils import load_object


# @dataclass
# class PredictionPipelineConfig:
#     prediction_output_dirname: str = "predictions"
#     prediction_file_name: str = "predicted_file.csv"
#     prediction_file_path: str = os.path.join(os.getcwd(), prediction_output_dirname, prediction_file_name)


# class PredictionPipeline:
#     def __init__(self, requests: request):

#         self.request = requests
#         self.prediction_pipeline_config = PredictionPipelineConfig()

#     def save_input_files(self) -> str:
#         try:
#             # creating the file
#             pred_file_input_dir = os.path.join(os.getcwd(), "prediction_artifacts")
#             os.makedirs(pred_file_input_dir, exist_ok=True)

#             input_csv_file = self.request.files['file']
#             print(input_csv_file)
#             print(input_csv_file.filename)

#             pred_file_path = os.path.join(pred_file_input_dir, input_csv_file.filename)
#             print(pred_file_path)
#             logging.info(f"{pred_file_path}")
#             input_csv_file.save(pred_file_path)

#             return pred_file_path
#         except Exception as e:
#             raise CustomException(e, sys)

#     def predict(self, features):
#         try:
#             preprocessor_path = (os.path.join(os.getcwd(), 'artifacts', 'preprocessor.pkl'))
#             model_path = (os.path.join(os.getcwd(), 'artifacts', 'model.pkl'))
#             model = load_object(model_path)
#             preprocessor = load_object(preprocessor_path)

#             transformed_x = preprocessor.transform(features)

#             preds = model.predict(transformed_x)

#             return preds

#         except Exception as e:
#             raise CustomException(e, sys)

#     def get_predicted_dataframe(self, input_dataframe_path):
#         try:

#             prediction_column_name: str = 'TARGET_COLUMN'
#             input_dataframe: pd.DataFrame = pd.read_csv(input_dataframe_path)

#             input_dataframe = input_dataframe.drop(
#                 columns="Unnamed: 0") if "Unnamed: 0" in input_dataframe.columns else input_dataframe

#             predictions = self.predict(input_dataframe)
#             input_dataframe[prediction_column_name] = [pred for pred in predictions]
#             target_column_mapping = {0: 'bad', 1: 'good'}

#             input_dataframe[prediction_column_name] = input_dataframe[prediction_column_name].map(target_column_mapping)

#             os.makedirs(self.prediction_pipeline_config.prediction_output_dirname, exist_ok=True)
#             input_dataframe.to_csv(self.prediction_pipeline_config.prediction_file_path, index=False)
#             logging.info("predictions completed. ")

#         except Exception as e:
#             logging.error("Error while predicting", exc_info=True)
#             raise CustomException(e, sys)

#     def run_pipeline(self):
#         try:
#             input_csv_path = self.save_input_files()
#             self.get_predicted_dataframe(input_csv_path)

#             return self.prediction_pipeline_config

#         except Exception as e:
#             logging.error("Error while running", exc_info=True)
#             raise CustomException(e, sys)






# Changes for values to lookin UI


# In src/pipeline/prediction_pipeline.py
import os
import sys
import pandas as pd

from src.exception import CustomException
from src.logger import logging
from src.utils import load_object

# We no longer need the config class for this simplified pipeline
# You can remove it or keep it if you use it elsewhere

class PredictionPipeline:
    def __init__(self):
        """
        The pipeline no longer needs the request object.
        """
        logging.info("Prediction Pipeline Initialized")

    def predict(self, features):
        """
        This method for prediction remains the same.
        """
        try:
            preprocessor_path = os.path.join(os.getcwd(), 'artifacts', 'preprocessor.pkl')
            model_path = os.path.join(os.getcwd(), 'artifacts', 'model.pkl')
            
            preprocessor = load_object(path=preprocessor_path)
            model = load_object(path=model_path)

            transformed_x = preprocessor.transform(features)
            preds = model.predict(transformed_x)
            return preds

        except Exception as e:
            raise CustomException(e, sys)

    def run_pipeline(self, uploaded_file):
        """
        This is the main method. It now takes the uploaded file object,
        processes it in memory, and returns a DataFrame with predictions.
        """
        try:
            input_dataframe = pd.read_csv(uploaded_file)
            logging.info("Uploaded CSV file read into pandas DataFrame")

            for column in input_dataframe.columns:
                input_dataframe[column] = pd.to_numeric(input_dataframe[column], errors='coerce')
            logging.info("Coerced all non-numeric inputs to NaN.")
            
            # --- FIX: Add .copy() here to de-fragment the DataFrame ---
            input_dataframe = input_dataframe.copy()
            
            predictions = self.predict(input_dataframe)
            logging.info("Predictions received from model")
            
            prediction_column_name = 'prediction'
            input_dataframe[prediction_column_name] = predictions
            
            target_column_mapping = {0: 'bad', 1: 'good'}
            input_dataframe[prediction_column_name] = input_dataframe[prediction_column_name].map(target_column_mapping)
            
            logging.info("Prediction column added to the DataFrame")
            
            return input_dataframe

        except Exception as e:
            raise CustomException(e, sys)