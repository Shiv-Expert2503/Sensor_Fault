import os
import sys
from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import RobustScaler

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object


def get_redundant_cols(df1: pd.DataFrame, missing_tresh=0.7):
    ratio = df1.isna().sum() / df1.shape[0]
    l1 = list(ratio[ratio > missing_tresh].index)
    return l1


@dataclass
class DataTransformationConfig:
    preprocessor_path = os.path.abspath(os.path.join(os.getcwd(), '..', '..', 'artifacts', 'preprocessor.pkl'))


class DataTransformation:
    def __init__(self):
        self.data_transformation = DataTransformationConfig()

    @staticmethod
    def get_preprocessor():
        try:
            logging.info("Creating Pipeline")
            imputer = KNNImputer(n_neighbors=5)
            pipeline = Pipeline(
                steps=[('imputer', imputer),
                       ('scaler', RobustScaler())]
            )

            return pipeline
        except Exception as e:
            logging.info("Error while Creating Pipeline")
            raise CustomException(e, sys)

    def initiate_data_transformation(self, data_path):
        try:
            logging.info('Reading Data')
            data = pd.read_csv(data_path)
            logging.info('Read Successfully')

            preprocessor = self.get_preprocessor()

            cols_to_drop = ['Unnamed: 0', 'Good/Bad']
            # cols_to_drop = get_redundant_cols(data)

            logging.info("Dividing into Dependent and independent features")
            X = data.drop(cols_to_drop, axis=1)
            y = np.where(data['Good/Bad'] == -1, 0, 1)
            logging.info("Dividing completed")

            logging.info("Splitting and Transforming Started")
            x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
            x_train_scaled = preprocessor.fit_transform(x_train)
            x_test_scaled = preprocessor.transform(x_test)
            logging.info("Transformation Completed")

            preprocessor_path = self.data_transformation.preprocessor_path

            save_object(
                preprocessor_path,
                preprocessor
            )

            logging.info("Preprocessor Saved")

            train_arr = np.c_[x_train_scaled, np.array(y_train)]
            test_arr = np.c_[x_test_scaled, np.array(y_test)]

            logging.info("DataTransformation Completed")
            return (
                train_arr,
                test_arr,
                preprocessor_path
            )

        except Exception as e:
            logging.info('Error Occurred in DataTransformation')
            raise CustomException(e, sys)
