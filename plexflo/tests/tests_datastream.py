import pytest
from plexflo.datastream import model
from plexflo.datastream.model import Model
from plexflo.datastream.inference import predict, predict_from_file

def run_load_model():

    model = Model()
    if model:
        return True

def run_predict_from_file():

    model = Model()
    file = "/Users/pranavraikote/Desktop/plexflo/docker/test.csv"
    
    df = predict_from_file(model, file, out_fname = None)
    
    if 'EV' in df.columns:
        return True

def test_wrong_extension():
    with pytest.raises(Exception):
        
        model = Model()
        file = "/Users/pranavraikote/Desktop/plexflo/docker/test.txt"
        df = predict_from_file(model, file, out_fname = None)

def test_correct():
    assert run_load_model() == True
    assert run_predict_from_file() == True

def test_wrong():
    test_wrong_extension()