"""
Bar Plot Tests
--------------
"""

import pytest
import matplotlib.pyplot as plt

import pltviz


def test_bar(
    monkeypatch,
    allocations,
    factioned_allocations,
    parties,
    faction_labels,
    party_colors,
):
    monkeypatch.setattr(plt, "show", lambda: None)
    pltviz.bar(
        counts=allocations,
        labels=None,
        faction_labels=None,
        colors=None,
        horizontal=False,
        stacked=False,
        label_bars=True,
        axis=None,
    )

    pltviz.bar(
        counts=allocations,
        labels=parties,
        faction_labels=None,
        colors=party_colors,
        horizontal=False,
        stacked=False,
        label_bars=True,
        axis=None,
    )

    pltviz.bar(
        counts=allocations,
        labels=parties,
        faction_labels=None,
        colors=party_colors,
        horizontal=False,
        stacked=True,
        label_bars=True,
        axis=None,
    )

    pltviz.bar(
        counts=allocations,
        labels=parties,
        faction_labels=None,
        colors=party_colors,
        horizontal=True,
        stacked=False,
        label_bars=False,
        axis=None,
    )

    pltviz.bar(
        counts=allocations,
        labels=parties,
        faction_labels=None,
        colors=party_colors,
        horizontal=True,
        stacked=True,
        label_bars=False,
        axis=None,
    )

    with pytest.raises(AssertionError):
        pltviz.bar(
            counts=allocations,
            labels=parties,
            faction_labels=faction_labels,
            colors=party_colors,
            horizontal=True,
            stacked=False,
            label_bars=False,
            axis=None,
        )

    pltviz.bar(
        counts=factioned_allocations,
        labels=parties,
        faction_labels=faction_labels,
        colors=party_colors,
        horizontal=False,
        stacked=False,
        label_bars=False,
        axis=None,
    )

    pltviz.bar(
        counts=factioned_allocations,
        labels=parties,
        faction_labels=faction_labels,
        colors=party_colors,
        horizontal=False,
        stacked=True,
        label_bars=False,
        axis=None,
    )

    pltviz.bar(
        counts=factioned_allocations,
        labels=parties,
        faction_labels=faction_labels,
        colors=party_colors,
        horizontal=True,
        stacked=False,
        label_bars=False,
        axis=None,
    )

    pltviz.bar(
        counts=factioned_allocations,
        labels=parties,
        faction_labels=faction_labels,
        colors=party_colors,
        horizontal=True,
        stacked=True,
        label_bars=False,
        axis=None,
    )
