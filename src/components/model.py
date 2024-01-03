import os
import sys
from dataclasses import dataclass

from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from xgboost import XGBClassifier

from src.exception import CustomException
from src.logger import logging
from src.utils import evaluate_model, save_object


@dataclass
class ModelConfig:
    model_path = os.path.abspath(os.path.join(os.getcwd(), '..', '..', 'artifacts', 'model.pkl'))


class ModelTrainer:
    """
    Initializing all the models here
    """
    def __init__(self):
        self.model_path = ModelConfig()

        self.models = {
            'svc_clf': SVC(kernel='linear'),
            'svc_rbf_clf': SVC(kernel='rbf'),
            'random_clf': RandomForestClassifier(random_state=42),
            'xgb_clf': XGBClassifier()
        }

    def initiate_model_training(self, train_array, test_array):
        """
        @params: train, test array
        This function takes the array and trains them on the model and log the reports in the folder.
        It then save the best model of all which gives the best accuracy.
        """
        try:
            logging.info("Splitting the data into dependent and independent features")
            (x_train, y_train, x_test, y_test) = (
                train_array[:, :-1],
                train_array[:, -1],
                test_array[:, :-1],
                test_array[:, -1]
            )

            model_report: dict = evaluate_model(x_train, y_train, self.models)

            logging.info(f"Model Report {model_report}")
            print(model_report, "\n")
            print('=' * 45)

            best_model_score = max(sorted(model_report.values()))

            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]

            best_model = self.models[best_model_name]

            logging.info(f"Best Model Name {best_model_name} Best model Score {best_model_score}")
            print(best_model_name)

            save_object(
                path=self.model_path.model_path,
                obj=best_model
            )
            logging.info(f"Saved {best_model}")

        except Exception as e:
            logging.error("Error while initiating model", exc_info=True)
            raise CustomException(e, sys)
