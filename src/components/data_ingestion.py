import os
import sys
from dataclasses import dataclass

import pandas as pd

from src.exception import CustomException
from src.logger import logging

from sklearn.model_selection import train_test_split


@dataclass
class DataIngestionConfig:
    raw_path: str = os.path.abspath(os.path.join(os.getcwd(), '..', '..', 'artifacts', 'raw.csv'))


class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def load_dataset(self):
        pass

    # Return train,test.csv paths
    def initiate_data_ingestion(self):
        try:

            # Load the dataset from mondodb
            logging.info('Directory made')
            os.makedirs(os.path.dirname(self.ingestion_config.raw_path), exist_ok=True)
            df = pd.read_csv(os.path.abspath(os.path.join(os.getcwd(), '..', '..', 'notebooks', 'Data',
                                                          'wafer_23012020_041211.csv')))  ## Change the path please of exported data
            df.to_csv(self.ingestion_config.raw_path, index=False)
            logging.info('Saved Successfully')
            return self.ingestion_config.raw_path

        except Exception as e:
            logging.info('Error occurred while handling data ingestion')
            raise CustomException(e, sys)
