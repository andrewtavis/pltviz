"""
Legend Tests
------------
"""

import matplotlib.pyplot as plt

import pltviz


def test_gen_handles(
    monkeypatch, party_colors,
):
    monkeypatch.setattr(plt, "show", lambda: None)
    pltviz.legend.gen_handles(colors=None)

    pltviz.legend.gen_handles(colors=party_colors)


def test_gen_elements(
    monkeypatch,
    allocations,
    factioned_allocations,
    parties,
    faction_labels,
    party_colors,
    white_black_hexes,
):
    monkeypatch.setattr(plt, "show", lambda: None)
    pltviz.legend.gen_elements(counts=allocations, labels=None, colors=None)

    pltviz.legend.gen_elements(counts=allocations, labels=parties, colors=party_colors)

    pltviz.legend.gen_elements(counts=None, labels=parties, colors=None)

    pltviz.legend.gen_elements(
        counts=allocations, labels=parties, colors=party_colors, padding_indexes=0,
    )

    pltviz.legend.gen_elements(
        counts=allocations,
        labels=parties,
        colors=party_colors,
        order=list(range(len(allocations))),
    )

    pltviz.legend.gen_elements(
        counts=None,
        labels=parties,
        colors=party_colors,
        order=list(range(len(parties))),
    )

    pltviz.legend.gen_elements(
        counts=allocations,
        labels=None,
        colors=None,
        order=list(range(len(allocations))),
    )

    pltviz.legend.gen_elements(
        counts=factioned_allocations, labels=parties, colors=white_black_hexes,
    )

    pltviz.legend.gen_elements(
        counts=factioned_allocations, labels=None, colors=white_black_hexes,
    )
