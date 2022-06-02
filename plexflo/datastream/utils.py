# Importing libraries

import os
import datetime
import matplotlib.pyplot as plt

# Function to plot the graph and export them as pngs
def export(history):
    
    """
    Description: 
    -----------
    This function is used to plot the graph and export them as pngs

    Parameters:
    -----------
    history: The history of the model (keras.callbacks.History)

    Returns:
    --------
    None
    """
    
    # Plotting the Accuracy Graph
    plt.figure()              
    plt.plot(history.history['accuracy'])
    
    # Handling the validation accuracy if the metrics exists in history object
    try:    
        plt.plot(history.history['val_accuracy'])
    except:
        pass

    plt.title('Model accuracy')
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Validation'], loc='upper left')
    plt.grid()

    # Saving the accuracy graph as png
    plt.savefig(os.path.join(os.getcwd(), "output", "graphs", "accuracy.png"))

    # Plotting the Accuracy Graph
    plt.figure()
    plt.plot(history.history['loss'])

    # Handling the validation accuracy if the metrics exists in history object
    try:
        plt.plot(history.history['val_loss'])
    except:
        pass

    plt.title('Model loss')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Validation'], loc='upper left')
    plt.grid()

    # Saving the loss graph as png
    plt.savefig(os.path.join(os.getcwd(), "output", "graphs", "loss.png"))