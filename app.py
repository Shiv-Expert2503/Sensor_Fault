import sys

from flask import Flask, render_template, request, send_file
from src.pipeline.prediction_pipeline import PredictionPipeline

from src.exception import CustomException
from src.logger import logging

app = Flask(__name__)


@app.route("/")
def home():
    return "Welcome to my application"


@app.route('/predict', methods=['POST', 'GET'])
def upload():
    try:
        if request.method == 'POST':
            # it is a object of prediction pipeline
            prediction_pipeline = PredictionPipeline(request)
            logging.info("Running")
            prediction_file_detail = prediction_pipeline.run_pipeline()

            logging.info("prediction completed. Downloading prediction file.")
            return send_file(prediction_file_detail.prediction_file_path,
                             download_name=prediction_file_detail.prediction_file_name,
                             as_attachment=True)
        else:
            return render_template('upload_file.html')
    except Exception as e:
        raise CustomException(e, sys)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
