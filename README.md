<div align="center">
  <a href="https://github.com/andrewtavis/stdviz"><img src="https://raw.githubusercontent.com/andrewtavis/stdviz/master/resources/stdviz_logo_transparent.png" width=488 height=157></a>
</div>

--------------------------------------

[![rtd](https://img.shields.io/readthedocs/stdviz.svg?logo=read-the-docs)](http://stdviz.readthedocs.io/en/latest/)
[![travis](https://img.shields.io/travis/andrewtavis/stdviz.svg?logo=travis-ci)](https://travis-ci.org/andrewtavis/stdviz)
[![codecov](https://codecov.io/gh/andrewtavis/stdviz/branch/master/graphs/badge.svg)](https://codecov.io/gh/andrewtavis/stdviz)
[![pyversions](https://img.shields.io/pypi/pyversions/stdviz.svg?logo=python)](https://pypi.org/project/stdviz/)
[![pypi](https://img.shields.io/pypi/v/stdviz.svg)](https://pypi.org/project/stdviz/)
[![pypistatus](https://img.shields.io/pypi/status/stdviz.svg)](https://pypi.org/project/stdviz/)
[![license](https://img.shields.io/github/license/andrewtavis/stdviz.svg)](https://github.com/andrewtavis/stdviz/blob/main/LICENSE)
[![codestyle](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![contributions](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](https://github.com/andrewtavis/stdviz/blob/main/CONTRIBUTING.md)
[![coc](https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg)](https://github.com/andrewtavis/stdviz/blob/main/.github/CODE_OF_CONDUCT.md)

### Standardized visualization in Python

[//]: # "The '-' after the section links is needed to make them work on GH (because of ↩s)"
**Jump to:**<a id="jumpto"></a> [plot](#plot-) • [To-Do](#to-do-)

**stdviz** is a Python package for standardized visualization. Routine plotting approaches are formatted to allow for easy variation while providing quick and exact results. Coloration functions are also included for precise colors across plots and to assure that all functions can be ran with color hexes.

# Installation via PyPi
```bash
pip install stdviz
```

```python
import stdviz
```

# plot [`↩`](#jumpto)

Plotting methods within [stdviz/plot](https://github.com/andrewtavis/stdviz/tree/main/stdviz/plot) are tailored to provide quick results for staples of data visualization.

See [examples/plot](https://github.com/andrewtavis/stdviz/blob/main/examples/plot.ipynb) for all plotting styles that seamlessly combine graphing functions of seaborn, matplotlib, and pandas.

```python
import matplotlib.pyplot as plt
import stdviz
```

Examples of routine plotting techniques made easy are:

```python
# The following will be used for the remaining examples

# German political parties
parties = ['CDU/CSU', 'FDP', 'Greens', 'Die Linke', 'SPD', 'AfD']
party_colors = ['#000000', '#ffed00', '#64a12d', '#be3075', '#eb001f', '#009ee0']

# Hypothetical seat allocations to the Bundestag (German parliament)
seat_allocations = [26, 9, 37, 12, 23, 5]
```

```python
# Bar plot options such as stacked and label bars are booleans
ax = stdviz.plot.bar(
    counts=seat_allocations,
    names=parties,
    faction_names=None,
    colors=party_colors,
    horizontal=False,
    stacked=False,
    label_bars=True,
    axis=None,
)

# Initialize empty handles and labels
handles, labels = stdviz.plot.legend.gen_elements()

# Add a majority line
ax.axhline(int(sum(seat_allocations) / 2) + 1, ls="--", color="black")
handles.insert(0, Line2D([0], [0], linestyle="--", color="black"))
labels.insert(0, "Majority: {} seats".format(int(sum(seat_allocations) / 2) + 1))

ax.legend(
    handles=handles,
    labels=labels,
    title="Bundestag: {} seats".format(sum(seat_allocations)),
    loc="upper left",
    bbox_to_anchor=(0, 0.9),
    title_fontsize=20,
    fontsize=15,
    frameon=True,
    facecolor="#FFFFFF",
    framealpha=1,
)

ax.set_ylabel("Seats", fontsize=15)
ax.set_xlabel("Party", fontsize=15)
```
<p align="middle">
  <img src="https://raw.githubusercontent.com/andrewtavis/stdviz/main/resources/gh_images/bar.png" width="600" />
</p>

```python
ax = stdviz.plot.semipie(counts=seat_allocations, colors=party_colors, donut_ratio=0.5)

handles, labels = stdviz.plot.legend.gen_elements(
    counts=seat_allocations,
    names=parties,
    colors=party_colors,
    size=15,
    marker="o",
    padding_indexes=None,
    order=None,
)

ax.legend(
    handles=handles,
    labels=labels,
    title="Bundestag: {} seats".format(sum(seat_allocations)),
    title_fontsize=20,
    fontsize=14,
    ncol=2,
    loc="center",
    bbox_to_anchor=(0.5, 0.17),
    frameon=False,
    facecolor="#FFFFFF",
    framealpha=1,
)

plt.show()
```

<p align="middle">
  <img src="https://raw.githubusercontent.com/andrewtavis/stdviz/main/resources/gh_images/semipie.png" width="600" />
</p>

# To-Do [`↩`](#jumpto)

- Adding further plotting standardizations
- Finishing the coloration on the outer ring of [stdviz.plot.pie](https://github.com/andrewtavis/stdviz/tree/main/stdviz/plot/pie)
- Allowing all plotting variations to be seamlessly plotted from either lists or dataframe columns where applicable
