"""
Pie Plot Tests
--------------
"""

import pytest
import matplotlib.pyplot as plt

import pltviz


def test_pie(
    monkeypatch,
    allocations,
    factioned_allocations,
    parties,
    faction_labels,
    party_colors,
):
    monkeypatch.setattr(plt, "show", lambda: None)
    pltviz.pie(
        counts=allocations,
        labels=None,
        faction_labels=None,
        colors=None,
        radius=1,
        outer_ring_density=100,
        donut_ratio=1,
        display_labels=False,
        display_counts=False,
        label_font_size=20,
        axis=None,
    )

    pltviz.pie(
        counts=allocations,
        labels=parties,
        faction_labels=None,
        colors=party_colors,
        radius=1,
        outer_ring_density=100,
        donut_ratio=1,
        display_labels=False,
        display_counts=False,
        label_font_size=20,
        axis=None,
    )

    pltviz.pie(
        counts=allocations,
        labels=parties,
        faction_labels=None,
        colors=party_colors,
        radius=1,
        outer_ring_density=100,
        donut_ratio=1,
        display_labels=True,
        display_counts=True,
        label_font_size=20,
        axis=None,
    )

    with pytest.raises(AssertionError):
        pltviz.pie(
            counts=allocations,
            labels=parties,
            faction_labels=faction_labels,
            colors=party_colors,
            radius=1,
            outer_ring_density=100,
            donut_ratio=1,
            display_labels=True,
            display_counts=True,
            label_font_size=20,
            axis=None,
        )

    pltviz.pie(
        counts=factioned_allocations,
        labels=parties,
        faction_labels=faction_labels,
        colors=party_colors,
        radius=1,
        outer_ring_density=100,
        donut_ratio=1,
        display_labels=False,
        display_counts=False,
        label_font_size=20,
        axis=None,
    )

    pltviz.pie(
        counts=factioned_allocations,
        labels=parties,
        faction_labels=faction_labels,
        colors=party_colors,
        radius=1,
        outer_ring_density=100,
        donut_ratio=1,
        display_labels=True,
        display_counts=True,
        label_font_size=20,
        axis=None,
    )
