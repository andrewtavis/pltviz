"""
Semipie Plot Tests
------------------
"""

import matplotlib.pyplot as plt

import pltviz


def test_semipie(
    monkeypatch, allocations, party_colors,
):
    monkeypatch.setattr(plt, "show", lambda: None)
    pltviz.semipie(counts=allocations, colors=None)

    pltviz.semipie(counts=allocations, colors=party_colors)
