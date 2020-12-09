# =============================================================================
# Functions for generating legends
#
# Contents
# --------
#   0. No Class
#       gen_handles
#       gen_elements
# =============================================================================

import pandas as pd

from matplotlib.lines import Line2D
import seaborn as sns

from stdviz import utils

default_sat = 0.95

def gen_handles(colors=None, 
                size=10, 
                marker='o', 
                dsat=default_sat):
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
        handles : list (countains unplotted 2D lines)
            A list of lines, the handles of which can be used for more advanced plots
    """
    if type(colors) == str:
        colors = [colors]
    elif colors == None:
        sns.set_palette("deep") # default sns palette
        colors = [utils.rgb_to_hex(c) for c in sns.color_palette()]

    # Marker edge colors are the same as legend boarder unless transparent RGBA
    marker_edge_colors = [c if (len(c) == 9) and (c[-2:] == '00') else '#D2D2D3' \
                          for c in colors]

    handles = [Line2D([0], [0], linestyle="none", marker=marker, markersize=size, 
                      markeredgecolor=marker_edge_colors[i], markeredgewidth=size/10,
                      markerfacecolor=utils.scale_saturation(rgb=colors[i], sat=dsat)) \
                        for i in range(len(colors))]

    return handles


def gen_elements(counts=None, 
                 names=None, 
                 colors=None, 
                 size=10, 
                 marker='o', 
                 padding_indexes=None,
                 order=None, 
                 dsat=default_sat):
    """
    Generates handles and labels for plot legends while allowing for label padding and reordering
    
    Parameters
    ----------
        counts : list or list of lists : optional (contains ints or floats)
            The data to be plotted
            Note: a list of lists produces a stacked plot where sublists define factions to be stacked

        names : list : optional (default=None; contains strs)
            The names of the groups

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
        handles, labels: list (countains unplotted 2D lines) and list (contains strs)
            A list of lines, the handles of which can be used for more advanced plots, as well as labels for the handles
    """
    if type(colors) == str:
        colors = [colors]
    elif colors == None:
        sns.set_palette("deep") # default sns palette
        colors = [utils.rgb_to_hex(c) for c in sns.color_palette()]

    colors_copy = colors[:]

    # Empty lists are returned if no arguments are passed 
    # Allows for easy experimentation with the legend
    handles = []
    labels = []
    if (counts is not None) or (names is not None):
        # Create 'None' copies to assure originals aren't altered
        counts_copy = None
        names_copy = None

        if counts is not None:
            if type(counts) == pd.Series:
                counts = list(counts)

            if list in [type(item) for item in counts]:
                counts = [item for sublist in counts for item in sublist]

            counts_copy = counts[:]

        if names is not None:
            names_copy = names[:]
        
        if order is not None:
            if list in [type(item) for item in order]:
                order = [item for sublist in order for item in sublist]
            
            if counts_copy is not None:
                counts_copy = [counts_copy[i] for i in order]
            if names_copy is not None:
                names_copy = [names_copy[i] for i in order]
            colors_copy = [colors_copy[i] for i in order]

        else:
            if counts_copy is not None:
                order = list(range(len(counts_copy)))
            elif names_copy is not None:
                order = list(range(len(names_copy)))

        if padding_indexes:
            if type(padding_indexes) == int:
                padding_indexes = [padding_indexes]
            sorted(padding_indexes)
            for i in padding_indexes:
                if counts_copy is not None:
                    counts_copy.insert(i, None)
                if names_copy is not None:
                    names_copy.insert(i, None)
                colors_copy.insert(i, '#ffffff00')

        handles = gen_handles(colors=colors_copy, size=size, marker=marker)
        
        if (counts_copy is not None) and (names_copy is not None):
            labels = [f"{names_copy[i]}: {counts_copy[i]}" if counts_copy[i] != None else '' for i in range(len(counts_copy))]
        elif (counts_copy is not None) and (names_copy is None):
            labels = [f"{counts_copy[i]}" if counts_copy[i] != None else '' for i in range(len(counts_copy))]
        elif (counts_copy is None) and (names_copy is not None):
            labels = [f"{names_copy[i]}" if names_copy[i] != None else '' for i in range(len(names_copy))]

    return handles, labels