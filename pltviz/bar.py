"""
Bar Plot
--------

Contents
    bar:
"""

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

from pltviz import utils

default_sat = 0.95


def bar(
    counts,
    labels=None,
    faction_labels=None,
    colors=None,
    horizontal=False,
    stacked=False,
    label_bars=False,
    dsat=default_sat,
    axis=None,
):
    """
    A customizable bar plot that allows for easy combination of inputs into factions

    Parameters
    ----------
        counts : list or list of lists (contains ints or floats)
            The data to be plotted
            Note: a list of lists produces a stacked plot where sublists define factions to be stacked

        labels : list : optional (default=None; contains strs)
            The labels of the groups

        faction_labels : list : optional (default=None; contains strs)
            The labels of potential factions
            Note: plotting with factions groups bars based on the list in which they're found

        colors : list : optional (default=None)
            The colors of the groups as hex keys

        horizontal : bool : optional (default=False)
            Whether the plot should be horizontal

        stacked : bool : optional (default=False)
            Whether the outputs should be stacked
            Note: the use of faction_labels will inherently stack faction members and separate factions

        label_bars : bool : optional (default=False)
            Whether or not to label the bars with their heights (or widths)

        dsat : float : optional (default=default_sat)
            The degree of desaturation to be applied to the colors

        axis : str : optional (default=None)
            Adds an axis to plots so they can be combined

    Returns
    -------
        ax : matplotlib.pyplot.subplot
            A bar plot with the above criteria
    """
    if faction_labels:
        assert (
            list(set([type(count) for count in counts]))[0] == list
            and len(set([type(count) for count in counts])) == 1
        ), "If plotting groups and their factions, then the 'counts' argument must be a list of lists, where sublists are group counts in the given faction"

    if list in [type(item) for item in counts]:
        total_groups = len([item for sublist in counts for item in sublist])
    else:
        total_groups = len(counts)

    if colors:
        assert (
            len(colors) == total_groups
        ), "The number of colors provided doesn't match the number of counts to be displayed"

    elif colors == None:
        sns.set_palette("deep")  # default sns palette
        colors = [
            utils.rgb_to_hex(c)
            for c in sns.color_palette(n_colors=total_groups, desat=1)
        ]

    if stacked:
        # Derive positions where bars should start
        if list in [type(i) for i in counts]:
            bar_starts = []
            for sub_list in counts:
                inputs_except_last = list(sub_list[:-1])
                inputs_except_last.insert(0, 0)
                bar_starts.append(list(np.cumsum(inputs_except_last)))

            bar_starts = [item for sublist in bar_starts for item in sublist]

        else:
            inputs_except_last = list(counts[:-1])
            inputs_except_last.insert(0, 0)
            bar_starts = np.cumsum(inputs_except_last)

    df_plot = pd.DataFrame(columns=["counts", "group", "faction"])
    if list in [type(i) for i in counts]:
        df_plot["counts"] = [item for sublist in counts for item in sublist]
    else:
        df_plot["counts"] = counts

    if faction_labels:
        factions_for_labels = [
            [lbl] * len(counts[i]) for i, lbl in enumerate(faction_labels)
        ]
        df_plot["faction"] = [
            item for sublist in factions_for_labels for item in sublist
        ]

    if type(labels) == pd.Series:
        labels = list(labels)

    if labels:
        df_plot["group"] = labels
    else:
        labels = range(len(counts))  # dummy labels to be removed
        df_plot["group"] = labels

    if horizontal:
        if stacked:
            if list not in [type(i) for i in counts]:
                for i in df_plot.index:
                    ax = sns.barplot(
                        data=pd.DataFrame(df_plot.loc[i]).T,
                        x="counts",
                        y="group",
                        color=colors[i],
                        saturation=dsat,
                        left=bar_starts[i],
                        orient="h",
                        ax=axis,
                    )

            else:
                pivot_plot = (
                    df_plot.pivot(columns="group", index="faction", values="counts")
                    .fillna(0)
                    .reindex(faction_labels)
                )
                pivot_plot = pivot_plot[labels]
                colors = [
                    utils.scale_saturation(rgb_trip=utils.hex_to_rgb(c), sat=dsat)
                    for c in colors
                ]

                ax = pivot_plot.plot.barh(stacked=True, color=colors, rot=90)
                plt.grid(b=None, axis="y")

            if label_bars:
                if list not in [type(i) for i in counts]:
                    label_text = str(utils.round_if_int(sum(counts)))
                    label_position = sum([p.get_width() for p in ax.patches]) + 1

                    ax.text(
                        x=label_position,
                        y=ax.patches[0].get_y() + ax.patches[0].get_height() / 2,
                        s=label_text,
                        ha="center",
                    )

                else:
                    # Start and end indexes of all factions
                    faction_start_idxs = list(set([p.get_y() for p in ax.patches]))

                    for i, c in enumerate(counts):
                        label_text = str(utils.round_if_int(sum(c)))
                        label_position = sum(c) + 1

                        ax.text(
                            x=label_position,
                            y=faction_start_idxs[i]
                            + ax.patches[0].get_height() / 2,  # all have equal height
                            s=label_text,
                            ha="center",
                        )

        else:
            if list not in [type(i) for i in counts]:
                colors = [
                    utils.scale_saturation(rgb_trip=utils.hex_to_rgb(c), sat=dsat)
                    for c in colors
                ]
                sns.set_palette(colors)
                ax = sns.barplot(
                    data=df_plot,
                    x="counts",
                    y="group",
                    saturation=1,
                    left=0,
                    orient="h",
                    ax=axis,
                )

            else:
                flat_counts = [item for sublist in counts for item in sublist]

                bar_positions = [
                    0.8 * i - 0.4 for i in list(range(0, len(flat_counts)))
                ]  # 0.8 is the default width of plt.bar
                bar_shifts = [[0.8 * i] * len(c) for i, c in enumerate(counts)]
                flat_bar_shifts = [item for sublist in bar_shifts for item in sublist]
                bar_locations = [
                    p + flat_bar_shifts[i] for i, p in enumerate(bar_positions)
                ]

                scaled_colors = [
                    utils.scale_saturation(rgb_trip=utils.hex_to_rgb(c), sat=dsat)
                    for c in colors
                ]

                if axis:
                    ax = axis
                else:
                    ax = plt.subplots()[1]

                ax.barh(y=bar_locations, width=flat_counts, color=scaled_colors)

                factioned_bar_locations = utils.gen_list_of_lists(
                    bar_locations, [len(f) for f in counts]
                )
                y_label_locs = [np.mean(f) for f in factioned_bar_locations]

                ax.set_yticks(ticks=y_label_locs)
                ax.set_yticklabels(labels=faction_labels, rotation=90)
                ax.tick_params(axis="y", grid_linewidth=0)

            if label_bars:
                for p in ax.patches:
                    ax.text(
                        x=p.get_width() + 1,
                        y=p.get_y() + p.get_height() / 2,
                        s=str(utils.round_if_int(p.get_width())),
                        ha="center",
                    )

    else:
        if stacked:
            if list not in [type(i) for i in counts]:
                for i in df_plot.index:
                    ax = sns.barplot(
                        data=pd.DataFrame(df_plot.loc[i]).T,
                        x="group",
                        y="counts",
                        color=colors[i],
                        saturation=dsat,
                        bottom=bar_starts[i],
                        orient="v",
                        ax=axis,
                    )

            else:
                pivot_plot = (
                    df_plot.pivot(columns="group", index="faction", values="counts")
                    .fillna(0)
                    .reindex(faction_labels)
                )
                pivot_plot = pivot_plot[labels]
                colors = [
                    utils.scale_saturation(rgb_trip=utils.hex_to_rgb(c), sat=dsat)
                    for c in colors
                ]

                ax = pivot_plot.plot.bar(stacked=True, color=colors, rot=0)
                plt.grid(b=None, axis="x")

            if label_bars:
                if list not in [type(i) for i in counts]:
                    label_text = str(utils.round_if_int(sum(counts)))
                    label_position = sum([p.get_height() for p in ax.patches]) + 1

                    ax.text(
                        x=ax.patches[0].get_x() + ax.patches[0].get_width() / 2.0,
                        y=label_position,
                        s=label_text,
                        ha="center",
                    )

                else:
                    faction_start_idxs = list(set([p.get_x() for p in ax.patches]))

                    for i, c in enumerate(counts):
                        label_text = str(utils.round_if_int(sum(c)))
                        label_position = sum(c) + 1

                        ax.text(
                            x=faction_start_idxs[i]
                            + ax.patches[0].get_width() / 2,  # all have equal width
                            y=label_position,
                            s=label_text,
                            ha="center",
                        )

        else:
            if list not in [type(i) for i in counts]:
                colors = [
                    utils.scale_saturation(rgb_trip=utils.hex_to_rgb(c), sat=dsat)
                    for c in colors
                ]
                sns.set_palette(colors)
                ax = sns.barplot(
                    data=df_plot,
                    x="group",
                    y="counts",
                    saturation=1,
                    bottom=0,
                    orient="v",
                    ax=axis,
                )

            else:
                flat_counts = [item for sublist in counts for item in sublist]

                bar_positions = [
                    0.8 * i - 0.4 for i in list(range(0, len(flat_counts)))
                ]  # 0.8 is the default width of plt.bar
                bar_shifts = [[0.8 * i] * len(c) for i, c in enumerate(counts)]
                flat_bar_shifts = [item for sublist in bar_shifts for item in sublist]
                bar_locations = [
                    p + flat_bar_shifts[i] for i, p in enumerate(bar_positions)
                ]

                scaled_colors = [
                    utils.scale_saturation(rgb_trip=utils.hex_to_rgb(c), sat=dsat)
                    for c in colors
                ]

                if axis:
                    ax = axis
                else:
                    ax = plt.subplots()[1]

                ax.bar(x=bar_locations, height=flat_counts, color=scaled_colors)

                factioned_bar_locations = utils.gen_list_of_lists(
                    bar_locations, [len(f) for f in counts]
                )
                x_label_locs = [np.mean(f) for f in factioned_bar_locations]

                ax.set_xticks(ticks=x_label_locs)
                ax.set_xticklabels(labels=faction_labels)
                ax.tick_params(axis="x", grid_linewidth=0)

            if label_bars:
                for p in ax.patches:
                    ax.text(
                        x=p.get_x() + p.get_width() / 2.0,
                        y=p.get_height() + 1,
                        s=str(utils.round_if_int(p.get_height())),
                        ha="center",
                    )

    if (stacked and list not in [type(i) for i in counts]) or (
        not labels and not faction_labels
    ):
        if horizontal:
            ax.axes.get_yaxis().set_ticks([])
        else:
            ax.axes.get_xaxis().set_ticks([])

    if ax.get_legend():
        ax.get_legend().remove()

    return ax
