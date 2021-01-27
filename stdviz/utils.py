"""
Utilities
---------

Utility functions for general operations and coloration

Note:
In order to standardize coloration and make plots more readable,
input colors are by default scaled to a lower saturation

This follows seaborn's default darkening of colors,
but is not as dark to roughly maintain input colors

Functions here use pandas, pyplot, and seaborn, hence the need for standardization

Contents
    round_if_int
    gen_list_of_lists
    add_num_commas

    hex_to_rgb
    rgb_to_hex
    scale_saturation
    create_color_palette
    gen_random_colors
"""

import random
import colorsys
from difflib import SequenceMatcher

import numpy as np
import pandas as pd

import matplotlib as mpl
import seaborn as sns

from colormath.color_objects import sRGBColor
from colormath.color_conversions import convert_color


def round_if_int(val):
    """Rounds off the decimal of a value if it is an integer float"""
    if type(val) == float:
        if val.is_integer():
            val = int(val)

    return val


def gen_list_of_lists(original_list, new_structure):
    """Generates a list of lists with a given structure from a given list"""
    assert len(original_list) == sum(
        new_structure
    ), "The number of elements in the original list and desired structure don't match"

    list_of_lists = [
        [original_list[i + sum(new_structure[:j])] for i in range(new_structure[j])]
        for j in range(len(new_structure))
    ]

    return list_of_lists


def add_num_commas(num):
    """Adds commas to a numeric string for readability"""
    num_str = str(num)
    num_str_no_decimal = num_str.split(".")[0]
    if "." in num_str:
        decimal = num_str.split(".")[1]
    else:
        decimal = None

    str_list = [i for i in num_str_no_decimal]
    str_list = str_list[::-1]

    str_list_with_commas = [
        str_list[i] + "," if i % 3 == 0 and i != 0 else str_list[i]
        for i in range(len(str_list))
    ]
    str_list_with_commas = str_list_with_commas[::-1]

    str_with_commas = ""
    for i in str_list_with_commas:
        str_with_commas += i

    if decimal != None:
        return str_with_commas + "." + decimal
    else:
        return str_with_commas


def hex_to_rgb(hex_rep):
    """Converts a hexidecimal representation to its RGB ratios"""
    return sRGBColor(
        *[int(hex_rep[i + 1 : i + 3], 16) for i in (0, 2, 4)], is_upscaled=True
    )


def rgb_to_hex(rgb_trip):
    """Converts rgb ratios to their hexidecimal representation"""
    trip_0, trip_1, trip_2 = rgb_trip[0], rgb_trip[1], rgb_trip[2]
    if type(trip_0) == float or np.float64:
        trip_0 *= 255
        trip_1 *= 255
        trip_2 *= 255
    return "#%02x%02x%02x" % (int(trip_0), int(trip_1), int(trip_2))


def scale_saturation(rgb, sat):
    """Changs the saturation of an rgb color"""
    if (type(rgb) == str) and (len(rgb) == 9) and (rgb[-2:] == "00"):
        # An RGBA has been provided and its alpha is 00, so return it for a transparent marker
        return rgb

    if (type(rgb) == str) and (len(rgb) == 7):
        rgb = hex_to_rgb(rgb)

    if type(rgb) == sRGBColor:
        rgb = rgb.get_value_tuple()

    h, l, s = colorsys.rgb_to_hls(*rgb)

    return colorsys.hls_to_rgb(h, min(1, l * sat), s=s)


def create_color_palette(start_rgb, end_rgb, num_colors, colorspace):
    """
    Generates a color palette between two colors

    Parameters
    ----------
        start_rgb : colormath.color_objects.sRGBColor
            The first color in the palette

        end_rgb : colormath.color_objects.sRGBColor
            The last color in the palette

        num_colors : int
            The total colors of the palette including the start and end colors

        colorspace : colormath.color_object
            The color scheme for the palette

    Returns
    -------
        palette : list (contains sts)
            A list of length num_colors with color hexes for the palette elements
    """
    # Define the start and end within a geometric space and find those points between
    start_tuple = convert_color(start_rgb, colorspace).get_value_tuple()
    end_tuple = convert_color(end_rgb, colorspace).get_value_tuple()

    points_between = list(
        zip(
            *[
                np.linspace(start=start_tuple[i], stop=end_tuple[i], num=num_colors)
                for i in range(3)
            ]
        )
    )

    # Convert points to RGB and then to hexes for the output
    rgb_colors = [
        convert_color(colorspace(*point), sRGBColor) for point in points_between
    ]
    palette = [color.get_rgb_hex() for color in rgb_colors]

    return palette


def gen_random_colors(num_groups, colors=None):
    """
    Generates random colors

    Parameters
    ----------
        num_groups : int
            The number of groups for which colors should be generated

        colors : list : optional (contains strs)
            Hex based colors that should be appended if not enough have been provided

    Returns
    -------
        colors or colors + new_colors : list (contains strs)
            Randomly generated colors for figures and plotting
    """
    if colors == None:
        colors = []

    if len(colors) < num_groups:
        new_colors = []
        while len(new_colors) < num_groups:
            random_rgba = (
                random.random(),
                random.random(),
                random.random(),
                random.random(),
            )

            new_colors.append(random_rgba)

        sns.set_palette(colors + new_colors)

        if type(new_colors[0][0]) == float:
            # Convert over for non-sns use
            new_colors = [
                mpl.colors.to_hex([c[0], c[1], c[2]]).upper() for c in new_colors
            ]

        return colors + new_colors

    else:
        return colors
