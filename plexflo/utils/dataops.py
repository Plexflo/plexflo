import numpy as np
import pandas as pd
import math
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.use('Agg')
plt.rcParams['axes.grid'] = False
from pathlib import Path

# from equations import *
from ..utils.equations import *

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


