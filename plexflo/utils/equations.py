import numpy as np

def kirchoffsLaw(sdfsdf):
    pass

def exponential(x, a, b, c):
    """
    Calculates the exponential function with constants a and b
    :param x:
    :param a:
    :param b:
    :return:
    """
    return a*np.exp(b*x)

def power_law(x, a, b, c):
    """
    Calculates the power law function with constants a and b
    :param x:
    :param a:
    :param b:
    :return:
    """
    return a*np.power(x, b)

def logarithmic(x, a, b, c):
    """
    Calculates the logarithmic function with constants a and b
    :param x:
    :param a:
    :param b:
    :param c:
    :return:
    """
    damping_factor = 0.25
    return a*np.log(x) + damping_factor*b

def linear(x, a, b):
    """
    Calculates the linear function with constants a and b
    :param x:
    :param a:
    :param b:
    :return:
    """
    return a*x + b

def gaussian(x, a, b, c):
    """
    Calculates the gaussian function with constants a, b and c
    :param x:
    :param a:
    :param b:
    :param c:
    :return:
    """
    return a*np.exp(-np.power(x - b, 2)/(2*np.power(c, 2)))

