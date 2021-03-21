"""
Gini Curve Plot
---------------

Contents:
    gini
"""

import numpy as np

from matplotlib import pyplot as plt
import seaborn as sns

default_sat = 0.95


def gini(shares=None, dsat=default_sat, axis=None):
    """
    Produces a semicircle plot of shares or allocations

    Parameters
    ----------
        shares : list (contains ints or floats)
            The data to be plotted

        dsat : float : optional (default=default_sat)
            The degree of desaturation to be applied to the colors

        axis : str : optional (default=None)
            Adds an axis to plots so they can be combined

    Returns
    -------
        ax, gini : matplotlib.pyplot.subplot, float
            A gini plot of dispropotionality and the area under the Lorenz curve
    """
    if sum(shares) != 1:
        shares = [s / 100 for s in shares]

        assert sum(shares) == 1, "The 'shares' argument must sum to 100 or 1."

    shares.insert(0, 0)

    shares_cumsum = np.cumsum(a=shares, axis=None)
    pe_line = np.linspace(start=0.0, stop=1.0, num=len(shares_cumsum))

    area_under_lorenz = np.trapz(y=shares_cumsum, dx=1 / len(shares_cumsum))
    area_under_pe = np.trapz(y=pe_line, dx=1 / len(shares_cumsum))

    gini = (area_under_pe - area_under_lorenz) / area_under_pe

    ax = sns.lineplot(x=pe_line, y=shares_cumsum, ax=axis)
    ax = sns.lineplot(x=pe_line, y=pe_line, ax=axis)
    plt.fill_between(pe_line, shares_cumsum)
    plt.tight_layout()

    return ax, gini
