"""
Fixtures
--------
"""

import pytest


# Allocations from examples.plot.ipynb.
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
