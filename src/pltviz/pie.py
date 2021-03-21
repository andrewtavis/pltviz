"""
Pie Plot
--------

Contents:
    pie
"""

import matplotlib.pyplot as plt
import seaborn as sns

from colormath.color_objects import sRGBColor

from poli_sci_kit.appointment.methods import highest_average

from pltviz import utils

default_sat = 0.95


def pie(
    counts,
    labels=None,
    faction_labels=None,
    colors=None,
    radius=1,
    outer_ring_density=100,
    donut_ratio=1,
    display_labels=False,
    display_counts=False,
    label_font_size=20,
    dsat=default_sat,
    axis=None,
):
    """
    Produces a donut plot of group (and faction) shares or allocations

    Parameters
    ----------
        counts : list or list of lists (contains ints or floats)
            The data to be plotted
            Note: a list of lists produces a two layer plot where sublists define factions

        labels : list : optional (default=None; contains strs)
            The labels of the groups

        faction_labels : list : optional (default=None; contains strs)
            The labels of potential factions

        colors : list or list of lists : optional (default=None)
            The colors of the groups as hex keys

        outer_ring_density : int (default=500)
            The density of the faction ring gradients

        radius : float : optional (default=1)
            The size of the plot

        donut_ratio : float (default=1, a full circle)
            The ratio of the center radius of a donut to the whole

        display_labels : bool : optional (default=False)
            Whether to display the labels of the groups (or factions if they're included)

                Note: labels can only be displayed for groups or factions, faction labels are if they're included

                Note: if factions are included, then a legend should be used for the inner group labels (see package examples)

        display_counts : bool : optional (default=False)
            Whether to display the counts of the groups or factions

        label_font_size : int (default=20)
            The size of the text in the labels

        dsat : float : optional (default=default_sat)
            The degree of desaturation to be applied to the colors

        axis : str : optional (default=None)
            Adds an axis to plots so they can be combined

    Returns
    -------
        ax : matplotlib.pyplot.subplot
            A donut plot that depicts shares or allocations (potentially including factions)
    """
    if faction_labels:
        assert (
            list(set([type(count) for count in counts]))[0] == list
            and len(set([type(count) for count in counts])) == 1
        ), "If plotting groups and their factions, then the 'counts' argument must be a list of lists, where sublists are group counts in the given faction"

    if (
        list(set([type(count) for count in counts]))[0] == list
        and len(set([type(count) for count in counts])) == 1
    ):
        assert (
            faction_labels
        ), "A list of lists has been provided for 'counts', implying that factions should also be represented, but no labels for the factions have been provided "

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

    colors = [
        utils.scale_saturation(rgb_trip=utils.hex_to_rgb(c), sat=dsat) for c in colors
    ]
    colors = [utils.rgb_to_hex(c) for c in colors]

    if axis:
        ax = axis  # to mirror seaborn axis plotting
    else:
        ax = plt.subplots(1, 1)[1]

    if faction_labels:
        faction_counts = [sum(sub_list) for sub_list in counts]

        # Indexes for later colors
        group_indexes = list(range(total_groups))
        factioned_indexes = utils.gen_list_of_lists(
            original_list=group_indexes,
            new_structure=[len(sublist) for sublist in counts],
        )

        # Outer sections to be colored and determined by outer_ring_density
        outer_ring_sections = [1 for i in range(outer_ring_density)]

        # Convert colors to rgb and classify them into factions
        rgb_colors = [utils.hex_to_rgb(c) for c in colors]
        faction_colors = [
            [rgb_colors[i] for i in sublist] for sublist in factioned_indexes
        ]

        # Use the Jefferson highest_average method divide the outer ring based on the proportions of the factions
        faction_sections = highest_average(
            shares=faction_counts, total_alloc=len(outer_ring_sections)
        )

        outer_ring_colors = []
        for faction_index in range(len(faction_labels)):
            # Use the Jefferson highest_average method again to allocate the faction's outer ring sections to colors
            # This would contain allocations for len(counts[faction_index]) colors, but there are len(counts[faction_index])-1 gradients
            # Thus average over Jefferson highest_average allocations when each element is removed for appropriately weighted gradients
            if len(counts[faction_index]) == 1:
                averaged_allocations = [faction_sections[faction_index]]
            else:
                one_removed_allocations = [
                    highest_average(
                        shares=counts[faction_index][:i]
                        + counts[faction_index][i + 1 :],
                        total_alloc=faction_sections[faction_index],
                    )
                    for i in range(len(counts[faction_index]))
                ]
                averaged_allocations = [
                    sum(
                        [
                            sub_allocation[i]
                            for sub_allocation in one_removed_allocations
                        ]
                    )
                    / len(one_removed_allocations)
                    for i in range(len(one_removed_allocations[0]))
                ]

            averaged_allocations = [round(i) for i in averaged_allocations]

            # Correct in case of rounding errors
            if sum(averaged_allocations) < faction_sections[faction_index]:
                averaged_allocations[0] += faction_sections[faction_index] - sum(
                    averaged_allocations
                )
            elif sum(averaged_allocations) > faction_sections[faction_index]:
                averaged_allocations[0] -= faction_sections[faction_index] - sum(
                    averaged_allocations
                )

            if len(faction_colors[faction_index]) == 1:
                # Assign sole group's color via a monochrome gradient
                outer_ring_colors.append(
                    utils.create_color_palette(
                        start_rgb=faction_colors[faction_index][0],
                        end_rgb=faction_colors[faction_index][0],
                        num_colors=averaged_allocations[0],
                        colorspace=sRGBColor,
                    )
                )
            else:
                # Create a gradient mix of the faction colors for the section of the outer ring
                for color_index in range(len(faction_colors[faction_index]))[:-1]:
                    outer_ring_colors.append(
                        utils.create_color_palette(
                            start_rgb=faction_colors[faction_index][color_index],
                            end_rgb=faction_colors[faction_index][color_index + 1],
                            num_colors=averaged_allocations[color_index],
                            colorspace=sRGBColor,
                        )
                    )

        outer_ring_colors = [item for sublist in outer_ring_colors for item in sublist]

        # Flatten counts for the inner ring and labelling
        counts = [item for sublist in counts for item in sublist]

        if display_labels:
            outer_ring_labels = []
            labels = [""] * len(counts)
            # Place labels in the middle of the faction's arc, and make the others blank
            factions_index = 0
            label_index = faction_counts[factions_index] / 2  # in the middle
            for i in range(outer_ring_density):
                if i == round(label_index / sum(faction_counts) * outer_ring_density):
                    if display_counts:
                        outer_ring_labels.append(
                            f"{faction_labels[factions_index]}: {faction_counts[factions_index]}"
                        )
                    else:
                        outer_ring_labels.append(faction_labels[factions_index])

                    factions_index += 1
                    if factions_index < len(faction_counts):
                        label_index += faction_counts[factions_index - 1] / 2
                        label_index += faction_counts[factions_index] / 2
                else:
                    outer_ring_labels.append("")

        else:
            label_font_size = 0
            outer_ring_labels = [""] * outer_ring_density
            labels = [""] * len(counts)

        outer_ring, _ = ax.pie(
            x=outer_ring_sections,
            radius=radius + (0.2 * radius),
            labels=outer_ring_labels,
            colors=outer_ring_colors,
            textprops={"fontsize": label_font_size},
        )
        plt.setp(obj=outer_ring, width=0.3 * radius, linewidth=0)

    if labels == None:
        labels = [f"group_{i}" for i in range(len(counts))]

    else:
        if display_counts:
            labels = [f"{lbl}: {counts[i]}" for i, lbl in enumerate(labels)]
        else:
            # Remove labels for those that have 0 counts to avoid confusion
            labels = [lbl if counts[i] > 0 else "" for i, lbl in enumerate(labels)]

        if not display_labels:
            labels = [""] * len(counts)

    inner_ring, _ = ax.pie(
        x=counts,
        radius=radius,
        labels=labels,
        colors=colors,
        textprops={"fontsize": label_font_size},
    )
    plt.setp(obj=inner_ring, width=radius * donut_ratio, edgecolor="white")

    return ax
