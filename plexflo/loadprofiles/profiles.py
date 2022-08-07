import os
import pandas as pd

import plexflo.utils.dataops as dataops


def impact_of_policy_every_year_on_peak_kW(policy_factors, residential_weights, commercial_weights, years_of_analysis, use_weights=True,
                                           percentage_commercial=50, percentage_residential=50):
    """
    Calculates the impact of policy every year as a percentage of kW increases, compared to the base kW peak for every feeder.
    The methodology is described in a whitepaper.

    :param policy_factors: Dictionary of policy factors, sample_file = "plexflo/examples/policy/policy.json"
    :param residential_weights: Dictionary of the importance given to a particular policy factor for residential customers, sample_file = "plexflo/examples/policy/policy_residential_weights.json"
    :param commercial_weights: Dictionary of the importance given to a particular policy factor for commercial customers, sample_file = ""plexflo/examples/policy/policy_commercial_weights.json"
    :param years_of_analysis: Integer, Number of years from base year (or current year) to analyze the impact of policy
    :param use_weights: Boolean, if True, the impact of the policy is calculated using the weights, if False, the impact of the policy is calculated using the policy factors, without giving any importance to any particular policy factor
    :param percentage_commercial: Float, percentage of commercial customers by total annual energy use (kWh), default = 50
    :param percentage_residential: Float, percentage of residential customers by total annual energy use (kWh), default = 50
    :return: List of impact of policy every year
    """
    impact_dict_residential = {}
    impact_dict_commercial = {}
    impact_dict_feeder = {}
    total_factors = 0

    for key, value in policy_factors.items():
        for k, v in value.items():
            value[k] = int(v) + 100
            total_factors += 1

    def reset_policy_values():
        for key, value in policy_factors.items():
            for k, v in value.items():
                value[k] = 100

    def reset_policy_weights():
        for key, value in residential_weights.items():
            for k, v in value.items():
                value[k] = 1
        for key, value in commercial_weights.items():
            for k, v in value.items():
                value[k] = 1

    if use_weights is False:
        reset_policy_values()
        reset_policy_weights()

    assert percentage_commercial + percentage_residential == 100, "Percentage of commercial and residential customers " \
                                                                  "must add up to 100 "
    assert 0 <= percentage_commercial <= 100, "Percentage of commercial customers must be " \
                                              "between 0 and 100 "
    assert 0 <= percentage_residential <= 100, "Percentage of residential customers must " \
                                               "be between 0 and 100 "

    percentage_residential_weight = 1
    percentage_commercial_weight = percentage_commercial / percentage_residential

    for key, value in policy_factors.items():
        sub_dict = value
        sub_dict_residential_weights = residential_weights[key]
        sub_dict_commercial_weights = commercial_weights[key]

        # weights are just to indicate the fraction of residential and customer types, based on the total energy they
        # use over a period of the year

        impact_dict_residential[key] = dataops.multiply_dict_values(sub_dict_residential_weights, sub_dict)
        impact_dict_commercial[key] = dataops.multiply_dict_values(sub_dict_commercial_weights, sub_dict)

        impact_dict_feeder[key] = dataops.combine_dicts(impact_dict_residential[key], impact_dict_commercial[key],
                                                weights_a=percentage_residential_weight,
                                                weights_b=percentage_commercial_weight)

    total_impact = 0
    for key, value in impact_dict_feeder.items():
        for k, v in value.items():
            total_impact += int(v)

    total_impact_over_years = total_impact / total_factors
    annual_peak_cagr = dataops.cagr_basic(100, total_impact_over_years, years_of_analysis)

    impact_on_peak_every_year = []
    for year in range(years_of_analysis):
        impact_on_peak_every_year.append(dataops.compound_interest(100, annual_peak_cagr, year)[1])

    return impact_on_peak_every_year


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
