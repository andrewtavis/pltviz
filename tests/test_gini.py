"""
Gini Plot Tests
---------------
"""

import pytest
import matplotlib.pyplot as plt

import pltviz


def test_gini(monkeypatch):
    monkeypatch.setattr(plt, "show", lambda: None)
    shares = [0.49, 0.59, 0.69, 0.79, 1.89, 2.55, 5.0, 10.0, 18.0, 60.0]
    pltviz.gini(shares=shares)
