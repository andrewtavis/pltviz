"""
Semipie Plot
------------

Contents:
    semipie
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.collections import PatchCollection
import seaborn as sns

from pltviz import utils

default_sat = 0.95


def semipie(counts, colors=None, donut_ratio=1, dsat=default_sat, axis=None):
    """
    Produces a semicircle plot of shares or allocations

    Parameters
    ----------
        counts : list (contains ints or floats)
            The data to be plotted

        colors : list or list of lists : optional (default=None)
            The colors of the groups as hex keys

        donut_ratio : float (default=1, a full semicircle)
            The ratio of the center radius of a donut to the whole

        dsat : float : optional (default=default_sat)
            The degree of desaturation to be applied to the colors

        axis : str : optional (default=None)
            Adds an axis to plots so they can be combined

    Returns
    -------
        ax : matplotlib.pyplot.subplot
            A semicircle plot that depicts shares or allocations
    """
    if colors:
        assert len(colors) == len(
            counts
        ), "The number of colors provided doesn't match the number of counts to be displayed"

    elif colors == None:
        sns.set_palette("deep")  # default sns palette
        colors = [
            utils.rgb_to_hex(c)
            for c in sns.color_palette(n_colors=len(counts), desat=1)
        ]

    colors = [
        utils.scale_saturation(rgb_trip=utils.hex_to_rgb(c), sat=dsat) for c in colors
    ]
    sns.set_palette(colors)

    if axis:
        ax = axis  # to mirror seaborn axis plotting
    else:
        ax = plt.subplots()[1]

    patches = []
    thetas = [180 - (180 * sum(counts[:i]) / sum(counts)) for i in range(len(counts))]
    thetas.append(0)

    for i in range(len(counts)):
        wedge = mpatches.Wedge(
            center=(0, 0),
            r=1,
            theta1=thetas[i + 1],
            theta2=thetas[i],
            facecolor=colors[i],
            width=donut_ratio,
        )

        patches.append(wedge)

    collection = PatchCollection(patches, match_original=True)
    ax.add_collection(collection)

    plt.axis("equal")
    plt.axis("off")
    plt.tight_layout()

    return ax
