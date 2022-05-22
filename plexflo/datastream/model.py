# Importing libraries

import os
import tensorflow as tf
from pathlib import Path

import warnings
warnings.filterwarnings("ignore")

# Defining the constansts required for loading the model
batchsize = 64
seqlen = 900

# Defining a class for the loading the Custom model. This is a templatized class taken from TensorFlow's guide: https://www.tensorflow.org/guide/keras/save_and_serialize#custom_objects
class CustomModel(tf.keras.Model):    

    def train_step(self, data):
        
        x_batch_train, y_batch_train = data

        with tf.GradientTape() as tape:

            logits = self(tf.reshape(x_batch_train, shape = (batchsize, 1, seqlen)), training = True)
            loss = self.compiled_loss(tf.reshape(y_batch_train, shape = (batchsize, 1)), logits, regularization_losses = self.losses)

        trainable_vars = self.trainable_variables
        gradients = tape.gradient(loss, trainable_vars)

        self.optimizer.apply_gradients(zip(gradients, trainable_vars))
        self.compiled_metrics.update_state(tf.reshape(y_batch_train, shape = (batchsize, 1)), logits)

        return {m.name : m.result() for m in self.metrics}

    def test_step(self, data):
        
        x_batch_eval, y_batch_eval = data

        logits = self(tf.reshape(x_batch_eval, shape = (batchsize, 1, seqlen)), training = True)
        loss = self.compiled_loss(tf.reshape(y_batch_eval, shape = (batchsize, 1)), logits, regularization_losses = self.losses)

        self.compiled_metrics.update_state(tf.reshape(y_batch_eval, shape = (batchsize, 1)), logits)

        return {m.name : m.result() for m in self.metrics}

# Main Model Class for loading plexflo's trained models
class Model:

    def __init__(self, path=None):

        """
        Description:
        -----------
        This class is used to load the trained model

        Parameters:
        -----------
        path: The path to load the fine-tuned model. Has to be inside the output folder (str)

        Returns:
        --------
        None
        """

        # Handling the default loading of the model and the fine-tuned model
        if path is None:
            self.path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'models', 'model_15min.h5')
        else:
            self.path = os.path.join(os.getcwd(), 'output', 'models', path)

        # Loading the model with the custom model class
        try:
            self.model_15_min = tf.keras.models.load_model(self.path, custom_objects = {"CustomModel": CustomModel})
            print("15 Min Model loaded")

        except:
            raise Exception("15 Min Model not found")

        # Creates an output folder and a files sub-folder (if it doesn't exist) whenever this class is initialized
        Path(os.path.join(os.getcwd(), "output")).mkdir(parents=True, exist_ok=True)
        Path(os.path.join(os.getcwd(), "output", "files")).mkdir(parents=True, exist_ok=True)