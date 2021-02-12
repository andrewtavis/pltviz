"""
Comparative Line Plot Tests
---------------------------
"""

import pytest
import pandas as pd
import matplotlib.pyplot as plt

import pltviz


def test_comp_line(monkeypatch, parties, party_colors):
    monkeypatch.setattr(plt, "show", lambda: None)
    seats_1 = [13, 4, 15, 6, 10, 2]
    seats_2 = [18, 6, 21, 8, 14, 3]
    seats_3 = [22, 8, 27, 11, 18, 4]

    election_df = pd.DataFrame()
    election_df["parties"] = parties
    election_df.loc[:, "seats_1"] = pd.Series(seats_1, index=election_df.index,)
    election_df.loc[:, "seats_2"] = pd.Series(seats_2, index=election_df.index,)
    election_df.loc[:, "seats_3"] = pd.Series(seats_3, index=election_df.index,)

    pltviz.comp_line(
        df=election_df,
        dependent_cols=["seats_1", "seats_2", "seats_3"],
        indep_stats=[1, 2, 3],
        colors=party_colors,
        stacked=False,
        percent=False,
    )

    pltviz.comp_line(
        df=election_df,
        dependent_cols=["seats_1", "seats_2", "seats_3"],
        indep_stats=[1, 2, 3],
        colors=party_colors,
        stacked=True,
        percent=False,
    )

    pltviz.comp_line(
        df=election_df,
        dependent_cols=["seats_1", "seats_2", "seats_3"],
        indep_stats=[1, 2, 3],
        colors=None,
        stacked=False,
        percent=True,
    )

    pltviz.comp_line(
        df=election_df,
        dependent_cols=["seats_1", "seats_2", "seats_3"],
        indep_stats=[1, 2, 3],
        colors=None,
        stacked=True,
        percent=True,
    )

    # One column has values that are split across multiple instances
    seats = [1, 2, 3, 4, 5, 6] * 6
    years = [2000, 2001, 2002, 2003, 2004, 2005] * 6

    election_df = pd.DataFrame()
    election_df["parties"] = parties * 6
    election_df["years"] = years
    election_df["seats"] = seats
    pltviz.comp_line(
        df=election_df,
        dependent_cols="seats",
        indep_stats="years",
        group_col="parties",
        colors=party_colors,
        stacked=False,
        percent=False,
    )
