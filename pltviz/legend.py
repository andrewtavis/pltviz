"""
Legend
------

Functions for generating legends

Contents:
    gen_handles,
    gen_elements
"""

import pandas as pd

from matplotlib.lines import Line2D
import seaborn as sns

from pltviz import utils

default_sat = 0.95


def gen_handles(colors=None, size=10, marker="o", dsat=default_sat):
    """
    Generates handles for plot legends

    Parameters
    ----------
        colors : list (contains rgb strs)
            The colors to be used for the legend

        size : int or float (default=10)
            The size of the markers for the legend

        marker : str : optional (default='o')
            The kind of shape for the legend (takes matplotlib.marker types)

        dsat : float : optional (default=default_sat)
            The degree of desaturation to be applied to the colors

    Returns
    -------
        lgnd_handles : list (countains unplotted 2D lines)
            A list of lines, the handles of which can be used for more advanced plots
    """
    if type(colors) == str:
        colors = [colors]
    elif colors == None:
        sns.set_palette("deep")  # default sns palette
        colors = [utils.rgb_to_hex(c) for c in sns.color_palette()]

    # Marker edge colors are the same as legend boarder unless transparent RGBA
    marker_edge_colors = [
        c if (len(c) == 9) and (c[-2:] == "00") else "#D2D2D3" for c in colors
    ]

    lgnd_handles = [
        Line2D(
            [0],
            [0],
            linestyle="none",
            marker=marker,
            markersize=size,
            markeredgecolor=marker_edge_colors[i],
            markeredgewidth=size / 10,
            markerfacecolor=utils.scale_saturation(rgb_trip=c, sat=dsat),
        )
        for i, c in enumerate(colors)
    ]

    return lgnd_handles


def gen_elements(
    counts=None,
    labels=None,
    colors=None,
    size=10,
    marker="o",
    padding_indexes=None,
    order=None,
    dsat=default_sat,
):
    """
    Generates handles and labels for plot legends while allowing for label padding and reordering

    Parameters
    ----------
        counts : list or list of lists : optional (contains ints or floats)
            The data to be plotted

        labels : list : optional (default=None; contains strs)
            The labels of the groups

        colors : list : optional (contains rgb strs)
            The colors to be used for the legend

        size : int or float (default=10)
            The size of the markers for the legend

        marker : str : optional (default='o')
            The kind of shape for the legend (takes matplotlib.marker types)

        padding_indexes : int or list : optional (default=None)
            Which indexes in the label should be filled with blank space to organize it well

        order : list : optional (default=None)
            The order for the handles and labels

        dsat : float : optional (default=default_sat)
            The degree of desaturation to be applied to the colors

    Returns
    -------
        lgnd_handles, lgnd_labels: list (countains unplotted 2D lines) and list (contains strs)
            A list of lines, the handles of which can be used for more advanced plots, as well as labels for the handles
    """
    if type(colors) == str:
        colors = [colors]
    elif colors == None:
        sns.set_palette("deep")  # default sns palette
        colors = [utils.rgb_to_hex(c) for c in sns.color_palette()]

    colors_copy = colors[:]

    # Empty lists are returned if no arguments are passed
    # Allows for easy experimentation with the legend
    lgnd_handles = []
    lgnd_labels = []
    if (counts is not None) or (labels is not None):
        # Create 'None' copies to assure originals aren't altered
        counts_copy = None
        labels_copy = None

        if counts is not None:
            if type(counts) == pd.Series:
                counts = list(counts)

            if list in [type(item) for item in counts]:
                counts = [item for sublist in counts for item in sublist]

            counts_copy = counts[:]

        if labels is not None:
            labels_copy = labels[:]

        if order is not None:
            if list in [type(item) for item in order]:
                order = [item for sublist in order for item in sublist]

            if counts_copy is not None:
                counts_copy = [counts_copy[i] for i in order]
            if labels_copy is not None:
                labels_copy = [labels_copy[i] for i in order]
            colors_copy = [colors_copy[i] for i in order]

        else:
            if counts_copy is not None:
                order = list(range(len(counts_copy)))
            elif labels_copy is not None:
                order = list(range(len(labels_copy)))

        if padding_indexes:
            if type(padding_indexes) == int:
                padding_indexes = [padding_indexes]
            sorted(padding_indexes)
            for i in padding_indexes:
                if counts_copy is not None:
                    counts_copy.insert(i, None)
                if labels_copy is not None:
                    labels_copy.insert(i, None)
                colors_copy.insert(i, "#ffffff00")

        lgnd_handles = gen_handles(colors=colors_copy, size=size, marker=marker)

        if (counts_copy is not None) and (labels_copy is not None):
            lgnd_labels = [
                f"{labels_copy[i]}: {c}" if c != None else ""
                for i, c in enumerate(counts_copy)
            ]
        elif (counts_copy is not None) and (labels_copy is None):
            lgnd_labels = [
                f"{c}" if c != None else "" for i, c in enumerate(counts_copy)
            ]
        elif (counts_copy is None) and (labels_copy is not None):
            lgnd_labels = [
                f"{lbl}" if lbl != None else "" for i, lbl in enumerate(labels_copy)
            ]

    return lgnd_handles, lgnd_labels
