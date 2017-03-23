from DataImportAndFormatting import *
from DataCleaningAndProcessing import *
from DataTransformations import *
from SGDRegression import *
from RandomForestRegression import *
# Load the CSV file, process the data, and then transform that data
test_data_frame =transform_data( process_data( custom_import_test_data()))

# Obtain predicted values from the SGD model
SGD_predicted = TestSGDRegression(test_data_frame)

# Obtain predicted values from the RFR model
RFR_predicted = TestRFRegression(test_data_frame)

# Save the two sets of predicted values to a CSV file
combined_predictions = pd.DataFrame({'SGD_Predicted' : SGD_predicted})
combined_predictions['RFR_Predicted'] = RFR_predicted['predicted']
combined_predictions.to_csv('Results for Austin Collins.csv')

