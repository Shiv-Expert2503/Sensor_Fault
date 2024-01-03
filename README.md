# Sensor Fault Detection Project

## Table of Contents
1. Problem Statement
2. Overview
3. Technologies Used
4. Project Structure
5. Installation & Dependencies

## Problem Statement
Detecting sensor faults is a critical aspect of ensuring the reliability and accuracy of data collected from various sensors. In industrial and IoT applications, sensors play a pivotal role in monitoring and controlling processes. However, sensors may encounter issues such as drift, noise, or complete failure over time, leading to inaccurate readings and potentially compromising the performance of the systems they support. The goal of this project is to develop a machine learning-based solution that can predict and identify sensor faults, enabling timely maintenance and preventing the propagation of erroneous data throughout the system. By addressing sensor faults, the project aims to enhance the overall dependability and efficiency of applications relying on sensor-generated information.

## Overview
This project has  `complete end-to-end pipelines deployed on the Azure platform using Github actions and Docker`. First, we collect or ingest the data from DataBase MongoDB and then apply the transformation to it and train our model with the transformed data. Since this is a classification problem hence I have used several classifiers like `SVC and RandomForest for capturing the non-linearity in the data`. After training all the classifiers I saved the best one and used it for my prediction. Here I have also created one webpage using `HTML, and CSS and the backend is served by Flask`. The user will give us a data frame and that will be stored in the `MongoDB for further fine-tuning of the model`. Then I predicted the outcome using the model and gave the user the final data frame with a new output column added to it.


## Technologies Used
ML, Feature Engineering, EDA, MLOps, AZURE< Docker, Flask

## Project Structure
I have followed `modular coding` which is a common practice used in Industries. Making it more readable and beginner-friendly.
All the functions have been `documented properly` to understand the particular section of the code easily.

## Installation & Dependencies
As modular coding is used you can either run `python install setup.py` or just do   `pip install -r requirements.txt`. Both of these commands will install all necessary dependencies that are required for the project to run.
