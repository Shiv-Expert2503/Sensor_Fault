# import sys

# from flask import Flask, render_template, request, send_file
# from src.pipeline.prediction_pipeline import PredictionPipeline

# from src.exception import CustomException
# from src.logger import logging

# app = Flask(__name__)


# @app.route("/")
# def home():
#     return "Welcome to my application"


# @app.route('/predict', methods=['POST', 'GET'])
# def upload():
#     try:
#         if request.method == 'POST':
#             # it is a object of prediction pipeline
#             prediction_pipeline = PredictionPipeline(request)
#             logging.info("Running")
#             prediction_file_detail = prediction_pipeline.run_pipeline()

#             logging.info("prediction completed. Downloading prediction file.")
#             return send_file(prediction_file_detail.prediction_file_path,
#                              download_name=prediction_file_detail.prediction_file_name,
#                              as_attachment=True)
#         else:
#             return render_template('upload_file.html')
#     except Exception as e:
#         raise CustomException(e, sys)


# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000, debug=True)



## New changes as per needed
import sys
from flask import Flask, render_template, request, send_file
from src.pipeline.prediction_pipeline import PredictionPipeline
from src.exception import CustomException
from src.logger import logging

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('upload_file.html')

@app.route('/predict', methods=['POST', 'GET'])
def upload():
    try:
        if request.method == 'GET':
            # If a user just navigates to /predict, show the upload page
            return render_template('upload_file.html')
        
        # This block will only run for POST requests
        
        # --- FIX: Check for the file BEFORE running the pipeline ---
        if 'file' not in request.files:
            logging.error("No file part in the request")
            return "Error: No file part in the form submission.", 400

        file = request.files['file']

        if file.filename == '':
            logging.error("No file selected for uploading")
            return "Error: No file was selected for uploading.", 400
        # --- END OF FIX ---

        # If the checks pass, now we can safely run the pipeline
        if file:
            prediction_pipeline = PredictionPipeline(request)
            logging.info("Prediction pipeline started.")
            prediction_file_detail = prediction_pipeline.run_pipeline()

            logging.info("Prediction completed. Downloading prediction file.")
            return send_file(prediction_file_detail.prediction_file_path,
                             download_name=prediction_file_detail.prediction_file_name,
                             as_attachment=True)

    except Exception as e:
        # For Render logs, printing the exception is very helpful for debugging
        print(e)
        raise CustomException(e, sys)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
