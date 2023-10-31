import os
import pickle
import sys

from src.exception import CustomException
from src.logger import logging


def save_object(path: str, obj):
    try:
        logging.info(f"Dumping starts of {str(obj)}")
        os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(path, 'wb') as file_obj:
            pickle.dump(obj, file_obj)

        logging.info("Dumping Completed")

    except Exception as e:
        logging.info("Error Occurred while dumping")
        raise CustomException(e, sys)
