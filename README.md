# Sensor Fault Detection: An End-to-End MLOps Project

![Project Demo GIF](link_to_your_demo.gif)

This project demonstrates a complete, end-to-end MLOps pipeline for a real-world industrial problem: detecting faults in sensor data from semiconductor wafers. The focus is on building a robust, reproducible, and deployable system.

**Live Application:** [**sensor-fault-0bkp.onrender.com**](https://sensor-fault-0bkp.onrender.com/)

---

## Key Features

* **Interactive Web Interface:** A user-friendly frontend built with Flask, HTML, and vanilla JavaScript.
* **Dynamic Data Handling:** Upload a CSV, preview the data in an editable table, and manipulate values before prediction.
* **Real-Time Prediction:** Get instant fault predictions from the trained XGBoost model.
* **Downloadable Results:** View prediction results directly on the page and download them as a new CSV file.

---

## Tech Stack

- **Backend:** Python, Flask, Gunicorn
- **Frontend:** HTML, CSS, JavaScript
- **ML & Data:** Pandas, NumPy, Scikit-learn, XGBoost, Imbalanced-learn
- **Deployment:** Render, Git

---

## MLOps Pipeline Explained

This project was built following professional MLOps practices to ensure scalability and reproducibility.

1.  **Modular Code Structure:** The entire codebase is modular, separating concerns like data ingestion, transformation, and model training into distinct, reusable components.
2.  **Reproducible Pipelines:** The project features a `training_pipeline.py` that handles the complete model training process and a `prediction_pipeline.py` for inference. This ensures consistency between training and serving.
3.  **Artifact Management:** Trained model objects and preprocessors are saved as serialized artifacts (`.pkl` files), a core practice for versioning and deploying models.
4.  **Model Serving via API:** The Flask application wraps the prediction pipeline in a RESTful API, making the model's intelligence available to any web client.
5.  **Continuous Deployment:** The application is hosted on Render and configured for auto-deployment, where any `git push` to the main branch automatically triggers a new build and deployment.

---

## Model Limitations & Future Work

The primary goal of this project was to build and deploy a robust, end-to-end MLOps pipeline. The current model was trained on a highly imbalanced dataset where faulty ('bad') sensors constitute over 94% of the data.

As a result, the model exhibits a strong bias towards the majority class. While the focus of this iteration was on the pipeline's architecture, future work to improve the model's predictive performance would involve:

-   **Retraining** with techniques like **SMOTE** (from the `imblearn` library) to create a balanced training set.
-   **Hyperparameter tuning** of the XGBoost model, specifically the `scale_pos_weight` parameter, which is designed for imbalanced classification.
-   **Evaluating** the model using more appropriate metrics like the **F1-Score** or **AUC-ROC** instead of simple accuracy.

---

## How to Run Locally

1.  Clone the repository:
    ```bash
    git clone [https://github.com/Shiv-Expert2503/Sensor_Fault.git](https://github.com/Shiv-Expert2503/Sensor_Fault.git)
    cd Sensor_Fault
    ```
2.  Create and activate a Conda environment with Python 3.11.9:
    ```bash
    conda create --name sensor_fault python=3.11.9 -y
    conda activate sensor_fault
    ```
3.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Run the Flask application:
    ```bash
    python app.py
    ```
5.  Open your browser and navigate to `http://localhost:5000`.