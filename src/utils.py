import os
import pickle
import sys

from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

from src.exception import CustomException
from src.logger import logging


def evaluate_model(x, y, models) -> dict:
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
    try:
        logging.info("Loading starts ")
        with open(path, 'rb') as obj:
            return pickle.load(obj)
        # logging.info("Loading Completed")

    except Exception as e:
        logging.error("Error occurred while loading the data", exc_info=e)
        raise CustomException(e, sys)
