import os
import pandas as pd

# Defining a function for listing files in a directory
def show():
    
    """
    Description:
    -----------
    This function is used to list all the load profile files in the files directory

    Parameters:
    -----------
    None

    Returns:
    --------
    None
    """

    # Listing all the files in the directory
    files = os.listdir(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'files'))

    # Printing the files
    for file in files:
        print(file)

# Defining a function for loading a profile
def use(name="morning_peak_average_household_WD_SU.csv"):
        
    """
    Description:
    -----------
    This function is used to load a profile from the files directory

    Parameters:
    -----------
    profile: The filename to load (string)

    Returns:
    --------
    data: The dataframe with the predictions (pandas.DataFrame)
    """

    # Loading the profile
    df = pd.read_csv(os.path.join(os.path.dirname(os.path.realpath(__file__)), "files", name))

    # Returning the loaded profile
    return df