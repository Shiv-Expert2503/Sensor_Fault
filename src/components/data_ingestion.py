import os
import sys
from dataclasses import dataclass

import numpy as np
import pandas as pd
from pymongo.mongo_client import MongoClient

from src.exception import CustomException
from src.logger import logging


@dataclass
class DataIngestionConfig:
    raw_path: str = os.path.abspath(os.path.join(os.getcwd(), '..', '..', 'artifacts', 'raw.csv'))


class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    @staticmethod
    def load_dataset(collection_name, database_name):
        """
        @params: database_collection_name in string format
        @params: database_name in string format
        @returns: pd.DataFrame
        """
        try:
            uri = "uri"
            mongo_client = MongoClient(uri)

            collection = mongo_client[database_name][collection_name]
            df = pd.DataFrame(list(collection.find()))

            if "_id" in df.columns.to_list():
                df = df.drop("_id", axis=1)

            df.replace({"na": np.nan}, inplace=True)

            return df

        except Exception as e:
            logging.error("Error while exporting the data", exc_info=True)
            raise CustomException(e, sys)

    # Return train,test.csv paths
    def initiate_data_ingestion(self):
        try:

            logging.info('Directory made')
            os.makedirs(os.path.dirname(self.ingestion_config.raw_path), exist_ok=True)
            df = self.load_dataset("sensor_fault", "learning")
            df.to_csv(self.ingestion_config.raw_path, index=False)
            logging.info('Saved Successfully')
            return self.ingestion_config.raw_path

        except Exception as e:
            logging.info('Error occurred while handling data ingestion')
            raise CustomException(e, sys)
