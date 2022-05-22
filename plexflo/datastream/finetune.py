# Importing libraries

import os
import numpy as np
import pandas as pd
import tensorflow as tf
from pathlib import Path
from functools import partial
from plexflo.datastream.utils import export
from sklearn.model_selection import train_test_split

import warnings
warnings.filterwarnings("ignore")

# Defining a function to finetune the model

def finetune_15min_model(model, data, shift = 30, batchsize = 64, epochs = 5, val_split = 0, model_name = None):

    """
    Description: 
    -----------
    This function is used to fine-tune the model for a given dataframe

    Parameters:
    -----------
    model: The model to be finetuned (tf.keras.models.Model)
    data: The dataframe to be used for finetuning (pandas.DataFrame)
    shift: Number of samples to shift the data (int)
    batchsize: The batchsize of the data (int)
    epochs: The number of epochs for the model (int)
    val_split: The validation split for the model (float)
    model_name: The name of the model (str)

    Returns:
    --------
    The trained model (keras.Model)
    """    

    # Defining the constants
    seqlen = 900

    # Creates graphs and models folder (if it doesn't exist) whenever this method is called
    Path(os.path.join(os.getcwd(), "output", "graphs")).mkdir(parents=True, exist_ok=True)
    Path(os.path.join(os.getcwd(), "output", "models")).mkdir(parents=True, exist_ok=True)

    # Function for creating the sequence data
    def collate_pair(x, window):

        # a, last sample of b
        return x[:, 0], [x[-1,1:]]

    # Raise an exception if the dataframe is empty
    if data.empty:
        raise Exception("DataFrame is empty!")
    
    # Converting column names to lower case internally for validation purposes
    data.columns = map(str.lower, data.columns)
    
    # Raise an exception if the column grid and ground truth is not found
    if 'grid' and 'ground_truth' not in data.columns:
        raise Exception("No grid and ground_truth columns")
    
    # Raise an exception if the column grid has NaN values
    if data.grid.isna().any():
        raise Exception("Missing grid data (NaN values)")

    # Raise an exception if the column grid has data other than int and float
    if pd.api.types.is_numeric_dtype(data.grid) == False:
        raise Exception("Grid data must be a numeric type (integer or float)")
    
    # Raise an exception if there are not enough samples in the dataframe
    if data.shape[0] < seqlen:
        raise Exception("Data too short for 15 minute training")

    # Splitting the data into train and validation sets
    if val_split != 0:
        
        train_data, val_data = train_test_split(data, test_size = val_split, shuffle=False)

        train_arr = np.asarray(train_data[['grid', 'ground_truth']].to_numpy()).astype(np.float32)
        val_arr = np.asarray(val_data[['grid', 'ground_truth']].to_numpy()).astype(np.float32)
    
    else:        
        train_arr = np.asarray(data[['grid', 'ground_truth']].to_numpy()).astype(np.float32)

    # Creating the training dataset using tf.data.Dataset 
    try:
        train_dataset = tf.data.Dataset.from_tensor_slices(train_arr)
        train_dataset = train_dataset.window(seqlen, shift = shift, drop_remainder = True).flat_map(lambda x: x.batch(seqlen)).map(partial(collate_pair, window=seqlen))
        train_dataset = train_dataset.batch(batchsize, drop_remainder=True).prefetch(1)
    
    except:            
        raise Exception("Error in creating the training dataset")

    # Compiling the model with the optimizer and loss function
    model.model_15_min.compile(optimizer = tf.keras.optimizers.Adam(learning_rate = 0.001), loss = 'binary_crossentropy', metrics = ['accuracy'])
    
    # Setting the model export name
    f = "model_15_min.h5"
    if model_name is not None:
        f = model_name

    # Preparing the eval dataset using tf.data.Dataset and train the model (with eval dataset) for the given epochs
    if val_split != 0:            
        
        try:
            eval_dataset = tf.data.Dataset.from_tensor_slices(val_arr)
            eval_dataset = eval_dataset.window(seqlen, shift = shift, drop_remainder = True).flat_map(lambda x: x.batch(seqlen)).map(partial(collate_pair, window=seqlen))
            eval_dataset = eval_dataset.batch(batchsize, drop_remainder = True)

        except:
            raise Exception("Error in creating the validation dataset")

        chkpt = tf.keras.callbacks.ModelCheckpoint(filepath = os.path.join(os.getcwd(), "output", "models", f), monitor = 'val_loss', save_best_only = True, mode = 'min', verbose = 1)
        history = model.model_15_min.fit(train_dataset, epochs = epochs, validation_data = eval_dataset, verbose = 1, callbacks = [chkpt])

        # Generating and exporting the graphs
        export(history)

    # Training the model only on training dataset for the given epochs
    else:
        
        chkpt = tf.keras.callbacks.ModelCheckpoint(filepath = os.path.join(os.getcwd(), "output", "models", f), monitor = 'loss', save_best_only = True, mode = 'min', verbose = 1)
        history = model.model_15_min.fit(train_dataset, epochs = epochs, verbose = 1, callbacks = [chkpt])

        # Generating and exporting the graphs
        export(history)

    return model.model_15_min