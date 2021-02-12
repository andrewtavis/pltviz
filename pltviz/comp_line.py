"""
Comparative Line Plot
---------------------

Contents:
    comp_line
"""

import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

from pltviz import utils

default_sat = 0.95


def comp_line(
    df=None,
    dependent_cols=None,
    indep_stats=None,
    group_col=None,
    colors=None,
    stacked=False,
    percent=False,
    dsat=default_sat,
    axis=None,
):
    """
    Plots a line plot to compare statistics over a changing baseline

    Parameters
    ----------
        df : pd.DataFrame
            Dataframe that contains statistics to be compared

        dependent_cols : str or list (contains strs) (default=None)
            The column(s) in df which should be compared

        indep_stats : str or list (contains ints or floats) (default=None)
            A df column or the baseline stats that generated the columns in dependent_cols

        group_col : str (default=None)
            The name of the column in which groups are defined

            Note: this allows plotting across multiple instances in a single column

        colors : list or list of lists : optional (default=None)
            The colors of the groups as hex keys

        stacked : bool (default=False)
            Whether the plot is a stackplot

        percent : bool (default=False)
            Whether the y-axis should depict relative amounts or not

        dsat : float : optional (default=default_sat)
            The degree of desaturation to be applied to the colors

        axis : str : optional (default=None)
            Adds an axis to plots so they can be combined

    Returns
    -------
        ax : matplotlib.pyplot.subplot
            A line plot that shows the shifts in group allocations given seat limits
    """
    if colors == None:
        sns.set_palette("deep")  # default sns palette
        colors = [
            utils.rgb_to_hex(c) for c in sns.color_palette(n_colors=len(df), desat=1)
        ]

    if type(colors) == str or type(colors) == tuple:
        colors = [colors]

    # Check to see if colors haven't been formatted in a prior recursive step
    if type(colors[0]) != tuple:
        colors = [
            utils.scale_saturation(rgb_trip=utils.hex_to_rgb(c), sat=default_sat)
            for c in colors
        ]
    sns.set_palette(colors)

    df_copy = df.copy()

    if type(dependent_cols) == str:
        # Assume that the user is passing a single column with values corresponding to another column's
        if dependent_cols in df_copy.columns:
            assert (
                type(indep_stats) == str and type(df_copy[indep_stats]) == pd.Series
            ), "A corresponding column should be passed as 'indep_stats' if 'dependent_cols' is a single df column."
            assert (
                group_col != None
            ), "The 'group_col' argument must be passed if providing a single comparison column."

            # Create a similar form to the other path's df and recursively run this function
            new_indep_stats = [
                utils.round_if_int(float(s)) for s in df_copy[indep_stats].unique()
            ]
            # Sort the baseline stats, as they're likely years, so objective is a graph that's increasing in time
            sorted_nbs = sorted(new_indep_stats)

            # Derive whether it already was sorted to know how to order the value assignment
            was_sorted = sorted_nbs == new_indep_stats
            if was_sorted == True:
                was_sorted = -1
            else:
                was_sorted = 1

            new_dep_cols = [str(s) + "_" + dependent_cols for s in sorted_nbs]

            df_cols = ["locations"] + new_dep_cols

            df_new = pd.DataFrame(columns=df_cols)
            df_new["locations"] = df_copy[group_col].unique()

            for lctn in df_new["locations"]:
                df_new.loc[
                    df_new[df_new["locations"] == lctn].index, new_dep_cols
                ] = df_copy.loc[
                    df_copy[df_copy[group_col] == lctn].index, dependent_cols
                ].values[
                    ::was_sorted
                ]

            return comp_line(
                df=df_new,
                dependent_cols=new_dep_cols,
                indep_stats=new_indep_stats,
                colors=colors,
                stacked=stacked,
                percent=percent,
                dsat=dsat,
                axis=axis,
            )

        else:
            ValueError(
                "The 'dependent_cols' argument does not contain column labels for the provided dataframe."
            )

    if percent == True:
        for col in dependent_cols:
            df_copy[col] = df_copy[col] / sum(df_copy[col])

    if stacked:
        lol_allocations = []
        for i in df_copy.index:
            list_of_allocations = []
            for col in dependent_cols:
                list_of_allocations.append(df_copy.loc[i, col])

            lol_allocations.append(list_of_allocations)

        if axis:
            ax = axis  # to mirror seaborn axis plotting
        else:
            ax = plt.subplots()[1]
        print(indep_stats)
        print(lol_allocations)
        ax.stackplot(indep_stats, lol_allocations)

    else:
        if type(dependent_cols) == str:
            dependent_cols = [dependent_cols]
        for i in df_copy.index:
            ax = sns.lineplot(
                x=indep_stats, y=list(df_copy.loc[i, dependent_cols].values), ax=axis
            )

    if percent == True:
        ax.set_ylim([0, 1])

    ax.set_xlim([min(indep_stats), max(indep_stats)])

    return ax
