from DataImportAndFormatting import *
from DataCleaningAndProcessing import *
from DataTransformations import *
from SGDRegression import *
from RandomForestRegression import *
# Load the CSV file, process the data, and then transform that data
SGD_training_data_frame =transform_data( process_data( custom_import_data()))

SGD_r2, SGD_rmse = TrainSGDRegression(SGD_training_data_frame)
print("SGD model trained with resulting values: r2 = {0}, RMSE = {1}".format(SGD_r2, SGD_rmse))

# clear the previous data training frame, in case memory is tight
SGD_training_data_frame = None

# Load the CSV file, process the data, and then transform that data
RFR_training_data_frame =transform_data( process_data( custom_import_data()))
RFR_r2, RFR_rmse = TrainRFRegression(RFR_training_data_frame)

print("RFR model trained with resulting values: r2 = {0}, RMSE = {1}".format(RFR_r2, RFR_rmse))

