import pytest
import pandas as pd
from plexflo.datastream.model import Model
from plexflo.datastream.inference import predict_from_file
from plexflo.datastream.finetune import finetune_15min_model

def test_load_model():

    model = Model()
    if model:
        return True

def test_predict_from_file():

    model = Model()
    file = "/Users/pranavraikote/Desktop/plexflo/docker/test.csv"
    
    df = predict_from_file(model, file, out_fname = None)
    
    if 'EV' in df.columns:
        return True

def test_wrong_extension():
    with pytest.raises(Exception) as e:
        
        model = Model()
        file = "/Users/pranavraikote/Desktop/plexflo/docker/test.txt"
        df = predict_from_file(model, file, out_fname = None)

        assert e.value.args[0] == 'File extension not supported! File must be either in csv or excel format'

def test_finetune():
    
    model = Model()
    file = "/Users/pranavraikote/Desktop/plexflo/docker/finetune.csv"

    df = pd.read_csv(file)
    
    new_model = finetune_15min_model(model, data = df, shift = 30,    batchsize = 64, epochs = 5, val_split = 0, model_name = None)
    
    if new_model:
        return True

def test_wrong_finetune():
    with pytest.raises(Exception) as e:
        
        model = Model()
        file = "/Users/pranavraikote/Desktop/plexflo/docker/test.csv"

        df = pd.read_csv(file)
        
        new_model = finetune_15min_model(model, data = df, shift = 30,    batchsize = 64, epochs = 5, val_split = 0, model_name = None)

        assert e.value.args[0] == 'No grid and ground_truth columns'