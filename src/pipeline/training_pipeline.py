from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation

obj1 = DataIngestion()
obj2 = DataTransformation()
data_path = obj1.initiate_data_ingestion()

print(data_path)

_, _, preprocessor_path = obj2.initiate_data_transformation(data_path)
print(preprocessor_path)
