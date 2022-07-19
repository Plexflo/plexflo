# Import statement
from plexflo.datastream.model import Model

# This will initialize the ML model
model = Model()

# This will load a TensorFlow model which is capable of generating predictions every 15 minutes (~900s).

from plexflo.datastream.inference import predict_from_file

pred_data = predict_from_file(model, "test.csv")

print("Successfully generated predictions for test.csv")
print("For viewing the csv file, go to /usr/arc/app/output/files folder")