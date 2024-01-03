import os
import pickle
import sys

from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

from src.exception import CustomException
from src.logger import logging


def evaluate_model(x, y, models) -> dict:
    """
    This is a general function to evaluate a single model at a time.
    @params: x is the data without output and y is the output column, models is the list of models to predict
    @returns: The model score in dict format
    """
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
    report = {}

    for i in range(len(list(models))):
        model = list(models.values())[i]

        model.fit(x_train, y_train)  # Train model

        y_test_pred = model.predict(x_test)

        test_model_score = accuracy_score(y_test, y_test_pred)

        report[list(models.keys())[i]] = test_model_score

    return report


def save_object(path: str, obj):
    """
    This function is used to store objects in the local environment in write-binary format
    @params: path where to save and obj is object to store
    """
    try:
        logging.info(f"Dumping starts of {str(obj)}")
        os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(path, 'wb') as file_obj:
            pickle.dump(obj, file_obj)

        logging.info("Dumping Completed")

    except Exception as e:
        logging.info("Error Occurred while dumping")
        raise CustomException(e, sys)


def load_object(path):
    """
    This function is used to load the saved objects in read-binary format
    @params: Takes only the path where the object has been saved
    """
    try:
        logging.info("Loading starts ")
        with open(path, 'rb') as obj:
            return pickle.load(obj)
        # logging.info("Loading Completed")

    except Exception as e:
        logging.error("Error occurred while loading the data", exc_info=e)
        raise CustomException(e, sys)
