from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model import ModelTrainer
from src.logger import logging
from src.exception import CustomException
import sys

if __name__ == '__main__':
    try:
        logging.info('Data Injection Started')
        obj = DataIngestion()
        data_path = obj.initiate_data_ingestion()
        logging.info("Data Ingestion Completed")

        logging.info("Data Transformation Started")
        data_transformation = DataTransformation()
        train_arr, test_arr, preprocessor_path = data_transformation.initiate_data_transformation(data_path)
        logging.info("Data Ingestion Completed")

        logging.info('Model Training Started')
        model_trainer = ModelTrainer()
        model_trainer.initiate_model_training(train_arr, test_arr)
        logging.info("Model Training Completed")

        print('Completed')

    except Exception as e:
        logging.info("Error occurred In training pipeline")
        raise CustomException(e, sys)
