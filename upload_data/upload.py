import json  # as data in mongodb is stored in json
import os
import sys

import pandas as pd
from pymongo.mongo_client import MongoClient

from src.exception import CustomException
from src.logger import logging

try:
    logging.info("Trying to setup Mongo Db connection")
    uri = "mongodb+srv://shivansh1:yJpFVQCIQrcQUfht@cluster0.yc3hy9y.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(uri)
    logging.info("Pinged Successfully")

except Exception as e:
    logging.error("Error occurred while setuping mongoDb client", exc_info=True)
    raise CustomException(e, sys)

try:
    logging.info("Reading the Data")
    DATABASE_NAME = "learning"
    COLLECTION_NAME = "sensor_fault"
    path = os.path.abspath(os.path.join(os.getcwd(), '..', 'notebooks', 'data', 'wafer_23012020_041211.csv'))
    df = pd.read_csv(path)
    logging.info("Read successfully")

    logging.info("Dumping the data")
    json_records = list(json.loads(df.T.to_json()).values())

    client[DATABASE_NAME][COLLECTION_NAME].insert_many(json_records)
    logging.info("Dumped Successfully")

except Exception as e:
    logging.error("Error occurred while dumping ", exc_info=True)
    raise CustomException(e, sys)
