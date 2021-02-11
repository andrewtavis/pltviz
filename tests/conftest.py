"""
Fixtures
--------
"""

import pytest

from pltviz.utils import round_if_int
from pltviz.utils import gen_list_of_lists
from pltviz.utils import add_num_commas
from pltviz.utils import hex_to_rgb
from pltviz.utils import rgb_to_hex
from pltviz.utils import scale_saturation
from pltviz.utils import create_color_palette
from pltviz.utils import gen_random_colors

from pltviz.bar import bar
from pltviz.comp_line import comp_line
from pltviz.gini import gini
from pltviz import legend
from pltviz.pie import pie
from pltviz.semipie import semipie


# Allocations from examples.plot.ipynb
@pytest.fixture(params=[[26, 9, 37, 12, 23, 5]])
def allocations(request):
    return request.param


@pytest.fixture(params=[[[12, 5, 9, 26], [23, 37]]])
def factioned_allocations(request):
    return request.param


@pytest.fixture(params=[["CDU/CSU", "FDP", "Greens", "Die Linke", "SPD", "AfD"]])
def parties(request):
    return request.param


@pytest.fixture(
    params=[["#000000", "#ffed00", "#64a12d", "#be3075", "#eb001f", "#009ee0"]]
)
def party_colors(request):
    return request.param


@pytest.fixture(params=[["Opposition", "Government"]])
def faction_labels(request):
    return request.param


@pytest.fixture(params=[["#ffffff", "#000000"]])
def white_black_hexes(request):
    return request.param
