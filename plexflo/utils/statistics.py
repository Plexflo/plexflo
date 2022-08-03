import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from fitter import Fitter, get_common_distributions, get_distributions
from fitter import HistFit

np.set_printoptions(precision=3)


def kernel_density():
    pass


def histogram(val, x_axis="", y_axis="", title=None, bin_size=10, bin_and_count=False, show=True, save=False):
    val.plot.hist(grid=True, bins=bin_size, rwidth=0.9, color='#2463fb')
    plt.title(title)
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    if show:
        plt.show()
    if save:
        assert title is not None, "Title must be specified to save the plot"
        plt.savefig(title + ".png")
    if bin_and_count:
        hist, bin_edges = np.histogram(val, bins=bin_size)
        bbins = np.char.mod('%.2f', bin_edges)
        label = map('-'.join, zip(bbins[:-1], bbins[1:]))
        return dict(zip(label, hist))



def fit_common_distributions(val, sample_fraction=1):
    val_sample = val.sample(frac=sample_fraction, ignore_index=True)
    f = Fitter(val_sample)
    f.fit()
    print(f.summary())


def fit_best_distribution(val, sample_fraction=1, bin_size=100):
    val_sample = val.sample(frac=sample_fraction, ignore_index=True)
    f = Fitter(val_sample, bins=bin_size, distributions=['gamma', 'lognorm', "weibull"])
    f.fit()
    print(f.get_best(method='sumsquare_error'))


def build_probability_distribution_function(val, sample_fraction=1.0, bin_size=100, title="", ylabel="", xlabel="", save=False, show=True):
    """
    :param val:
    :param sample_fraction:
    :param bin_size:
    :param title:
    :param ylabel:
    :param xlabel:
    :param save:
    :param show:
    :return:
    """
    val_sample = val.sample(frac=sample_fraction, ignore_index=True)
    f = Fitter(val_sample, bins=bin_size, distributions=['gamma', 'lognorm', "weibull"])
    f.fit()
    f.plot_pdf(names=None, Nbest=1, lw=1, method='sumsquare_error')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if show:
        plt.show()
    z = f.get_best(method='sumsquare_error')
    return z.keys(), z.items()


# # TODO: Delete these tests in the final build
# df = pd.read_csv("C:\\Users\\Administrator\\PycharmProjects\\NG_specific_codes\\rooftopmodule\\Outputs"
#                  "\\Solar_Adoption_Testdataset.csv", index_col=None, low_memory=False)
# df_adopted = df[df['ADOPTED_SOLAR'] == 1]
# df_not_adopted = df[df['ADOPTED_SOLAR'] == 0]
# print(f"Total Adopted Solar = {len(df_adopted)}")
# histogram(df_adopted['W_SCORE'], title="Adopted Solar - W_Score Distribution", bin_size=100)
# histogram(df_not_adopted['W_SCORE'], title="Did not Adopt Solar - W_Score Distribution", bin_size=100)

# a, b = build_probability_distribution_function(df_not_adopted['W_SCORE'], sample_fraction=0.1, title="NOT Adopted
# Solar : W_Score PDF") print(a, b) fit_best_distribution(df_not_adopted['W_SCORE'], sample_fraction=0.1)
