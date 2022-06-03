# Import libraries

import os
import numpy as np
import pandas as pd
import tensorflow as tf

import warnings
warnings.filterwarnings("ignore")

# Function to generate predictions for a given file path
def predict_from_file(model, file, out_fname = None):

    """
    Description:
    -----------
    This function is used to predict the EV values for a given file path

    Parameters:
    -----------
    model: The model to be finetuned (tf.keras.models.Model)
    file: The file path to be predicted (str)
    out_fname: The file path for the exported dataframe (str)

    Returns:
    --------
    data: The dataframe with the predictions (pandas.DataFrame)
    """

    # Reading the data from the file only if the extension is .csv
    if file.endswith(".csv"):
        data = pd.read_csv(file)

        # Calling the predict function to generate the predictions
        return predict(model, data, out_fname)
    
    elif file.endswith(".xlsx"):
        data = pd.read_excel(file)

        # Calling the predict function to generate the predictions
        return predict(model, data, out_fname)
    else:
        raise Exception("File extension not supported! File must be either in csv or excel format")

# Function to generate predictions for a given dataframe
def predict(model, data, out_fname = None):

    """
    Description:
    -----------
    This function is used to predict the EV values for a given dataframe

    Parameters:
    -----------
    model: The model to be finetuned (tf.keras.models.Model)
    data: The dataframe to be predicted (pandas.DataFrame)
    out_fname: The file path for the exported dataframe (str)

    Returns:
    --------
    data: The dataframe with the predictions (pandas.DataFrame)
    """

    binary_threshold_15_min = 0.10

    # Raise an exception if the dataframe is empty
    if data.empty:
        raise Exception("DataFrame is empty!")

    # Converting column names to lower case internally for validation purposes
    data.columns = map(str.lower, data.columns)
            
    # Raise an exception if the column grid is not found
    if 'grid' not in data.columns:
        raise Exception("Column named 'grid' not found in the dataframe!")
    
    # Handling null values in the grid column
    if data.grid.isna().any():
        data.grid = data.grid.fillna(0)
    
    # Raise an exception if the column grid has data other than int and float    
    if pd.api.types.is_numeric_dtype(data.grid) == False:
        raise Exception("Grid data must be a numeric type (integer or float)")

    # Raise an exception if there are not enough samples in the dataframe
    if data.shape[0] < 900:
        raise Exception("Data too short for 15 minute prediction")

    # Internal function to output the EV 0/1 values given the sequence data
    def predict_loop(infer_data):

        """
        Description:
        -----------
        This function is used to predict the EV values for a given sequence data

        Parameters:
        -----------
        infer_data: The sequence data to be predicted (numpy.ndarray)

        Returns:
        --------
        EV: The EV value 0/1 for the sequence data (float)
        """

        # Reshaping the data to be compatible with the model and predicting the EV values
        outputs = model.model_15_min(tf.reshape(infer_data, shape = (1, 1, 900)), training = False).numpy()[0]
        
        # Converting the EV values to 0/1 based on the threshold
        EV = 0
        if outputs > binary_threshold_15_min:
            EV = 1

        return EV

    # Creating a new column for the EV values
    data['EV'] = " "

    print("Predicting 15 min EV values")

    # Looping through the dataframe and generating the EV values
    for i, r in data.iterrows():

       
        if i % 900 == 0 and i != 0:
                val = predict_loop(data.iloc[i-900:i]['grid'].to_list())
                data.loc[i-900:i, ["EV"]] = val

    # Exporting the dataframe with the predictions column to a csv file
    f = "predictions_" + str(15) + "_min.csv"

    if out_fname is not None:
        f = out_fname

    # Exporting the dataframe to a csv file
    data.to_csv(os.path.join(os.getcwd(), "output", "files", f))
    
    return data