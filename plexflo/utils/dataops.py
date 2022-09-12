import numpy as np
import pandas as pd
import math
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import matplotlib as mpl
# mpl.use('Agg')
plt.rcParams['axes.grid'] = False
from pathlib import Path

# from equations import *
# from ..utils.equations import *


def auto_data_quality_report(df):
    """
    This function will create a data quality report for a dataframe. It will check for missing values, duplicate rows,
    and duplicate columns.
    """

    # list all the continuous variable columns
    continuous_columns = [col for col in df.columns if df[col].dtype == "float64"]

    # list all the categorical variable columns
    categorical_columns = [col for col in df.columns if df[col].dtype == "object"]

    # list all the geographical variable columns
    geographical_columns = [col for col in df.columns if all([df[col].dtype == "float64", any([col.endswith("_lat"), col.endswith("_lon"), col.endswith("_latitude"), col.endswith("_X"), col.endswith("_Y")])])]

    # list all the date variable columns
    date_columns = [col for col in df.columns if df[col].dtype == "datetime64[ns]"]
    # breakpoint()
    # create a dataframe with just the continuous variable columns
    continuous_df = df[continuous_columns]
    # find the features, counts, and quartiles for each continuous variable column
    continuous_features = continuous_df.describe().T.reset_index()
    continuous_features.columns = ["feature", "count", "mean", "std", "min", "25%", "50%", "75%", "max"]
    # find the missing value of each continuous variable feature
    continuous_features["missing"] = continuous_df.isnull().sum()
    # find the duplicate rows of each continuous variable feature
    continuous_features["duplicate"] = continuous_df.duplicated().sum()

    # create a dataframe with just the categorical variable columns
    categorical_df = df[categorical_columns]

    # find the features, counts, and quartiles for each categorical variable column
    columns = ["feature", "count", "unique", "mode", "missing", "missing %", "mode freq", "mode freq %", "2nd mode", "2nd mode freq", "2nd mode freq %"]
    categorical_features = pd.DataFrame(columns=columns)
    for col in categorical_columns:
        # find the features, counts, and quartiles for each categorical variable column
        # empty initial temporary dataframe
        tmp_df = pd.DataFrame(columns=columns)
        # breakpoint()
        tmp_df["feature"] = col
        tmp_df["count"] = pd.Series(categorical_df[col].value_counts())
        tmp_df["unique"] = pd.Series(categorical_df[col].nunique())
        tmp_df["mode"] = pd.Series(categorical_df[col].mode().values[0])
        # tmp_df["mode freq"] = pd.Series(categorical_df[col].mode().values[1])
        # tmp_df["mode freq %"] = tmp_df[tmp_df.index == tmp_df["mode"]].values[0][0] / tmp_df["count"]
        # tmp_df["2nd mode"] = categorical_df[col].mode().values[1]
        # tmp_df["2nd mode freq"] = tmp_df[tmp_df.index == tmp_df["2nd mode"]].values[0][0]
        # tmp_df["2nd mode freq %"] = tmp_df[tmp_df.index == tmp_df["2nd mode"]].values[0][0] / tmp_df["count"]
        tmp_df["missing"] = categorical_df[col].isnull().sum()
        tmp_df["missing %"] = tmp_df["missing"] / tmp_df["count"]
        print(tmp_df)

        categorical_features = categorical_features.append(tmp_df, ignore_index=True)

    # Plot the distribution of each continuous variable feature
    # continuous_features.plot(kind="bar", x="feature", y="mean", figsize=(20, 10), legend=False, title="Mean Distribution")

    # print(categorical_features)

    return continuous_features, categorical_features


def min_max_normalize(val):
    """
    Min-max normalization is one of the most common ways to normalize data. For every feature, the minimum value of
    that feature gets transformed into a 0, the maximum value gets transformed into a 1, and every other value gets
    transformed into a decimal between 0 and 1.

    :param val: should be a dataframe or a dataframe column
    :return:
    """
    val.fillna(val.median(), inplace=True)
    return (val - val.min()) / (val.max() - val.min())


def min_max_inverse_normalize(val):
    """
    Sometimes low values indicate better or higher, however, there are several other parameters where this isn't
    true. For example, you have two columns like "1 indicates High Education, 10 indicates low", and you want to
    correlate it with "Cost of house they bought". Then, this function will come handy. Please note that Min-max
    normalization is one of the most common ways to normalize data. For every feature, the minimum value of that
    feature gets transformed into a 0, the maximum value gets transformed into a 1, and every other value gets
    transformed into a decimal between 0 and 1.

    :param val: should be a dataframe or a dataframe column
    :return:
    """
    val.fillna(val.median(), inplace=True)
    return 1 - (val - val.min()) / (val.max() - val.min())


def z_score_normalize(val):
    """
    Z-score normalization is a strategy of normalizing data that avoids the outlier issue.

    :param val: should be a dataframe or a dataframe column
    :return:
    """
    val.fillna(val.median(), inplace=True)
    return (val - val.mean()) / val.std()


def alphanumeric_inverse_normalize(val):
    """
    This is helpful when a dataset can have a column like this:
    A = >10
    B = 8-10
    C = 6-8
    .
    .

    F = 0
    ... and we want to normalize these values in a scale of 0 to 1, where 1 would indicate lower values.

    :param val: Dataframe Column
    :return:
    """
    val.fillna("_", inplace=True)
    tmp_list = val.unique().tolist()
    tmp_list = [str(i) for i in tmp_list]
    tmp_list.sort()
    fill_index = math.ceil(len(tmp_list) / 2)
    tmp_list[-1] = tmp_list[fill_index]
    tmp_list.sort()
    val.replace(to_replace="_", value=tmp_list[fill_index], inplace=True)
    val = val.apply(lambda x: tmp_list.index(str(x)) / len(tmp_list))
    return 1 - min_max_normalize(val)


def alphanumeric_normalize(val):
    """
    This is helpful when a dataset can have a column like this:
    A = $1 - $4,999
    B = $5,000 - $9,999
    C = $10,000 - $19,999
    .
    .
    .
    Q = $1,000,000 - $1,999,999
    R = Greater than $1,999,999
    ... and we want to normalize these values in a scale of 0 to 1.

    :param val: Dataframe Column

    """
    val.fillna("_", inplace=True)
    tmp_list = val.unique().tolist()
    tmp_list = [str(i) for i in tmp_list]
    tmp_list.sort()
    fill_index = math.ceil(len(tmp_list) / 2)
    tmp_list[-1] = tmp_list[fill_index]
    tmp_list.sort()
    val.replace(to_replace="_", value=tmp_list[fill_index], inplace=True)
    val = val.apply(lambda x: tmp_list.index(str(x)) / len(tmp_list))
    return min_max_normalize(val)


def cagr(df, period=None):
    """
    Calculate the CAGR of a dataframe row

    :param df:
    :return:
    """
    if period is None:
        period = len(df)
        try:
            answer = (df.iloc[-1] / df.iloc[0]) ** (1 / period) - 1
        except ZeroDivisionError:
            answer = 0
    else:
        try:
            idx_of_first_non_zero_value =  df.to_numpy().nonzero()[0][0]
            try:
                answer = (df[len(df) - period:].iloc[-1] / df[len(df) - period:].iloc[idx_of_first_non_zero_value]) ** (
                        1 / period) - 1
            except ZeroDivisionError:
                answer = 0
        except IndexError:
            answer = 0

    return answer


def cagr_basic(initial_value, final_value, years_of_analysis):
    return round(((final_value/initial_value)**(1/years_of_analysis) - 1)*100,2 )

def compound_interest(principle, rate, time):
    # Calculates compound interest
    amount = principle * (pow((1 + rate / 100), time))
    return amount - principle, amount

def intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))


def row_plot(df, savePlot=False, savePath= None, showPlot=True, title=None, xlabel=None, ylabel=None):
    """
    Plot a row of a dataframe

    :param df:
    :return:
    """
    df.plot(kind='line', figsize=(10, 5))
    if title is not None:
        plt.title(title)
    if xlabel is not None:
        plt.xlabel(xlabel)
    if ylabel is not None:
        plt.ylabel(ylabel)
    if savePlot:
        q = Path(savePath)
        if not q.is_dir():
            q.mkdir(parents=True, exist_ok=True)
        plt.savefig(savePath + "/" + title + ".png")
    if showPlot:
        plt.show()
    plt.close('all')

def trendline_forecast(df, method='logarithmic', backward_period=2, forward_period=1):
    """
    Calculate the logarithmic trendline forecast of a dataframe row

    :param df:
    :param method: Choose from 'logarithmic', 'power_law', 'exponential'
    :param backward_period: int
    :param forward_period: int
    :param damping_factor: float, Default 0
    :return:
    """
    assert backward_period > 2, "backward_period must be greater than 2"
    assert forward_period > 1, "forward_period must be greater than 1"
    df = df.fillna(method='ffill',axis=0)
    assert len(df) >= backward_period, "length of dataframe must be greater than backward period"

    xdata = np.array(range(1, backward_period + 1))
    forecast_x = np.array(range(backward_period + 1, backward_period + forward_period + 1))

    if method == 'logarithmic':
        popt, pcov = curve_fit(f=logarithmic, xdata=xdata ,ydata=df[-backward_period:].values)
        forecast_y = logarithmic(forecast_x, *popt)
    elif method == 'power_law':
        popt, pcov = curve_fit(f=power_law, xdata=xdata ,ydata=df[-backward_period:].values)
        forecast_y = power_law(forecast_x, *popt)
    elif method == 'exponential':
        popt, pcov = curve_fit(f=exponential, xdata=xdata ,ydata=df[-backward_period:].values)
        forecast_y = exponential(forecast_x, *popt)
    elif method == 'linear':
        popt, pcov = curve_fit(f=linear, xdata=xdata ,ydata=df[-backward_period:].values)
        forecast_y = linear(forecast_x, *popt)
    elif method == 'gaussian':
        popt, pcov = curve_fit(f=gaussian, xdata=xdata ,ydata=df[-backward_period:].values)
        forecast_y = gaussian(forecast_x, *popt)
    else:
        raise ValueError("Method must be 'logarithmic', 'power_law', 'exponential', or 'linear'")

    return forecast_y


def create_cagr(df, years=5):
    row_hist = [f"Y{time}" for time in [*range(2021 - years, 2021)]]
    try:
        cagr_value = cagr(df[row_hist], period=years)
    except:
        breakpoint()

    return cagr_value


def multiply_dict_values(dict_a, dict_b):
    dict_c = {}
    for key in dict_a:
        dict_c[key] = int(dict_a[key]) * int(dict_b[key])
    return dict_c


def combine_dicts(dict_a, dict_b, weights_a=1, weights_b=1):
    dict_c = {}
    for key in dict_a:
        dict_c[key] = (int(dict_a[key]) * weights_a + int(dict_b[key]) * weights_b)/(weights_a + weights_b)
    return dict_c



df = pd.read_csv("/Users/sayon/Documents/GitHub/plexflo/plexflo/examples/datasets/test.csv")

auto_data_quality_report(df)